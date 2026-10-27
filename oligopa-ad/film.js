// 올리고파 — 38 s portrait ad in the Dark Tech Keynote style. One beat grid (120 BPM) drives picture and sound.
import * as E from './engine.js';
const { clamp, lerp, seg, ss, eo, ei, eio, back, hash, mulberry, TAU, W, H, PAL } = E;

export const BPM = 120, BEAT = .5, DUR = 38;
E.setAccent('#B7F34A');
const KR = (px, wt = 500) => `${wt} ${px}px NotoKR, InterTight`, NUM = px => `600 ${px}px InterTight`, MONO = px => `500 ${px}px JBMono`;

// ───────── key times (seconds, on the beat grid) ─────────
export const K = {
  bolt: .08, numLock: [.875, 1.0, 1.125, 1.25], numLabel: .5,
  toCard: 3.75, cards: [4.25, 4.75, 5.25], gridHead: 4.0,
  dive: 7.5, lycheeReveal: 8.0, lycheeText: [8.25, 8.4, 8.6],
  molecule: 12.5, split: 16.0, molText: [12.6, 16.25],
  silence: [19.75, 20.0], bars: [20.25, 20.75, 21.25, 22.0], bigNum: 22.75, bigLocks: [23.0, 23.125], foot: 20.75,
  taste: 26.0, sticks: 29.0, stickText: 30.0,
  collapse: 33.0, pkg: 33.5, title: 33.75, tagline: 34.25, badges: 34.75, brand: 35.0, bolt2: 33.4,
};

// ───────── helpers ─────────
function text(g, s, x, y, f, color = PAL.text, o = {}) {
  g.save(); g.font = f; g.fillStyle = color; g.textAlign = o.align ?? 'center'; g.textBaseline = 'alphabetic'; g.globalAlpha *= o.a ?? 1;
  if (o.track && g.letterSpacing !== undefined) g.letterSpacing = o.track;
  if (o.glow) { g.shadowColor = E.rgba(color, .7); g.shadowBlur = o.glow; }
  g.fillText(s, x, y); const w = g.measureText(s).width; g.restore(); return w;
}
// a line that rises in on a beat and leaves by squashing (nothing just fades)
function line(g, t, t0, t1, s, x, y, f, color, o = {}) {
  if (t < t0 || t > t1 + .25) return;
  const a = eo(seg(t, t0, t0 + .22)), out = ei(seg(t, t1, t1 + .25));
  g.save(); g.translate(x, y + (1 - a) * 22); g.scale(1, 1 - out * .85); g.globalAlpha = a * (1 - out);
  text(g, s, 0, 0, f, color, o); g.restore();
}
const TXT = [];                                      // every on-screen text with its time window, for the reading-time check
function reg(id, s, t0, t1, box) { if (!TXT.some(x => x.id === id)) TXT.push({ id, text: s, t0, t1, box }); }

// lightning: a jagged accent path, drawn on in a few frames and gone in a few more
function bolt(g, t, t0, x0, y0, x1, y1, seed, w = 7) {
  const u = t - t0; if (u < 0 || u > .45) return;
  const R = mulberry(seed), pts = [[x0, y0]], n = 9;
  for (let i = 1; i < n; i++) { const k = i / n; pts.push([lerp(x0, x1, k) + (R() - .5) * 140, lerp(y0, y1, k) + (R() - .5) * 40]); }
  pts.push([x1, y1]);
  const grow = eo(seg(u, 0, .06)), a = 1 - ss(seg(u, .12, .45)), m = Math.max(2, Math.ceil(pts.length * grow));
  g.save(); g.globalAlpha = a; g.strokeStyle = PAL.accent; g.lineWidth = w; g.lineJoin = 'round'; g.shadowColor = E.rgba(PAL.accent, .9); g.shadowBlur = 40;
  g.beginPath(); pts.slice(0, m).forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.stroke();
  g.lineWidth = w * .35; g.strokeStyle = '#F4FFE0'; g.shadowBlur = 0; g.stroke();
  // a branch
  g.lineWidth = w * .45; g.strokeStyle = PAL.accent; g.beginPath(); const b = pts[4]; g.moveTo(...b); g.lineTo(b[0] + 120, b[1] + 90); g.lineTo(b[0] + 90, b[1] + 200); g.stroke();
  g.restore();
  E.glow(g, (x0 + x1) / 2, (y0 + y1) / 2, 900, PAL.accent, .18 * a);
}

