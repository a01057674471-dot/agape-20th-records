// 영상 피드백 — 클라이언트 (프레임워크 없음)
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (t) => { t = Math.max(0, t || 0); const m = Math.floor(t / 60); return `${String(m).padStart(2, '0')}:${(t - m * 60).toFixed(2).padStart(5, '0')}`; };
const STATUS = { open: '미해결', fixed: '확인 대기', done: '완료' };

async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: opts.body && typeof opts.body === 'string' ? { 'Content-Type': 'application/json' } : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}
const json = (o) => JSON.stringify(o);

let toastTimer;
function toast(msg, ms = 2600) {
  const t = $('#toast'); t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => (t.hidden = true), ms);
}

// ---------------- 상태 ----------------
const S = {
  project: null, versionN: null, tab: 'notes', activeNote: null,
  edits: null, editsDirty: false, selectedSub: null, draft: null,
};
const video = $('#video');
const frame = $('#frame');

// ---------------- 라우팅 ----------------
function route() {
  const m = location.hash.match(/^#\/p\/(.+)$/);
  if (m) openProject(decodeURIComponent(m[1]));
  else showHome();
}
window.addEventListener('hashchange', route);

// ---------------- 홈 ----------------
async function showHome() {
  S.project = null;
  video.pause(); video.removeAttribute('src'); video.load();
  $('#project').hidden = true; $('#home').hidden = false;
  document.title = '영상 피드백';
  const list = await api('/api/projects');
  const grid = $('#projectGrid');
  if (!list.length) { grid.innerHTML = '<div class="empty">아직 프로젝트가 없습니다.</div>'; return; }
  grid.innerHTML = list.map((p) => {
    const c = p.counts, tot = c.total || 1;
    return `<div class="card" data-id="${esc(p.id)}">
      <div class="thumb">${p.latest ? `<video src="/media/${encodeURIComponent(p.id)}/${p.latest.file}#t=0.5" preload="metadata" muted></video>` : '<span class="muted">영상 없음</span>'}</div>
      <div class="body">
        <div class="name">${esc(p.name)}</div>
        <div class="meta">v${p.latest?.n || 0} · 주석 ${c.total}개 · ${new Date(p.updatedAt).toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' })}</div>
        <div class="mini-bar"><i style="width:${(c.done / tot) * 100}%;background:var(--done)"></i><i style="width:${(c.fixed / tot) * 100}%;background:var(--fixed)"></i><i style="width:${(c.open / tot) * 100}%;background:var(--open)"></i></div>
        <div class="meta"><span class="dot open"></span>${c.open} <span class="dot fixed"></span>${c.fixed} <span class="dot done"></span>${c.done}</div>
      </div></div>`;
  }).join('');
  $$('.card', grid).forEach((el) => el.addEventListener('click', () => (location.hash = `#/p/${encodeURIComponent(el.dataset.id)}`)));
}

$('#newProject').addEventListener('click', async () => {
  const name = prompt('프로젝트 이름', '새 릴스');
  if (!name) return;
  const p = await api('/api/projects', { method: 'POST', body: json({ name }) });
  location.hash = `#/p/${encodeURIComponent(p.id)}`;
});

const homeDrop = $('#homeDrop');
['dragenter', 'dragover'].forEach((e) => homeDrop.addEventListener(e, (ev) => { ev.preventDefault(); homeDrop.classList.add('over'); }));
['dragleave', 'drop'].forEach((e) => homeDrop.addEventListener(e, () => homeDrop.classList.remove('over')));
homeDrop.addEventListener('drop', async (ev) => {
  ev.preventDefault();
  const f = ev.dataTransfer.files[0]; if (!f) return;
  const p = await api('/api/projects', { method: 'POST', body: json({ name: f.name.replace(/\.[^.]+$/, '') }) });
  await uploadVersion(p.id, f);
  location.hash = `#/p/${encodeURIComponent(p.id)}`;
});

// ---------------- 업로드 ----------------
function uploadVersion(pid, file, note = '') {
  return new Promise((ok, fail) => {
    const ext = (file.name.match(/\.[^.]+$/)?.[0] || '.mp4').toLowerCase();
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `/api/projects/${encodeURIComponent(pid)}/versions?ext=${encodeURIComponent(ext)}&note=${encodeURIComponent(note)}`);
    xhr.upload.onprogress = (e) => e.lengthComputable && toast(`업로드 중… ${Math.round((e.loaded / e.total) * 100)}%`, 60000);
    xhr.onload = () => { if (xhr.status < 300) { toast('새 버전이 올라갔습니다'); ok(JSON.parse(xhr.responseText)); } else { toast('업로드 실패'); fail(new Error(xhr.responseText)); } };
    xhr.onerror = () => { toast('업로드 실패'); fail(new Error('network')); };
    xhr.send(file);
  });
}
$('#uploadInput').addEventListener('change', async (e) => {
  const f = e.target.files[0]; e.target.value = '';
  if (!f || !S.project) return;
  const note = prompt('이번 버전 메모 (선택)', '') ?? '';
  const v = await uploadVersion(S.project.id, f, note);
  S.versionN = v.n; await reloadProject();
});
// 프로젝트 화면 전체에 끌어다 놓기
let dragDepth = 0;
document.addEventListener('dragenter', (e) => { if (!S.project) return; e.preventDefault(); dragDepth++; $('#dropOverlay').hidden = false; });
document.addEventListener('dragover', (e) => { if (S.project) e.preventDefault(); });
document.addEventListener('dragleave', () => { if (--dragDepth <= 0) { dragDepth = 0; $('#dropOverlay').hidden = true; } });
document.addEventListener('drop', async (e) => {
  dragDepth = 0; $('#dropOverlay').hidden = true;
  if (!S.project) return;
  e.preventDefault();
  const f = e.dataTransfer.files[0]; if (!f) return;
  const v = await uploadVersion(S.project.id, f);
  S.versionN = v.n; await reloadProject();
});

