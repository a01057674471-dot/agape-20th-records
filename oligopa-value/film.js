// 올리고파 — 39 s portrait ad, cut to the user's narration, Swiss Motion Graphics. Value first: the viewer's empty battery, three moments it happens,
// the answer (하루 1포), then the reasons (high dose, low-molecular polyphenol 2~8배), the routine, the product and a call to action.
// Paper / ink / greys and one signal colour (lime = energy). Every element snaps to a 6-column grid on a 120 bpm beat. No music: print foley.
import { lerp, seg, snap, lin, steps, E8, E16, BEAT } from './ease.js';

export const W = 1080, H = 1920, DUR = 39;
export const C = { page: '#ECEBE6', paper: '#FFFFFF', ink: '#111111', grid: '#D3D2CC', mute: '#77766F', lime: '#B4EC2D' };
const M = 72, CW = 136, GU = 24;
const fx = i => M + i * (CW + GU);
const FAM = 'NotoKR';

// ---------- key moments (seconds, on the eighth-note grid) ----------
export const K = {
  drain: [.25, .5, .75, 1.0, 1.25], empty: .5, cutA: 3.4,                              // 01 battery 100 → 10      (voice 0.2 오늘도 방전이에요?)
  cells: [3.5, 5.0, 6.5], cutB: 7.75,                                                  // 02 three moments         (3.6 / 5.1 / 6.6)
  lead3: 7.8, one: 8.9, name: 9.9, batt: 10.25, charge: [10.75, 11.5], cutC: 11.875,   // 03 the answer            (7.9 한 잔 더 대신 / 9.0 하루 한 포 / 10.1 올리고파)
  grid: 11.875, row0Label: 12.0, head: 12.25, rows: [13.875, 16.5, 16.875, 17.25], push: 18.75, pushD: .75,   // 04 (12.0 엘 아르지닌 / 14.0 천 밀리그램 / 16.1 고함량 에너지 부스터)
  limeIn: 18.75, lyc: 18.5, square: 19.75, label: 20.0, knives: 20.75, apart: 21.75, small: 22.25,     // 05 (18.6 리치추출분말 올리고놀…)
  lead5: 22.625, big: [24.75, 25.25], foot: 22.125, limeWipe: 27.5,                                  //    (22.8 일반 원료 대비 … 두 배에서 여덟 배)
  taste: 27.375, sticks: 27.75, pack: 28.75, day: 29.0, card: 32.375,                               // 06 (27.65 상큼한 리치맛 / 29.1 하루 한 포씩)
  title: 32.375, rule: 32.875, tag: 33.125, badges: 33.625, cta: 34.375,                             // 07 (32.25 closing line)
};
// voices/narration.wav (the user's recording, 31.2 s) placed in three pieces [from, to, at] (seconds): the gaps give
// the comparison and the 14 sticks their reading time
export const VOICE = [[0, 26.16, 0], [26.16, 28.75, 27.5], [28.75, 31.22, 31.94]];

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
let T = 0, PKG = null;
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
      g.fillStyle = color; g.fillText(wd, cx, y + (1 - p) * size * 1.1 - q * size * 1.4);
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
// caption row: 1.5 px rule and three small notes, wiped in from the left
function captions(g, y, t0, t1, a, b, c, color = C.ink, size = 26) {
  if (T < t0 || T > t1 + E8) return;
  const p = lin(T, t0, t0 + E8 * 2), q = snap(T, t1 + E8, E8);
  g.fillStyle = color; g.fillRect(M, y, (W - 2 * M) * p * (1 - q), 1.5);
  font(g, size > 26 ? 700 : 500, size);
  [[a, fx(0)], [b, fx(2)], [c, fx(4)]].forEach(([s, x], i) => {
    if (!s) return;
    const r = snap(T, t0 + E16 * (i + 2), E16);
    g.save(); g.beginPath(); g.rect(x - 2, y + 8, 340, size + 16); g.clip();
    g.fillText(s, x, y + size + 14 + (1 - r) * (size + 8) - q * (size + 14)); g.restore();
  });
}
// a battery: ink outline, cap, lime fill at `level` (0..1)
function battery(g, x, y, w, h, level, lw = 6) {
  g.fillStyle = C.lime; g.fillRect(x + lw * 2, y + lw * 2, Math.max(0, (w - lw * 4) * level), h - lw * 4);
  g.strokeStyle = C.ink; g.lineWidth = lw; g.strokeRect(x + lw / 2, y + lw / 2, w - lw, h - lw);
  g.fillStyle = C.ink; g.fillRect(x + w, y + h * .3, lw * 2.2, h * .4);
}

