// 파일 기반 저장소. 서버(server.mjs)와 CLI(cli.mjs)가 함께 사용합니다.
// data/
//   rev                       — 변경될 때마다 증가 (서버가 감시해서 화면을 새로고침)
//   projects/<id>/project.json
//   projects/<id>/versions/v1.mp4 ...
//   projects/<id>/annotations.json
//   projects/<id>/edits.json
//   projects/<id>/snapshots/<annotationId>.jpg
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(here, '..');
export const DATA = path.resolve(process.env.VF_DATA || path.join(ROOT, 'data'));
export const INBOX = path.resolve(process.env.VF_INBOX || path.join(ROOT, 'inbox'));
const PROJECTS = path.join(DATA, 'projects');
const REV = path.join(DATA, 'rev');

export const VIDEO_EXT = ['.mp4', '.webm', '.mov', '.m4v'];

fs.mkdirSync(PROJECTS, { recursive: true });
fs.mkdirSync(INBOX, { recursive: true });

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fallback; }
}
function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2));
  fs.renameSync(tmp, file);
}

export function bump() {
  const n = Number(readJson(REV, 0)) + 1;
  writeJson(REV, n);
  return n;
}
export function rev() { return Number(readJson(REV, 0)); }

export function slugify(name) {
  const s = String(name).trim().toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '');
  return s || `project-${Date.now()}`;
}

const pdir = (id) => {
  if (!/^[\p{L}\p{N}-]+$/u.test(id)) throw new Error(`잘못된 프로젝트 ID: ${id}`);
  return path.join(PROJECTS, id);
};

export function listProjects() {
  return fs.readdirSync(PROJECTS, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => summary(d.name))
    .filter(Boolean)
    .sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));
}

function summary(id) {
  const p = readJson(path.join(pdir(id), 'project.json'), null);
  if (!p) return null;
  const anns = annotations(id);
  return {
    ...p,
    versionCount: p.versions.length,
    latest: p.versions.at(-1) || null,
    counts: countStatus(anns),
  };
}

export function countStatus(anns) {
  const c = { total: anns.length, open: 0, fixed: 0, done: 0 };
  for (const a of anns) c[a.status] = (c[a.status] || 0) + 1;
  return c;
}

export function getProject(id) {
  const p = readJson(path.join(pdir(id), 'project.json'), null);
  if (!p) return null;
  return { ...p, annotations: annotations(id), edits: getEdits(id), counts: countStatus(annotations(id)) };
}

export function findProject(idOrName) {
  if (!idOrName) return null;
  const all = listProjects();
  return all.find((p) => p.id === idOrName)
    || all.find((p) => p.name === idOrName)
    || all.find((p) => p.id === slugify(idOrName)) || null;
}

export function createProject(name) {
  const base = slugify(name);
  let id = base, i = 2;
  while (fs.existsSync(pdir(id))) id = `${base}-${i++}`;
  const now = new Date().toISOString();
  const p = { id, name: String(name).trim() || id, createdAt: now, updatedAt: now, versions: [] };
  writeJson(path.join(pdir(id), 'project.json'), p);
  bump();
  return p;
}

export function ensureProject(nameOrId) {
  return findProject(nameOrId) || createProject(nameOrId);
}

function saveMeta(id, mut) {
  const file = path.join(pdir(id), 'project.json');
  const p = readJson(file, null);
  if (!p) throw new Error(`프로젝트 없음: ${id}`);
  mut(p);
  p.updatedAt = new Date().toISOString();
  writeJson(file, p);
  bump();
  return p;
}

export function probe(file) {
  try {
    const out = execFileSync('ffprobe', ['-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', file], { encoding: 'utf8' });
    const j = JSON.parse(out);
    const v = j.streams.find((s) => s.codec_type === 'video');
    const [num, den] = String(v?.avg_frame_rate || '30/1').split('/').map(Number);
    return {
      duration: Number(j.format?.duration) || null,
      width: v?.width || null,
      height: v?.height || null,
      fps: den ? Math.round((num / den) * 100) / 100 : 30,
    };
  } catch {
    return { duration: null, width: null, height: null, fps: 30 };
  }
}

/** 새 버전 추가. srcFile 을 복사(move=true 면 이동)합니다. */
export function addVersion(id, srcFile, { note = '', move = false, by = 'claude' } = {}) {
  const ext = (path.extname(srcFile).toLowerCase() || '.mp4');
  if (!VIDEO_EXT.includes(ext)) throw new Error(`지원하지 않는 형식: ${ext}`);
  const dir = path.join(pdir(id), 'versions');
  fs.mkdirSync(dir, { recursive: true });
  let version;
  saveMeta(id, (p) => {
    const n = (p.versions.at(-1)?.n || 0) + 1;
    const file = `v${n}${ext}`;
    const dest = path.join(dir, file);
    if (move) {
      try { fs.renameSync(srcFile, dest); } catch { fs.copyFileSync(srcFile, dest); fs.rmSync(srcFile); }
    } else fs.copyFileSync(srcFile, dest);
    version = { n, file, note, by, createdAt: new Date().toISOString(), ...probe(dest) };
    p.versions.push(version);
  });
  return version;
}

