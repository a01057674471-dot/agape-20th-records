// AHCC — whiteboard explainer, 1080×1920. Narration lines (lines.json) drive the timeline; measured voice
// durations (voices/dur.json) replace the estimates when they exist.
import * as W from './engine/wb.js';
import { loadHangul } from './engine/hangul.js';

const SW = innerWidth, SH = innerHeight;
W.setScreen(SW, SH);
const LINES = await (await fetch('lines.json')).json();
let DURS = {}; try { const r = await fetch('voices/dur.json'); if (r.ok) DURS = await r.json(); } catch (e) { }
await W.loadFont('tech', 'fonts/EMSTech.json');
await document.fonts.load('700 52px Gaegu');

// ---------- timing: one narration line after another ----------
const GAP = .35, LEAD = .7;
let t = LEAD;
for (const L of LINES) {
  if (L.id === 'v06') t += .8;                    // a beat of silence before the turn: "not a medicine"
  L.d = DURS[L.id] ?? L.est; L.t0 = +t.toFixed(3); L.t1 = +(t + L.d).toFixed(3); t = L.t1 + GAP;
}
const V = Object.fromEntries(LINES.map(L => [L.id, L]));
const at = (id, u) => V[id].t0 + V[id].d * u;     // a moment inside line id (u = 0..1)
const DUR = +(V.v09.t1 + 3.6).toFixed(2);

// ---------- pens and helpers ----------
const K = new W.Pen('k', W.INK.black, { park: [SW + 140, SH * .55] }), B = new W.Pen('b', W.INK.blue, { park: [SW + 160, SH * .7] }), O = new W.Pen('o', W.INK.orange, { park: [SW + 150, SH * .4] });
const tl = new W.Timeline();
const ko = (s, x, y, h, o = {}) => W.text(s, x, y, { h, w: o.w ?? Math.max(4.5, h * .085), align: o.align ?? 'center', color: o.color, jitter: .3 });
const C = 750;                                    // board centre line

// collect every Hangul character used on the board, then skeletonise them before building strokes
const BOARD_TEXT = ['그냥 표고버섯 분말?', '갓', '줄기', '균사체', '영양분 흡수', '일본 아미노업', '배양', '여과', '동결건조', '원료',
  '식약처 개별인정형', '기능성 원료', '표고버섯균사체 AHCC', '제2008-78호', '인정 기능성', '면역기능 증진에', '도움을 줄 수 있음',
  '의약품 · 치료제', '건강기능식품 원료', '표고버섯 분말', '확인할 3가지', '원료명', '식약처 인정번호', '섭취방법 · 표시사항', '후기', '공식 정보',
  '제대로 알고 선택', '정보 제공용 영상', '출처: 식약처 개별인정 원료 정보 · FACTS.md'];
await loadHangul(BOARD_TEXT.join(''));

// ---------- 1. title: "just shiitake powder?" ----------
tl.draw(K, W.text('AHCC', C, 760, { h: 210, w: 15, align: 'center' }), at('v01', .0), { by: at('v01', .3) });
tl.draw(B, ko('그냥 표고버섯 분말?', C, 470, 70, { color: W.INK.blue }), at('v01', .32), { by: at('v01', .9) });
tl.draw(K, W.line(C - 300, 830, C + 300, 822, { w: 9, over: 10 }), at('v01', .9), { by: at('v01', 1.0) });