export async function load() {
  PKG = await new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = 'assets/package.jpg'; });
}
export function measure() {}

// ====================================================================
// 01 · 0–4.5: the whole frame is a battery at 100 %. It drains to 10 % in five beats; "오늘도 방전?"
const LEVELS = [1, .8, .6, .4, .2, .1];
const level = t => { let v = LEVELS[0]; K.drain.forEach((tc, i) => { v = lerp(v, LEVELS[i + 1], snap(t, tc, E16 * 1.5)); }); return v; };
function sceneDrain(g, t) {
  const lv = level(t), out = snap(t, K.cutA + E8, E8);
  g.fillStyle = C.lime; g.fillRect(0, H * (1 - lv) + out * H * lv, W, H * lv);
  // the percentage: each new value rises in, the old one leaves upward
  const by = 1000, size = 330;
  const k = knife(g, K.cutA, 0, W, by - 120);
  collapse(g, k, by - 120, () => {
    font(g, 900, size); g.fillStyle = C.ink;
    let i = 0; K.drain.forEach(tc => { if (t >= tc - E16 * 1.5) i++; });
    const tc = i ? K.drain[i - 1] : -1, p = i ? snap(t, tc, E16 * 1.5) : 1;
    g.save(); g.beginPath(); g.rect(0, by - 290, W, 340); g.clip();
    if (i && p < 1) g.fillText(`${Math.round(LEVELS[i - 1] * 100)}%`, M, by - p * 320);
    g.fillText(`${Math.round(LEVELS[i] * 100)}%`, M, by + (1 - p) * 320);
    g.restore();
    reg('pct', '100% → 10%', 0, K.cutA, [M, by - 240, 900, 240]);
  });
  say(g, 'empty', '오늘도 방전?', M, 1420, 132, 900, C.ink, K.empty, K.cutA);
  captions(g, 96, .25, K.cutA, '에너지 잔량', '01 / 07', '올리고파');
}

// 02 · 4.5–10.5: split frame, three equal cells = three moments, each with its own small battery at 10 %
const CELLS = [['15:00', '회의 끝난 오후', '직장인'], ['07:00', '운동 시작 전', '운동'], ['22:00', '아이 재운 밤', '육아']];
function sceneCells(g, t) {
  const k = knife(g, K.cutB, 0, W, 980);
  collapse(g, k, 980, () => {
    CELLS.forEach(([hh, s, who], i) => {
      const t0 = K.cells[i], y0 = 200 + i * 580, p = snap(t, t0 + E8, E8 * 2);
      if (p <= 0) return;
      g.fillStyle = C.ink; g.fillRect(M, y0, (W - 2 * M) * p, 2);
      numeral(g, 'cellt' + i, hh, M, y0 + 210, 170, C.ink, t0, t0 + BEAT, 99);
      say(g, 'cell' + i, s, M, y0 + 330, 64, 700, C.ink, t0, 99);
      say(g, 'cellw' + i, who, fx(4), y0 + 50, 28, 500, C.mute, t0 + E8, 99);
      if (t > t0 + BEAT + E8) {
        const r = snap(t, t0 + BEAT + E8 * 2, E8);
        g.save(); g.beginPath(); g.rect(fx(4) - 10, y0 + 380, 400, 190 * r); g.clip();
        battery(g, fx(4), y0 + 390, 250, 100, .1, 5);
        font(g, 700, 34); g.fillStyle = C.ink; g.fillText('10%', fx(4), y0 + 540);
        g.restore();
      }
    });
  });
}

