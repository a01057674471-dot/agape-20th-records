// 올리고파 — 40.5 s portrait product film in the Swiss Motion Graphics style.
// One family (Noto Sans KR), paper / ink / greys and one signal colour (lime, from the package). Every element snaps to
// a 6-column grid on the beat (120 bpm); entrances are clip-reveals and wipes, deletions are knife cuts. No music: print foley only.
import { clamp, lerp, seg, E, snap, lin, steps, E8, E16, BEAT } from './ease.js';

export const W = 1080, H = 1920, DUR = 40.5;
export const C = { page: '#ECEBE6', paper: '#FFFFFF', ink: '#111111', grid: '#D3D2CC', mute: '#77766F', lime: '#B4EC2D' };
// frame grid: 6 columns of 136, margin 72, gutter 24
const M = 72, CW = 136, GU = 24;
const fx = i => M + i * (CW + GU);
const FAM = 'NotoKR';

// ---------- key moments (seconds, on eighth-note grid) ----------
export const K = {
  climb: [0, 1.0], limeOut: 1.25, numText: 1.25, capA: 1.5, cutA: 4.5,
  grid: 4.75, head: 5.0, rows: [5.75, 6.25, 6.75, 7.25], push: 12.0, pushD: .75,
  capC: 12.25, lyc: 12.25, fruit: 12.75, cutFruit: 16.75, mol1: 16.9, square: 17.0, label: 17.25, knives: 18.0, apart: 19.0, mol2: 18.75, small: 19.5,
  limeWipe: 22.25, silence: [22.25, 22.5], lead: 22.5, bars: [23.0, 23.5, 24.0, 24.75], big: [25.25, 25.75], foot: 23.0,
  cutD: 29.0, taste: 29.375, sticks: 30.0, pack: 31.5, day: 31.75,
  card: 35.75, title: 35.75, rule: 36.25, tag: 36.25, badges: 36.75,
};

