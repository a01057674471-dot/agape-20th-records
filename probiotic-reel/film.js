// 「유산균, 먹는다고 다 장에 남을까요?」 — 47초 세로 릴스. 의학 다큐 톤: 장 속 3D 이미지는 크게, 글자는 흰색 + 민트 포인트,
// 결론의 실천법 3가지는 흰 카드와 번호로 정리. 화면은 사용자 나레이션(audio/narration.mp3)의 실제 시간에 맞췄다.
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = 1080, H = 1920, DUR = 47.0;
const BG = '#1d1014', MINT = '#9BF2B9', WHITE = '#FFF8F5', INK = '#2A1A1D', MUTE = '#B9A6A9', FONT = '"Noto Sans KR"';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = t => { t = clamp(t); const s = 1.7; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };

// narration phrases (seconds in the recording, from speech recognition + pauses)
const SUBS = [
  [0.16, 2.77, '유산균, 먹는다고 다 장에 남을까요?'],
  [3.30, 7.15, '이스라엘 와이즈만 연구소가 내시경으로 장 속을 직접 들여다봤어요.'],
  [7.61, 9.86, '그랬더니 유산균이 장에 머무는 사람과,'],
  [10.06, 11.48, '밀어내는 사람으로 나뉘었죠.'],
  [11.85, 15.44, '그 차이를 만든 건, 원래 내 장에 살던 미생물이었어요.'],
  [15.97, 18.28, '항생제를 다 먹은 뒤 유산균을 먹었더니,'],
  [18.62, 21.79, '원래 장내 미생물이 돌아오는 게 오히려 늦어지기도 했고요.'],
  [22.26, 23.92, '그럼 어떻게 먹어야 할까요?'],
  [24.31, 26.99, '첫째, 유산균은 장에 저축되지 않아요.'],
  [27.42, 30.43, '끊으면 대부분 빠져나가니, 꾸준히 먹는 게 중요해요.'],
  [30.87, 33.78, '둘째, 장에 남지 않는다고 효과가 없는 건 아니에요.'],
  [34.14, 36.89, '정착보다 내 몸의 변화를 기준으로 판단하세요.'],
  [37.41, 41.19, '셋째, 항생제를 먹는다면 유산균을 언제 시작할지'],
  [41.40, 43.60, '의사나 약사와 꼭 상의하세요.'],
];
const SC = [
  { t0: 0, kind: 'img', img: 1, head: ['유산균, 먹는다고', '다 *장에 남을까요?*'], z: [1.12, 1.0], at: [540, 960] },
  { t0: 3.0, kind: 'img', img: 6, head: ['이스라엘 와이즈만 연구소', '*내시경*으로 장 속을 직접'], z: [1.0, 1.1], at: [540, 900] },
  { t0: 7.4, kind: 'split', head: ['장에 *머무는* 사람,', '*밀어내는* 사람'] },
  { t0: 11.65, kind: 'img', img: 7, head: ['차이를 만든 건', '*원래 내 장의 미생물*'], z: [1.15, 1.25], at: [540, 960] },
  { t0: 15.75, kind: 'img', img: 5, head: ['항생제 뒤 유산균,', '회복이 *오히려 늦어지기도*'], z: [1.0, 1.12], at: [540, 980] },
  { t0: 22.05, kind: 'img', img: 4, head: ['그럼', '*어떻게* 먹어야 할까?'], z: [1.06, 1.0], at: [540, 960] },
  { t0: 24.15, kind: 'tip', n: 1, title: ['장에 *저축*되지 않아요'], body: '끊으면 대부분 빠져나가요', key: '꾸준히', icon: 'cal' },
  { t0: 30.65, kind: 'tip', n: 2, title: ['정착보다', '*내 몸의 변화*로 판단'], body: '장에 남지 않아도 효과가 없는 건 아니에요', key: '내 몸 기준', icon: 'body' },
  { t0: 37.2, kind: 'tip', n: 3, title: ['항생제를 먹는다면'], body: '유산균 시작 시점을', key: '의사·약사와 상의', icon: 'rx' },
  { t0: 43.85, kind: 'sum' },
];
const IMG = {};
const sceneAt = t => { let i = 0; while (i + 1 < SC.length && t >= SC[i + 1].t0) i++; return i; };
const end = i => i + 1 < SC.length ? SC[i + 1].t0 : DUR;

