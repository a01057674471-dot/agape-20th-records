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
  if (L.id === 'v08') t += .9;                    // a beat of silence before "하지만"
  L.d = DURS[L.id] ?? L.est; L.t0 = +t.toFixed(3); L.t1 = +(t + L.d).toFixed(3); t = L.t1 + GAP;
}
const V = Object.fromEntries(LINES.map(L => [L.id, L]));
const at = (id, u) => V[id].t0 + V[id].d * u;     // a moment inside line id (u = 0..1)
const DUR = +(V.v10.t1 + 3.6).toFixed(2);

// ---------- pens and helpers ----------
const K = new W.Pen('k', W.INK.black, { park: [SW + 140, SH * .55] }), B = new W.Pen('b', W.INK.blue, { park: [SW + 160, SH * .7] }), O = new W.Pen('o', W.INK.orange, { park: [SW + 150, SH * .4] });
const tl = new W.Timeline();
const ko = (s, x, y, h, o = {}) => W.text(s, x, y, { h, w: o.w ?? Math.max(4.5, h * .085), align: o.align ?? 'center', color: o.color, jitter: .3 });
const C = 750;                                    // board centre line

// collect every Hangul character used on the board, then skeletonise them before building strokes
const BOARD_TEXT = ['버섯 뿌리에서 온 연구 소재', '일본 삿포로', '아미노업', '표고버섯 균사체', '추출물', '배양', '여과', '동결건조', '가루',
  '올리고당', '말린 무게의', '면역세포', 'NK세포', 'T세포', '연구', '2022 미국 임상', 'HPV 2년 이상', '여성 50명', '6개월', '34명 중', '음성 전환',
  '소규모 연구', '아직 재현 안 됨', '설사 · 가려움', '일부 약과 상호작용', '치료제', '연구 중인 소재', '복용 전 의사와 상의', '정보 제공용 영상', '출처: Smith et al. 2022 · MSK 외'];
await loadHangul(BOARD_TEXT.join(''));

// ---------- 1. title ----------
tl.draw(K, W.text('AHCC?', C, 760, { h: 210, w: 15, align: 'center' }), at('v01', .38), { by: at('v01', .78) });
tl.draw(B, ko('버섯 뿌리에서 온 연구 소재', C, 470, 62, { color: W.INK.blue }), at('v01', .02), { by: at('v01', .36) });
tl.draw(K, W.line(C - 330, 830, C + 330, 822, { w: 9, over: 10 }), at('v01', .8), { by: at('v01', .98) });

// ---------- 2. shiitake and its mycelium (the pen leads the camera down) ----------
const capY = 1640, mx = 560;
const mush = [
  W.curve([[mx - 250, capY + 40], [mx - 220, capY - 120], [mx - 60, capY - 210], [mx + 120, capY - 190], [mx + 240, capY - 80], [mx + 260, capY + 40]], { w: 10 }),
  W.curve([[mx - 250, capY + 40], [mx - 80, capY + 70], [mx + 100, capY + 70], [mx + 260, capY + 40]], { w: 9 }),
  ...[-170, -100, -30, 40, 110, 180].map(dx => W.line(mx + dx * .9, capY + 52, mx + dx * .45, capY + 18, { w: 5 })),
  W.curve([[mx - 40, capY + 70], [mx - 52, capY + 200], [mx - 60, capY + 300]], { w: 9 }),
  W.curve([[mx + 40, capY + 70], [mx + 46, capY + 200], [mx + 58, capY + 300]], { w: 9 }),
  ...[[-150, -120, 34], [30, -150, 26], [150, -90, 30]].map(([dx, dy, r]) => W.circle(mx + dx, capY + dy, r, { w: 5, lap: .1 })),
];
const ground = W.line(160, capY + 300, 1340, capY + 296, { w: 7, over: 8 });
const myc = [];                                   // mycelium threads: branching blue lines under the ground
const thread = (x0, y0, a, L, depth, seed) => {
  const pts = [[x0, y0]]; let x = x0, y = y0, ang = a;
  for (let i = 0; i < 6; i++) { ang += Math.sin(seed * 3.7 + i * 1.9) * .35; x += Math.cos(ang) * L / 6; y += Math.sin(ang) * L / 6; pts.push([x, y]); }
  myc.push(W.curve(pts, { w: 4.5, alpha: .9 }));
  if (depth > 0) { thread(pts[3][0], pts[3][1], a - .6, L * .55, depth - 1, seed + 1); thread(pts[5][0], pts[5][1], a + .5, L * .5, depth - 1, seed + 2); }
};
thread(mx - 50, capY + 300, 1.9, 300, 2, 1); thread(mx + 50, capY + 300, 1.25, 320, 2, 5); thread(mx, capY + 300, 1.57, 360, 1, 9);
tl.draw(K, [...ko('일본 삿포로', 1080, capY - 160, 58), ...ko('아미노업', 1080, capY - 60, 58), ...W.text('(Amino Up)', 1080, capY + 20, { h: 42, w: 5, align: 'center' })], at('v02', .03), { by: at('v02', .38) });
tl.draw(K, mush, at('v02', .4), { by: at('v02', .6) });
tl.draw(K, ground, at('v02', .6), { by: at('v02', .65) });
tl.draw(B, myc, at('v02', .55), { by: at('v02', .72) });
tl.draw(B, [...ko('표고버섯 균사체', 1040, capY + 520, 54, { color: W.INK.blue }), ...W.arrow(840, capY + 500, 700, capY + 470, { w: 7, head: 22 })], at('v02', .72), { by: at('v02', .9) });
tl.draw(K, [...ko('추출물', 1080, capY + 170, 64), ...W.rect(965, capY + 100, 230, 100, { w: 6, over: 6 })], at('v02', .82), { by: at('v02', 1.0) });
const MAG = { x: 1300, y: capY - 250, t: at('v02', .02) };   // the Sapporo pin drops onto the board

