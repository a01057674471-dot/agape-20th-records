// 라파힐 AHCC — value cut. 30 s portrait ad, Swiss Motion Graphics, built only from the brand's detail page (FACTS.md).
// The viewer gets a way to choose: three things to check in any immune product. The product then passes each one
// (a stamp lands on every criterion), and the verdict puts all three on one card. Navy and paper cards alternate;
// big type, beat-locked cuts and stamps carry the impact. Cut to the user's narration (tools/voice.py → voices/times.js).
import { lerp, snap, lin, steps, E8, E16, BEAT } from './ease.js';
import { DUR as VDUR, CARD_T0, V } from './voices/times.js';

export const W = 1080, H = 1920, DUR = VDUR;
const at = id => V[id][0];
export const C = { page: '#F3F3F6', paper: '#FFFFFF', ink: '#111111', grid: '#D8D9E0', mute: '#6F7180', navy: '#2B2E8F', soft: '#AEB2E6', deep: '#1E2170' };
const M = 72, CW = 136, GU = 24;
const fx = i => M + i * (CW + GU);
const FAM = 'NotoKR';

// ---------- edit list (seconds) ----------
const ORDER = [['hook', 'navy'], ['three', 'page'], ['c1', 'navy'], ['c2', 'page'], ['c3', 'navy'], ['verdict', 'page'], ['end', 'navy']];
export const SC = ORDER.map(([id, bg], i) => ({ id, bg, t0: CARD_T0[id], t1: i + 1 < ORDER.length ? CARD_T0[ORDER[i + 1][0]] : DUR }));
// every answer lands with its phrase: the stamp on the product's answer, the count during the question, the name on its word
const VT = CARD_T0.verdict;
export const K = { stamp: { c1: at('v06'), c2: at('v10'), c3: at('v13') }, rows: [VT + .05, VT + .2, VT + .35], name: at('v16') - .1, marks: VT + .2, cta: CARD_T0.end + .3, note: CARD_T0.c2 };

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
const onNavy = s => s.bg === 'navy';
const fg = s => onNavy(s) ? C.paper : C.ink;
const acc = s => onNavy(s) ? C.soft : C.navy;
// the stamp: a ring with a tick lands big and settles (one overshoot is allowed only here: it is the film's exception)
function stamp(g, x, y, r, t, t0, col, ink) {
  if (t < t0) return;
  const u = clamp01((t - t0) / .22), s = u < 1 ? lerp(1.9, 1, u * u) : 1, rot = -.18;
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s); g.globalAlpha = Math.min(1, u * 2);
  g.fillStyle = col; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill();
  g.strokeStyle = ink; g.lineWidth = r * .18; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(-r * .42, 0); g.lineTo(-r * .1, r * .32); g.lineTo(r * .45, -r * .34); g.stroke();
  g.restore();
}
const clamp01 = x => Math.max(0, Math.min(1, x));
function product(g, y, w, bgCol = C.paper) {
  if (!PKG) return; const h = w * PKG.height / PKG.width;
  g.fillStyle = bgCol; g.fillRect(M, y, W - 2 * M, h + 80); g.drawImage(PKG, W / 2 - w / 2, y + 40, w, h);
}