// ───────── the lychee (drawn once, revealed by light) ─────────
const SKIN = '#B8606E', FLESH = '#EEF0E6';
const lychee = (() => {
  const [c, g] = E.buf('lychee', 900, 900); g.clearRect(0, 0, 900, 900);
  // whole fruit, left-back
  const fx = 340, fy = 470, fr = 260;
  let gr = g.createRadialGradient(fx - 90, fy - 110, 20, fx, fy, fr * 1.05);
  gr.addColorStop(0, '#E79AA3'); gr.addColorStop(.55, SKIN); gr.addColorStop(1, '#4A1E2A');
  g.fillStyle = gr; g.beginPath(); g.arc(fx, fy, fr, 0, TAU); g.fill();
  const R = mulberry(7);
  for (let i = 0; i < 520; i++) {             // the bumpy skin: small lit studs
    const a = R() * TAU, rr = Math.sqrt(R()) * fr * .96, x = fx + Math.cos(a) * rr, y = fy + Math.sin(a) * rr, d = rr / fr;
    const s = 9 * (1 - d * .45);
    g.fillStyle = `rgba(255,220,225,${.10 + .14 * (1 - d) * (x < fx ? 1 : .5)})`; g.beginPath(); g.arc(x - 2, y - 2, s * .55, 0, TAU); g.fill();
    g.fillStyle = `rgba(40,10,18,${.18 + .2 * d})`; g.beginPath(); g.arc(x + 2, y + 3, s * .5, 0, TAU); g.fill();
  }
  // halved fruit, right-front: skin rim + glossy translucent flesh + a seed
  const hx = 600, hy = 610, hr = 230;
  g.fillStyle = '#5A2532'; g.beginPath(); g.ellipse(hx, hy, hr, hr * .92, 0, 0, TAU); g.fill();
  gr = g.createRadialGradient(hx - 60, hy - 70, 10, hx, hy, hr * .9);
  gr.addColorStop(0, '#FFFFFF'); gr.addColorStop(.6, FLESH); gr.addColorStop(1, '#BFC6B6');
  g.fillStyle = gr; g.beginPath(); g.ellipse(hx, hy, hr * .86, hr * .8, 0, 0, TAU); g.fill();
  g.fillStyle = 'rgba(255,255,255,.55)'; g.beginPath(); g.ellipse(hx - 70, hy - 80, 70, 34, -.5, 0, TAU); g.fill();
  gr = g.createRadialGradient(hx + 20, hy + 20, 5, hx + 30, hy + 30, 80);
  gr.addColorStop(0, '#7A4A35'); gr.addColorStop(1, '#2E1A14');
  g.fillStyle = gr; g.beginPath(); g.ellipse(hx + 30, hy + 30, 62, 52, .3, 0, TAU); g.fill();
  // a leaf
  g.fillStyle = '#3E5A36'; g.beginPath(); g.moveTo(200, 230); g.quadraticCurveTo(110, 120, 40, 140); g.quadraticCurveTo(110, 250, 200, 230); g.fill();
  return c;
})();

// ───────── polyphenol molecule: hexagon rings ─────────
function hexPath(cx, cy, r, rot = 0) { const p = new Path2D(); for (let i = 0; i < 6; i++) { const a = rot + i * TAU / 6; i ? p.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r) : p.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r); } p.closePath(); return p; }
const RINGS = (() => {                                // a big cluster on a hex lattice, then each ring's small-molecule home
  const out = [], R = mulberry(3), r = 46, dx = r * 1.73, dy = r * 1.5;
  const cells = [];
  for (let j = -4; j <= 4; j++) for (let i = -4; i <= 4; i++) { const x = i * dx + (j & 1 ? dx / 2 : 0), y = j * dy; if (Math.hypot(x, y * 1.1) < 300 + (R() - .5) * 90) cells.push([x, y]); }
  const home = E.snapGrid(5, 6, 120, 34, W / 2 - (5 * 120 + 4 * 34) / 2, 760);
  cells.slice(0, 30).forEach((c, k) => out.push({ x: c[0], y: c[1], hx: home[k].x, hy: home[k].y, seed: k }));
  return out;
})();

// ───────── scenes ─────────
function stage(g, t, o = {}) {
  E.bg(g, { lift: o.lift ?? 1, cool: o.cool ?? .8 });
  E.grid(g, { ox: W / 2, oy: H / 2, alpha: o.grid ?? 1 });
}

