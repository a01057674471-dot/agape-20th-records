// 「러닝 후 바로 하면 안 되는 것 5가지」 — 31초 세로 릴스. 밝고 깔끔한 라이프스타일 톤:
// 사진은 화면 가득, ❌는 빨간 ✕ 도장 + 살짝 흔들림, ⭕는 청록 동그라미가 그려지며 옆으로 밀려 넘어감.
// 시간은 audio/lines_paced.json (나레이션 녹음을 음성 인식으로 맞춘 줄별 시간, 카드마다 숨 쉴 틈을 넣은 것).
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = 1080, H = 1920, FONT = '"Noto Sans KR"';
const NOSUB = new URLSearchParams(location.search).has('nosub');
const RED = '#FF4D5A', TEAL = '#22C3B4', WHITE = '#FFFFFF', DARK = '#12201F';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = t => { t = clamp(t); const s = 1.8; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };

const ITEMS = [
  { x: 1, o: 3, xi: 1, oi: 4, xt: '바로 주저앉기', xr: '피가 다리에 몰려 어지러울 수 있어요', ot: '3~5분 천천히 걷기', or: '숨이 고르게 내려올 때까지' },
  { x: 4, o: 6, xi: 3, oi: 2, xt: '땀에 젖은 옷 그대로', xr: '몸이 식고 피부 트러블이 생길 수 있어요', ot: '바로 갈아입기', or: '땀은 닦고, 마른 옷으로' },
  { x: 7, o: 8, xi: 5, oi: 6, xt: '바로 뜨거운 샤워·사우나', xr: '심박이 덜 내려와 어지러울 수 있어요', ot: '숨 고른 뒤 미지근한 물부터', or: '' },
  { x: 9, o: 10, xi: 7, oi: 8, xt: '물 안 마시기 · 벌컥벌컥', xr: '한 번에 많이 마시면 속이 불편할 수 있어요', ot: '조금씩 나눠 마시기', or: '' },
  { x: 11, o: 13, xi: 9, oi: 10, xt: '\'뛰었으니까\' 바로 맥주', xr: '수분이 더 빠지고 회복이 느려져요', ot: '물과 식사 먼저', or: '' },
];
let LN, PH, DUR;
const IMG = {};