// ---------------- 프로젝트 ----------------
async function openProject(id) {
  $('#home').hidden = true; $('#project').hidden = false;
  if (S.project?.id !== id) { S.versionN = null; S.edits = null; S.editsDirty = false; S.selectedSub = null; S.activeNote = null; }
  await reloadProject(id);
}

async function reloadProject(id = S.project?.id) {
  let p;
  try { p = await api(`/api/projects/${encodeURIComponent(id)}`); } catch { location.hash = ''; return; }
  const prev = S.project;
  const prevLatest = prev?.id === p.id ? prev.versions.at(-1)?.n : null;
  const newest = p.versions.at(-1)?.n ?? null;
  S.project = p;
  // 새 버전이 올라왔고 최신 버전을 보고 있었다면 자동으로 넘어갑니다.
  if (S.versionN == null || !p.versions.some((v) => v.n === S.versionN)) S.versionN = newest;
  else if (prevLatest != null && newest > prevLatest && S.versionN === prevLatest) {
    S.versionN = newest; toast(`🎬 v${newest} 이(가) 올라왔습니다`);
  }
  if (!S.editsDirty && !isTypingInEdit() && (!S.edits || S.edits.updatedAt !== p.edits.updatedAt)) {
    S.edits = structuredClone(p.edits); renderSubList(); renderVolume();
  }
  document.title = `${p.name} · 영상 피드백`;
  $('#projTitle').textContent = p.name;
  renderVersionSelect();
  loadVideo();
  renderAll();
}
function isTypingInEdit() { const a = document.activeElement; return a && a.closest?.('[data-body=edit]') && /INPUT|TEXTAREA/.test(a.tagName); }

$('#back').addEventListener('click', () => (location.hash = ''));

function currentVersion() { return S.project?.versions.find((v) => v.n === S.versionN) || null; }

function renderVersionSelect() {
  const sel = $('#versionSel');
  const vs = S.project.versions;
  sel.innerHTML = vs.length ? vs.map((v) => `<option value="${v.n}">v${v.n}${v.n === vs.at(-1).n ? ' (최신)' : ''}</option>`).slice().reverse().join('') : '<option>버전 없음</option>';
  sel.value = S.versionN ?? '';
  const v = currentVersion();
  $('#verNote').textContent = v ? `${v.by === 'claude' ? '🤖' : '🙋'} ${v.note || ''} · ${new Date(v.createdAt).toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' })}` : '';
}
$('#versionSel').addEventListener('change', (e) => { S.versionN = Number(e.target.value); renderVersionSelect(); loadVideo(); renderAll(); });