// ---------- text ----------
function font(g, wt, size) {
  g.font = `${wt} ${size}px ${FAM}`;
  g.letterSpacing = size >= 90 ? `${(-size * .02).toFixed(1)}px` : '0px';
}
const tw = (g, s) => g.measureText(s).width;
const TXT = [], WORDS = [];   // on-screen texts (reading check) and word landings (foley)
function reg(id, text, t0, t1, box, words) {
  if (TXT.some(x => x.id === id)) return;
  TXT.push({ id, text, t0, t1, box });
  if (words) words.forEach((w, i) => WORDS.push({ t: t0 + (i + 1) * E16, big: w > 90 }));
}
// a line that rises word by word out of a clip rect (lands on sixteenths) and leaves upward at t1
function say(g, id, s, x, y, size, wt, color, t0, t1, o = {}) {
  font(g, wt, size);
  const words = s.split(' '), sp = tw(g, ' '), w = tw(g, s);
  reg(id, o.text ?? s, t0, t1, [x, y - size, w, size * 1.3], words.map(() => size));
  if (T < t0 - E16 || T > t1 + E8) return;
  const q = snap(T, t1 + E8, E8);
  let cx = x;
  words.forEach((wd, i) => {
    const p = snap(T, t0 + (i + 1) * E16, E16), ww = tw(g, wd);
    if (p > 0 && q < 1) {
      if (o.block && i === 0) { const h = size * 1.32 * p * (1 - q); g.fillStyle = o.block; g.fillRect(x - 14, y + size * .3 - h, w + 28, h); }
      g.save(); g.beginPath(); g.rect(cx - 4, y - size * 1.08, ww + 8, size * 1.36); g.clip();
      g.fillStyle = o.colors?.[i] ?? color; g.fillText(wd, cx, y + (1 - p) * size * 1.1 - q * size * 1.4);
      g.restore();
    }
    cx += ww + sp;
  });
}
// a giant numeral that climbs into its clip rect in four eased steps ("one module at a time")
function numeral(g, id, s, x, y, size, color, t0, t1, tOut, text) {
  font(g, 900, size);
  const w = tw(g, s), asc = g.measureText(s).actualBoundingBoxAscent;
  reg(id, text ?? s, t0, tOut, [x, y - asc, w, asc]);
  if (T < t0 || T > tOut + E8) return;
  const p = steps(T, t0, t1, 4), q = snap(T, tOut + E8, E8);
  g.save(); g.beginPath(); g.rect(x - 20, y - asc - 30, w + 40, asc + 60); g.clip();
  g.fillStyle = color; g.fillText(s, x, y + (1 - p) * (asc + 40) - q * (asc + 60));
  g.restore();
}
// knife cut: a 3 px line crosses linearly in one sixteenth, landing at tc; returns the collapse factor (1 → 0 over an eighth)
function knife(g, tc, x0, x1, y, color = C.ink) {
  if (T > tc - E16 && T < tc + E16) { g.fillStyle = color; g.fillRect(x0, y - 1.5, (x1 - x0) * lin(T, tc - E16, tc), 3); }
  return 1 - snap(T, tc + E8, E8);
}
function collapse(g, k, my, fn) {
  if (k <= 0) return;
  g.save(); if (k < 1) { g.translate(0, my); g.scale(1, Math.max(.001, k)); g.translate(0, -my); } fn(); g.restore();
}
// caption row: 1 px rule and three small notes, wiped in from the left
function captions(g, y, t0, t1, a, b, c, color = C.ink) {
  if (T < t0 || T > t1 + E8) return;
  const p = lin(T, t0, t0 + E8 * 2), q = snap(T, t1 + E8, E8);
  g.fillStyle = color; g.fillRect(M, y, (W - 2 * M) * p * (1 - q), 1.5);
  font(g, 500, 26);
  [[a, fx(0)], [b, fx(2)], [c, fx(4)]].forEach(([s, x], i) => {
    if (!s) return;
    const r = snap(T, t0 + E16 * (i + 2), E16);
    g.save(); g.beginPath(); g.rect(x - 2, y + 8, 340, 40); g.clip();
    g.fillText(s, x, y + 40 + (1 - r) * 34 - q * 40); g.restore();
  });
}

let T = 0, PKG = null, NUM = 380;
export async function load() {
  PKG = await new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = 'assets/package.jpg'; });
}
export function measure(g) { font(g, 900, 100); NUM = Math.floor((W - 2 * M) / tw(g, '1,000') * 100); }

// ====================================================================
// 01 · 0–4.5: lime field, a giant 1,000 climbs in; the lime collapses into one rule under it
function sceneNumber(g, t) {
  const by = 1040;
  const k = knife(g, K.cutA, 0, W, by - 140);
  collapse(g, k, by - 140, () => numeral(g, 'num', '1,000', M, by, NUM, C.ink, K.climb[0], K.climb[1], 99));
  // lime: full frame → a 14 px rule at y 1088, then the rule retracts along its length at the cut
  const p = snap(t, K.limeOut + E8 * 2, E8 * 2);
  const top = lerp(0, by + 48, p), bot = lerp(H, by + 62, p), rw = W * (1 - lin(t, K.cutA, K.cutA + E8));
  g.globalCompositeOperation = 'multiply'; g.fillStyle = C.lime; g.fillRect(0, top, rw, bot - top); g.globalCompositeOperation = 'source-over';
  say(g, 'mg', 'mg', M, 1250, 150, 900, C.ink, K.numText, K.cutA);
  say(g, 'num-t', 'L-아르지닌 · 1포 기준', M, 1370, 54, 700, C.ink, K.numText + E8, K.cutA);
  captions(g, 96, K.capA, K.cutA, '올리고파', '01 / 05', '함량 · 1포 기준');
}