// ---------- 3. how it is made ----------
const pY = 2780;
const flask = [W.poly([[330, pY - 150], [330, pY - 60], [240, pY + 90], [240, pY + 110], [480, pY + 110], [480, pY + 90], [390, pY - 60], [390, pY - 150]], { w: 8, jitter: .8 }), W.curve([[262, pY + 50], [300, pY + 40], [360, pY + 58], [420, pY + 44], [460, pY + 56]], { w: 5 })];
const flaskThreads = [W.curve([[300, pY + 90], [320, pY + 70], [345, pY + 82], [365, pY + 66]], { w: 3.5 }), W.curve([[380, pY + 95], [400, pY + 76], [420, pY + 88]], { w: 3.5 })];
const funnel = [W.poly([[640, pY - 120], [860, pY - 120], [775, pY + 10], [775, pY + 100], [725, pY + 100], [725, pY + 10], [640, pY - 120]], { w: 8, jitter: .8 }), W.line(670, pY - 80, 830, pY - 80, { w: 4 })];
const flake = []; for (let k = 0; k < 3; k++) { const a = k * Math.PI / 3, cx = 1130, cy = pY - 10, r = 105; flake.push(W.line(cx - Math.cos(a) * r, cy - Math.sin(a) * r, cx + Math.cos(a) * r, cy + Math.sin(a) * r, { w: 7 })); for (const s of [-1, 1]) { const ex = cx + Math.cos(a) * r * .62 * s, ey = cy + Math.sin(a) * r * .62 * s; flake.push(W.line(ex, ey, ex + Math.cos(a + 2.4 * s) * 34, ey + Math.sin(a + 2.4 * s) * 34, { w: 5 }), W.line(ex, ey, ex + Math.cos(a - 2.4 * s) * 34, ey + Math.sin(a - 2.4 * s) * 34, { w: 5 })); } }
const pile = [W.curve([[560, pY + 480], [640, pY + 400], [750, pY + 370], [860, pY + 400], [940, pY + 480]], { w: 8 }), W.line(540, pY + 482, 960, pY + 482, { w: 7 }), ...[[650, 440], [720, 410], [790, 430], [860, 455], [700, 455], [770, 462]].map(([x, y]) => W.line(x, pY + y, x + 4, pY + y + 4, { w: 7 }))];
tl.draw(K, [...flask, ...flaskThreads], at('v03', .0), { by: at('v03', .22) });
tl.draw(B, ko('배양', 360, pY + 200, 56, { color: W.INK.blue }), at('v03', .2), { by: at('v03', .3) });
tl.draw(B, W.arrow(500, pY - 20, 615, pY - 20, { w: 7, head: 22 }), at('v03', .3), { by: at('v03', .35) });
tl.draw(K, funnel, at('v03', .35), { by: at('v03', .5) });
tl.draw(B, ko('여과', 750, pY + 200, 56, { color: W.INK.blue }), at('v03', .5), { by: at('v03', .58) });
tl.draw(B, W.arrow(880, pY - 20, 995, pY - 20, { w: 7, head: 22 }), at('v03', .58), { by: at('v03', .62) });
tl.draw(K, flake, at('v03', .62), { by: at('v03', .76) });
tl.draw(B, ko('동결건조', 1130, pY + 200, 56, { color: W.INK.blue }), at('v03', .74), { by: at('v03', .84) });
tl.draw(B, W.arrow(1130, pY + 250, 900, pY + 400, { w: 7, head: 22, curve: [1080, pY + 360] }), at('v03', .84), { by: at('v03', .9) });
tl.draw(K, [...pile, ...ko('가루', 750, pY + 600, 60)], at('v03', .88), { by: at('v03', 1.0) + .25 });