let loadedSrc = null;
function loadVideo(seekTo) {
  const v = currentVersion();
  $('#emptyStage').hidden = !!v; frame.hidden = !v;
  if (!v) { loadedSrc = null; return; }
  const src = `/media/${encodeURIComponent(S.project.id)}/${v.file}`;
  if (src === loadedSrc) { if (seekTo != null) video.currentTime = seekTo; return; }
  const keep = seekTo ?? (loadedSrc ? video.currentTime : 0);
  const wasPlaying = !video.paused;
  loadedSrc = src;
  video.src = src;
  video.addEventListener('loadedmetadata', () => {
    video.currentTime = Math.min(keep, Math.max(0, video.duration - 0.01));
    if (wasPlaying) video.play();
    renderAll();
  }, { once: true });
}
function fps() { return currentVersion()?.fps || 30; }

// ---------------- 재생 컨트롤 ----------------
let audioCtx, gainNode;
function ensureAudio() {
  if (audioCtx) return;
  try {
    audioCtx = new AudioContext();
    const srcNode = audioCtx.createMediaElementSource(video);
    gainNode = audioCtx.createGain();
    srcNode.connect(gainNode).connect(audioCtx.destination);
    applyGain();
  } catch (e) { console.warn('WebAudio 사용 불가', e); }
}
function applyGain() { if (gainNode) gainNode.gain.value = S.edits?.volume ?? 1; }

function togglePlay() { ensureAudio(); audioCtx?.resume(); if (video.paused) { closeComposer(); video.play(); } else video.pause(); }
function step(dt) { video.pause(); video.currentTime = Math.max(0, Math.min(video.duration || 0, video.currentTime + dt)); }
$('#playBtn').addEventListener('click', togglePlay);
$('#prevFrame').addEventListener('click', () => step(-1 / fps()));
$('#nextFrame').addEventListener('click', () => step(1 / fps()));
$('#rateSel').addEventListener('change', (e) => (video.playbackRate = Number(e.target.value)));
$('#muteBtn').addEventListener('click', () => { video.muted = !video.muted; $('#muteBtn').textContent = video.muted ? '🔇' : '🔊'; });
video.addEventListener('play', () => { $('#playBtn').textContent = '⏸'; frame.classList.remove('annotatable'); });
video.addEventListener('pause', () => { $('#playBtn').textContent = '▶'; frame.classList.add('annotatable'); renderPins(); });
video.addEventListener('timeupdate', onTime);
video.addEventListener('seeked', onTime);
let raf;
video.addEventListener('play', () => { const loop = () => { onTime(); if (!video.paused) raf = requestAnimationFrame(loop); }; raf = requestAnimationFrame(loop); });

function onTime() {
  const d = video.duration || 0, t = video.currentTime;
  $('#timeLabel').textContent = `${fmt(t)} / ${fmt(d)}`;
  const pct = d ? (t / d) * 100 : 0;
  $('#played').style.width = `${pct}%`;
  const tl = $('#timeline');
  $('#playhead').style.left = `calc(16px + (100% - 32px) * ${pct / 100})`;
  void tl;
  renderSubsOverlay();
  renderPins();
}

document.addEventListener('keydown', (e) => {
  if (!S.project || /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
  if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
  else if (e.key === 'ArrowLeft') { e.preventDefault(); step(e.shiftKey ? -1 : -1 / fps()); }
  else if (e.key === 'ArrowRight') { e.preventDefault(); step(e.shiftKey ? 1 : 1 / fps()); }
  else if (e.key === 'Escape') closeComposer();
});

// 타임라인 클릭·드래그로 이동
const timeline = $('#timeline');
function seekFromEvent(e) {
  const r = timeline.getBoundingClientRect();
  const x = Math.max(0, Math.min(1, (e.clientX - r.left - 16) / (r.width - 32)));
  if (video.duration) video.currentTime = x * video.duration;
}
timeline.addEventListener('pointerdown', (e) => {
  if (e.target.closest('.mark, .seg')) return;
  video.pause(); seekFromEvent(e);
  const move = (ev) => seekFromEvent(ev);
  const up = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
});

// ---------------- 주석 남기기 ----------------
frame.addEventListener('click', (e) => {
  if (e.target.closest('.pin, .sub-item') || subDragMoved) return;
  if (!currentVersion()) return;
  video.pause();
  const r = video.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
  if (x < 0 || x > 1 || y < 0 || y > 1) return;
  S.draft = { x, y, time: video.currentTime, version: S.versionN };
  renderPins();
  const c = $('#composer');
  c.hidden = false;
  $('#composerMeta').textContent = `v${S.versionN} · ${fmt(S.draft.time)} · 클릭한 위치에 표시됩니다`;
  const w = 300, h = c.offsetHeight || 150;
  c.style.left = `${Math.min(window.innerWidth - w - 12, Math.max(12, e.clientX + 18))}px`;
  c.style.top = `${Math.min(window.innerHeight - h - 12, Math.max(12, e.clientY - 20))}px`;
  $('#composerText').value = '';
  $('#composerText').focus();
});
function closeComposer() { $('#composer').hidden = true; S.draft = null; renderPins(); }
$('#composerCancel').addEventListener('click', closeComposer);
$('#composerSave').addEventListener('click', saveDraft);
$('#composerText').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); saveDraft(); }
  if (e.key === 'Escape') closeComposer();
});