// 03 · 10.5–15.5: the answer. One stick a day; a big battery charges in four steps
function sceneAnswer(g, t) {
  const k = knife(g, K.cutC, 0, W, 960);
  collapse(g, k, 960, () => {
    say(g, 'ans0', '한 잔 더 대신', M, 400, 44, 500, C.mute, K.lead3, 99);
    say(g, 'ans1', '하루 1포', M, 620, 210, 900, C.ink, K.one, 99, { text: '하루 1포 올리고파' });
    say(g, 'ans2', '올리고파', M, 800, 120, 900, C.ink, K.name, 99);
    if (t > K.batt) {
      const r = snap(t, K.batt + E8 * 2, E8 * 2), lv = lerp(.1, 1, steps(t, K.charge[0], K.charge[1], 4));
      g.save(); g.beginPath(); g.rect(0, 1000, W, 460 * r); g.clip();
      battery(g, M, 1040, W - 2 * M - 30, 360, lv, 8);
      font(g, 900, 120); g.fillStyle = C.ink; g.fillText(`${Math.round(lv * 100)}%`, M + 50, 1270);
      g.restore();
    }
    captions(g, 96, K.lead3, 99, '하루 1포', '03 / 07', '15g 스틱');
  });
}

// 04 · 15.5–22: why it works, 1 — the dose. Horizontal grid: 1 column = 250 mg, each bar is its real dose
const MG = 112 / 250;
const ROWS = [['L-아르지닌', '1,000', 1000], ['프락토올리고당', '1,875', 1875], ['수용성마카추출물', '300', 300], ['리치추출분말 (Oligonol®)', '100', 100]];
const rowY = i => 500 + i * 290;
function specSheet(g, t) {
  for (let i = 0; i <= 8; i++) {
    const p = lin(t, K.grid + i * E16, K.grid + i * E16 + E8 * 2);
    if (p > 0) { g.fillStyle = C.grid; g.fillRect(M + i * 112, 450, 1.5, (1690 - 450) * p); }
  }
  font(g, 500, 22); g.fillStyle = C.mute;
  for (let i = 0; i <= 8; i += 2) if (t > K.grid + i * E16 + E8) g.fillText(`${i * 250}`, M + i * 112 + 6, 1720);
  say(g, 'grid-lead', '1포(15g)에 담은 4가지', M, 230, 36, 500, C.mute, K.head, 99);
  say(g, 'grid', '고함량 에너지 부스터', M, 340, 92, 900, C.ink, K.head + E8, 99);
  ROWS.forEach(([name, n, mg], i) => {
    const t0 = K.rows[i], y = rowY(i);
    say(g, 'row' + i, name, M, y, 32, 500, C.mute, i ? t0 - E8 : K.row0Label, 99);
    numeral(g, 'rown' + i, n, M, y + 112, 96, C.ink, t0, t0 + BEAT, 99, n + 'mg');
    font(g, 900, 96); const nw = tw(g, n);
    say(g, 'rowu' + i, 'mg', M + nw + 12, y + 112, 40, 700, C.ink, t0 + BEAT, 99);
    const p = snap(t, t0 + BEAT + E8, E8 * 2);
    if (p > 0) { g.fillStyle = i === 3 ? C.lime : C.ink; g.fillRect(M, y + 140, Math.max(2, mg * MG * p), 72); }
  });
  captions(g, 96, K.grid, 99, '가로 1칸 = 250mg', '04 / 07', '1포 기준');
}
function scenePush(g, t) {     // push into the lime bar until it is the whole frame
  const p = snap(t, K.push, K.pushD), r = [M, rowY(3) + 140, 100 * MG, 72];
  const s = Math.exp(lerp(0, Math.log(Math.max(W / r[2], H / r[3]) * 1.02), p));
  const cx = lerp(W / 2, r[0] + r[2] / 2, Math.min(1, p * 1.6)), cy = lerp(H / 2, r[1] + r[3] / 2, Math.min(1, p * 1.6));
  g.save(); g.translate(W / 2, H / 2); g.scale(s, s); g.translate(-cx, -cy); specSheet(g, t); g.restore();
}