function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function photo(c, k, z, dx = 0) { const im = IMG[k], h = H * z, w = h * im.width / im.height; c.drawImage(im, W / 2 - w / 2 + dx, H / 2 - h / 2, w, h); }
function topShade(c, a = .55) {
  const g = c.createLinearGradient(0, 0, 0, 760); g.addColorStop(0, `rgba(10,20,20,${a})`); g.addColorStop(1, 'rgba(10,20,20,0)'); c.fillStyle = g; c.fillRect(0, 0, W, 760);
  const b = c.createLinearGradient(0, H, 0, H - 620); b.addColorStop(0, 'rgba(10,20,20,.5)'); b.addColorStop(1, 'rgba(10,20,20,0)'); c.fillStyle = b; c.fillRect(0, H - 620, W, 620);
}
function rich(c, ln, x, y, col = WHITE, acc = TEAL) {
  const parts = ln.split('*'), ws = parts.map(s => c.measureText(s).width), tot = ws.reduce((a, b) => a + b, 0); let xx = x - tot / 2; c.textAlign = 'left';
  parts.forEach((s, k) => { c.fillStyle = k % 2 ? acc : col; c.fillText(s, xx, y); xx += ws[k]; });
}
function mark(c, bad, x, y, r, p, col) {     // the red cross or the teal circle, drawn as strokes
  c.save(); c.translate(x, y); c.lineCap = 'round'; c.lineWidth = Math.max(4, r * .22); c.strokeStyle = col || (bad ? RED : TEAL);
  c.shadowColor = 'rgba(0,0,0,.3)'; c.shadowBlur = 16;
  if (bad) { const q1 = eo(seg(p, 0, .5)), q2 = eo(seg(p, .4, .9));
    c.beginPath(); c.moveTo(-r, -r); c.lineTo(-r + 2 * r * q1, -r + 2 * r * q1); c.stroke();
    if (q2 > 0) { c.beginPath(); c.moveTo(r, -r); c.lineTo(r - 2 * r * q2, -r + 2 * r * q2); c.stroke(); } }
  else { c.beginPath(); c.arc(0, 0, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * eo(p)); c.stroke(); }
  c.restore();
}
const TY = 940;   // the NG/OK block sits at the middle of the frame, below the faces
function band(c, y0, y1, a = .42) {   // a soft dark band behind middle text, so it reads without a box
  const g = c.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, 'rgba(10,20,20,0)'); g.addColorStop(.3, `rgba(10,20,20,${a})`); g.addColorStop(.7, `rgba(10,20,20,${a})`); g.addColorStop(1, 'rgba(10,20,20,0)');
  c.fillStyle = g; c.fillRect(0, y0, W, y1 - y0);
}
function titleBlock(c, bad, n, title, reason, lt) {
  band(c, TY - 190, TY + (reason ? 190 : 120), .4 * eo(seg(lt, 0, .25)));
  for (let k = 1; k <= 5; k++) { const x = 540 + (k - 3) * 52, on = k <= n;
    c.fillStyle = k === n ? (bad ? RED : TEAL) : on ? 'rgba(255,255,255,.9)' : 'rgba(255,255,255,.35)'; c.beginPath(); c.arc(x, TY - 140, k === n ? 12 : 8, 0, 7); c.fill(); }
  const p = back(seg(lt, 0, .32));
  c.save(); c.translate(540, TY); c.scale(p, p);
  c.font = `900 40px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  const tag = bad ? `NG 0${n}` : `OK 0${n}`, tw = c.measureText(tag).width + 100;
  c.fillStyle = bad ? RED : TEAL; rr(c, -tw / 2, -90, tw, 58, 29); c.fill(); c.fillStyle = WHITE; c.fillText(tag, 24, -60);
  c.restore();
  mark(c, bad, 540 - tw * p / 2 + 34, TY - 61, 13, seg(lt, .15, .5), WHITE);
  c.save(); c.translate(540, TY); c.scale(p, p); c.textAlign = 'center'; c.textBaseline = 'middle';
  c.font = `900 ${title.length > 13 ? 64 : 76}px ${FONT}`; c.shadowColor = 'rgba(0,0,0,.6)'; c.shadowBlur = 24; c.fillStyle = WHITE; c.fillText(title, 0, 28);
  c.restore();
  if (reason) { const q = eo(seg(lt, .3, .7)); c.save(); c.globalAlpha = q; c.font = `700 40px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
    c.shadowColor = 'rgba(0,0,0,.7)'; c.shadowBlur = 18; c.fillStyle = 'rgba(255,255,255,.94)'; c.fillText(reason, 540, TY + 120 + (1 - q) * 14); c.restore(); }
}
function subtitle(c, t) {
  for (const [k, l] of LN.entries()) {
    const nx = k + 1 < LN.length ? LN[k + 1].t0 - .1 : 1e9, e = Math.min(l.t1 + .35, nx);
    const al = ss(seg(t, l.t0 - .1, l.t0 + .06)) * (1 - ss(seg(t, e - .1, e))); if (al <= 0) continue;
    c.save(); c.globalAlpha = al; c.font = `700 42px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
    const tw = c.measureText(l.text).width; c.fillStyle = 'rgba(10,20,20,.6)'; rr(c, W / 2 - tw / 2 - 28, 1500 - 40, tw + 56, 80, 18); c.fill();
    c.fillStyle = WHITE; c.fillText(l.text, W / 2, 1502); c.restore();
  }
}

// ---------- the phases ----------
function phases() {
  const P = [{ t0: 0, kind: 'hook' }];
  ITEMS.forEach((it, i) => { P.push({ t0: LN[it.x].t0 - .15, kind: 'x', i }); P.push({ t0: LN[it.o].t0 - .15, kind: 'o', i }); });
  P.push({ t0: LN[14].t0 - .2, kind: 'end' });
  return P;
}
const at = t => { let i = 0; while (i + 1 < PH.length && t >= PH[i + 1].t0) i++; return i; };
function draw(c, k, t) {
  const p = PH[k], lt = t - p.t0, len = (k + 1 < PH.length ? PH[k + 1].t0 : DUR) - p.t0;
  c.fillStyle = DARK; c.fillRect(0, 0, W, H);
  if (p.kind === 'hook') {
    photo(c, 1, 1.12 - .06 * ss(lt / len)); topShade(c, .3); band(c, 720, 1100, .4);
    c.font = `900 82px ${FONT}`; c.textBaseline = 'middle';
    ['러닝 끝나고 이거 하면,', '뛴 거 *손해* 봅니다'].forEach((ln, j) => { const q = eo(seg(lt, .15 + j * .25, .55 + j * .25));
      c.save(); c.globalAlpha = q; c.shadowColor = 'rgba(0,0,0,.65)'; c.shadowBlur = 26; rich(c, ln, 540, 880 + j * 110 + (1 - q) * 30, WHITE, '#FFD34D'); c.restore(); });
  } else if (p.kind === 'x' || p.kind === 'o') {
    const it = ITEMS[p.i], bad = p.kind === 'x', img = bad ? it.xi : it.oi;
    // ❌: a jolt when the cross lands; ⭕: a calm push
    const j = bad ? Math.max(0, 1 - Math.abs(lt - .42) / .16) : 0, sx = (hash(Math.floor(t * 30)) - .5) * 26 * j;
    photo(c, img, bad && p.i === 0 ? 1.06 - .02 * ss(lt / len) : 1.03 + .04 * ss(lt / len), sx);
    topShade(c, .25);
    if (bad) { c.fillStyle = `rgba(255,77,90,${.10 * j})`; c.fillRect(0, 0, W, H); }
    titleBlock(c, bad, p.i + 1, bad ? it.xt : it.ot, bad ? it.xr : it.or, lt);
  } else {
    photo(c, 4, 1.06 + .03 * ss(lt / len)); c.fillStyle = 'rgba(10,20,20,.55)'; c.fillRect(0, 0, W, H);
    c.font = `900 84px ${FONT}`; c.textBaseline = 'middle';
    ['잘 뛰는 것만큼,', '잘 끝내는 게 *실력*'].forEach((ln, jj) => { const q = eo(seg(lt, .1 + jj * .28, .5 + jj * .28));
      c.save(); c.globalAlpha = q; c.shadowColor = 'rgba(0,0,0,.5)'; c.shadowBlur = 20; rich(c, ln, 540, 700 + jj * 116 + (1 - q) * 30); c.restore(); });
    const q1 = back(seg(lt, 1.9, 2.3)), q2 = back(seg(lt, 2.6, 3.0));
    const pill = (txt, y, q, fill, col, ic) => { if (q <= 0) return; c.save(); c.translate(540, y); c.scale(q, q); c.font = `900 46px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
      const w = c.measureText(txt).width + 150; c.fillStyle = fill; rr(c, -w / 2, -48, w, 96, 48); c.fill(); c.fillStyle = col; c.fillText(txt, 26, 3); ic(c, -w / 2 + 58, 0); c.restore(); };
    pill('몇 개 해당돼요? 댓글로', 1040, q1, TEAL, WHITE, (c, x, y) => { c.strokeStyle = WHITE; c.lineWidth = 7; c.lineCap = 'round'; c.lineJoin = 'round';
      const b = Math.sin(t * 6) * 5; c.beginPath(); c.moveTo(x, y - 20 + b); c.lineTo(x, y + 18 + b); c.moveTo(x - 14, y + 4 + b); c.lineTo(x, y + 18 + b); c.lineTo(x + 14, y + 4 + b); c.stroke(); });
    pill('저장해 두고 다음 러닝 때', 1160, q2, WHITE, DARK, (c, x, y) => { c.fillStyle = TEAL; c.beginPath(); c.moveTo(x - 14, y - 22); c.lineTo(x + 14, y - 22); c.lineTo(x + 14, y + 22); c.lineTo(x, y + 10); c.lineTo(x - 14, y + 22); c.closePath(); c.fill(); });
  }
}
const BUF = document.createElement('canvas'); BUF.width = W; BUF.height = H; const b = BUF.getContext('2d');
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  const k = at(t), p = PH[k], q = k ? seg(t, p.t0, p.t0 + .3) : 1;
  if (q < 1 && !(p.kind === 'x' && p.i === 0)) {
    draw(ctx, k - 1, t); draw(b, k, t);
    if (p.kind === 'o') {          // ❌ → ⭕: the next card pushes the last one off to the left
      const e = eio(q); ctx.drawImage(BUF, W * (1 - e), 0);
      
    } else {                       // a new item: a quick white flash and a zoom-in cut
      const z = 1.08 - .08 * eo(q); ctx.globalAlpha = ss(q * 1.6); ctx.drawImage(BUF, W / 2 - W * z / 2, H / 2 - H * z / 2, W * z, H * z); ctx.globalAlpha = 1;
      const f = Math.max(0, 1 - Math.abs(q - .35) / .35); ctx.fillStyle = `rgba(255,255,255,${.5 * f})`; ctx.fillRect(0, 0, W, H);
    }
  } else draw(ctx, k, t);
  if (p.kind !== 'end' && !NOSUB) subtitle(ctx, t);   // ?nosub=1: captions are laid on later by the caption-motion pass (captions/)
  const f = 1 - ss(seg(t, 0, .2)); if (f > 0) { ctx.fillStyle = `rgba(18,32,31,${f})`; ctx.fillRect(0, 0, W, H); }
}
window.render = render;
(async () => {
  LN = await (await fetch('audio/lines_paced.json')).json();
  DUR = Math.round((LN[LN.length - 1].t1 + 3.0) * 100) / 100; window.DUR = DUR; PH = phases();
  window.EV = PH.slice(1).map(p => ({ t: p.t0, type: p.kind }));
  await Promise.all(Array.from({ length: 10 }, (_, i) => new Promise(r => { const im = new Image(); im.onload = () => { IMG[i + 1] = im; r(); }; im.src = `assets/${String(i + 1).padStart(2, '0')}.png`; })));
  await Promise.all(['700 42px', '900 76px'].map(f => document.fonts.load(`${f} ${FONT}`, '러닝')));
  window.READY = true;
})();