// ---------- 4. composition: a pie with 74 % oligosaccharides ----------
const pieY = 3900, pr = 270, a0 = -Math.PI / 2, a1 = a0 + .74 * Math.PI * 2;
tl.draw(K, [W.circle(C, pieY, pr, { w: 9 }), ...ko('말린 무게의', C, pieY - pr - 60, 54)], at('v04', .0), { by: at('v04', .3) });
const wedge = [[C, pieY]]; for (let i = 0; i <= 30; i++) { const a = a0 + (a1 - a0) * i / 30; wedge.push([C + Math.cos(a) * pr * .93, pieY + Math.sin(a) * pr * .93]); }
tl.draw(B, [W.line(C, pieY, C + Math.cos(a0) * pr, pieY + Math.sin(a0) * pr, { w: 7 }), W.line(C, pieY, C + Math.cos(a1) * pr, pieY + Math.sin(a1) * pr, { w: 7 })], at('v04', .3), { by: at('v04', .42) });
tl.draw(B, W.hatch(wedge, { angle: -.7, spacing: 24, w: 7, color: W.INK.blue }), at('v04', .42), { by: at('v04', .75) });
tl.draw(O, W.text('74%', C, pieY + pr + 140, { h: 120, w: 11, align: 'center' }), at('v04', .5), { by: at('v04', .72) });
tl.draw(K, ko('올리고당', C, pieY + pr + 250, 70), at('v04', .74), { by: at('v04', 1.0) });

// ---------- 5. immune cells ----------
const cY = 4980;
const cell = (x, r, seed) => { const out = [W.circle(x, cY, r, { w: 8, lap: .15 })]; out.push(W.circle(x + 12, cY - 8, r * .4, { w: 6, lap: .1 })); for (let k = 0; k < 7; k++) { const a = k / 7 * Math.PI * 2 + seed; out.push(W.line(x + Math.cos(a) * r, cY + Math.sin(a) * r, x + Math.cos(a) * (r + 26), cY + Math.sin(a) * (r + 26), { w: 5 })); } return out; };
tl.draw(K, ko('면역세포', C, cY - 300, 70), at('v05', .0), { by: at('v05', .22) });
tl.draw(K, [...cell(470, 130, .3), ...ko('NK세포', 470, cY + 250, 60)], at('v05', .3), { by: at('v05', .58) });
tl.draw(K, [...cell(1030, 130, 1.1), ...ko('T세포', 1030, cY + 250, 60)], at('v05', .58), { by: at('v05', .8) });
tl.draw(B, [...W.arrow(C, cY + 420, 560, cY + 300, { w: 7, head: 22 }), ...W.arrow(C, cY + 420, 940, cY + 300, { w: 7, head: 22 }), ...W.text('?', C, cY + 520, { h: 90, w: 9, align: 'center' })], at('v05', .8), { by: at('v05', 1.0) });

// ---------- 6–7. the 2022 trial ----------
const tY = 6000;
tl.draw(B, ko('2022 미국 임상', C, tY, 70, { color: W.INK.blue }), at('v06', .0), { by: at('v06', .25) });
tl.draw(K, ko('HPV 2년 이상', C, tY + 110, 56), at('v06', .25), { by: at('v06', .45) });
const people = []; for (let r = 0; r < 5; r++) for (let c = 0; c < 10; c++) { const x = 345 + c * 90, y = tY + 230 + r * 92; people.push(W.circle(x, y, 13, { w: 5, lap: .1 }), W.arc(x, y + 52, 26, Math.PI * 1.08, Math.PI * 1.92, { w: 5 })); }
tl.draw(K, people, at('v06', .45), { by: at('v06', .9) });
tl.draw(K, ko('여성 50명', C, tY + 760, 62), at('v06', .88), { by: at('v06', 1.0) + .2 });
const bY = 7020, bx0 = 300, bx1 = 1200, fill = bx0 + (bx1 - bx0) * .588;
const cal = []; for (let k = 0; k < 6; k++) cal.push(...W.rect(300 + k * 82, bY - 220, 66, 60, { w: 5, over: 3 }));
tl.draw(K, [...cal, ...ko('6개월', 960, bY - 170, 56)], at('v07', .0), { by: at('v07', .3) });
tl.draw(K, ko('34명 중', 420, bY - 40, 52), at('v07', .3), { by: at('v07', .42) });
tl.draw(K, W.rect(bx0, bY, bx1 - bx0, 110, { w: 7, over: 6 }), at('v07', .42), { by: at('v07', .52) });
tl.draw(B, W.hatch([[bx0 + 8, bY + 8], [fill, bY + 8], [fill, bY + 102], [bx0 + 8, bY + 102]], { angle: -1.0, spacing: 18, w: 8, alpha: .7, color: W.INK.blue }), at('v07', .52), { by: at('v07', .7) });
tl.draw(B, [...W.text('58.8%', fill, bY + 270, { h: 120, w: 11, align: 'center' }), ...ko('음성 전환', fill, bY + 380, 56, { color: W.INK.blue })], at('v07', .72), { by: at('v07', 1.0) });

