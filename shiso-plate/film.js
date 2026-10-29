// 깻잎인 줄 알았던 그 잎 — 30 s portrait reel in the Copperplate Engraving style, cut to the user's narration.
// Six photographs, each engraved into the plate first (three hatch families cut from the photo's own tones),
// then hand-coloured: the real photograph blooms in under the ink. Roundels carry the details (two molecules,
// a balance), lettering is cut glyph by glyph, every new plate is a fresh sheet laid on the bed.
import { B, drawSheet, engraveText, roundelFrame, leader, PAL } from './engine/index.js';
const { clamp, noise1 } = B;
export const W = 1080, H = 1920, DUR = 30;
const KR = 'Noto Serif KR', ROMAN = 'Bodoni Moda';
const E = t => 1 - Math.pow(1 - clamp(t), 3), EIO = t => (t = clamp(t), t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const R = [76, 250, 1004, 1570];                     // the picture inside the plate mark
const PLATE = [40, 40, 1040, 1880];

// ---------- edit list ----------
// photo: assets/pN.jpg, fy: which photo row sits at the centre of the crop (0..1), ink: cutting window, bloom: hand colouring
export const SC = [      // cut to the narration (tools/voice.py): each plate opens just before its phrase
  { id: 'q',     t0: 0,    t1: 3.9,  photo: 6, fy: .45, ink: [-.8, .9],     bloom: 1.2,  pl: 'I',   sub: 'var. frutescens  &  var. crispa' },
  { id: 'shiso', t0: 3.9,  t1: 9.6,  photo: 2, fy: .42, ink: [3.9, 4.8],    bloom: 4.65, pl: 'II',  sub: 'var. crispa  —  shiso' },
  { id: 'chem',  t0: 9.6,  t1: 13.1, photo: 1, fy: .40, ink: [9.6, 10.5],   bloom: 10.35, pl: 'III', sub: 'Rosmarinic acid  ·  Luteolin' },
  { id: 'lab',   t0: 13.1, t1: 18.4, photo: 5, fy: .50, ink: [13.1, 14.0],  bloom: 13.85, pl: 'IV', sub: 'Ueda et al.  1997  ·  2002' },
  { id: 'table', t0: 18.4, t1: 22.6, photo: 4, fy: .45, ink: [18.4, 19.2],  bloom: 19.05, pl: 'V',  sub: 'Juice  ·  Yukari  ·  Salad' },
  { id: 'end',   t0: 22.6, t1: 30,   photo: 3, fy: .38, ink: [22.6, 23.5],  bloom: 23.35, pl: 'VI', sub: 'Perilla frutescens var. crispa' },
];
export const K = {
  answer: 2.05, cut1: [6.0, 6.4], roundels: [10.55, 11.45], balance: 14.0, level: [15.6, 16.6],
  stops: [[18.75, 19.35], [19.4, 19.95], [20.0, 22.0]], cap6b: 24.8,
};
const CAPS = {
  q:     [['둘 중 깻잎은 뭘까요?', .1]],
  shiso: [['이건 자소예요.', 4.0], ['일본 식탁에 늘 오르는 잎', 4.2]],
  chem:  [['로즈마린산, 루테올린이', 9.7], ['들어 있는 잎', 9.95]],
  lab:   [['일본에선 면역 반응의 균형,', 13.2], ['TNF-α 조절 작용이 연구됐어요', 13.45]],
  table: [['주스로, 밥에, 샐러드로.', 18.5], ['일본 식탁의 단골 잎', 18.8]],
  end:   [['이제 깻잎과 헷갈리지 마세요', 22.7], ['몰랐던 건강 소재, 팔로우하고 더 알아가요', K.cap6b]],
};

// ---------- text registry (reading check) ----------
const TXT = [];
function reg(id, text, t0, t1, box) { if (!TXT.some(x => x.id === id)) TXT.push({ id, text, t0, t1, box }); }
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }
// Korean lettering, cut glyph by glyph like the roman capitals (≈ 14 glyphs a second)
function cut(ctx, id, s, x, y, t, t0, t1, o = {}) {
  const size = o.size || 54;
  ctx.save(); ctx.font = `${o.weight || 700} ${size}px "${o.font || KR}"`; const w = ctx.measureText(s).width; ctx.restore();
  const ax = o.align === 'left' ? x : o.align === 'right' ? x - w : x - w / 2;
  reg(id, o.text ?? s, t0, t1, [ax, y - size, w, size * 1.3]);
  if (t < t0) return;                                    // after t1 the letters stay until a new sheet covers them
  if (o.chip) { const pc = E((t - t0) / .25); ctx.fillStyle = 'rgba(241,232,210,.93)'; ctx.fillRect(ax - size * .35, y - size * 1.0, (w + size * .7) * pc, size * 1.35); }
  engraveText(ctx, s, x, y, { size, font: o.font || KR, weight: o.weight || 700, italic: o.italic, align: o.align || 'center', track: o.track || 0, color: o.color || PAL.ink, p: clamp((t - t0) / Math.max(.25, s.length / 14)) });
}