function sceneNumber(g, t) {
  // 0–3.75: the giant number locks out of glyph noise, digits right to left (the hook)
  const push = 1 + .05 * eo(seg(t, .3, 3));
  g.save(); g.translate(W / 2, 980); g.scale(push, push);
  E.glow(g, 0, -80, 520, PAL.accent, .16 * eo(seg(t, .8, 1.4)));
  E.scramble(g, '1,000', 0, 0, t, [K.numLock[3], K.numLock[3], K.numLock[2], K.numLock[1], K.numLock[0]], { px: 300, align: 'center', color: PAL.accent, start: .25, tracking: -.045 });
  if (t > 1.3) text(g, 'mg', 0, 120, NUM(110), PAL.text, { a: eo(seg(t, 1.3, 1.6)) });
  g.restore();
  line(g, t, K.numLabel, K.toCard - .15, 'L-아르지닌 · 1포 기준', W / 2, 640, KR(46, 500), PAL.dim);
  line(g, t, .5, K.toCard - .15, 'L-ARGININE', W / 2, 560, MONO(30), PAL.mute, { track: '6px' });
  reg('num', 'L-아르지닌 · 1포 기준', K.numLabel, K.toCard - .15, [W / 2 - 230, 595, 460, 60]);
}

const CARDS = [
  { name: 'L-아르지닌', v: '1,000', slot: 0 }, { name: '프락토올리고당', v: '1,875', slot: 1 },
  { name: '수용성마카추출물', v: '300', slot: 2 }, { name: '리치추출분말', v: '100', slot: 3, hero: 1 },
];
const SLOT = E.snapGrid(2, 2, 440, 40, 80, 640).map(s => ({ x: s.x, y: s.y }));
function card(g, c, x, y, s, t, lockT, a = 1) {
  g.save(); g.translate(x, y); g.scale(s, s); g.globalAlpha *= a;
  E.panel(g, -220, -220, 440, 440, { r: 36, fill: PAL.surf, shadow: 1 });
  if (c.hero) { g.strokeStyle = E.rgba(PAL.accent, .7); g.lineWidth = 2; E.rr(g, -219, -219, 438, 438, 36); g.stroke(); }
  text(g, c.name, 0, -120, KR(38, 500), PAL.dim);
  E.scramble(g, c.v, 0, 60, t, [lockT + .25, lockT + .125, lockT + .125, lockT].slice(0, c.v.length), { px: 130, align: 'center', color: c.slot === 0 ? PAL.accent : PAL.text, tracking: -.04 });
  text(g, 'mg', 0, 150, NUM(54), PAL.dim);
  g.restore();
}
function sceneCards(g, t) {
  // 3.75–7.5: the number becomes the first card; three more fly in and snap into a 2×2 grid
  line(g, t, K.gridHead, K.dive - .2, '한 포에 담은 4가지', W / 2, 500, KR(76, 800), PAL.text);
  reg('grid', '한 포에 담은 4가지', K.gridHead, K.dive - .2, [W / 2 - 330, 420, 660, 100]);
  for (const c of CARDS) {
    const to = SLOT[c.slot];
    if (c.slot === 0) {
      const p = clamp(seg(t, K.toCard, K.toCard + .45)), q = back(p, 1.3);
      card(g, c, lerp(W / 2, to.x, q), lerp(930, to.y, q), lerp(1.9, 1, eo(p)), t, 0);
    } else {
      const t0 = K.cards[c.slot - 1] - .3, p = clamp(seg(t, t0, t0 + .3)); if (p <= 0) continue;
      const from = [{ x: W + 300, y: to.y - 200 }, { x: -300, y: to.y + 200 }, { x: W + 300, y: to.y + 300 }][c.slot - 1];
      const fp = E.flyPose({ ...from, rot: (c.slot & 1 ? .35 : -.35) }, { ...to, rot: 0 }, p);
      g.save(); g.translate(fp.x, fp.y); g.rotate(fp.rot); card(g, c, 0, 0, 1, t, K.cards[c.slot - 1] + .25); g.restore();
    }
  }
  line(g, t, K.cards[2] + .15, K.dive - .2, '1포(15g) 기준', W / 2, 1640, KR(32, 500), PAL.mute);
}