// 02 · 4.5–12: the spec sheet. Horizontal grid: 1 column = 250 mg, so each bar is its real dose
const MG = 112 / 250;          // px per mg
const ROWS = [
  ['L-아르지닌', '1,000', 1000], ['프락토올리고당', '1,875', 1875], ['수용성마카추출물', '300', 300], ['리치추출분말 (Oligonol®)', '100', 100],
];
const rowY = i => 470 + i * 290;
function specSheet(g, t) {
  // grid lines grow downward on sixteenths
  for (let i = 0; i <= 8; i++) {
    const p = lin(t, K.grid + i * E16, K.grid + i * E16 + E8 * 2);
    if (p > 0) { g.fillStyle = C.grid; g.fillRect(M + i * 112, 420, 1.5, (1660 - 420) * p); }
  }
  font(g, 500, 22); g.fillStyle = C.mute;
  for (let i = 0; i <= 8; i += 2) if (t > K.grid + i * E16 + E8) g.fillText(`${i * 250}`, M + i * 112 + 6, 1690);
  say(g, 'grid-lead', '1포(15g) 기준', M, 230, 34, 500, C.mute, K.head, 99);
  say(g, 'grid', '한 포에 담은 4가지', M, 330, 88, 900, C.ink, K.head + E8, 99);
  ROWS.forEach(([name, n, mg], i) => {
    const t0 = K.rows[i], y = rowY(i), hero = i === 3;
    say(g, 'row' + i, name, M, y, 32, 500, C.mute, t0 - E8, 99);
    numeral(g, 'rown' + i, n, M, y + 112, 96, C.ink, t0, t0 + BEAT, 99, n + 'mg');
    font(g, 700, 40); const nw = (() => { font(g, 900, 96); return tw(g, n); })();
    say(g, 'rowu' + i, 'mg', M + nw + 12, y + 112, 40, 700, C.ink, t0 + BEAT, 99);
    const p = snap(t, t0 + BEAT + E8, E8 * 2);
    if (p > 0) { g.fillStyle = hero ? C.lime : C.ink; g.fillRect(M, y + 140, Math.max(2, mg * MG * p), 72); }
  });
  captions(g, 1760, K.grid, 99, '가로 1칸 = 250mg', '02 / 05', '4가지 원료');
}
// push into the lime bar until it is the whole frame
function scenePush(g, t) {
  const p = snap(t, K.push, K.pushD);
  const r = [M, rowY(3) + 140, 100 * MG, 72];
  const s = Math.exp(lerp(0, Math.log(Math.max(W / r[2], H / r[3]) * 1.02), p));
  const cx = lerp(W / 2, r[0] + r[2] / 2, Math.min(1, p * 1.6)), cy = lerp(H / 2, r[1] + r[3] / 2, Math.min(1, p * 1.6));
  g.save(); g.translate(W / 2, H / 2); g.scale(s, s); g.translate(-cx, -cy);
  specSheet(g, t); g.restore();
}