function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function cover(c, im, cx, cy, z, a = 1) {      // fill the frame's height, centred on (cx, cy)
  const h = H * z, w = h * im.width / im.height; c.globalAlpha = a; c.drawImage(im, cx - w / 2, cy - h / 2, w, h); c.globalAlpha = 1;
}
function shade(c, top = .55, bottom = .65) {    // darken top and bottom for the text
  let g = c.createLinearGradient(0, 0, 0, 620); g.addColorStop(0, `rgba(29,16,20,${top})`); g.addColorStop(1, 'rgba(29,16,20,0)'); c.fillStyle = g; c.fillRect(0, 0, W, 620);
  g = c.createLinearGradient(0, H, 0, H - 700); g.addColorStop(0, `rgba(29,16,20,${bottom})`); g.addColorStop(1, 'rgba(29,16,20,0)'); c.fillStyle = g; c.fillRect(0, H - 700, W, 700);
}
function rich(c, ln, x, y, col = WHITE, acc = MINT, align = 'center') {   // text with *accent* words
  const parts = ln.split('*'), ws = parts.map(s => c.measureText(s).width), tot = ws.reduce((a, b) => a + b, 0);
  let xx = align === 'center' ? x - tot / 2 : x; c.textAlign = 'left';
  parts.forEach((s, k) => { c.fillStyle = k % 2 ? acc : col; c.fillText(s, xx, y); xx += ws[k]; });
}
function headline(c, lines, t, t0, y = 290) {
  c.font = `900 76px ${FONT}`; c.textBaseline = 'middle';
  lines.forEach((ln, i) => {
    const p = eo(seg(t, t0 + .08 + i * .16, t0 + .5 + i * .16)); if (p <= 0) return;
    c.save(); c.globalAlpha = p; c.shadowColor = 'rgba(20,8,12,.8)'; c.shadowBlur = 26; rich(c, ln, W / 2, y + i * 100 + (1 - p) * 28); c.restore();
  });
}
function subtitle(c, t) {
  for (const [k, [a, b, txt]] of SUBS.entries()) {
    const nx = k + 1 < SUBS.length ? SUBS[k + 1][0] - .14 : 1e9, e = Math.min(b + .4, nx);
    const al = ss(seg(t, a - .12, a + .08)) * (1 - ss(seg(t, e - .12, e))); if (al <= 0) continue;
    c.save(); c.globalAlpha = al; c.font = `700 44px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
    const lines = wrap(c, txt, 900), y0 = 1500 - (lines.length - 1) * 30;
    const tw = Math.max(...lines.map(l => c.measureText(l).width));
    c.fillStyle = 'rgba(29,16,20,.66)'; rr(c, W / 2 - tw / 2 - 30, y0 - 42, tw + 60, 84 + (lines.length - 1) * 60, 18); c.fill();
    c.fillStyle = WHITE; lines.forEach((l, j) => c.fillText(l, W / 2, y0 + 2 + j * 60)); c.restore();
  }
}
function wrap(c, txt, maxW) {
  if (c.measureText(txt).width <= maxW) return [txt];
  const ci = txt.indexOf(', ');
  if (ci > 0) { const a = txt.slice(0, ci + 1), b = txt.slice(ci + 2); if (c.measureText(a).width <= maxW && c.measureText(b).width <= maxW) return [a, b]; }
  const w = txt.split(' '); let best = null;
  for (let i = 1; i < w.length; i++) { const a = w.slice(0, i).join(' '), b = w.slice(i).join(' '), m = Math.max(c.measureText(a).width, c.measureText(b).width); if (!best || m < best[0]) best = [m, a, b]; }
  return [best[1], best[2]];
}
function chip(c, txt, x, y, on) {
  c.font = `700 36px ${FONT}`; c.textBaseline = 'middle'; c.textAlign = 'left'; const w = c.measureText(txt).width + 44;
  c.fillStyle = on ? MINT : 'rgba(255,248,245,.18)'; rr(c, x, y - 30, w, 60, 30); c.fill(); c.fillStyle = on ? INK : WHITE; c.fillText(txt, x + 22, y + 1);
}

// ---------- icons for the tips (drawn, so they move) ----------
function icon(c, kind, x, y, s, p) {
  c.save(); c.translate(x, y); c.scale(s, s); c.lineWidth = 7; c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = INK;
  if (kind === 'cal') {           // a calendar filling with checks, day by day
    rr(c, -80, -70, 160, 150, 18); c.stroke(); c.beginPath(); c.moveTo(-80, -30); c.lineTo(80, -30); c.stroke();
    for (const xx of [-40, 40]) { c.beginPath(); c.moveTo(xx, -88); c.lineTo(xx, -52); c.stroke(); }
    for (let k = 0; k < 6; k++) {
      const q = seg(p, .1 + k * .1, .2 + k * .1); if (q <= 0) continue;
      const cx = -50 + (k % 3) * 50, cy = 5 + Math.floor(k / 3) * 44;
      c.fillStyle = MINT; c.beginPath(); c.arc(cx, cy, 17 * back(q), 0, 7); c.fill();
      c.lineWidth = 5; c.beginPath(); c.moveTo(cx - 8, cy); c.lineTo(cx - 2, cy + 7); c.lineTo(cx + 9, cy - 7); c.stroke(); c.lineWidth = 7;
    }
  } else if (kind === 'body') {   // a person with a rising line beside
    c.beginPath(); c.arc(-30, -50, 26, 0, 7); c.stroke();
    c.beginPath(); c.moveTo(-82, 80); c.quadraticCurveTo(-82, -10, -30, -10); c.quadraticCurveTo(22, -10, 22, 80); c.stroke();
    const q = eo(seg(p, .15, .7)); c.strokeStyle = '#3BBF72'; c.beginPath();
    const P = [[40, 60], [62, 30], [82, 42], [108, 0]]; const m = 1 + (P.length - 1) * q, k = Math.floor(m);
    c.moveTo(P[0][0], P[0][1]); for (let i = 1; i < Math.min(k, P.length); i++) c.lineTo(P[i][0], P[i][1]);
    if (k < P.length) { const f = m - k, a = P[k - 1], b = P[k]; c.lineTo(lerp(a[0], b[0], f), lerp(a[1], b[1], f)); }
    c.stroke();
    if (q >= 1) { c.fillStyle = '#3BBF72'; c.beginPath(); c.arc(108, 0, 9, 0, 7); c.fill(); }
  } else if (kind === 'rx') {     // a capsule and a speech bubble with a question mark
    c.save(); c.rotate(-.6); rr(c, -98, -24, 100, 48, 24); c.stroke(); c.fillStyle = MINT; rr(c, -48, -24, 50, 48, 24); c.fill(); rr(c, -98, -24, 100, 48, 24); c.stroke(); c.restore();
    const q = back(seg(p, .2, .55)); c.save(); c.translate(48, -30); c.scale(q, q);
    rr(c, -40, -48, 96, 76, 22); c.stroke(); c.beginPath(); c.moveTo(-14, 28); c.lineTo(-28, 52); c.lineTo(8, 28); c.stroke();
    c.font = `900 52px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = INK; c.fillText('?', 8, -8); c.restore();
  }
  c.restore();
}