// ====================================================================
// 01 · 0–3.25: twelve identical boxes all say 면역. The question.
function sceneHook(g, t, s) {
  say(g, 'h1', '면역 제품,', M, 330, 140, 900, C.paper, -.45, s.t1, { text: '면역 제품, 뭘 보고 고르세요?' });
  say(g, 'h2', '뭘 보고 고르세요?', M, 490, 120, 900, C.soft, -.3, s.t1);
  const cols = 3, bw = (W - 2 * M - 2 * GU) / cols, bh = 220;
  for (let i = 0; i < 12; i++) {
    const r = Math.floor(i / cols), c = i % cols, x = M + c * (bw + GU), y = 640 + r * (bh + GU);
    const p = snap(t, .1 + i * E16 * .5, E16);
    if (p <= 0) continue;
    g.save(); g.beginPath(); g.rect(x, y + bh * (1 - p), bw, bh * p); g.clip();
    g.fillStyle = C.deep; g.fillRect(x, y, bw, bh);
    font(g, 900, 54); g.fillStyle = 'rgba(255,255,255,.55)'; g.fillText('면역', x + 28, y + bh - 34);
    font(g, 600, 22); g.fillStyle = 'rgba(255,255,255,.35)'; g.fillText(['?', '??', '?'][i % 3], x + bw - 50, y + 46);
    g.restore();
  }
  captions(g, 96, .1, s.t1, '라파힐 AHCC', '01 / 07', '고르는 법', C.paper);
}
// 02 · 3.25–6: a giant 3
function sceneThree(g, t, s) {
  numeral(g, 'n3', '3', M - 20, 1020, 820, C.navy, s.t0, s.t0 + BEAT, s.t1, '3');
  say(g, 't1', '가지만 확인하세요', M, 1200, 104, 900, C.ink, s.t0, s.t1);
  captions(g, 96, s.t0, s.t1, '고르는 기준', '02 / 07', '3가지', C.ink);
}
// 03–05: one criterion per card: the criterion, then the product's answer with a stamp
const CRIT = {
  c1: { n: '01', title: ['식약처가 인정한', '기능성인가?'], ans: ['식약처 개별인정 제2008-78호', '면역기능 증진에 도움을 줄 수 있음'], cap: '기능성' },
  c2: { n: '02', title: ['사람에게서', '확인됐는가?'], ans: ['인체시험으로 확인', '수지상세포 증가 · NK세포 활성'], src: 'Nutrition and Cancer 2008 · Biotherapy 2000', cap: '인체시험' },
  c3: { n: '03', title: ['오래 검증된', '원료인가?'], ans: ['오래된 데는 이유가 있다', '1980년대 개발 · 30년 넘는 연구'], cap: '검증' },
};
function sceneCrit(g, t, s) {
  const c = CRIT[s.id], st = K.stamp[s.id], F = fg(s), A = acc(s);
  captions(g, 96, s.t0, s.t1, `기준 ${c.n}`, `${Number(c.n) + 2} / 07`, c.cap, F);
  numeral(g, 'cn' + s.id, c.n, M - 6, 470, 300, A, s.t0, s.t0 + BEAT, s.t1, c.n);
  say(g, 'ct' + s.id, c.title[0], M, 640, 110, 900, F, s.t0 + .2, s.t1, { text: c.title.join(' ') });
  say(g, 'cu' + s.id, c.title[1], M, 780, 110, 900, F, s.t0 + .35, s.t1);
  if (s.id === 'c3') {      // the years, counted up to "30년+" (AHCC was developed in Japan in the late 1980s: 1987 or 1989 by source)
    const n = Math.round(30 * steps(t, st - 1.0, st - .25, 6));
    if (t >= st - 1.0) { font(g, 900, 300); g.fillStyle = A; g.fillText(String(n), M - 10, 1120); font(g, 900, 90); g.fillStyle = F; g.fillText(n >= 30 ? '년+' : '년', M + (n >= 10 ? 340 : 180), 1120); }
    reg('c3n', '30년+', st - 1.0, s.t1, [M, 880, 600, 260]);
  }
  // the answer panel
  const y = s.id === 'c3' ? 1200 : 960, p = snap(t, st - E8, E8 * 2);
  if (p > 0) { g.fillStyle = onNavy(s) ? C.paper : C.navy; g.fillRect(M, y, (W - 2 * M) * p, 360); }
  const AF = onNavy(s) ? C.navy : C.paper, AS = onNavy(s) ? C.ink : C.paper;
  say(g, 'ca' + s.id, c.ans[0], M + 40, y + 130, 48, 900, AF, st, s.t1);
  say(g, 'cb' + s.id, c.ans[1], M + 40, y + 200, 40, 700, AS, st, s.t1);
  font(g, 700, 30); if (t > st) { g.fillStyle = AF; g.fillText('라파힐 AHCC', M + 40, y + 300); }
  stamp(g, W - M - 60, y - 6, 78, t, st + E8 * 2, onNavy(s) ? C.navy : C.paper, onNavy(s) ? C.paper : C.navy);
  if (c.src) say(g, 'cs' + s.id, c.src, M, y + 420, 24, 500, C.mute, s.t0 + .5, s.t1);
}
// 06 · 19.75–25.25: the verdict — three ticks, one name, the product, the three marks
function sceneVerdict(g, t, s) {
  captions(g, 96, s.t0, s.t1, '결론', '06 / 07', '3가지 모두', C.ink);
  ['식약처 인정 기능성', '인체시험 근거', '30년 넘게 연구된 원료'].forEach((txt, i) => {
    const t0 = K.rows[i], y = 300 + i * 120;
    stamp(g, M + 40, y - 18, 38, t, t0, C.navy, C.paper);
    say(g, 'vr' + i, txt, M + 110, y, 60, 900, C.ink, t0, s.t1);
  });
  say(g, 'vn', '3가지 모두,', M, 800, 72, 900, C.mute, s.t0 + .05, s.t1, { text: '3가지 모두, 라파힐 AHCC' });
  say(g, 'vn2', '라파힐 AHCC', M, 950, 150, 900, C.navy, K.name, s.t1);
  const p = snap(t, K.name + E8 * 2, E8 * 2);
  g.save(); g.beginPath(); g.rect(0, 1010, W, 440 * p); g.clip(); product(g, 1030, 860); g.restore();
}
// 07 · 25.25–30: the value line and the call to action
function sceneEnd(g, t, s) {
  captions(g, 96, s.t0, s.t1, '라파힐 AHCC', '07 / 07', '(주)KCFKOREA', C.paper);
  say(g, 'e1', '면역의 기본,', M, 420, 130, 900, C.paper, s.t0 + .05, DUR, { text: '면역의 기본, 근거로 고르세요' });
  say(g, 'e2', '근거로 고르세요', M, 580, 130, 900, C.soft, s.t0 + .2, DUR);
  say(g, 'e3', '라파힐 AHCC', M, 800, 84, 900, C.paper, s.t0 + .45, DUR);
  const c = snap(t, K.cta + E8, E8);
  if (c > 0) { g.fillStyle = C.paper; g.fillRect(0, 1060, W * c, 230); }
  say(g, 'e4', '프로필 링크에서', M, 1150, 52, 700, C.navy, K.cta, DUR, { text: '프로필 링크에서 만나보세요 →' });
  say(g, 'e5', '만나보세요 →', M, 1250, 84, 900, C.navy, K.cta + E8, DUR);
}
const DRAW = { hook: sceneHook, three: sceneThree, c1: sceneCrit, c2: sceneCrit, c3: sceneCrit, verdict: sceneVerdict, end: sceneEnd };
const BG = { navy: C.navy, page: C.page };