// 03 · 12–22.25: on lime. The ingredient, then a big block cut into small ones
function sceneLime(g, t) {
  // lime wipes away upward at the end, the page underneath
  const wipe = snap(t, K.limeWipe, E8 * 2);
  g.fillStyle = C.lime; g.fillRect(0, 0, W, H * (1 - wipe));
  g.save(); g.beginPath(); g.rect(0, 0, W, H * (1 - wipe)); g.clip();
  captions(g, 96, K.capC, 99, '원료 04 / 04', '03 / 05', '리치추출분말');
  say(g, 'lyc1', '리치추출분말', M, 400, 112, 900, C.ink, K.lyc, K.cutFruit - E8, { text: '리치추출분말 Oligonol®' });
  say(g, 'lyc1b', 'Oligonol®', M, 525, 112, 900, C.ink, K.lyc + E8, K.cutFruit - E8);
  say(g, 'lyc2', '리치 열매에서 추출한 폴리페놀', M, 620, 44, 500, C.ink, K.lyc + E8 * 2, K.cutFruit - E8);
  // the fruit as two flat circles: ink skin, paper flesh, an ink seed. Wiped in, knife-cut out
  if (t > K.fruit && t < K.cutFruit + E8 * 2) {
    const k = knife(g, K.cutFruit, M, W - M, 1180);
    const p = snap(t, K.fruit + E8 * 2, E8 * 2);
    collapse(g, k, 1180, () => {
      g.save(); g.beginPath(); g.rect(0, 860, W, 640 * p); g.clip();
      g.fillStyle = C.ink; g.beginPath(); g.arc(fx(2) + 40, 1180, 300, 0, Math.PI * 2); g.fill();
      g.fillStyle = C.paper; g.beginPath(); g.arc(fx(3) + 120, 1240, 230, 0, Math.PI * 2); g.fill();
      g.fillStyle = C.ink; g.beginPath(); g.ellipse(fx(3) + 120, 1240, 70, 92, 0, 0, Math.PI * 2); g.fill();
      g.restore();
    });
  }
  say(g, 'mol1', '폴리페놀, 크기가 다르다', M, 400, 84, 900, C.ink, K.mol1, K.limeWipe - E8);
  // the big block (600 × 600) wipes in, six knife cuts make a 4 × 4 grid, then the pieces separate, nearest the centre first
  if (t > K.square) {
    const x0 = 240, y0 = 760, S = 600, pw = (S - 3 * GU) / 4;
    const p = snap(t, K.square + E8 * 2, E8 * 2);
    g.save(); g.beginPath(); g.rect(0, y0, W, S * p); g.clip();
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
      const d = Math.hypot(c - 1.5, r - 1.5), a = snap(t, K.apart + E8 + Math.round(d) * E16, E8);
      const cell = S / 4, x = x0 + c * lerp(cell, pw + GU, a), y = y0 + r * lerp(cell, pw + GU, a), w = lerp(cell, pw, a);
      g.fillStyle = C.ink; g.fillRect(x - (a < 1 ? .5 : 0), y - (a < 1 ? .5 : 0), w + (a < 1 ? 1 : 0), w + (a < 1 ? 1 : 0));
    }
    g.restore();
    for (let i = 0; i < 6; i++) {          // knife lines in lime, crossing the black block
      const tc = K.knives + (i + 1) * E16, v = i < 3, k = (i % 3 + 1) * S / 4;
      if (t > tc - E16 && t < K.apart + E8) {
        const L = S * lin(t, tc - E16, tc); g.fillStyle = C.lime;
        if (v) g.fillRect(x0 + k - 2, y0, 4, L); else g.fillRect(x0, y0 + k - 2, L, 4);
      }
    }
    say(g, 'big', '큰 분자', x0, y0 - 28, 32, 700, C.ink, K.label, K.small - E8);
    say(g, 'small', '저분자', x0, y0 - 28, 32, 700, C.ink, K.small, K.limeWipe - E8);
  }
  say(g, 'mol2', '저분자 폴리페놀이 풍부', M, 1600, 76, 900, C.ink, K.mol2, K.limeWipe - E8);
  g.restore();
}