// 05 · 22–30: why it works, 2 — on lime. A big block cut into sixteen small ones, then the 2~8배
function sceneLime(g, t) {
  const wipe = snap(t, K.limeWipe, E8 * 2);
  g.fillStyle = C.lime; g.fillRect(0, 0, W, H * (1 - wipe));
  g.save(); g.beginPath(); g.rect(0, 0, W, H * (1 - wipe)); g.clip();
  captions(g, 96, K.lyc, 99, '리치추출분말', '05 / 07', 'Oligonol®');
  say(g, 'lyc0', '리치추출분말 Oligonol®', M, 250, 40, 700, C.ink, K.lyc, K.limeWipe - E8);
  say(g, 'lyc1', '생체이용률이 높은', M, 370, 92, 900, C.ink, K.lyc + E8, K.limeWipe - E8, { text: '생체이용률이 높은 폴리페놀' });
  say(g, 'lyc2', '폴리페놀', M, 480, 92, 900, C.ink, K.lyc + E8 * 2, K.limeWipe - E8);
  if (t > K.square) {
    const x0 = M, y0 = 600, S = 440, pw = (S - 3 * GU) / 4;
    const p = snap(t, K.square + E8 * 2, E8 * 2);
    g.save(); g.beginPath(); g.rect(0, y0, W, S * p); g.clip();
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
      const d = Math.hypot(c - 1.5, r - 1.5), a = snap(t, K.apart + E8 + Math.round(d) * E16, E8);
      const cell = S / 4, x = x0 + c * lerp(cell, pw + GU, a), y = y0 + r * lerp(cell, pw + GU, a), w = lerp(cell, pw, a), o = a < 1 ? .5 : 0;
      g.fillStyle = C.ink; g.fillRect(x - o, y - o, w + 2 * o, w + 2 * o);
    }
    g.restore();
    for (let i = 0; i < 6; i++) {
      const tc = K.knives + (i + 1) * E16, v = i < 3, k = (i % 3 + 1) * S / 4;
      if (t > tc - E16 && t < K.apart + E8) {
        const L = S * lin(t, tc - E16, tc); g.fillStyle = C.lime;
        if (v) g.fillRect(x0 + k - 2, y0, 4, L); else g.fillRect(x0, y0 + k - 2, L, 4);
      }
    }
    say(g, 'big', '큰 분자', fx(3) + 40, y0 + 60, 44, 700, C.ink, K.label, K.small - E8);
    say(g, 'small', '저분자', fx(3) + 40, y0 + 60, 44, 700, C.ink, K.small, K.limeWipe - E8);
  }
  say(g, 'lead5', '일반 폴리페놀 원료 대비 저분자 폴리페놀', M, 1200, 38, 700, C.ink, K.lead5, K.limeWipe - E8);
  numeral(g, 'big2', '2~8배', M, 1520, 280, C.ink, K.big[0], K.big[1], K.limeWipe - E8);
  say(g, 'foot', '* 원료사 자료 기준 · 시중 일반 폴리페놀 원료와 비교', M, 1780, 26, 500, C.ink, K.foot, K.limeWipe - E8);
  g.restore();
}

// 06 · 30–36: the routine — the taste, fourteen sticks in a 7 × 2 grid, the first one lime
function sceneSticks(g, t) {
  say(g, 'taste', '상큼한 리치맛', M, 420, 128, 900, C.ink, K.taste, K.card - E8);
  captions(g, 96, K.taste, K.card - E8, '구성', '06 / 07', '15g × 14포');
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
  say(g, 'sticks', '15g × 14포', M, 1500, 104, 900, C.ink, K.pack, K.card - E8, { text: '15g × 14포 하루 1포, 2주 루틴' });
  say(g, 'day', '하루 1포, 2주 루틴', M + 14, 1640, 60, 900, C.ink, K.day, K.card - E8, { block: C.lime });
}

// 07 · 36–42: the product on paper, the name, badges, and the call to action on a lime bar
function sceneProduct(g, t) {
  const p = snap(t, K.card + E8 * 2, E8 * 2), cy = 620, ch = 660;
  if (p > 0) {
    g.save(); g.beginPath(); g.rect(M, cy, W - 2 * M, ch * p); g.clip();
    g.fillStyle = C.paper; g.fillRect(M, cy, W - 2 * M, ch);
    if (PKG) { const h = ch - 100, w = h * PKG.width / PKG.height; g.drawImage(PKG, W / 2 - w / 2, cy + 50, w, h); }
    g.restore();
  }
  numeral(g, 'title', '올리고파', M, 500, 230, C.ink, K.title, K.title + BEAT, 99);
  g.fillStyle = C.lime; g.fillRect(M, 546, (W - 2 * M) * lin(t, K.rule, K.rule + E8 * 2), 14);
  say(g, 'tag', '하루 1포로 에너지 UP', M, 1365, 60, 900, C.ink, K.tag, 99);
  captions(g, 1420, K.badges, 99, '의사 공동개발', 'HACCP', 'RAPHAHEAL', C.ink, 30);
  reg('badges', '의사 공동개발 HACCP RAPHAHEAL', K.badges, DUR, [M, 1420, W - 2 * M, 60]);
  // call to action: a lime bar wipes in from the left, black type rises onto it
  const c = snap(t, K.cta + E8 * 2, E8 * 2);
  if (c > 0) { g.fillStyle = C.lime; g.fillRect(0, 1560, W * c, 260); }
  say(g, 'cta0', '지금 만나보세요', M, 1660, 44, 700, C.ink, K.cta + E8, 99, { text: '지금 만나보세요 프로필 링크 클릭' });
  say(g, 'cta1', '프로필 링크 클릭 →', M, 1770, 84, 900, C.ink, K.cta + E8 * 2, 99);
}