function snapshot(x, y) {
  try {
    const W = Math.min(960, video.videoWidth), H = Math.round((W / video.videoWidth) * video.videoHeight);
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
    const g = cv.getContext('2d');
    g.drawImage(video, 0, 0, W, H);
    const r = Math.max(14, W * 0.035);
    g.lineWidth = Math.max(3, W * 0.006);
    g.strokeStyle = '#ff2d2d'; g.beginPath(); g.arc(x * W, y * H, r, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = 'rgba(255,255,255,.9)'; g.lineWidth = 1.5; g.beginPath(); g.arc(x * W, y * H, r + g.lineWidth * 2, 0, Math.PI * 2); g.stroke();
    return cv.toDataURL('image/jpeg', 0.85);
  } catch (e) { console.warn('스냅샷 실패', e); return null; }
}

async function saveDraft() {
  const text = $('#composerText').value.trim();
  if (!text || !S.draft) return;
  const d = S.draft;
  // 정확한 프레임을 위해 저장 직전 위치 확인
  if (Math.abs(video.currentTime - d.time) > 0.01) video.currentTime = d.time;
  const body = { ...d, text, snapshot: snapshot(d.x, d.y) };
  closeComposer();
  const a = await api(`/api/projects/${encodeURIComponent(S.project.id)}/annotations`, { method: 'POST', body: json(body) });
  S.activeNote = a.id;
  toast(`#${a.num} 주석을 남겼습니다`);
  await reloadProject();
}

// ---------------- 렌더 ----------------
function renderAll() {
  if (!S.project) return;
  renderProgress(); renderMarks(); renderSubSegs(); renderNotes(); renderChecklist(); renderPins(); renderSubsOverlay();
}

function renderProgress() {
  const c = S.project.counts;
  $('#progressPill').innerHTML = `<span><span class="dot open"></span><b>${c.open}</b> 미해결</span><span><span class="dot fixed"></span><b>${c.fixed}</b> 확인 대기</span><span><span class="dot done"></span><b>${c.done}</b> 완료</span>`;
  $('#tabCountNotes').textContent = c.total || '';
  $('#tabCountCheck').textContent = c.total ? `${c.done}/${c.total}` : '';
}

function renderMarks() {
  const d = video.duration || currentVersion()?.duration || 0;
  const lane = $('#annLane');
  if (!d) { lane.innerHTML = ''; return; }
  lane.innerHTML = S.project.annotations.map((a) => `<div class="mark ${a.status}" data-id="${a.id}" style="left:${Math.min(100, (a.time / d) * 100)}%;${a.version !== S.versionN ? 'opacity:.45' : ''}" title="#${a.num} ${esc(a.text)}"></div>`).join('');
  $$('.mark', lane).forEach((el) => el.addEventListener('click', () => focusNote(el.dataset.id)));
}

function renderPins() {
  const layer = $('#pinLayer');
  if (!S.project) return;
  const t = video.currentTime;
  const near = video.paused ? S.project.annotations.filter((a) => Math.abs(a.time - t) < 0.35 && (a.version === S.versionN || a.status !== 'done')) : [];
  let html = near.map((a) => `<div class="pin ${a.status} ${S.activeNote === a.id ? 'active' : ''}" data-id="${a.id}" style="left:${a.x * 100}%;top:${a.y * 100}%;${a.version !== S.versionN ? 'opacity:.6' : ''}">${a.num}<div class="pin-tip">#${a.num}${a.version !== S.versionN ? ` (v${a.version})` : ''} · ${STATUS[a.status]}\n${esc(a.text)}</div></div>`).join('');
  if (S.draft) html += `<div class="pin draft" style="left:${S.draft.x * 100}%;top:${S.draft.y * 100}%">+</div>`;
  layer.innerHTML = html;
  $$('.pin[data-id]', layer).forEach((el) => el.addEventListener('click', (e) => { e.stopPropagation(); focusNote(el.dataset.id); }));
}

function noteCard(a, { compact = false } = {}) {
  const pid = encodeURIComponent(S.project.id);
  const acts = [];
  if (a.status === 'fixed') acts.push(`<button class="btn small ok" data-act="done">✓ 확인 완료</button><button class="btn small warn" data-act="reopen">↺ 다시 요청</button>`);
  if (a.status === 'done') acts.push(`<button class="btn small" data-act="reopen">↺ 다시 열기</button>`);
  if (a.status === 'open') acts.push(`<button class="btn small" data-act="done" title="직접 확인했으면 완료 처리">✓ 완료</button>`);
  if (!compact) acts.push(`<button class="link-btn" data-act="edit">수정</button><button class="link-btn" data-act="delete">삭제</button>`);
  const reopen = a.history.filter((h) => h.to === 'open' && h.note).at(-1);
  return `<div class="note ${S.activeNote === a.id ? 'active' : ''}" data-id="${a.id}">
    ${a.snapshot ? `<img class="snap" loading="lazy" src="/snap/${pid}/${a.id}.jpg">` : '<div class="snap"></div>'}
    <div>
      <div class="head"><span class="num">#${a.num}</span><span class="chip ${a.status}">${STATUS[a.status]}</span><span>v${a.version} · ${fmt(a.time)}</span>${a.fixedIn ? `<span>→ v${a.fixedIn}</span>` : ''}</div>
      <div class="txt">${esc(a.text)}</div>
      ${a.resolution ? `<div class="res">🤖 ${esc(a.resolution)}</div>` : ''}
      ${reopen && a.status === 'open' ? `<div class="res" style="color:var(--accent-2)">↺ ${esc(reopen.note)}</div>` : ''}
      <div class="acts">${acts.join('')}</div>
    </div></div>`;
}

function renderNotes() {
  const scope = $('#noteScope').value, st = $('#noteStatus').value;
  const list = S.project.annotations
    .filter((a) => (scope === 'all' || a.version === S.versionN) && (st === 'all' || a.status === st))
    .sort((a, b) => a.time - b.time);
  const el = $('#noteList');
  el.innerHTML = list.length ? list.map((a) => noteCard(a)).join('')
    : `<div class="empty-list">${S.project.annotations.length ? '조건에 맞는 주석이 없습니다.' : '영상을 멈추고 고칠 곳을 클릭해 보세요.<br>시간·위치·화면 스냅샷이 함께 저장됩니다.'}</div>`;
  bindNoteEvents(el);
}
$('#noteScope').addEventListener('change', renderNotes);
$('#noteStatus').addEventListener('change', renderNotes);

function bindNoteEvents(root) {
  $$('.note', root).forEach((el) => {
    el.addEventListener('click', (e) => {
      const act = e.target.dataset.act;
      if (act) { e.stopPropagation(); return noteAction(el.dataset.id, act); }
      focusNote(el.dataset.id);
    });
  });
}

async function noteAction(id, act) {
  const a = S.project.annotations.find((x) => x.id === id);
  const url = `/api/projects/${encodeURIComponent(S.project.id)}/annotations/${id}`;
  if (act === 'delete') { if (!confirm(`#${a.num} 주석을 삭제할까요?`)) return; await api(url, { method: 'DELETE' }); }
  if (act === 'edit') { const text = prompt('주석 수정', a.text); if (text == null) return; await api(url, { method: 'PATCH', body: json({ text }) }); }
  if (act === 'done') await api(url, { method: 'PATCH', body: json({ status: 'done' }) });
  if (act === 'reopen') {
    const note = prompt('무엇이 아직 부족한가요? (Claude에게 전달됩니다)', '');
    if (note == null) return;
    await api(url, { method: 'PATCH', body: json({ status: 'open', note }) });
  }
  await reloadProject();
}

/** 주석으로 이동: 확인 대기면 고쳐진 버전으로, 아니면 남긴 버전의 같은 시간으로 */
function focusNote(id, { preferFixed = false } = {}) {
  const a = S.project.annotations.find((x) => x.id === id);
  if (!a) return;
  S.activeNote = id;
  const target = preferFixed && a.fixedIn ? a.fixedIn : (S.versionN ?? a.version);
  video.pause();
  if (target !== S.versionN && S.project.versions.some((v) => v.n === target)) { S.versionN = target; renderVersionSelect(); loadVideo(a.time); }
  else video.currentTime = a.time;
  renderNotes(); renderPins();
  $(`.note[data-id="${id}"]`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

// ---------------- 체크리스트 ----------------
function renderChecklist() {
  const anns = S.project.annotations;
  const c = S.project.counts, tot = c.total || 1;
  $('#checkBar').innerHTML = `<i style="width:${(c.done / tot) * 100}%;background:var(--done)"></i><i style="width:${(c.fixed / tot) * 100}%;background:var(--fixed)"></i>`;
  $('#checkStats').innerHTML = c.total
    ? `<b>${c.done}</b> / ${c.total} 완료 · 확인 대기 ${c.fixed} · 미해결 ${c.open}${c.done === c.total ? ' — 🎉 모든 수정이 반영됐어요!' : ''}`
    : '아직 주석이 없습니다.';
  $('#confirmAll').hidden = !c.fixed;
  const groups = [['fixed', '확인 대기 — Claude가 고쳤어요. 보고 확인해 주세요'], ['open', '미해결'], ['done', '완료']];
  $('#checkList').innerHTML = groups.map(([st, title]) => {
    const items = anns.filter((a) => a.status === st).sort((a, b) => a.time - b.time);
    if (!items.length) return '';
    return `<div class="group-title">${title} (${items.length})</div>` + items.map((a) => `
      <div class="check ${a.status}" data-id="${a.id}">
        <div class="box" data-act="toggle">${a.status === 'done' ? '✓' : ''}</div>
        <div><div class="t">#${a.num} ${esc(a.text)}</div>${a.resolution ? `<div class="r">🤖 ${esc(a.resolution)}</div>` : ''}
          <div class="m">${fmt(a.time)} · v${a.version}에서 요청${a.fixedIn ? ` → v${a.fixedIn}에서 수정` : ''}</div></div>
        ${a.status === 'fixed' ? '<button class="btn small warn" data-act="reopen">↺</button>' : '<span></span>'}
      </div>`).join('');
  }).join('');
  $$('#checkList .check').forEach((el) => el.addEventListener('click', async (e) => {
    const id = el.dataset.id, act = e.target.closest('[data-act]')?.dataset.act;
    const a = anns.find((x) => x.id === id);
    if (act === 'toggle') {
      const url = `/api/projects/${encodeURIComponent(S.project.id)}/annotations/${id}`;
      const next = a.status === 'done' ? (a.fixedIn ? 'fixed' : 'open') : 'done';
      await api(url, { method: 'PATCH', body: json({ status: next, fixedIn: a.fixedIn }) });
      return reloadProject();
    }
    if (act === 'reopen') return noteAction(id, 'reopen');
    focusNote(id, { preferFixed: true });
  }));
}
$('#confirmAll').addEventListener('click', async () => {
  const fixed = S.project.annotations.filter((a) => a.status === 'fixed');
  if (!confirm(`확인 대기 ${fixed.length}개를 모두 완료 처리할까요?`)) return;
  for (const a of fixed) await api(`/api/projects/${encodeURIComponent(S.project.id)}/annotations/${a.id}`, { method: 'PATCH', body: json({ status: 'done' }) });
  await reloadProject();
});

// ---------------- 탭 ----------------
$$('.tabs button').forEach((b) => b.addEventListener('click', () => {
  S.tab = b.dataset.tab;
  $$('.tabs button').forEach((x) => x.classList.toggle('active', x === b));
  $$('.tab-body').forEach((x) => (x.hidden = x.dataset.body !== S.tab));
  frame.classList.toggle('editing', S.tab === 'edit');
  $('#subLane').style.display = S.tab === 'edit' ? '' : 'none';
  renderSubsOverlay();
}));
$('#subLane').style.display = 'none';

// ---------------- 편집: 소리 ----------------
function renderVolume() {
  const v = Math.round((S.edits?.volume ?? 1) * 100);
  $('#volRange').value = v; $('#volNum').value = v;
  applyGain();
}
function setVolume(pct) {
  S.edits.volume = Math.max(0, Math.min(300, Number(pct) || 0)) / 100;
  $('#volRange').value = Math.round(S.edits.volume * 100); $('#volNum').value = Math.round(S.edits.volume * 100);
  ensureAudio(); applyGain(); scheduleSave();
}
$('#volRange').addEventListener('input', (e) => setVolume(e.target.value));
$('#volNum').addEventListener('change', (e) => setVolume(e.target.value));

// ---------------- 편집: 자막 ----------------
let saveTimer;
function scheduleSave() {
  S.editsDirty = true;
  $('#saveState').textContent = '저장 중…';
  clearTimeout(saveTimer);
  saveTimer = setTimeout(async () => {
    try {
      const saved = await api(`/api/projects/${encodeURIComponent(S.project.id)}/edits`, { method: 'PUT', body: json(S.edits) });
      S.edits.updatedAt = saved.updatedAt;
      S.editsDirty = false;
      $('#saveState').textContent = '✓ 저장됨 · Claude가 다음 렌더에 반영';
    } catch (e) { $('#saveState').textContent = `저장 실패: ${e.message}`; }
  }, 500);
}

const subId = () => `s${Date.now().toString(36)}${Math.random().toString(36).slice(2, 5)}`;
$('#addSub').addEventListener('click', () => {
  if (!S.edits) return;
  const t = video.currentTime;
  const last = S.edits.subtitles.at(-1);
  const s = { id: subId(), start: +t.toFixed(2), end: +Math.min(t + 2, video.duration || t + 2).toFixed(2), text: '자막을 입력하세요',
    x: last?.x ?? 0.5, y: last?.y ?? 0.82, size: last?.size ?? 5, color: last?.color ?? '#ffffff', box: last?.box ?? false };
  S.edits.subtitles.push(s);
  S.edits.subtitles.sort((a, b) => a.start - b.start);
  S.selectedSub = s.id;
  renderSubList(); renderSubSegs(); renderSubsOverlay(); scheduleSave();
  $(`.sub[data-id="${s.id}"] textarea`)?.select();
});

function renderSubList() {
  const el = $('#subList');
  if (!S.edits) { el.innerHTML = ''; return; }
  const subs = S.edits.subtitles;
  el.innerHTML = subs.length ? subs.map((s) => `
    <div class="sub ${S.selectedSub === s.id ? 'selected' : ''}" data-id="${s.id}">
      <textarea rows="2" data-k="text">${esc(s.text)}</textarea>
      <div class="times">
        <label>시작 <input type="number" step="0.05" min="0" data-k="start" value="${s.start}"><button class="link-btn" data-now="start" title="현재 시간으로">⏱</button></label>
        <label>끝 <input type="number" step="0.05" min="0" data-k="end" value="${s.end}"><button class="link-btn" data-now="end" title="현재 시간으로">⏱</button></label>
      </div>
      <div class="opts">
        <label>크기 <input type="range" min="2" max="14" step="0.5" data-k="size" value="${s.size}"></label>
        <input type="color" data-k="color" value="${s.color}" title="글자색">
        <label><input type="checkbox" data-k="box" ${s.box ? 'checked' : ''}> 배경</label>
        <span class="spacer"></span>
        <button class="link-btn" data-act="go">▶ 이동</button>
        <button class="link-btn" data-act="del">삭제</button>
      </div>
    </div>`).join('') : '<div class="empty-list">자막이 없습니다. 재생 위치에서 “+ 현재 위치에 추가”를 눌러보세요.<br>Claude가 만든 자막도 <code>import-subs</code>로 불러와 여기서 고칠 수 있어요.</div>';
  $$('.sub', el).forEach((row) => {
    const s = () => S.edits.subtitles.find((x) => x.id === row.dataset.id);
    row.addEventListener('focusin', () => selectSub(row.dataset.id, false));
    row.addEventListener('input', (e) => {
      const k = e.target.dataset.k; if (!k) return;
      const sub = s();
      sub[k] = k === 'box' ? e.target.checked : ['start', 'end', 'size'].includes(k) ? Number(e.target.value) : e.target.value;
      renderSubSegs(); renderSubsOverlay(); scheduleSave();
    });
    row.addEventListener('click', (e) => {
      const sub = s();
      if (e.target.dataset.now) {
        sub[e.target.dataset.now] = +video.currentTime.toFixed(2);
        $(`[data-k=${e.target.dataset.now}]`, row).value = sub[e.target.dataset.now];
        renderSubSegs(); renderSubsOverlay(); scheduleSave();
      }
      if (e.target.dataset.act === 'go') { video.pause(); video.currentTime = sub.start + 0.01; }
      if (e.target.dataset.act === 'del') {
        S.edits.subtitles = S.edits.subtitles.filter((x) => x.id !== sub.id);
        renderSubList(); renderSubSegs(); renderSubsOverlay(); scheduleSave();
      }
    });
  });
}

function selectSub(id, scroll = true) {
  S.selectedSub = id;
  $$('#subList .sub').forEach((r) => r.classList.toggle('selected', r.dataset.id === id));
  if (scroll) $(`#subList .sub[data-id="${id}"]`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  renderSubSegs(); renderSubsOverlay();
}

function renderSubSegs() {
  const d = video.duration || currentVersion()?.duration || 0;
  const lane = $('#subLane');
  if (!d || !S.edits) { lane.innerHTML = ''; return; }
  lane.innerHTML = S.edits.subtitles.map((s) => `<div class="seg ${S.selectedSub === s.id ? 'selected' : ''}" data-id="${s.id}" style="left:${(s.start / d) * 100}%;width:${Math.max(0.4, ((s.end - s.start) / d) * 100)}%" title="${esc(s.text)}"></div>`).join('');
  $$('.seg', lane).forEach((el) => el.addEventListener('click', () => {
    const s = S.edits.subtitles.find((x) => x.id === el.dataset.id);
    video.pause(); video.currentTime = s.start + 0.01;
    if (S.tab !== 'edit') $('.tabs [data-tab=edit]').click();
    selectSub(s.id);
  }));
}

function renderSubsOverlay() {
  const layer = $('#subLayer');
  if (!S.edits) { layer.innerHTML = ''; return; }
  const t = video.currentTime, h = frame.clientHeight || 1;
  const active = S.edits.subtitles.filter((s) => t >= s.start && t < s.end);
  layer.innerHTML = active.map((s) => `<div class="sub-item ${s.box ? 'box' : ''} ${S.selectedSub === s.id ? 'selected' : ''}" data-id="${s.id}"
    style="left:${s.x * 100}%;top:${s.y * 100}%;font-size:${(s.size / 100) * h}px;color:${s.color}">${esc(s.text)}</div>`).join('');
}
window.addEventListener('resize', renderSubsOverlay);

// 자막 끌어서 위치 옮기기
let subDragMoved = false;
$('#subLayer').addEventListener('pointerdown', (e) => {
  const el = e.target.closest('.sub-item');
  if (!el || S.tab !== 'edit') return;
  e.preventDefault(); e.stopPropagation();
  const sub = S.edits.subtitles.find((x) => x.id === el.dataset.id);
  selectSub(sub.id);
  const r = frame.getBoundingClientRect();
  const ox = e.clientX - (sub.x * r.width + r.left), oy = e.clientY - (sub.y * r.height + r.top);
  subDragMoved = false;
  const move = (ev) => {
    subDragMoved = true;
    sub.x = Math.max(0, Math.min(1, (ev.clientX - ox - r.left) / r.width));
    sub.y = Math.max(0, Math.min(1, (ev.clientY - oy - r.top) / r.height));
    // 가운데 정렬 스냅
    if (Math.abs(sub.x - 0.5) < 0.015) sub.x = 0.5;
    renderSubsOverlay();
  };
  const up = () => {
    window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up);
    if (subDragMoved) scheduleSave();
    setTimeout(() => (subDragMoved = false), 0);
  };
  window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
});

// ---------------- 실시간 반영 (Claude가 새 버전/처리 결과를 올리면) ----------------
let lastRev = null, reloadTimer;
const es = new EventSource('/api/events');
es.onmessage = (e) => {
  const r = Number(e.data);
  if (lastRev !== null && r !== lastRev) {
    clearTimeout(reloadTimer);
    reloadTimer = setTimeout(() => (S.project ? reloadProject() : !$('#home').hidden && showHome()), 250);
  }
  lastRev = r;
};

route();