export function versionPath(id, file) {
  if (!/^v\d+\.[a-z0-9]+$/i.test(file)) throw new Error('잘못된 파일명');
  return path.join(pdir(id), 'versions', file);
}

// ---------- 주석 ----------
// status: open(미해결) → fixed(Claude가 수정함, 확인 필요) → done(확인 완료)
export function annotations(id) {
  return readJson(path.join(pdir(id), 'annotations.json'), []);
}
function saveAnnotations(id, list) {
  writeJson(path.join(pdir(id), 'annotations.json'), list);
  saveMeta(id, () => {});
}

export function snapshotPath(id, aid) {
  if (!/^[a-z0-9]+$/i.test(aid)) throw new Error('잘못된 주석 ID');
  return path.join(pdir(id), 'snapshots', `${aid}.jpg`);
}

export function addAnnotation(id, { version, time, x, y, text, snapshot, author = 'me' }) {
  const list = annotations(id);
  const num = (list.reduce((m, a) => Math.max(m, a.num || 0), 0)) + 1;
  const aid = crypto.randomBytes(5).toString('hex');
  const a = {
    id: aid, num, version: Number(version), time: Number(time),
    x: clamp01(x), y: clamp01(y), text: String(text || '').trim(),
    author, status: 'open', createdAt: new Date().toISOString(), history: [],
  };
  if (snapshot && /^data:image\/(jpeg|png);base64,/.test(snapshot)) {
    const file = snapshotPath(id, aid);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, Buffer.from(snapshot.split(',')[1], 'base64'));
    a.snapshot = true;
  }
  list.push(a);
  saveAnnotations(id, list);
  return a;
}

export function updateAnnotation(id, aidOrNum, patch, by = 'me') {
  const list = annotations(id);
  const a = list.find((x) => x.id === aidOrNum || String(x.num) === String(aidOrNum).replace(/^#/, ''));
  if (!a) throw new Error(`주석 없음: ${aidOrNum}`);
  if (patch.text !== undefined) a.text = String(patch.text);
  if (patch.status && patch.status !== a.status) {
    if (!['open', 'fixed', 'done'].includes(patch.status)) throw new Error('잘못된 상태');
    a.history.push({ at: new Date().toISOString(), by, from: a.status, to: patch.status, note: patch.note || '' });
    a.status = patch.status;
    if (patch.status === 'fixed') {
      a.fixedIn = patch.fixedIn ?? latestVersion(id);
      a.resolution = patch.note || a.resolution || '';
    }
    if (patch.status === 'open') { delete a.fixedIn; }
  } else if (patch.note) {
    a.history.push({ at: new Date().toISOString(), by, note: patch.note });
  }
  saveAnnotations(id, list);
  return a;
}

export function deleteAnnotation(id, aid) {
  const list = annotations(id).filter((a) => a.id !== aid);
  try { fs.rmSync(snapshotPath(id, aid)); } catch {}
  saveAnnotations(id, list);
}

function latestVersion(id) {
  const p = readJson(path.join(pdir(id), 'project.json'), { versions: [] });
  return p.versions.at(-1)?.n || null;
}

// ---------- 직접 편집 (자막 · 소리) ----------
export function getEdits(id) {
  return readJson(path.join(pdir(id), 'edits.json'), { volume: 1, subtitles: [], updatedAt: null });
}
export function saveEdits(id, edits) {
  const clean = {
    volume: Math.max(0, Math.min(3, Number(edits.volume ?? 1))),
    subtitles: (edits.subtitles || []).map((s, i) => ({
      id: String(s.id || `s${i + 1}`),
      start: Math.max(0, Number(s.start) || 0),
      end: Math.max(0, Number(s.end) || 0),
      text: String(s.text || ''),
      x: clamp01(s.x ?? 0.5),
      y: clamp01(s.y ?? 0.85),
      size: Math.max(1, Math.min(20, Number(s.size) || 5)), // 화면 높이 대비 %
      color: /^#[0-9a-f]{6}$/i.test(s.color) ? s.color : '#ffffff',
      box: Boolean(s.box),
    })).sort((a, b) => a.start - b.start),
    updatedAt: new Date().toISOString(),
  };
  writeJson(path.join(pdir(id), 'edits.json'), clean);
  saveMeta(id, () => {});
  return clean;
}

function clamp01(v) { const n = Number(v); return Number.isFinite(n) ? Math.max(0, Math.min(1, n)) : 0.5; }

export function fmtTime(t) {
  const m = Math.floor(t / 60), s = t - m * 60;
  return `${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`;
}

/** 화면 위치를 사람이 읽기 쉬운 말로 (Claude 가 이해하기 쉽게) */
export function describePos(x, y) {
  const col = x < 0.34 ? '왼쪽' : x > 0.66 ? '오른쪽' : '가운데';
  const row = y < 0.34 ? '위' : y > 0.66 ? '아래' : '중간';
  if (col === '가운데' && row === '중간') return '화면 정중앙';
  return `${col} ${row}`;
}