// ---------- 2. the mushroom: cap, stem and mycelium ----------
const capY = 1640, mx = 620;
const mush = [
  W.curve([[mx - 250, capY + 40], [mx - 220, capY - 120], [mx - 60, capY - 210], [mx + 120, capY - 190], [mx + 240, capY - 80], [mx + 260, capY + 40]], { w: 10 }),
  W.curve([[mx - 250, capY + 40], [mx - 80, capY + 70], [mx + 100, capY + 70], [mx + 260, capY + 40]], { w: 9 }),
  ...[-170, -100, -30, 40, 110, 180].map(dx => W.line(mx + dx * .9, capY + 52, mx + dx * .45, capY + 18, { w: 5 })),
  ...[[-150, -120, 34], [30, -150, 26], [150, -90, 30]].map(([dx, dy, r]) => W.circle(mx + dx, capY + dy, r, { w: 5, lap: .1 })),
];
const stem = [W.curve([[mx - 40, capY + 70], [mx - 52, capY + 200], [mx - 60, capY + 300]], { w: 9 }), W.curve([[mx + 40, capY + 70], [mx + 46, capY + 200], [mx + 58, capY + 300]], { w: 9 })];
const ground = W.line(160, capY + 300, 1340, capY + 296, { w: 7, over: 8 });
const myc = [];
const thread = (x0, y0, a, L, depth, seed) => {
  const pts = [[x0, y0]]; let x = x0, y = y0, ang = a;
  for (let i = 0; i < 6; i++) { ang += Math.sin(seed * 3.7 + i * 1.9) * .35; x += Math.cos(ang) * L / 6; y += Math.sin(ang) * L / 6; pts.push([x, y]); }
  myc.push(W.curve(pts, { w: 4.5, alpha: .9 }));
  if (depth > 0) { thread(pts[3][0], pts[3][1], a - .6, L * .55, depth - 1, seed + 1); thread(pts[5][0], pts[5][1], a + .5, L * .5, depth - 1, seed + 2); }
};
thread(mx - 50, capY + 300, 1.9, 300, 2, 1); thread(mx + 50, capY + 300, 1.25, 320, 2, 5); thread(mx, capY + 300, 1.57, 360, 1, 9);
tl.draw(K, [...mush, ...ko('갓', mx + 380, capY - 120, 64), ...W.arrow(mx + 340, capY - 130, mx + 230, capY - 100, { w: 6, head: 20 })], at('v02', .0), { by: at('v02', .3) });
tl.draw(K, [...stem, ground, ...ko('줄기', mx + 330, capY + 200, 64), ...W.arrow(mx + 270, capY + 190, mx + 80, capY + 190, { w: 6, head: 20 })], at('v02', .3), { by: at('v02', .55) });
tl.draw(B, myc, at('v02', .55), { by: at('v02', .78) });
tl.draw(O, [...ko('균사체', mx + 420, capY + 520, 76, { color: W.INK.orange }), ...W.arrow(mx + 300, capY + 500, mx + 140, capY + 470, { w: 7, head: 22 }), ...ko('영양분 흡수', mx + 420, capY + 610, 48, { color: W.INK.orange })], at('v02', .74), { by: at('v02', 1.0) });

