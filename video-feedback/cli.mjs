#!/usr/bin/env node
// Claude 가 피드백 사이트와 대화하는 CLI.
//   node video-feedback/cli.mjs help
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import * as store from './lib/store.mjs';

const [cmd, ...rest] = process.argv.slice(2);
const flags = {}; const args = [];
for (let i = 0; i < rest.length; i++) {
  const r = rest[i];
  if (r.startsWith('--')) {
    const k = r.slice(2);
    const next = rest[i + 1];
    if (next === undefined || next.startsWith('--')) flags[k] = true; else { flags[k] = next; i++; }
  } else args.push(r);
}

const STATUS_KO = { open: '미해결', fixed: '수정됨·확인대기', done: '완료' };

function die(msg) { console.error(`✖ ${msg}`); process.exit(1); }

/** 프로젝트 인자가 없으면 가장 최근 프로젝트 */
function project(arg) {
  const p = arg ? store.findProject(arg) : store.listProjects()[0];
  if (!p) die(arg ? `프로젝트를 찾을 수 없습니다: ${arg}` : '프로젝트가 없습니다. 먼저 upload 하세요.');
  return store.getProject(p.id);
}

function printAnn(p, a) {
  const snap = a.snapshot ? store.snapshotPath(p.id, a.id) : null;
  console.log(`#${a.num}  [${STATUS_KO[a.status]}]  v${a.version} @ ${store.fmtTime(a.time)}  (${a.time.toFixed(2)}s)`);
  console.log(`    위치: ${store.describePos(a.x, a.y)}  — x ${(a.x * 100).toFixed(0)}%, y ${(a.y * 100).toFixed(0)}%`);
  console.log(`    요청: ${a.text}`);
  if (a.resolution) console.log(`    처리: ${a.resolution}${a.fixedIn ? ` (v${a.fixedIn})` : ''}`);
  const reopen = a.history.filter((h) => h.to === 'open').at(-1);
  if (reopen?.note) console.log(`    재요청: ${reopen.note}`);
  if (snap) console.log(`    스냅샷: ${snap}`);
  console.log('');
}

