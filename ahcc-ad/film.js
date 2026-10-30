// 라파힐 AHCC — 30 s portrait ad in the Swiss Motion Graphics style. Built from the brand's detail page only (FACTS.md).
// Paper, ink, greys and one signal colour (the brand's navy). Every element snaps to a 6-column grid on a 120 bpm beat;
// entrances are clip-reveals, deletions are knife cuts. Narration comes later; the cards leave room for it.
import { lerp, snap, lin, steps, E8, E16, BEAT } from './ease.js';

export const W = 1080, H = 1920, DUR = 30;
export const C = { page: '#F3F3F6', paper: '#FFFFFF', ink: '#111111', grid: '#D8D9E0', mute: '#6F7180', navy: '#2B2E8F', soft: '#C9CBE6' };
const M = 72, CW = 136, GU = 24;
const fx = i => M + i * (CW + GU);
const FAM = 'NotoKR';

// ---------- edit list (seconds) ----------
export const SC = [
  { id: 'hook', t0: 0, t1: 3.75 }, { id: 'who', t0: 3.75, t1: 8.0 }, { id: 'prod', t0: 8.0, t1: 12.5 }, { id: 'trial', t0: 12.5, t1: 17.5 },
  { id: 'trust', t0: 17.5, t1: 22.5 }, { id: 'check', t0: 22.5, t1: 26.25 }, { id: 'end', t0: 26.25, t1: 30 },
];
export const K = { cuts: [.5, .85, 1.2], cells: [4.0, 4.15, 4.3], rows: [12.75, 13.6], count: [17.75, 18.5], checks: [22.75, 22.95, 23.15], cta: 26.3, note: 22.5 };

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
export async function load() {
  PKG = await new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = 'assets/product.jpg'; });
}
const navyBlock = (g, x, y, w, h) => { g.fillStyle = C.navy; g.fillRect(x, y, w, h); };
function arrowUp(g, x, y, s, col) { g.fillStyle = col; g.fillRect(x - s * .12, y - s * .2, s * .24, s * .7); g.beginPath(); g.moveTo(x - s * .38, y - s * .1); g.lineTo(x + s * .38, y - s * .1); g.lineTo(x, y - s * .55); g.closePath(); g.fill(); }
function check(g, x, y, r, p, col = C.navy) {
  if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p);
  g.fillStyle = col; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill();
  g.strokeStyle = C.paper; g.lineWidth = r * .22; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(-r * .42, 0); g.lineTo(-r * .1, r * .32); g.lineTo(r * .45, -r * .32); g.stroke(); g.restore();
}
function product(g, y, w) {          // the product photograph on a white sheet
  if (!PKG) return; const h = w * PKG.height / PKG.width;
  g.fillStyle = C.paper; g.fillRect(M, y, W - 2 * M, h + 80); g.drawImage(PKG, W / 2 - w / 2, y + 40, w, h);
}