// ---------- 8–9. the caveats (orange) ----------
const kY = 7720;
const mag = [W.circle(400, kY, 90, { w: 9 }), W.line(465, kY + 65, 560, kY + 160, { w: 14 })];
tl.draw(O, mag, at('v08', .0), { by: at('v08', .25) });
tl.draw(O, [...ko('소규모 연구', 900, kY - 30, 66, { color: W.INK.orange }), ...ko('아직 재현 안 됨', 900, kY + 80, 66, { color: W.INK.orange })], at('v08', .25), { by: at('v08', .95) });
const wY = 8250;
tl.draw(O, [W.poly([[400, wY - 110], [520, wY + 90], [280, wY + 90], [400, wY - 110]], { w: 9 }), W.line(400, wY - 40, 400, wY + 20, { w: 10 }), W.line(400, wY + 50, 402, wY + 54, { w: 11 })], at('v09', .0), { by: at('v09', .25) });
tl.draw(K, [...ko('설사 · 가려움', 880, wY - 20, 60), ...ko('일부 약과 상호작용', 880, wY + 80, 60)], at('v09', .25), { by: at('v09', 1.0) });

// ---------- 10. the conclusion ----------
const zY = 8900;
tl.draw(K, ko('치료제', 650, zY, 96), at('v10', .0), { by: at('v10', .18) });
tl.draw(O, [W.line(860, zY - 90, 960, zY + 10, { w: 13 }), W.line(960, zY - 90, 860, zY + 10, { w: 13 })], at('v10', .18), { by: at('v10', .28) });
tl.draw(K, ko('연구 중인 소재', 680, zY + 190, 96), at('v10', .28), { by: at('v10', .52) });
tl.draw(O, W.text('✓', 1100, zY + 200, { h: 110, w: 13, align: 'center' }), at('v10', .52), { by: at('v10', .58) });
tl.draw(O, [W.circle(730, zY + 150, 490, { w: 9, ry: 125, lap: .3 }), W.circle(730, zY + 152, 505, { w: 7, ry: 138, lap: .2, a0: -1.4 })], at('v10', .58), { by: at('v10', .74) });
tl.draw(K, [...ko('복용 전 의사와 상의', C, zY + 420, 70), W.line(380, zY + 450, 1120, zY + 446, { w: 7 })], at('v10', .72), { by: at('v10', 1.0) });
tl.draw(K, [...ko('정보 제공용 영상', C, zY + 600, 40), ...ko('출처: Smith et al. 2022 · MSK 외', C, zY + 660, 34)], V.v10.t1 + .2, { by: V.v10.t1 + 1.2 });
tl.cue(V.v10.t1 + 1.6, 'cap');
tl.end();

// ---------- camera ----------
const L = id => V[id];
const cam = new W.Camera([
  [0, C, 880, 1.12], [L('v01').t1 - .2, C, 975, 1.0],
  [L('v02').t0 + 1.2, C, 1720, 1.0], [L('v02').t1, C, 1840, 1.0],
  [L('v03').t0 + .6, C, 2960, 1.0, 0, 'io'], [L('v03').t1, C, 3020, 1.0],
  [L('v04').t0 + .5, C, 4020, 1.0], [L('v04').t1, C, 4060, 1.08],
  [L('v05').t0 + .35, C, 5040, 1.0, 0, 'o'], [L('v05').t1, C, 5080, 1.0],
  [L('v06').t0 + .5, C, 6320, 1.0], [L('v06').t1, C, 6350, 1.0],
  [L('v07').t0 + .5, C, 7000, 1.0], [L('v07').t1 + .3, C, 7030, 1.03],
  [L('v08').t0 + .25, C, 7820, 1.0, -.015, 'o'], [L('v08').t1, C, 7840, 1.0],
  [L('v09').t0 + .4, C, 8240, 1.0], [L('v09').t1, C, 8260, 1.0],
  [L('v10').t0 + .45, C, 9100, 1.0], [L('v10').t1 + 1.3, C, 9230, 1.0],
  [DUR, C, 8300, .48],
]);

// ---------- board, props, subtitles ----------
const board = new W.Board(tl, { W: 1500, H: 10500 });
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