function sceneLychee(g, t) {
  // 7.5–12.5: dive into the lychee card, the fruit revealed by a band of light
  const ex = eio(seg(t, K.dive, K.dive + .45)), s = SLOT[3];
  if (ex < 1) { // the hero card expands to the frame
    const x = lerp(s.x - 220, 0, ex), y = lerp(s.y - 220, 0, ex), w = lerp(440, W, ex), h = lerp(440, H, ex);
    stage(g, t); for (const c of CARDS) if (!c.hero) card(g, c, SLOT[c.slot].x, SLOT[c.slot].y, 1, t, 0, 1 - ex);
    E.panel(g, x, y, w, h, { r: lerp(36, 0, ex), fill: PAL.surf }); card(g, CARDS[3], s.x, s.y, 1, t, 0, 1 - ex * 3); g.save(); g.strokeStyle = E.rgba(PAL.accent, .7 * (1 - ex)); g.lineWidth = 2; E.rr(g, x, y, w, h, lerp(36, 0, ex)); g.stroke(); g.restore();
    return;
  }
  stage(g, t, { lift: 1.1 });
  const p = seg(t, K.lycheeReveal, K.lycheeReveal + 1.3), drift = 1 + .04 * seg(t, K.lycheeReveal, K.molecule);
  g.save(); g.translate(W / 2, 1080); g.scale(drift, drift);
  E.glow(g, 60, 40, 520, '#E79AA3', .10 * p);
  E.lightReveal(g, lychee, -450, -450, 900, 900, p, { base: .04, glint: .2, soft: 320 });
  g.restore();
  line(g, t, K.lycheeText[0], K.molecule - .1, 'INGREDIENT', W / 2, 300, MONO(30), PAL.mute, { track: '6px' });
  line(g, t, K.lycheeText[0], K.molecule - .1, '리치추출분말', W / 2, 420, KR(92, 800), PAL.text);
  line(g, t, K.lycheeText[1], K.molecule - .1, 'Oligonol®', W / 2, 520, NUM(70), PAL.accent, { glow: 24 });
  line(g, t, K.lycheeText[2], K.molecule - .1, '리치 열매에서 추출한 폴리페놀', W / 2, 1640, KR(48, 500), PAL.text);
  reg('lyc1', '리치추출분말 Oligonol®', K.lycheeText[1], K.molecule - .1, [W / 2 - 300, 340, 600, 200]);
  reg('lyc2', '리치 열매에서 추출한 폴리페놀', K.lycheeText[2], K.molecule - .1, [W / 2 - 360, 1590, 720, 70]);
}

function sceneMolecule(g, t) {
  // 12.5–19.75: one big polyphenol cluster splits into small molecules that snap into a grid
  stage(g, t);
  const appear = eo(seg(t, K.molecule, K.molecule + .5)), sp = seg(t, K.split, K.split + .9);
  const cx = W / 2, cy = 1080;
  // bonds between neighbouring rings while still one big molecule
  if (sp < .2) { g.save(); g.globalAlpha = appear * (1 - sp * 5); g.strokeStyle = 'rgba(255,255,255,.16)'; g.lineWidth = 3;
    for (let a = 0; a < RINGS.length; a++) for (let b = a + 1; b < RINGS.length; b++) { const A = RINGS[a], B = RINGS[b]; if (Math.hypot(A.x - B.x, A.y - B.y) < 90) { g.beginPath(); g.moveTo(cx + A.x, cy + A.y); g.lineTo(cx + B.x, cy + B.y); g.stroke(); } }
    g.restore(); }
  RINGS.forEach((r, k) => {
    const delay = (k % 6) * .04, p = clamp(seg(t, K.split + delay, K.split + delay + .55));
    const fp = E.flyPose({ x: cx + r.x, y: cy + r.y, rot: 0, s: 1 }, { x: r.hx, y: r.hy, rot: 0, s: 1.15 }, p);
    const tremble = t > K.split - .6 && t < K.split ? Math.sin(t * 90 + k) * 2.5 : 0;
    const path = hexPath(fp.x + tremble, fp.y, 40 * fp.s * (.6 + .4 * appear), TAU / 12);
    E.litShape(g, path, p > .4 ? { accent: true, glowR: 18, alpha: appear } : { color: '#5B6479', glowR: 0, alpha: appear });
  });
  line(g, t, K.molText[0], K.split - .1, '폴리페놀, 크기가 다르다', W / 2, 460, KR(72, 800), PAL.text);
  line(g, t, K.molText[0] + .4, K.split - .1, '큰 분자', W / 2, 1500, KR(40, 500), PAL.dim);
  if (t >= K.molText[1] && t < K.silence[0]) {
    const a = eo(seg(t, K.molText[1], K.molText[1] + .22));
    g.save(); g.globalAlpha = a; g.translate(0, (1 - a) * 22);
    g.font = KR(76, 800); const w1 = g.measureText('저분자 ').width, w2 = g.measureText('폴리페놀이 풍부').width, x0 = W / 2 - (w1 + w2) / 2;
    text(g, '저분자 ', x0, 500, KR(76, 800), PAL.accent, { align: 'left', glow: 22 }); text(g, '폴리페놀이 풍부', x0 + w1, 500, KR(76, 800), PAL.text, { align: 'left' });
    g.restore();
  }
  reg('mol1', '폴리페놀, 크기가 다르다', K.molText[0], K.split - .1, [W / 2 - 380, 390, 760, 100]);
  reg('mol2', '저분자 폴리페놀이 풍부', K.molText[1], K.silence[0], [W / 2 - 420, 420, 840, 110]);
}