// 04 · 22.5–29: one beat of silence, then the comparison. Bars on a shared base, the hero in lime, the giant 2~8배
const BARS = [['포도씨', '추출물', .13], ['소나무 껍질', '추출물', .2], ['리치 열매', '추출물', .48], ['리치추출분말', 'Oligonol®', 1]];
function sceneChart(g, t) {
  const k = knife(g, K.cutD, 0, W, 960);
  collapse(g, k, 960, () => {
    say(g, 'chart', '일반 폴리페놀 원료 대비 저분자 폴리페놀', M, 300, 40, 700, C.ink, K.lead, 99);
    numeral(g, 'chartn', '2~8배', M, 740, 300, C.ink, K.big[0], K.big[1], 99);
    const base = 1560, bw = 200, gap = (W - 2 * M - 4 * bw) / 3;
    g.fillStyle = C.ink; g.fillRect(M, base, (W - 2 * M) * lin(t, K.lead, K.lead + E8 * 2), 2);
    BARS.forEach(([a, b, v], i) => {
      const x = M + i * (bw + gap), p = snap(t, K.bars[i], E8 * (i === 3 ? 3 : 2)), h = 640 * v * p;
      if (p > 0) { g.fillStyle = i === 3 ? C.lime : C.ink; g.fillRect(x, base - h, bw, h); }
      say(g, 'bl' + i, a, x, base + 46, 28, i === 3 ? 700 : 500, C.ink, K.bars[i] - E8, 99);
      say(g, 'bl2' + i, b, x, base + 82, 28, i === 3 ? 700 : 500, C.ink, K.bars[i] - E8 + E16, 99);
    });
    say(g, 'foot', '* 원료사 자료 기준 · 시중 일반 폴리페놀 원료와 비교', M, 1760, 26, 500, C.mute, K.foot, 99);
    captions(g, 96, K.lead, 99, '저분자 폴리페놀', '04 / 05', '원료 비교');
  });
}

// 05 · 29–35.75: the taste, and fourteen sticks snapping into a 7 × 2 grid, the first in lime
function sceneSticks(g, t) {
  say(g, 'taste', '상큼한 리치맛', M, 420, 128, 900, C.ink, K.taste, K.card - E8);
  captions(g, 96, K.taste, K.card - E8, '구성', '05 / 05', '15g × 14포');
  const sw = (W - 2 * M - 6 * GU) / 7, sh = 340;
  for (let i = 0; i < 14; i++) {
    const r = Math.floor(i / 7), c = i % 7, x = M + c * (sw + GU), y = 640 + r * (sh + GU);
    const p = snap(t, K.sticks + (i + 1) * E16, E8), q = snap(t, K.card - E8 * 2 + c * E16 * .5, E8);
    if (p <= 0 || q >= 1) continue;
    g.save(); g.beginPath(); g.rect(x - 1, y + sh * (1 - p) + sh * q, sw + 2, sh * p - sh * q); g.clip();
    g.fillStyle = i ? C.ink : C.lime; g.fillRect(x, y, sw, sh);
    font(g, 700, 26); g.fillStyle = i ? C.page : C.ink; g.fillText(String(i + 1).padStart(2, '0'), x + 12, y + sh - 16);
    g.restore();
  }
  say(g, 'sticks', '15g × 14포', M, 1500, 104, 900, C.ink, K.pack, K.card - E8, { text: '15g × 14포 하루 1포' });
  say(g, 'day', '하루 1포', M + 14, 1640, 60, 900, C.ink, K.day, K.card - E8, { block: C.lime });
}

// 06 · 35.75–40.5: the product on a sheet of paper; the name, one lime rule, the badges in a caption row
function sceneProduct(g, t) {
  const p = snap(t, K.card + E8 * 2, E8 * 2), cy = 680, ch = 900;
  if (p > 0) {
    g.save(); g.beginPath(); g.rect(M, cy, W - 2 * M, ch * p); g.clip();
    g.fillStyle = C.paper; g.fillRect(M, cy, W - 2 * M, ch);
    if (PKG) { const h = ch - 120, w = h * PKG.width / PKG.height; g.drawImage(PKG, W / 2 - w / 2, cy + 60, w, h); }
    g.restore();
  }
  numeral(g, 'title', '올리고파', M, 560, 230, C.ink, K.title, K.title + BEAT, 99);
  const rp = lin(t, K.rule, K.rule + E8 * 2);
  g.fillStyle = C.lime; g.fillRect(M, 606, (W - 2 * M) * rp, 14);
  say(g, 'tag', '하루 1포로 에너지 UP', M, 1700, 64, 900, C.ink, K.tag, 99);
  captions(g, 1770, K.badges, 99, '의사 공동개발', 'HACCP', 'RAPHAHEAL');
  reg('badges', '의사 공동개발 HACCP RAPHAHEAL', K.badges, DUR, [M, 1770, W - 2 * M, 60]);
}