// ====================================================================
// 01 · 0–3.5: "면역이 기본이다". Four navy blocks; drinking, smoking and stress each knife one out
const FACTORS = ['음주', '흡연', '스트레스'];
function sceneHook(g, t, s) {
  say(g, 'h1', '면역이 기본이다', M, 360, 128, 900, C.ink, -.4, s.t1, { text: '면역이 기본이다' });
  captions(g, 96, .1, s.t1, '라파힐 AHCC', '01 / 07', '면역 이야기');
  const bw = W - 2 * M, bh = 200, y0 = 560;
  for (let i = 0; i < 4; i++) {
    const y = y0 + i * (bh + GU), k = i < 3 ? knife(g, K.cuts[i], M, M + bw, y + bh / 2, C.ink) : 1;
    collapse(g, k, y + bh / 2, () => { navyBlock(g, M, y, bw, bh); font(g, 900, 64); g.fillStyle = C.paper; g.fillText(i < 3 ? '면역' : '면역', M + 36, y + bh / 2 + 22); });
    if (i < 3) say(g, 'f' + i, FACTORS[i], M, y + bh / 2 + 34, 96, 900, C.navy, K.cuts[i] + E8, s.t1);
  }
}
// 02 · 3.5–8: three cells, three people (the detail page's own list)
const WHO = [['01', '과다한 업무와 사회생활'], ['02', '체력이 떨어지는 노년층'], ['03', '스트레스를 많이 받는 분']];
function sceneWho(g, t, s) {
  captions(g, 96, s.t0, s.t1, '이런 분들께', '02 / 07', '권해드립니다');
  say(g, 'w0', '이런 분들께', M, 330, 110, 900, C.ink, s.t0 + .05, s.t1);
  WHO.forEach(([n, txt], i) => {
    const t0 = K.cells[i], y = 480 + i * 430, p = snap(t, t0 + E8, E8 * 2);
    if (p <= 0) return;
    g.fillStyle = C.ink; g.fillRect(M, y, (W - 2 * M) * p, 2);
    numeral(g, 'wn' + i, n, M, y + 190, 150, C.navy, t0, t0 + BEAT, 99);
    say(g, 'wt' + i, txt, M, y + 300, 58, 800, C.ink, t0 + E8, s.t1);
  });
}
// 03 · 8–12.5: the answer. The product, its ingredient, its one approved function
function sceneProd(g, t, s) {
  captions(g, 96, s.t0, s.t1, '건강기능식품', '03 / 07', '식약처 개별인정');
  const p = snap(t, s.t0 + E8 * 3, E8 * 3);
  g.save(); g.beginPath(); g.rect(0, 250, W, 500 * p); g.clip(); product(g, 260, 860); g.restore();
  say(g, 'p1', '라파힐 AHCC', M, 900, 120, 900, C.ink, s.t0 + .25, s.t1);
  say(g, 'p2', '표고버섯균사체 AHCC', M, 990, 52, 700, C.mute, s.t0 + .4, s.t1);
  say(g, 'p3', '면역기능 증진에 도움을 줄 수 있음', M + 18, 1180, 60, 900, C.paper, s.t0 + .5, s.t1, { block: C.navy });
  say(g, 'p4', '식약처 개별인정 제2008-78호', M, 1310, 44, 700, C.ink, s.t0 + .7, s.t1);
}
// 04 · 12.5–17.5: the human trials, as on the detail page
const ROWS = [
  ['수지상세포 증가', '면역반응을 담당하는 세포 · 인체시험', 'Nutrition and Cancer 60(5), 2008'],
  ['NK세포 활성', 'IL-12 · IFN-γ 증가 · 인체시험', 'Biotherapy 14(3), 2000'],
];
function sceneTrial(g, t, s) {
  captions(g, 96, s.t0, s.t1, '인체적용시험', '04 / 07', '확인 내용');
  say(g, 't0', '인체시험으로 확인', M, 330, 104, 900, C.ink, s.t0 + .05, s.t1);
  ROWS.forEach(([a, b, src], i) => {
    const t0 = K.rows[i], y = 470 + i * 620; if (t < t0 - E16) return;
    g.fillStyle = C.ink; g.fillRect(M, y, (W - 2 * M) * snap(t, t0 + E8, E8 * 2), 2);
    // concept bars: before (grey) and after (navy) — a schematic, the measured plots are in the cited papers
    const bx = W - M - 300, base = y + 470, p1 = snap(t, t0 + E8 * 2, E8 * 2), p2 = snap(t, t0 + E8 * 4, E8 * 3);
    g.fillStyle = C.grid; g.fillRect(bx, base - 200 * p1, 120, 200 * p1);
    g.fillStyle = C.navy; g.fillRect(bx + 160, base - 330 * p2, 120, 330 * p2);
    if (p2 > .9) arrowUp(g, bx + 220, base - 360, 90, C.navy);
    font(g, 700, 28); g.fillStyle = C.mute; if (p1 > 0) g.fillText('전', bx + 46, base + 40); if (p2 > 0) g.fillText('후', bx + 206, base + 40);
    font(g, 500, 20); if (p2 > 0) g.fillText('개념도', bx, base + 80);
    say(g, 'ta' + i, a, M, y + 130, 84, 900, C.ink, t0, s.t1);
    say(g, 'tb' + i, b, M, y + 200, 32, 600, C.mute, t0 + E8, s.t1);
    say(g, 'tc' + i, src, M, y + 520, 24, 500, C.mute, t0 + E8 * 2, s.t1);
  });
}
// 05 · 17.5–22.5: trust. 24 years, the approvals, the conference and the awards
function sceneTrust(g, t, s) {
  captions(g, 96, s.t0, s.t1, '라파힐 스토리', '05 / 07', '(주)KCFKOREA');
  const n = Math.round(24 * steps(t, K.count[0], K.count[1], 6));
  if (t >= K.count[0]) { font(g, 900, 420); g.fillStyle = C.navy; g.fillText(String(n), M - 10, 700); font(g, 900, 120); g.fillStyle = C.ink; g.fillText('년', M + (n >= 10 ? 470 : 250), 700); }
  reg('cnt', '24년', K.count[0], s.t1, [M, 400, 700, 300]);
  say(g, 'r1', 'AHCC 국내 최초 소개 · 24년 정식 유통', M, 820, 46, 800, C.ink, K.count[0] + .25, s.t1);
  [['식약처 개별인정', '3건 · 제2008-78호 등'], ['국제학회 ICNIM', '기초·임상 연구 발표'], ['해외 수상', '2002 · 2004 · 2007']].forEach(([a, b], i) => {
    const t0 = K.count[1] + .1 + i * .4, y = 1000 + i * 230;
    if (t >= t0) { g.fillStyle = C.ink; g.fillRect(M, y - 70, (W - 2 * M) * snap(t, t0 + E8, E8 * 2), 2); }
    say(g, 'ra' + i, a, M, y, 56, 900, C.navy, t0, s.t1);
    say(g, 'rb' + i, b, M, y + 70, 38, 600, C.ink, t0 + E8, s.t1);
  });
}
// 06 · 22.5–26: check three marks before you buy
const MARKS = ['건강기능식품', '식품이력추적관리', 'GMP'];
function sceneCheck(g, t, s) {
  captions(g, 96, s.t0, s.t1, 'CHECK', '06 / 07', '구매 전 확인');
  say(g, 'c0', '꼭 확인하세요', M, 330, 120, 900, C.ink, s.t0 + .05, s.t1);
  MARKS.forEach((m, i) => {
    const t0 = K.checks[i], y = 560 + i * 300;
    if (t >= t0 - E16) { g.fillStyle = C.ink; g.fillRect(M, y - 120, (W - 2 * M) * snap(t, t0, E8 * 2), 2); }
    check(g, M + 70, y - 22, 66, Math.min(1, snap(t, t0 + E8, E8) * 1.1));
    say(g, 'cm' + i, m + ' 마크', M + 170, y, 72, 900, C.ink, t0, s.t1);
  });
}
// 07 · 26–30: the product, the maker, the call to action
function sceneEnd(g, t, s) {
  captions(g, 96, s.t0, s.t1, '라파힐 AHCC', '07 / 07', '(주)KCFKOREA');
  const p = snap(t, s.t0 + E8 * 3, E8 * 3);
  g.save(); g.beginPath(); g.rect(0, 250, W, 500 * p); g.clip(); product(g, 260, 860); g.restore();
  say(g, 'e1', '라파힐 AHCC', M, 900, 140, 900, C.navy, s.t0 + .2, DUR);
  const c = snap(t, K.cta + E8, E8);
  if (c > 0) { g.fillStyle = C.navy; g.fillRect(0, 1180, W * c, 240); }
  say(g, 'e3', '프로필 링크에서', M, 1280, 56, 700, C.paper, K.cta, DUR, { text: '프로필 링크에서 만나보세요 →' });
  say(g, 'e4', '만나보세요 →', M, 1380, 84, 900, C.paper, K.cta + E8, DUR);
}
const DRAW = { hook: sceneHook, who: sceneWho, prod: sceneProd, trial: sceneTrial, trust: sceneTrust, check: sceneCheck, end: sceneEnd };