const commands = {
  help() {
    console.log(`영상 피드백 CLI

  list                                   프로젝트 목록
  upload <프로젝트> <영상파일> [--note 메모] [--fixes 1,2,5]
                                         새 버전 올리기 (없으면 프로젝트 생성). --fixes 로 고친 주석 표시
  feedback [프로젝트] [--status open|fixed|done|all] [--json]
                                         주석 읽기 (기본: 미해결만). 스냅샷 경로 포함
  resolve [프로젝트] <#번호...> --note "무엇을 고쳤는지" [--in 버전]
                                         수정 완료 표시 → 사용자가 사이트에서 확인
  status [프로젝트]                       진행 현황 요약
  edits [프로젝트] [--json]                사용자가 편집 탭에서 직접 고친 자막·소리
  import-subs [프로젝트] <자막.srt|.json> [--replace] [--y 0.82] [--size 5]
                                         Claude 자막을 편집 탭으로 (사용자가 직접 고칠 수 있게)
  export-subs [프로젝트] <out.srt|out.ass>  편집 탭 자막을 SRT/ASS 로 저장
  apply-edits [프로젝트] <입력영상> <출력영상>  편집 탭 자막·소리를 ffmpeg 로 입혀서 렌더

프로젝트를 생략하면 가장 최근 프로젝트를 사용합니다.`);
  },

  list() {
    const all = store.listProjects();
    if (!all.length) return console.log('(프로젝트 없음)');
    for (const p of all) {
      const c = p.counts;
      console.log(`${p.id}  "${p.name}"  v${p.latest?.n || 0}  주석 ${c.total} (미해결 ${c.open} · 확인대기 ${c.fixed} · 완료 ${c.done})`);
    }
  },

  upload() {
    const [name, file] = args;
    if (!name || !file) die('사용법: upload <프로젝트> <영상파일> [--note 메모]');
    if (!fs.existsSync(file)) die(`파일 없음: ${file}`);
    const p = store.ensureProject(name);
    const v = store.addVersion(p.id, path.resolve(file), { note: flags.note === true ? '' : flags.note || '' });
    console.log(`✔ ${p.name} v${v.n} 업로드 (${v.duration?.toFixed(1) ?? '?'}s, ${v.width}x${v.height})`);
    if (flags.fixes && flags.fixes !== true) {
      for (const n of String(flags.fixes).split(/[,\s]+/).filter(Boolean)) {
        const a = store.updateAnnotation(p.id, n, { status: 'fixed', fixedIn: v.n, note: flags.note === true ? '' : flags.note || '' }, 'claude');
        console.log(`  ✔ #${a.num} → 수정됨: ${a.text}`);
      }
    }
    const open = store.annotations(p.id).filter((a) => a.status === 'open').length;
    if (open) console.log(`  아직 미해결 주석 ${open}개가 있습니다. 고친 것은 resolve 로 표시하세요.`);
  },

  feedback() {
    const p = project(args[0]);
    const want = flags.status || 'open';
    const list = p.annotations.filter((a) => want === 'all' || a.status === want).sort((a, b) => a.time - b.time);
    if (flags.json) {
      return console.log(JSON.stringify(list.map((a) => ({ ...a, position: store.describePos(a.x, a.y), snapshotPath: a.snapshot ? store.snapshotPath(p.id, a.id) : null })), null, 2));
    }
    const latest = p.versions.at(-1);
    console.log(`🎬 ${p.name} — 최신 v${latest?.n ?? '-'} (${latest?.width}x${latest?.height}, ${latest?.fps}fps, ${latest?.duration?.toFixed(2)}s)`);
    console.log(`   ${STATUS_KO[want] || '전체'} 주석 ${list.length}개 / 전체 ${p.counts.total}개\n`);
    for (const a of list) printAnn(p, a);
    const e = p.edits;
    if (e.updatedAt) console.log(`ℹ 편집 탭 변경 있음 (소리 ${Math.round(e.volume * 100)}%, 자막 ${e.subtitles.length}개) — "edits" 로 확인`);
  },

  resolve() {
    // 첫 인자가 번호(#3, 3)가 아니면 프로젝트 이름으로 봅니다.
    const p = project(args[0] && !/^#?\d+$/.test(args[0]) ? args.shift() : undefined);
    if (!args.length) die('사용법: resolve [프로젝트] <#번호...> --note "고친 내용"');
    for (const n of args) {
      const a = store.updateAnnotation(p.id, n, { status: 'fixed', fixedIn: flags.in ? Number(flags.in) : undefined, note: flags.note === true ? '' : flags.note || '' }, 'claude');
      console.log(`✔ #${a.num} → 수정됨 (v${a.fixedIn}) : ${a.text}`);
    }
  },

  status() {
    const p = project(args[0]);
    const c = p.counts;
    const pct = c.total ? Math.round((c.done / c.total) * 100) : 0;
    console.log(`🎬 ${p.name}  버전 ${p.versions.length}개`);
    console.log(`   주석 ${c.total}개 — 미해결 ${c.open} · 확인대기 ${c.fixed} · 완료 ${c.done}  (${pct}% 완료)`);
  },

  edits() {
    const p = project(args[0]);
    if (flags.json) return console.log(JSON.stringify(p.edits, null, 2));
    const e = p.edits;
    console.log(`🔊 소리 크기: ${Math.round(e.volume * 100)}%`);
    console.log(`💬 자막 ${e.subtitles.length}개`);
    for (const s of e.subtitles) {
      console.log(`  ${store.fmtTime(s.start)} → ${store.fmtTime(s.end)}  "${s.text}"  (${store.describePos(s.x, s.y)}, 크기 ${s.size}%, ${s.color}${s.box ? ', 배경박스' : ''})`);
    }
  },

  'export-subs'() {
    const p = project(args.length > 1 ? args.shift() : undefined);
    const out = args[0]; if (!out) die('사용법: export-subs [프로젝트] <out.srt|out.ass>');
    const v = p.versions.at(-1) || { width: 1080, height: 1920 };
    fs.writeFileSync(out, out.endsWith('.ass') ? toAss(p.edits, v.width || 1080, v.height || 1920) : toSrt(p.edits));
    console.log(`✔ ${out}`);
  },

  'import-subs'() {
    const p = project(args.length > 1 ? args.shift() : undefined);
    const file = args[0]; if (!file) die('사용법: import-subs [프로젝트] <자막.srt|자막.json> [--y 0.82] [--size 5] [--replace]');
    const raw = fs.readFileSync(file, 'utf8');
    let subs;
    if (file.endsWith('.json')) subs = JSON.parse(raw);
    else {
      const t = (s) => { const [h, m, rest] = s.trim().replace(',', '.').split(':'); return Number(h) * 3600 + Number(m) * 60 + Number(rest); };
      subs = raw.replace(/\r/g, '').split(/\n\s*\n/).map((b) => b.trim().split('\n')).filter((l) => l.length >= 2).map((l) => {
        const i = l.findIndex((x) => x.includes('-->'));
        const [a, b] = l[i].split('-->');
        return { start: t(a), end: t(b), text: l.slice(i + 1).join('\n') };
      });
    }
    const base = {
      x: 0.5, y: flags.y ? Number(flags.y) : 0.82, size: flags.size ? Number(flags.size) : 5, color: '#ffffff', box: false,
    };
    const existing = flags.replace ? [] : p.edits.subtitles;
    const merged = [...existing, ...subs.map((s, i) => ({ ...base, id: `i${Date.now().toString(36)}${i}`, ...s }))];
    const saved = store.saveEdits(p.id, { ...p.edits, subtitles: merged });
    console.log(`✔ 자막 ${subs.length}개 → 편집 탭 (총 ${saved.subtitles.length}개). 이 자막은 영상에 굽지 말고 apply-edits 로 입히세요.`);
  },

  'apply-edits'() {
    const p = project(args.length > 2 ? args.shift() : undefined);
    const [input, output] = args;
    if (!input || !output) die('사용법: apply-edits [프로젝트] <입력영상> <출력영상>');
    const info = store.probe(input);
    const filters = [];
    const tmpAss = path.join(path.dirname(path.resolve(output)), `.vf-${Date.now()}.ass`);
    const ff = ['-hide_banner', '-loglevel', 'error', '-y', '-i', input];
    if (p.edits.subtitles.length) {
      fs.writeFileSync(tmpAss, toAss(p.edits, info.width || 1080, info.height || 1920));
      filters.push(`ass=${tmpAss.replace(/([:\\'])/g, '\\$1')}`);
      ff.push('-vf', filters.join(','), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p');
    } else ff.push('-c:v', 'copy');
    if (p.edits.volume !== 1) ff.push('-af', `volume=${p.edits.volume}`, '-c:a', 'aac', '-b:a', '192k');
    else ff.push('-c:a', 'copy');
    ff.push(output);
    try { execFileSync('ffmpeg', ff, { stdio: ['ignore', 'ignore', 'inherit'] }); }
    finally { fs.rmSync(tmpAss, { force: true }); }
    console.log(`✔ 편집 반영 → ${output}`);
  },
};

function srtTime(t) {
  const ms = Math.round(t * 1000);
  const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`;
}
function toSrt(e) {
  return e.subtitles.map((s, i) => `${i + 1}\n${srtTime(s.start)} --> ${srtTime(s.end)}\n${s.text}\n`).join('\n');
}
function assTime(t) {
  const cs = Math.round(t * 100);
  const h = Math.floor(cs / 360000), m = Math.floor(cs / 6000) % 60, s = Math.floor(cs / 100) % 60;
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs % 100).padStart(2, '0')}`;
}
function assColor(hex) { const [r, g, b] = [1, 3, 5].map((i) => hex.slice(i, i + 2)); return `&H00${b}${g}${r}`.toUpperCase(); }
function toAss(e, W, H) {
  const lines = [
    '[Script Info]', 'ScriptType: v4.00+', `PlayResX: ${W}`, `PlayResY: ${H}`, 'WrapStyle: 0', '',
    '[V4+ Styles]',
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
    `Style: Default,Pretendard,${Math.round(H * 0.05)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,${Math.max(2, Math.round(H / 400))},0,5,0,0,0,1`,
    `Style: Box,Pretendard,${Math.round(H * 0.05)},&H00FFFFFF,&H00FFFFFF,&HA0000000,&HA0000000,1,0,0,0,100,100,0,0,3,${Math.round(H / 120)},0,5,0,0,0,1`,
    '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
  ];
  for (const s of e.subtitles) {
    const txt = s.text.replace(/\n/g, '\\N').replace(/[{}]/g, '');
    const tags = `{\\an5\\pos(${Math.round(s.x * W)},${Math.round(s.y * H)})\\fs${Math.round((s.size / 100) * H)}\\c${assColor(s.color)}&}`;
    lines.push(`Dialogue: 0,${assTime(s.start)},${assTime(s.end)},${s.box ? 'Box' : 'Default'},,0,0,0,,${tags}${txt}`);
  }
  return lines.join('\n') + '\n';
}

(commands[cmd] || commands.help)();