export function render(g, t) {
  T = t;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.letterSpacing = '0px';
  g.fillStyle = C.page; g.fillRect(0, 0, W, H);
  if (t < K.cutA + E8 * 2) sceneNumber(g, t);
  else if (t < K.push - K.pushD) specSheet(g, t);
  else if (t < K.push) scenePush(g, t);
  else if (t < K.limeWipe + E8) sceneLime(g, t);
  if (t >= K.limeWipe - E8 * 2 && t < K.cutD + E8 * 2) { if (t < K.limeWipe + E8) { g.save(); g.beginPath(); g.rect(0, H * (1 - snap(t, K.limeWipe, E8 * 2)), W, H); g.clip(); sceneChart(g, t); g.restore(); } else sceneChart(g, t); }
  if (t >= K.cutD + E8) sceneSticks(g, t);
  if (t >= K.card) sceneProduct(g, t);
}
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }

// sound events: print foley only (no music)
export function events() {
  const ev = [{ t: 0, type: 'thump' }, { t: K.limeOut + E8 * 2, type: 'slide' }];
  [.25, .5, .75, 1].forEach(u => ev.push({ t: lerp(K.climb[0], K.climb[1], u), type: 'thunk' }));
  ev.push({ t: K.cutA, type: 'knife' });
  for (let i = 0; i <= 8; i++) ev.push({ t: K.grid + i * E16 + E8, type: 'rule' });
  K.rows.forEach((t0, i) => { [.25, .5, .75, 1].forEach(u => ev.push({ t: t0 + BEAT * u, type: 'tick' })); ev.push({ t: t0 + BEAT + E8, type: i === 3 ? 'snapHero' : 'snap' }); });
  ev.push({ t: K.push, type: 'swish', d: K.pushD }, { t: K.push, type: 'paper' });
  ev.push({ t: K.fruit + E8 * 2, type: 'paper' }, { t: K.cutFruit, type: 'knife' }, { t: K.square + E8 * 2, type: 'thump' });
  for (let i = 0; i < 6; i++) ev.push({ t: K.knives + (i + 1) * E16, type: 'knife' });
  for (let d = 0; d < 3; d++) ev.push({ t: K.apart + E8 + d * E16, type: 'snap' });
  ev.push({ t: K.limeWipe - .03, type: 'paper' }, { t: K.silence[0], type: 'silence', d: K.silence[1] - K.silence[0] });
  K.bars.forEach((t0, i) => ev.push({ t: t0, type: i === 3 ? 'snapHero' : 'snap' }));
  [.25, .5, .75, 1].forEach(u => ev.push({ t: lerp(K.big[0], K.big[1], u), type: 'thunk' }));
  ev.push({ t: K.cutD, type: 'knife' });
  for (let i = 0; i < 14; i++) ev.push({ t: K.sticks + (i + 1) * E16, type: i ? 'snap' : 'snapHero' });
  ev.push({ t: K.card + E8 * 2, type: 'paper' }, { t: K.card + E8, type: 'slide' });
  [.25, .5, .75, 1].forEach(u => ev.push({ t: lerp(K.title, K.title + BEAT, u), type: 'thunk' }));
  ev.push({ t: K.rule + E8 * 2, type: 'rule' }, { t: K.badges + E8 * 2, type: 'stamp' });
  for (const w of WORDS) ev.push({ t: w.t, type: w.big ? 'clackBig' : 'clack' });
  return ev.filter(e => e.type === 'silence' || !(e.t > K.silence[0] - .01 && e.t < K.silence[1] - .01)).sort((a, b) => a.t - b.t);
}