const BARS = [{ n: '포도씨\n추출물', v: .13 }, { n: '소나무 껍질\n추출물', v: .2 }, { n: '리치 열매\n추출물', v: .48 }, { n: '리치추출분말\nOligonol®', v: 1, hero: 1 }];
function sceneChart(g, t) {
  // 20–26: one beat of silence, the bars fill one per beat, then the number
  stage(g, t);
  if (t < K.silence[1]) return;
  const x0 = 120, bw = 170, gap = 50, base = 1420, top = 860;
  BARS.forEach((b, i) => {
    const x = x0 + i * (bw + gap), tf = K.bars[i], p = back(clamp(seg(t, tf, tf + .35)), 1.2);
    E.panel(g, x, top - 20, bw, base - top + 40, { r: 24, fill: PAL.surf, shadow: .6, alpha: eo(seg(t, K.silence[1], K.silence[1] + .25)) });
    const h = (base - top) * b.v * p;
    if (h > 2) { const path = new Path2D(); path.roundRect(x + 18, base - h, bw - 36, h, 14); E.litShape(g, path, b.hero ? { accent: true, glowR: 30 } : { bbox: [x, base - h, bw, h] }); }
    b.n.split('\n').forEach((s, k) => text(g, s, x + bw / 2, 1500 + k * 44, KR(32, b.hero ? 800 : 500), b.hero ? PAL.text : PAL.dim, { a: eo(seg(t, K.silence[1], K.silence[1] + .3)) }));
  });
  line(g, t, K.silence[1], K.taste - .15, '일반 폴리페놀 원료 대비 저분자 폴리페놀', W / 2, 330, KR(40, 500), PAL.dim);
  if (t >= K.bigNum) {
    g.save(); E.glow(g, W / 2, 520, 420, PAL.accent, .14 * eo(seg(t, K.bigLocks[1], K.bigLocks[1] + .3)));
    const w = E.scramble(g, '2~8', W / 2 - 70, 600, t, [K.bigLocks[0], K.bigLocks[0], K.bigLocks[1]], { px: 230, align: 'center', color: PAL.accent, start: K.bigNum, tracking: -.03 });
    text(g, '배', W / 2 - 70 + w / 2 + 20, 600, KR(150, 800), PAL.text, { align: 'left', a: eo(seg(t, K.bigLocks[1], K.bigLocks[1] + .2)) });
    g.restore();
  }
  line(g, t, K.foot, K.taste - .15, '* 원료사 자료 기준 · 시중 일반 폴리페놀 원료와 비교', W / 2, 1720, KR(28, 500), PAL.mute);
  reg('chart', '일반 폴리페놀 원료 대비 저분자 폴리페놀 2~8배', K.silence[1], K.taste - .15, [80, 280, 920, 360]);
  reg('foot', '* 원료사 자료 기준 · 시중 일반 폴리페놀 원료와 비교', K.foot, K.taste - .15, [W / 2 - 400, 1690, 800, 40]);
}