// ---------- photographs: crop, tone field, engraving, colour ----------
const P = {};
export async function load() {
  for (const s of SC) {
    const img = await new Promise((res, rej) => { const im = new Image(); im.onload = () => res(im); im.onerror = rej; im.src = `assets/p${s.photo}.jpg`; });
    const w = R[2] - R[0], h = R[3] - R[1], k = Math.max(w / img.width, h / img.height);
    const sw = w / k, sh = h / k, sx = (img.width - sw) / 2, sy = clamp(img.height * s.fy - sh / 2, 0, img.height - sh);
    const c = document.createElement('canvas'); c.width = w; c.height = h; c.getContext('2d').drawImage(img, sx, sy, sw, sh, 0, 0, w, h);
    // tone grid (1 = darkest) from luminance, at a quarter resolution, contrast lifted a little
    const q = 4, gw = Math.ceil(w / q), gh = Math.ceil(h / q), g = document.createElement('canvas'); g.width = gw; g.height = gh;
    const gx = g.getContext('2d'); gx.drawImage(c, 0, 0, gw, gh); const d = gx.getImageData(0, 0, gw, gh).data, T = new Float32Array(gw * gh);
    for (let i = 0; i < gw * gh; i++) { const L = (0.2126 * d[4 * i] + 0.7152 * d[4 * i + 1] + 0.0722 * d[4 * i + 2]) / 255; T[i] = clamp(Math.pow(1 - L, 1.05) * 1.6 - .12); }
    const tone = (x, y) => { const i = clamp(Math.floor((x - R[0]) / q), 0, gw - 1), j = clamp(Math.floor((y - R[1]) / q), 0, gh - 1); return T[j * gw + i]; };
    const ink = new B.Ink(), poly = [[[R[0], R[1]], [R[2], R[1]], [R[2], R[3]], [R[0], R[3]]]], sd = s.photo * 11;
    ink.group('h1'); B.hatch(ink, poly, { angle: -.62, spacing: 4.6, tone, thr: .1, wMin: .25, wMax: 2.8, step: 4, seed: sd, bend: .00012 });
    ink.group('h2'); B.hatch(ink, poly, { angle: .5, spacing: 5.2, tone, thr: .42, wMin: .25, wMax: 2.3, step: 4, seed: sd + 1 });
    ink.group('h3'); B.hatch(ink, poly, { angle: -1.25, spacing: 6.2, tone, thr: .7, wMin: .25, wMax: 1.8, step: 4, seed: sd + 2 });
    const [a, b] = s.ink, m = (b - a);
    ink.schedule('h1', a, a + m * .7, { conc: 40 }); ink.schedule('h2', a + m * .3, a + m * .9, { conc: 40 }); ink.schedule('h3', a + m * .55, b, { conc: 40 }); ink.build();
    P[s.id] = { c, ink };
  }
}
// the hand colouring: the photograph blooms out from where the brush touched, with a ragged wet front
function bloom(ctx, s, t) {
  const u = clamp((t - s.bloom) / .85); if (u <= 0) return;
  const o = [R[0] + (R[2] - R[0]) * .55, R[1] + (R[3] - R[1]) * .45], far = 1150 * E(u);
  ctx.save(); ctx.beginPath();
  for (let i = 0; i <= 96; i++) { const a = i / 96 * Math.PI * 2, r = far * (.82 + .3 * noise1(i * .35 + s.photo * 7, 3)); i ? ctx.lineTo(o[0] + Math.cos(a) * r, o[1] + Math.sin(a) * r) : ctx.moveTo(o[0] + Math.cos(a) * r, o[1] + Math.sin(a) * r); }
  ctx.closePath(); ctx.clip();
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = .95; ctx.drawImage(P[s.id].c, R[0], R[1]);
  ctx.restore();
}