export function render(g, t) {
  T = t;
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.letterSpacing = '0px';
  let i = SC.findIndex(s => t < s.t1); if (i < 0) i = SC.length - 1;
  const s = SC[i], prev = SC[i - 1];
  // cut: the new card's colour wipes up from the bottom in an eighth note, over the old card
  if (prev && t < s.t0 + E8) {
    g.fillStyle = BG[prev.bg]; g.fillRect(0, 0, W, H); DRAW[prev.id](g, t, prev);
    const p = snap(t, s.t0 + E8, E8); g.save(); g.beginPath(); g.rect(0, H * (1 - p), W, H * p); g.clip();
    g.fillStyle = BG[s.bg]; g.fillRect(0, 0, W, H); DRAW[s.id](g, t, s); g.restore();
  } else { g.fillStyle = BG[s.bg]; g.fillRect(0, 0, W, H); DRAW[s.id](g, t, s); }
  // the detail page's own caveat, from the human trials to the end
  if (t >= K.note) say(g, 'note', '※ 시험결과가 모든 사람에게 동일하게 나타나는 것은 아닙니다.', M, 1820, 24, 500, onNavy(s) ? C.soft : C.mute, K.note, DUR);
}
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }

export function events() {
  const ev = SC.map((s, i) => ({ t: s.t0, type: i ? 'cut' : 'start', i, bg: s.bg }));
  for (let i = 0; i < 12; i++) ev.push({ t: .1 + i * E16 * .5 + E16, type: 'tick' });
  [.25, .5, .75, 1].forEach(u => ev.push({ t: CARD_T0.three + BEAT * u, type: 'thunk' }));
  Object.values(K.stamp).forEach(t => ev.push({ t: t + E8 * 2, type: 'stampHit' }, { t: t - E8, type: 'slide' }));
  for (let k = 1; k <= 6; k++) ev.push({ t: lerp(K.stamp.c3 - 1.0, K.stamp.c3 - .25, k / 6), type: 'thunk' });
  K.rows.forEach(t => ev.push({ t, type: 'stampSmall' }));
  ev.push({ t: K.name, type: 'boom' }, { t: K.name + E8 * 2, type: 'paper' }, { t: K.cta + E8, type: 'slide' });
  for (const w of WORDS) ev.push({ t: w.t, type: w.big ? 'clackBig' : 'clack' });
  return ev.filter(e => e.t >= 0).sort((a, b) => a.t - b.t);
}