// ---------- scenes ----------
function sceneImg(c, s, t) {
  const p = seg(t, s.t0, end(SC.indexOf(s)) + .4), z = lerp(s.z[0], s.z[1], ss(p));
  cover(c, IMG[s.img], s.at[0], s.at[1], z);
  shade(c);
}
function sceneSplit(c, s, t) {
  c.fillStyle = BG; c.fillRect(0, 0, W, H);
  const Y1 = 430, Y2 = 950, BH = 490, a1 = eo(seg(t, 7.55, 8.15)), a2 = eo(seg(t, 9.95, 10.55));
  const panel = (im, y, a, on, label, dz) => {
    if (a <= 0) return;
    c.save(); c.globalAlpha = a; rr(c, 50, y + (1 - a) * 40, W - 100, BH, 26); c.clip();
    const h = (W - 100) * im.height / im.width; c.drawImage(im, 50 - 40 * dz, y + (1 - a) * 40 + BH / 2 - h / 2 - 40 * dz, W - 100 + 80 * dz, h + 80 * dz); c.restore();
    c.save(); c.globalAlpha = a; c.lineWidth = 3; c.strokeStyle = on ? 'rgba(155,242,185,.85)' : 'rgba(255,248,245,.3)'; rr(c, 50, y + (1 - a) * 40, W - 100, BH, 26); c.stroke();
    chip(c, label, 80, y + (1 - a) * 40 + 52, on); c.restore();
  };
  const dz = seg(t, s.t0, end(SC.indexOf(s)));
  panel(IMG[2], Y1, a1, true, '유산균이 머무는 사람', dz);
  panel(IMG[3], Y2, a2, false, '유산균을 밀어내는 사람', dz);
}
function sceneTip(c, s, t) {
  const i = SC.indexOf(s), lt = t - s.t0, dur = end(i) - s.t0;
  cover(c, IMG[1], 540, 960, 1.04 + .04 * lt / dur);
  c.fillStyle = 'rgba(29,16,20,.62)'; c.fillRect(0, 0, W, H);
  // the three steps as a rail across the top
  for (let k = 1; k <= 3; k++) {
    const x = 540 + (k - 2) * 150, on = k <= s.n, cur = k === s.n;
    c.fillStyle = on ? MINT : 'rgba(255,248,245,.22)'; c.beginPath(); c.arc(x, 210, cur ? 34 : 26, 0, 7); c.fill();
    c.font = `900 ${cur ? 38 : 30}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = on ? INK : WHITE; c.fillText(k, x, 212);
    if (k < 3) { c.fillStyle = k < s.n ? MINT : 'rgba(255,248,245,.22)'; c.fillRect(x + 40, 208, 70, 4); }
  }
  // the card
  const p = back(seg(lt, .05, .55)), y = 340 + (1 - p) * 120, ch = 1040;
  c.save(); c.globalAlpha = clamp(p * 1.4); c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 50; c.fillStyle = WHITE; rr(c, 70, y, W - 140, ch, 44); c.fill(); c.restore();
  c.save(); c.globalAlpha = clamp(p * 1.4);
  c.fillStyle = MINT; c.beginPath(); c.arc(190, y + 130, 62, 0, 7); c.fill();
  c.font = `900 72px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = INK; c.fillText(s.n, 190, y + 134);
  icon(c, s.icon, W / 2, y + 400, 1.55, seg(lt, .5, 3));
  c.font = `900 64px ${FONT}`; c.textBaseline = 'middle';
  s.title.forEach((ln, k) => { const q = eo(seg(lt, .35 + k * .14, .8 + k * .14)); c.globalAlpha = q; rich(c, ln, W / 2, y + 640 + k * 84, INK, '#1F9D57'); });
  const bq = eo(seg(lt, 1.2, 1.7)); c.globalAlpha = bq; c.font = `500 38px ${FONT}`; c.textAlign = 'center'; c.fillStyle = '#6E5D60';
  const by = y + 640 + s.title.length * 84 + 10; c.fillText(s.body, W / 2, by);
  const kq = back(seg(lt, 2.0, 2.5)); c.globalAlpha = clamp(kq);
  c.font = `900 52px ${FONT}`; const kw = c.measureText('→ ' + s.key).width + 80, ky = by + 130;
  c.save(); c.translate(W / 2, ky); c.scale(kq, kq); c.fillStyle = INK; rr(c, -kw / 2, -46, kw, 92, 46); c.fill(); c.fillStyle = MINT; c.textAlign = 'center'; c.fillText('→ ' + s.key, 0, 4); c.restore();
  c.restore(); c.globalAlpha = 1;
}
function sceneSum(c, s, t) {
  const lt = t - s.t0;
  cover(c, IMG[1], 540, 960, 1.08); c.fillStyle = 'rgba(29,16,20,.78)'; c.fillRect(0, 0, W, H);
  c.font = `900 64px ${FONT}`; c.textBaseline = 'middle'; c.globalAlpha = eo(seg(lt, 0, .5)); rich(c, '유산균, *이렇게* 드세요', W / 2, 330); c.globalAlpha = 1;
  [['꾸준히', '장에 저축되지 않아요'], ['내 몸 기준', '정착보다 몸의 변화로 판단'], ['의사·약사와 상의', '항생제와 함께라면 시작 시점']].forEach(([k, b], i) => {
    const q = eo(seg(lt, .2 + i * .22, .7 + i * .22)), y = 470 + i * 230 + (1 - q) * 40;
    c.globalAlpha = q; c.fillStyle = 'rgba(255,248,245,.1)'; rr(c, 90, y, W - 180, 190, 30); c.fill();
    c.fillStyle = MINT; c.beginPath(); c.arc(180, y + 95, 46, 0, 7); c.fill();
    c.font = `900 52px ${FONT}`; c.textAlign = 'center'; c.fillStyle = INK; c.fillText(i + 1, 180, y + 98);
    c.textAlign = 'left'; c.fillStyle = WHITE; c.font = `900 54px ${FONT}`; c.fillText(k, 260, y + 70);
    c.fillStyle = MUTE; c.font = `500 36px ${FONT}`; c.fillText(b, 260, y + 132); c.globalAlpha = 1;
  });
  c.globalAlpha = eo(seg(lt, .9, 1.4)); c.font = `500 27px ${FONT}`; c.textAlign = 'center'; c.fillStyle = MUTE;
  c.fillText('출처: 와이즈만 연구소, Cell (2018) · ISAPP(국제프로바이오틱스·프리바이오틱스학회)', W / 2, 1300);
  c.fillText('※ 개인의 건강 상태에 따라 다를 수 있으며, 의료 상담을 대신하지 않습니다.', W / 2, 1346);
  c.globalAlpha = 1;
}
function frame(c, i, t) {
  const s = SC[i]; c.fillStyle = BG; c.fillRect(0, 0, W, H);
  if (s.kind === 'img') sceneImg(c, s, t);
  else if (s.kind === 'split') sceneSplit(c, s, t);
  else if (s.kind === 'tip') sceneTip(c, s, t);
  else sceneSum(c, s, t);
  if (s.head) headline(c, s.head, t, s.t0, s.kind === 'split' ? 250 : 290);
}

const BUF = document.createElement('canvas'); BUF.width = W; BUF.height = H; const bctx = BUF.getContext('2d');
const XF = .34;
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  const i = sceneAt(t), s = SC[i], p = i ? seg(t, s.t0, s.t0 + XF) : 1;
  if (p < 1) {
    frame(ctx, i - 1, t); frame(bctx, i, t);
    // a soft push-through: the next scene grows in from slightly smaller while it fades up
    const z = .94 + .06 * eo(p); ctx.globalAlpha = ss(p);
    ctx.drawImage(BUF, W / 2 - W * z / 2, H / 2 - H * z / 2, W * z, H * z); ctx.globalAlpha = 1;
  } else frame(ctx, i, t);
  if (s.kind !== 'sum') subtitle(ctx, t);
  const f = 1 - ss(seg(t, 0, .25)); if (f > 0) { ctx.fillStyle = `rgba(29,16,20,${f})`; ctx.fillRect(0, 0, W, H); }
  const e = ss(seg(t, DUR - .5, DUR)); if (e > 0) { ctx.fillStyle = `rgba(29,16,20,${e})`; ctx.fillRect(0, 0, W, H); }
}
window.DUR = DUR; window.render = render;
window.EV = SC.slice(1).map(s => ({ t: s.t0, type: s.kind === 'tip' ? 'card' : 'whoosh' }));
(async () => {
  const load = k => new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.src = `assets/0${k}.png`; });
  await Promise.all([1, 2, 3, 4, 5, 6, 7].map(load));
  await Promise.all(['500 36px', '700 44px', '900 76px'].map(f => document.fonts.load(`${f} ${FONT}`, '유산균')));
  window.READY = true;
})();