// ---------- 3. made by culturing the mycelium ----------
const pY = 2780;
const flask = [W.poly([[330, pY - 150], [330, pY - 60], [240, pY + 90], [240, pY + 110], [480, pY + 110], [480, pY + 90], [390, pY - 60], [390, pY - 150]], { w: 8, jitter: .8 }), W.curve([[262, pY + 50], [300, pY + 40], [360, pY + 58], [420, pY + 44], [460, pY + 56]], { w: 5 })];
const flaskThreads = [W.curve([[300, pY + 90], [320, pY + 70], [345, pY + 82], [365, pY + 66]], { w: 3.5 }), W.curve([[380, pY + 95], [400, pY + 76], [420, pY + 88]], { w: 3.5 })];
const funnel = [W.poly([[640, pY - 120], [860, pY - 120], [775, pY + 10], [775, pY + 100], [725, pY + 100], [725, pY + 10], [640, pY - 120]], { w: 8, jitter: .8 }), W.line(670, pY - 80, 830, pY - 80, { w: 4 })];
const flake = []; for (let k = 0; k < 3; k++) { const a = k * Math.PI / 3, cx = 1130, cy = pY - 10, r = 105; flake.push(W.line(cx - Math.cos(a) * r, cy - Math.sin(a) * r, cx + Math.cos(a) * r, cy + Math.sin(a) * r, { w: 7 })); for (const s of [-1, 1]) { const ex = cx + Math.cos(a) * r * .62 * s, ey = cy + Math.sin(a) * r * .62 * s; flake.push(W.line(ex, ey, ex + Math.cos(a + 2.4 * s) * 34, ey + Math.sin(a + 2.4 * s) * 34, { w: 5 }), W.line(ex, ey, ex + Math.cos(a - 2.4 * s) * 34, ey + Math.sin(a - 2.4 * s) * 34, { w: 5 })); } }
const pile = [W.curve([[560, pY + 480], [640, pY + 400], [750, pY + 370], [860, pY + 400], [940, pY + 480]], { w: 8 }), W.line(540, pY + 482, 960, pY + 482, { w: 7 }), ...[[650, 440], [720, 410], [790, 430], [860, 455], [700, 455], [770, 462]].map(([x, y]) => W.line(x, pY + y, x + 4, pY + y + 4, { w: 7 }))];
tl.draw(K, [...ko('일본 아미노업', C, pY - 330, 66), ...W.text('(Amino Up)', C, pY - 250, { h: 44, w: 5, align: 'center' })], at('v03', .1), { by: at('v03', .38) });
const MAG = { x: 1180, y: pY - 380, t: at('v03', .12) };     // a pin on "Japan"
tl.draw(K, [...flask, ...flaskThreads], at('v03', .38), { by: at('v03', .52) });
tl.draw(B, [...ko('배양', 360, pY + 200, 56, { color: W.INK.blue }), ...W.arrow(500, pY - 20, 615, pY - 20, { w: 7, head: 22 })], at('v03', .52), { by: at('v03', .62) });
tl.draw(K, funnel, at('v03', .62), { by: at('v03', .72) });
tl.draw(B, [...ko('여과', 750, pY + 200, 56, { color: W.INK.blue }), ...W.arrow(880, pY - 20, 995, pY - 20, { w: 7, head: 22 })], at('v03', .72), { by: at('v03', .79) });
tl.draw(K, flake, at('v03', .79), { by: at('v03', .87) });
tl.draw(B, [...ko('동결건조', 1130, pY + 200, 56, { color: W.INK.blue }), ...W.arrow(1130, pY + 250, 900, pY + 400, { w: 7, head: 22, curve: [1080, pY + 360] })], at('v03', .86), { by: at('v03', .94) });
tl.draw(K, [...pile, ...ko('원료', 750, pY + 600, 64)], at('v03', .93), { by: at('v03', 1.0) + .3 });

// ---------- 4–5. the official card: approved ingredient and its approved claim ----------
const cY = 3800, cw = 940, ch = 760, cx0 = C - cw / 2;
tl.draw(K, [W.roundRect(cx0, cY, cw, ch, 36, { w: 8 }), W.line(cx0 + 40, cY + 150, cx0 + cw - 40, cY + 148, { w: 5 })], at('v04', .0), { by: at('v04', .1) });
tl.draw(K, [...ko('식약처 개별인정형', C, cY + 80, 60), ...ko('기능성 원료', C, cY + 128, 40)], at('v04', .1), { by: at('v04', .42) });
tl.draw(K, ko('표고버섯균사체 AHCC', C, cY + 280, 70), at('v04', .45), { by: at('v04', .75) });
tl.draw(B, ko('제2008-78호', C, cY + 400, 70, { color: W.INK.blue }), at('v04', .76), { by: at('v04', .98) });
tl.draw(K, ko('인정 기능성', C, cY + 520, 46), at('v05', .0), { by: at('v05', .2) });
tl.draw(O, [...ko('면역기능 증진에', C, cY + 610, 66, { color: W.INK.orange }), ...ko('도움을 줄 수 있음', C, cY + 700, 66, { color: W.INK.orange })], at('v05', .2), { by: at('v05', .82) });
tl.draw(O, [W.line(C - 260, cY + 725, C + 260, cY + 721, { w: 6 }), W.line(C - 250, cY + 742, C + 252, cY + 740, { w: 5 })], at('v05', .84), { by: at('v05', 1.0) });