// ---------- roundels ----------
function roundel(ctx, x, y, r, t, t0, fn) {
  if (t < t0) return;
  const p = E((t - t0) / .45), s = .25 + .75 * p, yy = y + (1 - p) * 60;
  ctx.save(); ctx.translate(x, yy); ctx.scale(s, s);
  ctx.fillStyle = PAL.paper; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.arc(0, 0, r - 8, 0, Math.PI * 2); ctx.clip(); fn(ctx, clamp((t - t0 - .3) / .9)); ctx.restore();
  roundelFrame(ctx, 0, 0, r, { p: clamp((t - t0) / .4), w: 3 });
  ctx.restore();
}
// polylines cut in order: p 0→1 over their total length
function cutLines(ctx, lines, p, w = 3) {
  const L = lines.map(l => l.slice(1).reduce((a, q, i) => a + Math.hypot(q[0] - l[i][0], q[1] - l[i][1]), 0)), tot = L.reduce((a, b) => a + b, 0);
  let left = tot * clamp(p);
  ctx.save(); ctx.strokeStyle = PAL.ink; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  lines.forEach(l => {
    if (left <= 0) return; ctx.beginPath(); ctx.moveTo(l[0][0], l[0][1]);
    for (let i = 1; i < l.length && left > 0; i++) { const [ax, ay] = l[i - 1], [bx, by] = l[i], d = Math.hypot(bx - ax, by - ay), f = Math.min(1, left / d); ctx.lineTo(ax + (bx - ax) * f, ay + (by - ay) * f); left -= d; }
    ctx.stroke();
  });
  ctx.restore();
}
const dir = (a, r = 1) => [Math.cos(a * Math.PI / 180) * r, Math.sin(a * Math.PI / 180) * r];
const add = (p, v) => [p[0] + v[0], p[1] + v[1]];
const hex = (c, r) => [-90, -30, 30, 90, 150, 210].map(a => add(c, dir(a, r)));
function ring(lines, c, r) { const v = hex(c, r); lines.push([...v, v[0]]); return v; }
function label(ctx, s, p, size = 17) { ctx.save(); ctx.font = `600 ${size}px "${ROMAN}"`; ctx.fillStyle = PAL.ink; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const w = ctx.measureText(s).width + 6; ctx.fillStyle = PAL.paper; ctx.fillRect(p[0] - w / 2, p[1] - size * .6, w, size * 1.2); ctx.fillStyle = PAL.ink; ctx.fillText(s, p[0], p[1]); ctx.restore(); }
// luteolin: 2-(3,4-dihydroxyphenyl)-5,7-dihydroxychromen-4-one. A ring fused to the pyranone C ring, B ring on C2.
function luteolin(ctx, p) {
  const r = 28, A = [-62, 4], Cc = add(A, [r * Math.sqrt(3), 0]), lines = [], labels = [];
  const a = ring(lines, A, r), c = hex(Cc, r);
  lines.push([c[5], c[0], c[1], c[2], c[3], c[4]]);                 // C ring (shares the A ring's right edge)
  const C2 = c[1], C3 = c[2], C4 = c[3];
  lines.push([add(C2, dir(120, 5)), add(C3, dir(120, 5))].map((q, i) => add(q, [-4, i ? 0 : 2])));  // C2=C3
  const O4 = add(C4, dir(90, r)); lines.push([C4, O4], [add(C4, [5, 0]), add(O4, [5, 0])]); labels.push(['O', add(O4, [0, 11])]);
  labels.push(['O', c[0]]);
  const B1 = add(C2, dir(-30, r)), Bc = add(B1, dir(-30, r)), b = hex(Bc, r); lines.push([...b, b[0]]); lines.push([C2, b[5]]);
  [[b[2], -30], [b[3], 30]].forEach(([v, ang]) => { const e = add(v, dir(ang + 30, r * .9)); lines.push([v, e]); labels.push(['OH', add(e, dir(ang + 30, 14))]); });
  [[a[4], 210], [a[3], 90]].forEach(([v, ang]) => { const e = add(v, dir(ang, r * .9)); lines.push([v, e]); labels.push(['OH', add(e, dir(ang, 15))]); });
  ctx.save(); ctx.translate(-14, -6);
  cutLines(ctx, lines, p, 2.6);
  [A, Bc].forEach(cc => { if (p > .6) { ctx.strokeStyle = PAL.ink; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(cc[0], cc[1], r * .55 * clamp((p - .6) / .2), 0, Math.PI * 2); ctx.stroke(); } });
  if (p > .85) labels.forEach(([s, q]) => label(ctx, s, q));
  ctx.restore();
}
// rosmarinic acid: caffeic acid esterified with 3-(3,4-dihydroxyphenyl)lactic acid
function rosmarinic(ctx, p) {
  const r = 20, lines = [], labels = [];
  const c1 = [-112, 18], v1 = ring(lines, c1, r);
  [[v1[0], -90], [v1[5], 210]].forEach(([v, a]) => { const e = add(v, dir(a, r * .85)); lines.push([v, e]); labels.push(['OH', add(e, dir(a, 12))]); });
  const p0 = v1[1], p1 = add(p0, dir(-30, r)), p2 = add(p1, dir(30, r)), p3 = add(p2, dir(-30, r)), p4 = add(p3, dir(30, r)), p5 = add(p4, dir(-30, r)), p6 = add(p5, dir(30, r));
  lines.push([p0, p1, p2, p3, p4, p5, p6]);
  lines.push([add(p1, [2, 5]), add(p2, [-2, 5])]);                    // CH=CH
  const o3 = add(p3, dir(-90, r)); lines.push([p3, o3], [add(p3, [4, 0]), add(o3, [4, 0])]); labels.push(['O', add(o3, [2, -9])]);
  labels.push(['O', p4]);
  const cooh = add(p5, dir(-90, r)); lines.push([p5, cooh]); labels.push(['COOH', add(cooh, [0, -10])]);
  const c2 = add(add(p6, dir(-30, r)), dir(-30, r)), v2 = hex(c2, r); lines.push([...v2, v2[0]]); lines.push([p6, v2[5]]);
  [[v2[2], 30], [v2[1], -30]].forEach(([v, a]) => { const e = add(v, dir(a, r * .85)); lines.push([v, e]); labels.push(['OH', add(e, dir(a, 12))]); });
  ctx.save(); ctx.translate(-6, 6);
  cutLines(ctx, lines, p, 2.2);
  [c1, c2].forEach(cc => { if (p > .6) { ctx.strokeStyle = PAL.ink; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.arc(cc[0], cc[1], r * .55 * clamp((p - .6) / .2), 0, Math.PI * 2); ctx.stroke(); } });
  if (p > .85) labels.forEach(([s, q]) => label(ctx, s, q, 14));
  ctx.restore();
}
// a balance: the beam starts tipped toward TNF-α and levels
function balance(ctx, p, t) {
  const th = (14 - 14 * EIO((t - K.level[0]) / (K.level[1] - K.level[0]))) * Math.PI / 180;
  const lines = [[[0, 120], [0, -70]], [[-70, 128], [70, 128]], [[-40, 120], [0, 96], [40, 120]]];
  cutLines(ctx, lines, p, 4);
  if (p < .5) return;
  ctx.save(); ctx.translate(0, -70); ctx.rotate(-th);
  ctx.strokeStyle = PAL.ink; ctx.lineCap = 'round'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(-140, 0); ctx.lineTo(140, 0); ctx.stroke();
  [-140, 140].forEach((x, i) => {
    ctx.save(); ctx.translate(x, 0); ctx.rotate(th);
    ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-44, 92); ctx.moveTo(0, 0); ctx.lineTo(44, 92); ctx.stroke();
    ctx.lineWidth = 3.5; ctx.beginPath(); ctx.ellipse(0, 96, 52, 12, 0, 0, Math.PI); ctx.stroke();
    ctx.font = `italic 600 ${i ? 24 : 26}px "${i ? KR : ROMAN}"`; ctx.fillStyle = PAL.ink; ctx.textAlign = 'center'; ctx.fillText(i ? '자소' : 'TNF-α', 0, 84);
    ctx.restore();
  });
  ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, 0, 7, 0, Math.PI * 2); ctx.stroke();
  ctx.restore();
}

