#!/usr/bin/env node
// 영상 피드백 사이트 서버 — 의존성 없음 (Node 18+)
// 실행: node video-feedback/server.mjs   →  http://localhost:4321
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import * as store from './lib/store.mjs';

const PORT = Number(process.env.PORT || 4321);
const PUBLIC = path.join(store.ROOT, 'public');
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime', '.m4v': 'video/mp4',
};

// ---------- 실시간 새로고침 (SSE) ----------
const clients = new Set();
let lastRev = store.rev();
setInterval(() => {
  const r = store.rev();
  if (r !== lastRev) {
    lastRev = r;
    for (const res of clients) res.write(`data: ${r}\n\n`);
  }
}, 700);
setInterval(() => { for (const res of clients) res.write(': ping\n\n'); }, 25000);

// ---------- inbox 감시: 렌더된 영상을 inbox/<프로젝트이름>.mp4 로 두면 자동 업로드 ----------
const pending = new Map();
function scanInbox() {
  for (const name of fs.readdirSync(store.INBOX)) {
    const ext = path.extname(name).toLowerCase();
    if (!store.VIDEO_EXT.includes(ext)) continue;
    const file = path.join(store.INBOX, name);
    let st; try { st = fs.statSync(file); } catch { continue; }
    const prev = pending.get(file);
    // 파일 크기가 두 번 연속 같으면(쓰기 완료) 가져옵니다.
    if (!prev || prev !== `${st.size}:${st.mtimeMs}`) { pending.set(file, `${st.size}:${st.mtimeMs}`); continue; }
    pending.delete(file);
    const base = path.basename(name, ext);
    const [projName, ...noteParts] = base.split('__');
    try {
      const p = store.ensureProject(projName);
      const v = store.addVersion(p.id, file, { move: true, note: noteParts.join(' ').replace(/[-_]/g, ' ') || 'inbox 자동 업로드' });
      console.log(`📥 inbox → ${p.name} v${v.n}`);
    } catch (e) { console.error('inbox 가져오기 실패:', e.message); }
  }
}
setInterval(scanInbox, 1500);

// ---------- 유틸 ----------
function send(res, code, body, type = 'application/json; charset=utf-8') {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(typeof body === 'string' || Buffer.isBuffer(body) ? body : JSON.stringify(body));
}
async function readBody(req, limit = 30 * 1024 * 1024) {
  const chunks = []; let size = 0;
  for await (const c of req) { size += c.length; if (size > limit) throw new Error('요청이 너무 큽니다'); chunks.push(c); }
  const txt = Buffer.concat(chunks).toString('utf8');
  return txt ? JSON.parse(txt) : {};
}
function serveFile(req, res, file, type) {
  let st;
  try { st = fs.statSync(file); } catch { return send(res, 404, { error: 'not found' }); }
  const ct = type || MIME[path.extname(file).toLowerCase()] || 'application/octet-stream';
  const range = req.headers.range;
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range);
    let start = m[1] ? Number(m[1]) : 0;
    let end = m[2] ? Number(m[2]) : st.size - 1;
    if (!m[1] && m[2]) { start = st.size - Number(m[2]); end = st.size - 1; }
    if (start >= st.size) { res.writeHead(416, { 'Content-Range': `bytes */${st.size}` }); return res.end(); }
    res.writeHead(206, {
      'Content-Type': ct, 'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1,
      'Content-Range': `bytes ${start}-${end}/${st.size}`, 'Cache-Control': 'no-cache',
    });
    fs.createReadStream(file, { start, end }).pipe(res);
  } else {
    res.writeHead(200, { 'Content-Type': ct, 'Content-Length': st.size, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache' });
    fs.createReadStream(file).pipe(res);
  }
}

// ---------- 라우팅 ----------
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const parts = url.pathname.split('/').filter(Boolean).map(decodeURIComponent);
  try {
    if (parts[0] === 'api') {
      const [, a, id, b, sub] = parts;
      if (a === 'events') {
        res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-store', Connection: 'keep-alive' });
        res.write(`data: ${store.rev()}\n\n`);
        clients.add(res); req.on('close', () => clients.delete(res));
        return;
      }
      if (a === 'projects' && !id) {
        if (req.method === 'GET') return send(res, 200, store.listProjects());
        if (req.method === 'POST') { const { name } = await readBody(req); return send(res, 201, store.createProject(name || '새 프로젝트')); }
      }
      if (a === 'projects' && id) {
        if (!b && req.method === 'GET') {
          const p = store.getProject(id);
          return p ? send(res, 200, p) : send(res, 404, { error: '프로젝트 없음' });
        }
        if (b === 'versions' && req.method === 'POST') {
          // 원본 바이트 스트림 업로드 (브라우저 드래그 앤 드롭)
          const ext = (url.searchParams.get('ext') || '.mp4').toLowerCase();
          const tmp = path.join(os.tmpdir(), `vf-upload-${Date.now()}${ext}`);
          await new Promise((ok, fail) => { const w = fs.createWriteStream(tmp); req.pipe(w); w.on('finish', ok); w.on('error', fail); });
          const v = store.addVersion(id, tmp, { move: true, note: url.searchParams.get('note') || '', by: 'me' });
          return send(res, 201, v);
        }
        if (b === 'annotations' && !sub && req.method === 'POST') return send(res, 201, store.addAnnotation(id, await readBody(req)));
        if (b === 'annotations' && sub && req.method === 'PATCH') return send(res, 200, store.updateAnnotation(id, sub, await readBody(req), 'me'));
        if (b === 'annotations' && sub && req.method === 'DELETE') { store.deleteAnnotation(id, sub); return send(res, 200, { ok: true }); }
        if (b === 'edits' && req.method === 'GET') return send(res, 200, store.getEdits(id));
        if (b === 'edits' && req.method === 'PUT') return send(res, 200, store.saveEdits(id, await readBody(req)));
      }
      return send(res, 404, { error: 'unknown api' });
    }
    if (parts[0] === 'media' && parts.length === 3) return serveFile(req, res, store.versionPath(parts[1], parts[2]));
    if (parts[0] === 'snap' && parts.length === 3) return serveFile(req, res, store.snapshotPath(parts[1], parts[2].replace(/\.jpg$/, '')), 'image/jpeg');

    // 정적 파일 (화면 이동은 #/p/<id> 해시 라우팅)
    const rel = parts.length ? parts.join('/') : 'index.html';
    const file = path.join(PUBLIC, rel);
    if (file.startsWith(PUBLIC) && fs.existsSync(file) && fs.statSync(file).isFile()) return serveFile(req, res, file);
    return serveFile(req, res, path.join(PUBLIC, 'index.html'));
  } catch (e) {
    console.error(e);
    return send(res, 400, { error: e.message });
  }
});

server.listen(PORT, () => {
  console.log(`\n🎬 영상 피드백 사이트: http://localhost:${PORT}`);
  console.log(`📂 데이터: ${store.DATA}`);
  console.log(`📥 자동 업로드 폴더: ${store.INBOX}  (파일명 = 프로젝트 이름.mp4)\n`);
});