const STICKS = E.snapGrid(7, 2, 96, 24, (W - (7 * 96 + 6 * 24)) / 2, 900);
function stick(g, x, y, s, rot, a = 1) {
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); g.globalAlpha *= a;
  E.panel(g, -46, -150, 92, 300, { r: 16, fill: '#1B2240', shadow: .8, cheap: true });
  g.fillStyle = PAL.accent; g.shadowColor = E.rgba(PAL.accent, .8); g.shadowBlur = 10; E.rr(g, -34, -40, 68, 14, 7); g.fill(); g.shadowBlur = 0;
  g.fillStyle = 'rgba(255,255,255,.18)'; E.rr(g, -34, -120, 68, 6, 3); g.fill();
  g.restore();
}
function sceneTaste(g, t) {
  // 26–33: the taste, then fourteen sticks snap into a grid
  stage(g, t);
  const lp = eo(seg(t, K.taste, K.taste + .4)), lout = ei(seg(t, K.sticks - .3, K.sticks));
  if (lout < 1) { g.save(); g.translate(W / 2, 1030); const sc = .7 * lerp(.85, 1, lp) * (1 - lout); g.scale(sc, sc); g.globalAlpha = lp; g.drawImage(lychee, -450, -450); g.restore();
    for (let k = 0; k < 4; k++) { const tk = K.taste + .3 + k * .25, u = seg(t, tk, tk + .5); if (u > 0 && u < 1) E.litShape(g, E.sparklePath(W / 2 + [-220, 230, 160, -150][k], 1030 + [-210, -160, 220, 180][k], 40 * Math.sin(u * Math.PI), .2), { accent: true, glowR: 20 }); } }
  line(g, t, K.taste + .1, K.sticks - .1, '상큼한 리치맛', W / 2, 500, KR(92, 800), PAL.text);
  reg('taste', '상큼한 리치맛', K.taste + .1, K.sticks - .1, [W / 2 - 320, 410, 640, 110]);
  STICKS.forEach((s, k) => {
    const t0 = K.sticks + k * .0625, p = clamp(seg(t, t0, t0 + .3)); if (p <= 0) return;
    const fp = E.flyPose({ x: W / 2, y: 1900, rot: (k % 2 ? .6 : -.6) }, { x: s.x, y: s.j ? 1210 : 860, rot: 0 }, p);
    const out = seg(t, K.collapse, K.collapse + .4), cx = lerp(fp.x, W / 2, eio(out)), cy = lerp(fp.y, 1000, eio(out));
    stick(g, cx, cy, 1 - out * .7, fp.rot, 1 - out);
  });
  if (t >= K.stickText && t < K.collapse + .1) {
    const a = eo(seg(t, K.stickText, K.stickText + .22));
    g.save(); g.globalAlpha = a; g.translate(0, (1 - a) * 22);
    text(g, '15g × 14포', W / 2, 1560, NUM(84), PAL.text);
    text(g, '하루 1포', W / 2, 1660, KR(56, 800), PAL.accent, { glow: 18 }); g.restore();
  }
  reg('sticks', '15g × 14포 하루 1포', K.stickText, K.collapse, [W / 2 - 260, 1480, 520, 210]);
}