export function render(g, t) {
  T = t;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.letterSpacing = '0px';
  g.fillStyle = C.page; g.fillRect(0, 0, W, H);
  const i = Math.max(0, SC.findIndex(s => t < s.t1)) , s = SC[i < 0 ? SC.length - 1 : i];
  // the outgoing card is knifed across the middle on the cut; the new one builds over the page
  const prev = SC[SC.indexOf(s) - 1];
  if (prev && t < s.t0 + E8 * 2) { const k = knife(g, s.t0, 0, W, 960); collapse(g, k, 960, () => DRAW[prev.id](g, t, prev)); }
  DRAW[s.id](g, t, s);
  // the detail page's own caveat, held under the last two cards
  say(g, 'note', '※ 시험결과가 모든 사람에게 동일하게 나타나는 것은 아닙니다.', M, 1800, 26, 500, C.mute, K.note, DUR);
}
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }

// sound events (print foley + score accents)
export function events() {
  const ev = SC.map((s, i) => ({ t: s.t0, type: i ? 'cut' : 'start', i }));
  K.cuts.forEach(t => ev.push({ t, type: 'knife' }));
  K.cells.forEach(t => [.25, .5, .75, 1].forEach(u => ev.push({ t: t + BEAT * u, type: 'thunk' })));
  ev.push({ t: 8.0 + E8 * 3, type: 'paper' }, { t: 8.5, type: 'stamp' });
  K.rows.forEach(t => ev.push({ t: t + E8 * 2, type: 'snap' }, { t: t + E8 * 4, type: 'snapHero' }));
  for (let k = 1; k <= 6; k++) ev.push({ t: lerp(K.count[0], K.count[1], k / 6), type: 'thunk' });
  K.checks.forEach(t => ev.push({ t: t + E8, type: 'stamp' }));
  ev.push({ t: 26.25 + E8 * 3, type: 'paper' }, { t: K.cta + E8 * 2, type: 'slide' }, { t: K.cta + E8 * 4, type: 'thump' });
  for (const w of WORDS) ev.push({ t: w.t, type: w.big ? 'clackBig' : 'clack' });
  return ev.filter(e => e.t >= 0).sort((a, b) => a.t - b.t);
}