// ---------- 6. not a medicine ----------
const zY = 4900;
tl.draw(K, ko('의약품 · 치료제', 640, zY, 86), at('v06', .0), { by: at('v06', .3) });
tl.draw(O, [W.line(1110, zY - 80, 1200, zY + 10, { w: 13 }), W.line(1200, zY - 80, 1110, zY + 10, { w: 13 })], at('v06', .3), { by: at('v06', .4) });
tl.draw(K, ko('건강기능식품 원료', 640, zY + 170, 86), at('v06', .45), { by: at('v06', .82) });
tl.draw(O, W.text('✓', 1160, zY + 180, { h: 110, w: 13, align: 'center' }), at('v06', .84), { by: at('v06', .95) });

// ---------- 7. same name, not the same ingredient ----------
const nY = 5700;
tl.draw(K, [...ko('표고버섯 분말', C, nY, 74), W.curve([[C - 140, nY + 60], [C - 70, nY + 30], [C, nY + 20], [C + 70, nY + 30], [C + 140, nY + 60]], { w: 7 })], at('v07', .0), { by: at('v07', .35) });
tl.draw(O, [W.line(C - 70, nY + 150, C + 70, nY + 150, { w: 11 }), W.line(C - 70, nY + 200, C + 70, nY + 200, { w: 11 }), W.line(C + 40, nY + 110, C - 40, nY + 240, { w: 11 })], at('v07', .38), { by: at('v07', .55) });
tl.draw(K, ko('표고버섯균사체 AHCC', C, nY + 360, 74), at('v07', .55), { by: at('v07', 1.0) });

// ---------- 8. three things to check ----------
const kY = 6500;
tl.draw(K, [...ko('확인할 3가지', C, kY, 84), W.line(C - 280, kY + 40, C + 280, kY + 36, { w: 7 })], at('v08', .0), { by: at('v08', .22) });
const items = ['원료명', '식약처 인정번호', '섭취방법 · 표시사항'];
items.forEach((s, i) => {
  const y = kY + 200 + i * 170, u0 = .3 + i * .23;
  tl.draw(K, [...W.rect(260, y - 70, 80, 80, { w: 6, over: 4 }), ...ko(s, 390, y, 66, { align: 'left' })], at('v08', u0), { by: at('v08', u0 + .15) });
  tl.draw(B, W.text('✓', 302, y - 10, { h: 90, w: 11, align: 'center' }), at('v08', u0 + .15), { by: at('v08', u0 + .21) });
});

// ---------- 9. official information first ----------
const fY = 7350;
tl.draw(K, ko('후기', 450, fY, 84), at('v09', .0), { by: at('v09', .12) });
tl.draw(O, [W.line(760, fY - 70, 640, fY - 30, { w: 11 }), W.line(640, fY - 30, 760, fY + 10, { w: 11 })], at('v09', .12), { by: at('v09', .2) });   // 후기 < 공식 정보
tl.draw(K, ko('공식 정보', 1010, fY, 84), at('v09', .2), { by: at('v09', .4) });
tl.draw(K, [...W.text('AHCC', C, fY + 240, { h: 120, w: 11, align: 'center' }), ...ko('제대로 알고 선택', C, fY + 380, 82)], at('v09', .42), { by: at('v09', .82) });
tl.draw(O, [W.circle(C, fY + 310, 430, { w: 9, ry: 170, lap: .3 }), W.circle(C, fY + 312, 445, { w: 7, ry: 182, lap: .2, a0: -1.4 })], at('v09', .82), { by: at('v09', 1.0) });
tl.draw(K, [...ko('정보 제공용 영상', C, fY + 640, 40), ...ko('출처: 식약처 개별인정 원료 정보 · FACTS.md', C, fY + 700, 32)], V.v09.t1 + .2, { by: V.v09.t1 + 1.3 });
tl.cue(V.v09.t1 + 1.7, 'cap');
tl.end();