export function render(g, t) {
  T = t;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.letterSpacing = '0px';
  g.fillStyle = C.page; g.fillRect(0, 0, W, H);
  if (t < K.cutA + E8 * 2) sceneDrain(g, t);
  if (t >= K.cells[0] && t < K.cutB + E8 * 2) sceneCells(g, t);
  if (t >= K.lead3 && t < K.cutC + E8 * 2) sceneAnswer(g, t);
  if (t >= K.grid && t < K.push - K.pushD) specSheet(g, t);
  else if (t >= K.push - K.pushD && t < K.push) scenePush(g, t);
  if (t >= K.push && t < K.limeWipe + E8) sceneLime(g, t);
  if (t >= K.limeWipe - E8 * 2 && t < K.card + E8 * 2) {
    g.save(); if (t < K.limeWipe + E8) { g.beginPath(); g.rect(0, H * (1 - snap(t, K.limeWipe, E8 * 2)), W, H); g.clip(); }
    sceneSticks(g, t); g.restore();
  }
  if (t >= K.card) sceneProduct(g, t);
}
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }

// sound events: print foley only (no music)
export function events() {
  const ev = [{ t: 0, type: 'thump' }];
  K.drain.forEach((tc, i) => ev.push({ t: tc, type: 'thunk', g: 1 - i * .12 }));
  [K.cutA, K.cutB, K.cutC].forEach(t => ev.push({ t, type: 'knife' }));
  K.cells.forEach(t0 => { ev.push({ t: t0 + E8, type: 'paper' }); [.25, .5, .75, 1].forEach(u => ev.push({ t: t0 + BEAT * u, type: 'tick' })); ev.push({ t: t0 + BEAT + E8 * 2, type: 'snap' }); });
  ev.push({ t: K.batt + E8 * 2, type: 'paper' });
  [.25, .5, .75, 1].forEach((u, i) => ev.push({ t: lerp(K.charge[0], K.charge[1], u), type: i === 3 ? 'snapHero' : 'snap' }));
  for (let i = 0; i <= 8; i++) ev.push({ t: K.grid + i * E16 + E8, type: 'rule' });
  K.rows.forEach((t0, i) => { [.25, .5, .75, 1].forEach(u => ev.push({ t: t0 + BEAT * u, type: 'tick' })); ev.push({ t: t0 + BEAT + E8, type: i === 3 ? 'snapHero' : 'snap' }); });
  ev.push({ t: K.push, type: 'swish', d: K.pushD }, { t: K.push, type: 'paper' }, { t: K.square + E8 * 2, type: 'thump' });
  for (let i = 0; i < 6; i++) ev.push({ t: K.knives + (i + 1) * E16, type: 'knife' });
  for (let d = 0; d < 3; d++) ev.push({ t: K.apart + E8 + d * E16, type: 'snap' });
  [.25, .5, .75, 1].forEach(u => ev.push({ t: lerp(K.big[0], K.big[1], u), type: 'thunk' }));
  ev.push({ t: K.limeWipe, type: 'paper' });
  for (let i = 0; i < 14; i++) ev.push({ t: K.sticks + (i + 1) * E16, type: i ? 'snap' : 'snapHero' });
  ev.push({ t: K.card + E8 * 2, type: 'paper' });
  [.25, .5, .75, 1].forEach(u => ev.push({ t: lerp(K.title, K.title + BEAT, u), type: 'thunk' }));
  ev.push({ t: K.rule + E8 * 2, type: 'rule' }, { t: K.badges + E8 * 2, type: 'stamp' }, { t: K.cta + E8 * 2, type: 'slide' }, { t: K.cta + E8 * 4, type: 'thump' });
  for (const w of WORDS) ev.push({ t: w.t, type: w.big ? 'clackBig' : 'clack' });
  return ev.sort((a, b) => a.t - b.t);
}