let PKG = null;
function sceneProduct(g, t) {
  // 33–38: the product card revealed by light, then the name, the line and the marks
  stage(g, t, { lift: 1.15 });
  const p = seg(t, K.pkg, K.pkg + 1.3), iw = 600, ih = iw * (PKG ? PKG.height / PKG.width : 1.26), x = W / 2 - iw / 2, y = 560;
  E.glow(g, W / 2, y + ih / 2, 700, PAL.accent, .12 * p);
  if (PKG) {
    const [c, cg] = E.buf('pkgcard', iw, Math.ceil(ih)); cg.clearRect(0, 0, iw, ih);
    cg.save(); E.rr(cg, 0, 0, iw, ih, 40); cg.clip(); cg.drawImage(PKG, 0, 0, iw, ih); cg.restore();
    const lift = (1 - eo(seg(t, K.pkg, K.pkg + .6))) * 60;
    E.panel(g, x - 6, y - 6 + lift, iw + 12, ih + 12, { r: 46, fill: PAL.surf, shadow: 1 });
    E.lightReveal(g, c, x, y + lift, iw, ih, p, { base: .05, glint: .2, soft: 300 });
  }
  line(g, t, K.title, DUR, '올리고파', W / 2, 400, KR(120, 800), PAL.text);
  if (t >= K.tagline) {
    const a = eo(seg(t, K.tagline, K.tagline + .22)); g.save(); g.globalAlpha = a; g.translate(0, (1 - a) * 22);
    g.font = KR(58, 800); const w1 = g.measureText('하루 1포로 ').width, w2 = g.measureText('에너지 UP').width, x0 = W / 2 - (w1 + w2) / 2;
    text(g, '하루 1포로 ', x0, 1440, KR(58, 800), PAL.text, { align: 'left' }); text(g, '에너지 UP', x0 + w1, 1440, KR(58, 800), PAL.accent, { align: 'left', glow: 20 }); g.restore();
  }
  ['의사 공동개발', 'HACCP'].forEach((s, k) => {
    const tk = K.badges + k * .25, a = eo(seg(t, tk, tk + .22)); if (a <= 0) return;
    g.save(); g.globalAlpha = a; g.font = KR(36, 500); const w = g.measureText(s).width + 64, bx = W / 2 + (k ? 20 : -20 - w), by = 1500 + (1 - a) * 16;
    E.panel(g, bx, by, w, 70, { r: 35, fill: PAL.surf2, shadow: .5 }); text(g, s, bx + w / 2, by + 47, KR(36, 500), PAL.text); g.restore();
  });
  line(g, t, K.brand, DUR, 'RAPHAHEAL', W / 2, 1720, NUM(40), PAL.mute, { track: '10px' });
  reg('title', '올리고파', K.title, DUR, [W / 2 - 260, 290, 520, 140]);
  reg('tag', '하루 1포로 에너지 UP', K.tagline, DUR, [W / 2 - 330, 1375, 660, 85]);
  reg('badges', '의사 공동개발 HACCP', K.badges, DUR, [W / 2 - 330, 1500, 660, 70]);
}

// ───────── render ─────────
export async function load() {
  PKG = await new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = 'assets/package.jpg'; });
}
export function render(g, t) {
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1;
  if (t < K.toCard) { stage(g, t); bolt(g, t, K.bolt, W / 2 + 160, -40, W / 2 - 120, 760, 11); sceneNumber(g, t); }
  else if (t < K.dive) { stage(g, t); sceneCards(g, t); }
  else if (t < K.molecule) sceneLychee(g, t);
  else if (t < K.silence[1]) sceneMolecule(g, t);
  else if (t < K.taste) sceneChart(g, t);
  else if (t < K.pkg) sceneTaste(g, t);
  else sceneProduct(g, t);
  if (t >= K.bolt2 && t < K.bolt2 + .5) bolt(g, t, K.bolt2, W / 2 - 200, -40, W / 2 + 160, 900, 23);
  E.vignette(g, .5);
}
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }

// sound events for the mixer
export function events() {
  const ev = [{ t: K.bolt, type: 'bolt' }, { t: K.bolt2, type: 'bolt' }, { t: K.silence[0], type: 'silence', d: K.silence[1] - K.silence[0] }];
  K.numLock.forEach(t => ev.push({ t, type: 'lock' })); K.cards.forEach(t => ev.push({ t, type: 'snap' }), ev.push({ t: K.toCard, type: 'whoosh' }));
  CARDS.forEach((c, i) => { if (i) [0, .125, .25].forEach(d => ev.push({ t: K.cards[i - 1] + .25 + d, type: 'grain' })); });
  ev.push({ t: K.dive, type: 'expand' }, { t: K.lycheeReveal - .4, type: 'shimmer', d: 1.7 }, { t: K.molecule, type: 'pop' }, { t: K.split, type: 'split' });
  RINGS.forEach((r, k) => ev.push({ t: K.split + (k % 6) * .04 + .5, type: 'tap', i: k }));
  K.bars.forEach((t, i) => ev.push({ t, type: i === 3 ? 'barHero' : 'bar' }));
  K.bigLocks.forEach(t => ev.push({ t, type: 'lock' }));
  ev.push({ t: K.taste, type: 'sparkle' });
  STICKS.forEach((s, k) => ev.push({ t: K.sticks + k * .0625 + .3, type: 'tick', i: k }));
  ev.push({ t: K.collapse, type: 'whoosh' }, { t: K.pkg - .4, type: 'shimmer', d: 1.8 }, { t: K.title, type: 'chord' });
  [K.badges, K.badges + .25].forEach(t => ev.push({ t, type: 'snap' }));
  for (const x of TXT) ev.push({ t: x.t0, type: 'text' });
  return ev.sort((a, b) => a.t - b.t);
}