// ---------- camera ----------
const L = id => V[id];
const cam = new W.Camera([
  [0, C, 880, 1.12], [L('v01').t1 - .2, C, 975, 1.0],
  [L('v02').t0 + .9, C, 1820, 1.0], [L('v02').t1, C, 1860, 1.0],
  [L('v03').t0 + .6, C, 2780, 1.0, 0, 'io'], [L('v03').t1, C, 2820, 1.0],
  [L('v04').t0 + .6, C, 4140, 1.0], [L('v04').t1, C, 4160, 1.0],
  [L('v05').t1, C, 4200, 1.06],
  [L('v06').t0 + .3, C, 4980, 1.0, -.015, 'o'], [L('v06').t1, C, 5000, 1.0],
  [L('v07').t0 + .45, C, 5860, 1.0], [L('v07').t1, C, 5880, 1.0],
  [L('v08').t0 + .5, C, 6760, 1.0], [L('v08').t1, C, 6790, 1.0],
  [L('v09').t0 + .45, C, 7690, 1.0], [L('v09').t1 + 1.4, C, 7760, 1.0],
  [DUR, C, 6450, .48],
]);

// ---------- board, props, subtitles ----------
const board = new W.Board(tl, { W: 1500, H: 8600 });
board.objs.push({ draw: (ctx, tt, c) => { if (tt < MAG.t - .3) return; const u = Math.min(1, (tt - MAG.t + .3) / .3); W.drawPinMagnet(ctx, MAG.x, MAG.y, c, { size: 120, lift: 1 - u * u }); } });
board.objs.push({ draw: (ctx, tt, c) => { for (const p of [K, B, O]) W.drawMarker(ctx, p, W.penPose(p, tt, cam), c, tt); } });
const SUB_Y = SH - 150;
function wrap(ctx, s, max) { const words = s.split(' '), out = []; let cur = ''; for (const w of words) { const n = cur ? cur + ' ' + w : w; if (ctx.measureText(n).width > max && cur) { out.push(cur); cur = w; } else cur = n; } if (cur) out.push(cur); return out; }
board.overlays.push({ draw: (ctx, tt) => {
  const Lc = LINES.find(l => tt >= l.t0 && tt < Math.max(l.t1 + .25, l.t0 + 1.8)); if (!Lc) return;
  ctx.font = '700 50px Gaegu'; const lines = wrap(ctx, Lc.text, SW - 170), lh = 62;
  const wmax = Math.max(...lines.map(s => ctx.measureText(s).width)), bw = wmax + 70, bh = lines.length * lh + 34, x = (SW - bw) / 2, y = SUB_Y - bh / 2;
  const a = Math.min(1, (tt - Lc.t0) / .12, (Math.max(Lc.t1 + .25, Lc.t0 + 1.8) - tt) / .12);
  ctx.globalAlpha = a; ctx.fillStyle = 'rgba(255,253,248,.92)'; ctx.shadowColor = 'rgba(40,40,50,.18)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 4;
  ctx.beginPath(); ctx.roundRect(x, y, bw, bh, 22); ctx.fill(); ctx.shadowColor = 'transparent';
  ctx.fillStyle = W.INK.orange; ctx.fillRect(x + 26, y + 16, 46, 6);
  ctx.fillStyle = '#23262c'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  lines.forEach((s, i) => ctx.fillText(s, SW / 2, y + 17 + lh * (i + .5) + 4));
} });

const ctx = document.getElementById('c').getContext('2d');
window.DUR = DUR;
window.render = tt => board.render(ctx, tt, cam);
window.EV = [...tl.ev, ...LINES.map(l => ({ t: l.t0, type: 'vo', id: l.id, dur: l.d })), { t: MAG.t, type: 'magnet' }];
window.SUBS = LINES.map(l => ({ t0: l.t0, t1: Math.max(l.t1 + .25, l.t0 + 1.8), text: l.text }));
window.LINES = LINES;
window.READY = true;