// ---------- one plate ----------
const view = [0, 0, W, H];
function camera(s, t) {      // the loupe: only the table plate travels (juice → rice → salad)
  if (s.id !== 'table') return [W / 2, H / 2, 1];
  const F = [[300, 560], [560, 900], [880, 1330]];
  let c = [W / 2, H / 2, 1];
  K.stops.forEach(([a, b], i) => {
    const pin = EIO((t - a + .3) / .45);
    if (pin > 0) c = [c[0] + (F[i][0] - c[0]) * pin, c[1] + (F[i][1] - c[1]) * pin, c[2] + (1.65 - c[2]) * pin];
  });
  const out = EIO((t - (K.stops[2][1] - .5)) / .4); c = [c[0] + (W / 2 - c[0]) * out, c[1] + (H / 2 - c[1]) * out, c[2] + (1 - c[2]) * out];
  // keep the loupe over the photograph: the frame must never show the paper behind it
  const z = c[2], lim = (lo, hi, m) => [lo - (lo - m) / z, hi - (hi - m) / z];
  const [x0, x1] = lim(R[0], R[2], W / 2), [y0, y1] = lim(R[1], R[3], H / 2);
  return [clamp(c[0], Math.min(x0, x1), Math.max(x0, x1)), clamp(c[1], Math.min(y0, y1), Math.max(y0, y1)), z];
}
function plate(ctx, s, t) {
  const [cx, cy, z] = camera(s, t);
  drawSheet(ctx, { W, H, plate: PLATE, tone: .8 });
  ctx.save(); ctx.beginPath(); ctx.rect(R[0], R[1], R[2] - R[0], R[3] - R[1]); ctx.clip();
  ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy);
  if (z > 1.001) { ctx.fillStyle = PAL.paper; ctx.fillRect(R[0], R[1], R[2] - R[0], R[3] - R[1]); }
  bloom(ctx, s, t);
  const ia = 1 - .5 * clamp((t - s.bloom - .2) / .8);      // once the colour is in, the ink steps back a little (it stays on top)
  ctx.globalAlpha = ia; P[s.id].ink.draw(ctx, t, { view: null }); ctx.globalAlpha = 1;
  ctx.restore();
  ctx.strokeStyle = PAL.ink; ctx.lineWidth = 2.2; ctx.strokeRect(R[0] - 8, R[1] - 8, R[2] - R[0] + 16, R[3] - R[1] + 16);
  ctx.lineWidth = .8; ctx.strokeRect(R[0] - 14, R[1] - 14, R[2] - R[0] + 28, R[3] - R[1] + 28);
  // lettering at the head of the plate (outside the camera)
  engraveText(ctx, 'PERILLA FRUTESCENS', W / 2, 128, { size: 44, weight: 600, track: .16, p: clamp((t - s.t0 + (s.t0 ? 0 : 1)) / .7) });
  engraveText(ctx, s.sub, W / 2, 182, { size: 28, weight: 500, italic: true, p: clamp((t - s.t0 - .15) / .6) });
  engraveText(ctx, `PL. ${s.pl}`, PLATE[2] - 40, 92, { size: 22, weight: 600, track: .12, align: 'right', p: clamp((t - s.t0) / .4 + (s.t0 ? 0 : 1)) });
  reg('head' + s.id, s.sub, s.t0 + .15, s.t1, [140, 150, 800, 40]);
  overlay(ctx, s, t);
  // captions under the plate
  CAPS[s.id].forEach(([str, t0], i) => cut(ctx, `cap-${s.id}-${i}`, str, W / 2, 1668 + i * 76, t, t0, s.t1, { size: i && s.id === 'end' ? 40 : 54, weight: i && s.id === 'end' ? 600 : 700 }));
  if (s.id === 'lab') cut(ctx, 'foot', '* 자소잎 추출물을 먹인 생쥐 실험 · Ueda 외, 1997 · 2002', W / 2, 1832, t, 13.6, s.t1, { size: 22, weight: 600, text: '* 생쥐 실험 · Ueda 외, 1997 · 2002' });
}
function overlay(ctx, s, t) {
  if (s.id === 'q' && t >= K.answer) {
    cut(ctx, 'a1', '깻잎', 300, 1060, t, K.answer, s.t1, { size: 72, chip: true });
    cut(ctx, 'a2', '자소', 770, 1060, t, K.answer, s.t1, { size: 72, chip: true, color: '#2f5d1e' });
  }
  if (s.id === 'shiso') {
    const L = [['초밥 옆 그 잎', [530, 470], [180, 330], K.cut1[0]], ['우메보시의 붉은색', [870, 780], [770, 1000], K.cut1[1]]];
    L.forEach(([str, from, to, t0], i) => {
      if (t < t0) return;
      leader(ctx, from, to, { p: clamp((t - t0) / .35), w: 1.6 });
      ctx.fillStyle = PAL.ink; ctx.beginPath(); ctx.arc(from[0], from[1], 5, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.font = `700 36px "${KR}"`; const w = ctx.measureText(str).width; ctx.fillStyle = 'rgba(241,232,210,.92)';
      if (t > t0 + .25) ctx.fillRect(to[0] - (i ? w - 0 : 0) - 14, to[1] - 40, w + 28, 54); ctx.restore();
      cut(ctx, 'ld' + i, str, i ? to[0] : to[0], to[1], t, t0 + .25, s.t1, { size: 36, align: i ? 'right' : 'left' });
    });
  }
  if (s.id === 'chem') {
    roundel(ctx, 290, 1280, 210, t, K.roundels[0], (c, p) => { c.scale(1.2, 1.2); rosmarinic(c, p); });
    roundel(ctx, 790, 1280, 210, t, K.roundels[1], (c, p) => { c.scale(1.25, 1.25); luteolin(c, p); });
    if (t > K.roundels[0] + .5) engraveText(ctx, 'ROSMARINIC ACID', 290, 1530, { size: 22, weight: 600, track: .1, p: clamp((t - K.roundels[0] - .5) / .5) });
    if (t > K.roundels[1] + .5) engraveText(ctx, 'LUTEOLIN', 790, 1530, { size: 22, weight: 600, track: .1, p: clamp((t - K.roundels[1] - .5) / .5) });
  }
  if (s.id === 'lab') roundel(ctx, 330, 560, 230, t, K.balance, (c, p) => balance(c, p, t));
}

// ---------- frame: each plate is a new sheet laid on the bed ----------
let A2 = null;
export function render(ctx, t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  let i = SC.findIndex(s => t < s.t1); if (i < 0) i = SC.length - 1;
  const s = SC[i], into = t - s.t0, TR = .3;
  if (i === 0 || into >= TR) { plate(ctx, s, t); return; }
  plate(ctx, SC[i - 1], t);
  const y = (1 - EIO(into / TR)) * H;
  ctx.save(); ctx.translate(0, y);
  ctx.fillStyle = 'rgba(40,28,16,.25)'; ctx.fillRect(0, -14, W, 14);
  ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.clip(); plate(ctx, s, t); ctx.restore();
}

// ---------- sound events ----------
export function events() {
  const ev = [];
  SC.forEach((s, i) => { ev.push({ t: s.t0, type: i ? 'sheet' : 'start', i }, { t: Math.max(0, s.ink[0]), type: 'burin', d: s.ink[1] - Math.max(0, s.ink[0]) }, { t: s.bloom, type: 'wash' }); });
  ev.push({ t: K.answer, type: 'reveal' });
  K.cut1.forEach(t => ev.push({ t, type: 'leader' }));
  K.roundels.forEach(t => ev.push({ t, type: 'roundel' }));
  ev.push({ t: K.balance, type: 'roundel' }, { t: K.level[1], type: 'level' });
  K.stops.forEach(([a]) => ev.push({ t: a - .3, type: 'loupe' }));
  for (const x of TXT) if (x.t0 > .05) ev.push({ t: x.t0, type: 'letter' });
  return ev.sort((a, b) => a.t - b.t);
}
