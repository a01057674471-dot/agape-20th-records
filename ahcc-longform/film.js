// 면역과 AHCC, 확인된 사실만 — a ~5 min 16:9 film in the Data Storytelling style, for the brand's YouTube channel.
// One sheet of cream paper, a red–blue pencil, and only numbers that have a source (FACTS.md): a waffle of 100 white
// blood cells, the NK share of lymphocytes, the 74 % oligosaccharide share of AHCC, a timeline, the one approved function.
// No disease claims: the cancer question is answered once, as a line drawn under what a health functional food is not.
// The clock is voices/times.js (estimated until the narration is recorded; tools/timeline.py).
import * as E from './engine.js';
import { clamp, lerp } from '/core/lib.js';
import { DUR as TDUR, SCENE_T0 as S, V } from './voices/times.js';
const { P } = E;
export const W = 1920, H = 1080, DUR = TDUR;
const at = id => V[id][0], end = id => V[id][1];
const HAND = 'Gaegu', SERIF = "'Noto Serif KR'", MONO = "'IBM Plex Mono', 'Noto Serif KR'";
const AMBER = '#C98B2B';
const ease = x => (x = clamp(x), x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const pr = (t, t0, d) => clamp((t - t0) / d);

// ---------- registries: texts (reading check), sound events, the pencil's current tip ----------
const TXT = [], EVS = [];
let TIP = null;
const PT = [];          // the pencil's track: [t, tip] at every pre-render step where something was being drawn (deterministic)
const reg = (id, text, t0, t1, box) => { if (!TXT.some(x => x.id === id)) TXT.push({ id, text, t0, t1, box }); };
const evOnce = new Set();
const ev = (key, e) => { if (!evOnce.has(key)) { evOnce.add(key); EVS.push(e); } };
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }
function track(tip, p, t) { if (p > 0 && p < 1 && tip) TIP = tip; }
// handwriting: written on over `d` seconds from t0
function hand(g, id, s, x, y, t, t0, o = {}) {
  const d = o.d ?? Math.max(.5, s.length * .07);
  ev('w' + id, { t: t0, type: 'write', d });
  const p = pr(t, t0, d); if (p <= 0) return;
  const r = E.handText(g, s, x, y, { size: o.size || 38, color: o.color || P.blue, progress: p, font: HAND, weight: o.weight || 700, align: o.align || 'left', zoom: CAM.zoom });
  track(r.tip, p, t);
}
function line(g, key, pts, t, t0, d, o = {}) {
  ev('l' + key, { t: t0, type: o.rule ? 'rule' : 'stroke', d });
  const p = pr(t, t0, d); if (p <= 0) return;
  track(E.pencilStroke(g, pts, { width: o.width || 2, color: o.color || P.graphite, progress: p, seed: o.seed || key.length, wobble: o.wobble ?? .5, passes: o.passes || 2 }), p, t);
}
function type(g, s, x, y, t, t0, o = {}) {
  const p = pr(t, t0, o.d || .6); if (p <= 0) return;
  E.setType(g, s, x, y, { size: o.size || 20, font: o.font || MONO, weight: o.weight || 400, color: o.color || P.inkSoft, progress: p, align: o.align || 'left' });
}

// ---------- the camera: one take over the sheet ----------
const HOOK = [0, 0], IMM = [2600, 0], AH = [5200, 0], HIST = [2600, 1500], KOR = [5200, 1500], QA = [0, 1500];
const LYM = [2600 - 30, 40];        // centre of the lymphocyte rows in the waffle
const KEYS = [
  [0, HOOK[0], HOOK[1], 1, 0],
  [S.immune + 1.2, IMM[0], IMM[1], .92, 1.6], [at('l06') + .2, LYM[0] + 260, LYM[1] + 30, 1.3, 1.4], [at('l08') + .3, IMM[0] + 330, IMM[1] - 40, 1.25, 1.2],
  [at('l09') + .3, IMM[0], IMM[1] + 160, .88, 1.3], [at('l11'), IMM[0], IMM[1] + 60, .92, 1],
  [S.ahcc + 1.2, AH[0] - 560, AH[1] + 60, 1.25, 1.6], [at('l13') + .2, AH[0] - 380, AH[1] + 240, 1.05, 1.2], [at('l14'), AH[0] + 330, AH[1], 1.15, 1.2],
  [at('l15'), AH[0], AH[1] + 40, .9, 1.2],
  [S.history + 1.2, HIST[0] - 500, HIST[1], 1.05, 1.6], [at('l18'), HIST[0], HIST[1], .85, 1.6], [at('l19'), HIST[0], HIST[1] + 60, .85, 1.2],
  [S.korea + 1.2, KOR[0] - 200, KOR[1], 1.05, 1.6], [at('l21'), KOR[0] + 120, KOR[1] + 40, .95, 1.2], [at('l23'), KOR[0] + 80, KOR[1] + 240, 1.05, 1.2],
  [S.qa + 1.2, QA[0], QA[1] - 330, 1.1, 1.6], [at('l26'), QA[0], QA[1] - 160, 1.1, 1.0], [at('l27'), QA[0], QA[1] + 20, 1.1, 1.0],
  [at('l27b'), QA[0], QA[1] + 190, 1.1, 1.0], [at('l28'), QA[0], QA[1] + 330, 1.1, 1.0],
  [S.end + .8, HOOK[0], HOOK[1], 1, 1.8],
];
let CAM = { x: 0, y: 0, zoom: 1, roll: 0 };
function camAt(t) {
  let c = { x: KEYS[0][1], y: KEYS[0][2], zoom: KEYS[0][3], roll: 0 };
  for (let i = 1; i < KEYS.length; i++) {
    const [ta, x, y, z, d] = KEYS[i]; if (t < ta - d) break;
    const u = ease(pr(t, ta - d, d)), lz = Math.exp(lerp(Math.log(c.zoom), Math.log(z), u));
    c = { x: lerp(c.x, x, u), y: lerp(c.y, y, u), zoom: lz, roll: 0 };
  }
  c.roll = Math.sin(t * .23) * .004;                 // the hand-held sheet breathes a little
  return c;
}

// ====================================================================
// HOOK — an empty plot with one handwritten question; the film ends by revising it
function hook(g, t) {
  const [x, y] = HOOK;
  type(g, '면역과 AHCC, 확인된 사실만', x - 700, y - 400, t, .2, { size: 54, font: SERIF, weight: 700, color: P.ink, d: 1.2 });
  reg('title', '면역과 AHCC, 확인된 사실만', .2, S.immune, [x - 700, y - 450, 900, 60]);
  type(g, 'RAPHAHEAL · 정보 영상', x - 700, y - 350, t, .8, { size: 18 });
  line(g, 'box', [[x - 700, y - 300], [x + 700, y - 300], [x + 700, y + 320], [x - 700, y + 320], [x - 700, y - 300]], t, .4, 1.4, { width: 1.6, rule: true });
  const strike = S.end + 1.4;
  hand(g, 'q', '면역?', x, y + 60, t, at('l01') + .2, { size: 170, color: t > strike ? P.inkSoft : P.red, align: 'center', d: .9 });
  reg('q', '면역?', at('l01') + .2, S.immune, [x - 160, y - 90, 320, 170]);
  hand(g, 'q2', 'AHCC는?', x + 360, y - 170, t, at('l02') + 1.2, { size: 56, color: P.blue, d: .6 });
  E.leader(g, [x + 350, y - 180], [x + 180, y - 40], { progress: pr(t, at('l02') + 1.8, .4), color: P.blue });
  hand(g, 'q3', '과장 ✕   사실 ○', x - 610, y + 270, t, at('l03') + .6, { size: 44, color: P.blue, d: .9 });
  // the ending: the question is struck through and the answer written under it
  if (t > strike) {
    line(g, 'strike', [[x - 190, y + 10], [x + 200, y + 30]], t, strike, .4, { color: P.red, width: 5 });
    hand(g, 'ans', '근거로 고르세요', x, y + 230, t, at('l30') + .4, { size: 92, color: P.blue, align: 'center', d: 1.2 });
    reg('ans', '근거로 고르세요', at('l30') + .4, DUR, [x - 330, y + 150, 660, 100]);
    type(g, '라파힐 AHCC', x, y - 210, t, at('l31'), { size: 44, font: SERIF, weight: 700, color: P.ink, align: 'center', d: .8 });
    type(g, '※ 본 영상은 정보 제공용이며, 질병의 예방·치료를 목적으로 하지 않습니다.', x, y + 300, t, at('l31') + .5, { size: 18, align: 'center' });
    reg('disc', '※ 본 영상은 정보 제공용이며, 질병의 예방·치료를 목적으로 하지 않습니다.', at('l31') + .5, DUR, [x - 400, y + 280, 800, 24]);
  }
}

// IMMUNE — 100 white blood cells (one person inside the normal ranges), then the lymphocytes, NK and the dendritic cell
const KIND = [['호중구', 58, '#B9B1A4'], ['림프구', 30, P.blue], ['단핵구', 7, '#8C8478'], ['호산구', 4, '#C9A774'], ['호염기구', 1, P.ink]];
const CELLS = []; KIND.forEach(([k, n, c], ki) => { for (let i = 0; i < n; i++) CELLS.push({ k: ki, c }); });
const WS = 64, WX = IMM[0] - 288, WY = IMM[1] - 300;
const cellXY = i => [WX + (i % 10) * WS, WY + Math.floor(i / 10) * WS];
const NK = [61, 70, 83];             // three of the 30 lymphocytes (indices 58–87): ~10 %, inside the 3–14 % range
function immune(g, t) {
  const [x, y] = IMM;
  type(g, '백혈구 100개 중', WX, WY - 100, t, at('l04') + .3, { size: 40, font: SERIF, weight: 700, color: P.ink, d: .9 });
  reg('wh', '백혈구 100개 중', at('l04') + .3, S.ahcc, [WX, WY - 130, 500, 50]);
  const t0 = at('l05'), span = Math.min(3.2, end('l05') - t0);
  CELLS.forEach((c, i) => {
    const tl = t0 + span * i / 100, [cx, cy] = cellXY(i);
    if (i % 4 === 0) ev('d' + i, { t: tl, type: 'land', k: c.k });
    const nk = NK.includes(i) && t > at('l06') + .8;
    E.dataDot(g, cx, cy, 20, nk ? P.red : c.c, { fresh: t - tl, ripple: i % 4 === 0 ? 1 : 0 });
  });
  // the lymphocyte rows: bracket and note
  const ly0 = cellXY(58)[1] - 30, ly1 = cellXY(87)[1] + 30;
  line(g, 'lyb', [[WX + 640, ly0], [WX + 660, ly0], [WX + 660, ly1], [WX + 640, ly1]], t, end('l05') - .6, .5, { color: P.blue });
  hand(g, 'ly', '림프구 20~40개', WX + 690, (ly0 + ly1) / 2 + 12, t, end('l05') - .3, { size: 44 });
  reg('ly', '림프구 20~40개', end('l05') - .3, S.ahcc, [WX + 690, ly0, 300, 60]);
  hand(g, 'ne', '호중구 40~60개 · 세균과 맞섬', WX + 690, WY + 110, t, at('l05b') + .3, { size: 34, color: P.inkSoft });
  hand(g, 'mo', '단핵구 2~8개 · 청소 담당', WX + 690, cellXY(92)[1] + 10, t, at('l05b') + 1.6, { size: 34, color: P.inkSoft });
  type(g, '정상 범위: MedlinePlus · 그림은 범위 안의 한 사람 예시', WX, WY - 52, t, at('l05b'), { size: 18 });
  reg('src1', '정상 범위: MedlinePlus · 그림은 범위 안의 한 사람 예시', at('l05b'), S.ahcc, [WX, WY - 70, 600, 24]);
  // NK
  NK.forEach((i, k) => { const [cx, cy] = cellXY(i); line(g, 'nk' + k, E.ringPath(cx, cy, 30, k + 2), t, at('l06') + .8 + k * .2, .35, { color: P.red, width: 1.8 }); });
  hand(g, 'nk', 'NK세포 · 림프구의 약 3~14%', WX + 690, (ly0 + ly1) / 2 + 80, t, at('l07') + .2, { size: 40, color: P.red });
  reg('nk', 'NK세포 · 림프구의 약 3~14%', at('l07') + .2, S.ahcc, [WX + 690, (ly0 + ly1) / 2 + 40, 500, 50]);
  // the dendritic cell: a drawn star-shaped cell outside the blood, passing word to the lymphocytes
  const dc = [x + 640, y - 150];
  line(g, 'dc', E.sparklePath(dc[0], dc[1], 70, .3), t, at('l08') + .2, 1.1, { color: P.ink, width: 2.2 });
  hand(g, 'dct', '수지상세포', dc[0] - 90, dc[1] + 130, t, at('l08') + 1.0, { size: 44, color: P.ink });
  hand(g, 'dct2', '정보를 전하는 전령', dc[0] - 90, dc[1] + 180, t, at('l08') + 1.8, { size: 34 });
  reg('dc', '수지상세포 정보를 전하는 전령', at('l08') + 1.0, S.ahcc, [dc[0] - 90, dc[1] + 90, 300, 100]);
  E.leader(g, [dc[0] - 80, dc[1] + 40], [WX + 600, cellXY(65)[1]], { progress: pr(t, at('l08') + 2.4, .5), color: P.blue, bend: -.25 });
  // innate | adaptive, the DC as the bridge
  const by = WY + 10 * WS + 80;
  hand(g, 'inn', '선천 면역 — NK세포', WX - 40, by + 40, t, at('l09') + .5, { size: 42, color: P.red });
  hand(g, 'ada', '적응 면역 — T·B세포', WX + 520, by + 40, t, at('l09') + 2.2, { size: 42, color: P.blue });
  reg('inad', '선천 면역 — NK세포 적응 면역 — T·B세포', at('l09') + .5, S.ahcc, [WX - 40, by, 1000, 60]);
  line(g, 'bridge', E.quadPath([WX + 300, by + 70], [WX + 470, by + 150], [WX + 640, by + 70]), t, at('l10') + 1.5, .8, { color: P.ink, width: 2.2 });
  hand(g, 'br', '수지상세포 = 다리', WX + 330, by + 190, t, at('l10') + 2.0, { size: 36, color: P.ink });
  reg('br', '수지상세포 = 다리', at('l10') + 2.0, S.ahcc, [WX + 330, by + 150, 300, 50]);
  hand(g, 'fn', '면역 기능 = 제자리에서 제 역할', WX + 520, WY - 100, t, at('l11') + .4, { size: 44, color: P.blue });
  reg('fn', '면역 기능 = 제자리에서 제 역할', at('l11') + .4, S.ahcc, [WX, WY - 200, 600, 50]);
}

// AHCC — the mushroom above ground, the mycelium below; the process; 74 of 100 squares
function mushroom() {
  const [x, y] = [AH[0] - 560, AH[1] - 60];
  const cap = [...E.quadPath([x - 170, y - 40], [x, y - 230], [x + 170, y - 40], 30), ...E.quadPath([x + 170, y - 40], [x, y - 10], [x - 170, y - 40], 20)];
  const stem = [[x - 30, y - 22], [x - 36, y + 120], [x + 36, y + 120], [x + 30, y - 22]];
  const ground = [[x - 330, y + 120], [x + 330, y + 120]];
  const threads = []; let s = 7;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (let k = 0; k < 9; k++) {
    let px = x - 40 + k * 10, py = y + 120, pts = [[px, py]];
    const ang = Math.PI / 2 + (k - 4) * .28;
    for (let j = 0; j < 9; j++) { const a = ang + (rnd() - .5) * .9; px += Math.cos(a) * 34; py += Math.sin(a) * 26; pts.push([px, py]); }
    threads.push(pts);
  }
  return { x, y, cap, stem, ground, threads };
}
const MU = mushroom();
const SQ = 58, SX = AH[0] + 40, SY = AH[1] - 290;
function ahcc(g, t) {
  const { x, y, cap, stem, ground, threads } = MU;
  line(g, 'gr', ground, t, S.ahcc + .8, .6, { color: P.inkSoft, rule: true });
  line(g, 'cap', cap, t, S.ahcc + 1.2, 1.0, { width: 2.6, color: P.ink });
  line(g, 'stem', stem, t, S.ahcc + 2.0, .6, { width: 2.4, color: P.ink });
  hand(g, 'capt', '갓', x + 190, y - 120, t, at('l12') + 1.2, { size: 40, color: P.inkSoft });
  hand(g, 'stt', '줄기', x + 60, y + 80, t, at('l12') + 1.9, { size: 40, color: P.inkSoft });
  threads.forEach((th, k) => line(g, 'th' + k, th, t, at('l12') + 3.0 + k * .18, .9, { color: AMBER, width: 1.8, passes: 1 }));
  hand(g, 'myc', '균사체', x - 300, y + 300, t, at('l12') + 4.4, { size: 54, color: P.red });
  line(g, 'mycr', E.ringPath(x, y + 230, 150, 3), t, at('l12') + 4.9, .7, { color: P.red, width: 2 });
  reg('myc', '갓 줄기 균사체', at('l12') + 1.2, S.history, [x - 300, y - 150, 600, 500]);
  hand(g, 'net', '땅 아래 그물처럼', x - 300, y + 360, t, at('l12b') + 3.0, { size: 36 });
  reg('net', '땅 아래 그물처럼', at('l12b') + 3.0, S.history, [x - 300, y + 330, 300, 40]);
  // the process, left to right
  const steps = ['배양', '분리', '살균', '동결건조'], px = x - 330, py = y + 470;
  steps.forEach((s, i) => {
    hand(g, 'ps' + i, s, px + i * 175, py, t, at('l13') + .6 + i * .9, { size: 40, color: P.ink });
    if (i < 3) line(g, 'pa' + i, [[px + i * 175 + 110, py - 12], [px + i * 175 + 150, py - 12], [px + i * 175 + 140, py - 20], [px + i * 175 + 150, py - 12], [px + i * 175 + 140, py - 4]], t, at('l13') + 1.1 + i * .9, .3, { color: P.inkSoft, width: 1.6, passes: 1 });
  });
  reg('proc', '배양 → 분리 → 살균 → 동결건조', at('l13') + .6, S.history, [px, py - 40, 700, 50]);
  // composition: 74 of 100 squares
  type(g, 'AHCC 건조 중량 100 중', SX, SY - 50, t, at('l14'), { size: 34, font: SERIF, weight: 700, color: P.ink, d: .8 });
  reg('cmp', 'AHCC 건조 중량 100 중', at('l14'), S.history, [SX, SY - 90, 450, 50]);
  for (let i = 0; i < 100; i++) {
    const tl = at('l14') + .8 + 2.4 * i / 100, c = i < 74 ? AMBER : '#DDD6C9', cx = SX + (i % 10) * SQ, cy = SY + Math.floor(i / 10) * SQ;
    if (i % 5 === 0) ev('sq' + i, { t: tl, type: 'land', k: i < 74 ? 5 : 6 });
    if (t >= tl) { const f = clamp((t - tl) / .2), s = 22 * (1 + .3 * Math.sin(f * Math.PI)); E.inkShape(g, [[cx - s, cy - s], [cx + s, cy - s], [cx + s, cy + s], [cx - s, cy + s]], { fill: c, hatch: .3, seed: i, width: 1 }); }
  }
  hand(g, 'olig', '올리고당 약 74%', SX + 10 * SQ + 10, SY + 170, t, at('l14') + 3.4, { size: 46, color: AMBER });
  hand(g, 'rest', '아미노산·미네랄 등', SX + 10 * SQ + 10, SY + 8 * SQ, t, at('l14') + 4.6, { size: 36, color: P.inkSoft });
  reg('olig', '올리고당 약 74% 아미노산·미네랄 등', at('l14') + 3.4, S.history, [SX + 590, SY + 120, 350, 400]);
  type(g, '출처: Shin 외, Journal of Immunology Research 2019', SX, SY + 10 * SQ + 6, t, at('l14') + 3.4, { size: 18 });
  reg('src2', '출처: Shin 외, Journal of Immunology Research 2019', at('l14') + 3.4, S.history, [SX, SY + 580, 560, 24]);
  // not the same thing
  hand(g, 'ne1', '표고버섯 분말', SX - 20, SY + 10 * SQ + 120, t, at('l15') + 1.4, { size: 46, color: P.inkSoft });
  hand(g, 'neq', '≠', SX + 300, SY + 10 * SQ + 122, t, at('l15') + 2.4, { size: 70, color: P.red, d: .3 });
  hand(g, 'ne2', '표고버섯균사체 AHCC', SX + 370, SY + 10 * SQ + 120, t, at('l15') + 2.7, { size: 46, color: P.blue });
  reg('neq', '표고버섯 분말 ≠ 표고버섯균사체 AHCC', at('l15') + 1.4, S.history, [SX - 20, SY + 660, 900, 60]);
}

// HISTORY — a time axis 1980 → 2030; the 1980s development bracket, the line of research to now, 2005, 2008
const TX0 = HIST[0] - 900, TX1 = HIST[0] + 900, TY = HIST[1] + 120, Y0 = 1980, Y1 = 2030;
const yx = yr => lerp(TX0, TX1, (yr - Y0) / (Y1 - Y0));
function history(g, t) {
  line(g, 'axis', [[TX0, TY], [TX1, TY]], t, S.history + .6, 1.2, { color: P.ink, width: 2, rule: true });
  for (let yr = 1980; yr <= 2030; yr += 10) { type(g, String(yr), yx(yr), TY + 40, t, S.history + .9 + (yr - 1980) * .02, { size: 20, align: 'center' }); }
  type(g, 'AMINO UP · 일본 삿포로', TX0, HIST[1] - 330, t, at('l16') + .2, { size: 40, font: SERIF, weight: 700, color: P.ink, d: .8 });
  reg('au', 'AMINO UP · 일본 삿포로', at('l16') + .2, S.korea, [TX0, HIST[1] - 370, 600, 50]);
  // 1987 or 1989: a bracket, not a dot (the sources disagree)
  line(g, 'dev', E.bracketPath(yx(1987), yx(1989), TY - 26, 12), t, at('l17') + .4, .5, { color: P.red, width: 2 });
  hand(g, 'devt', '1980년대 후반 개발', yx(1987) - 140, TY - 120, t, at('l17') + .8, { size: 44, color: P.red });
  hand(g, 'devt2', '도쿄대 약학부와 함께 · 1987/1989 (자료마다 다름)', yx(1987) - 140, TY - 72, t, at('l17') + 1.8, { size: 30, color: P.inkSoft });
  reg('dev', '1980년대 후반 개발 도쿄대 약학부와 함께 · 1987/1989 (자료마다 다름)', at('l17') + .8, S.korea, [yx(1987) - 140, TY - 160, 700, 100]);
  // the research line to now
  const now = 2026;
  line(g, 'res', [[yx(1989), TY - 10], [yx(now), TY - 10]], t, at('l18') + .4, 2.2, { color: P.blue, width: 6, passes: 1 });
  E.dataDot(g, yx(now), TY - 10, 12, P.blue, { fresh: t - (at('l18') + 2.6) });
  hand(g, 'now', '2026 · 30년+', yx(now) - 70, TY - 50, t, at('l18') + 2.6, { size: 38, color: P.blue });
  E.dataDot(g, yx(2005), TY - 10, 11, AMBER, { fresh: t - (at('l18') + 4.2) });
  ev('d2005', { t: at('l18') + 4.2, type: 'land', k: 5 });
  hand(g, 'ucd', '2005~ UC 데이비스 영양학과 석학 강연 후원', yx(2005) - 260, TY + 120, t, at('l18') + 4.4, { size: 34, color: P.ink });
  E.leader(g, [yx(2005) - 40, TY + 86], [yx(2005), TY + 6], { progress: pr(t, at('l18') + 5.6, .4), color: P.ink });
  reg('hist', '2026 · 30년+ 2005~ UC 데이비스 영양학과 석학 강연 후원', at('l18') + 2.6, S.korea, [yx(2005) - 260, TY - 90, 1100, 240]);
  hand(g, 'icnim', '국제학회 ICNIM · 매년 개최', yx(2010), TY + 210, t, at('l19') + .6, { size: 40, color: P.blue });
  reg('icnim', '국제학회 ICNIM · 매년 개최', at('l19') + .6, S.korea, [yx(2010), TY + 170, 500, 50]);
  // 2008: the individual recognition in Korea (lands when the next chapter names it)
  E.dataDot(g, yx(2008), TY - 10, 12, P.red, { fresh: t - (at('l20') - .2) });
  ev('d2008', { t: at('l20') - .2, type: 'land', k: 7 });
}

// KOREA — the recognition card: one function, one number; the process; the human study note
function korea(g, t) {
  const [x, y] = KOR, cx0 = x - 520, cy0 = y - 330, cw = 760, ch = 420;
  type(g, '한국 · 식약처 개별인정', cx0, cy0 - 40, t, S.korea + .9, { size: 40, font: SERIF, weight: 700, color: P.ink, d: .8 });
  const card = [[cx0, cy0], [cx0 + cw, cy0], [cx0 + cw, cy0 + ch], [cx0, cy0 + ch]];
  if (t > at('l20')) E.inkShape(g, card, { fill: '#FBF9F4', hatch: 0, progress: pr(t, at('l20'), .8), width: 1.6 });
  type(g, '원료명', cx0 + 40, cy0 + 70, t, at('l20') + .8, { size: 20 });
  type(g, '표고버섯균사체 AHCC', cx0 + 40, cy0 + 120, t, at('l20') + 1.0, { size: 40, font: SERIF, weight: 700, color: P.ink });
  type(g, '인정번호  제2008-78호', cx0 + 40, cy0 + 175, t, at('l20') + 1.6, { size: 24, color: P.ink });
  type(g, '기능성', cx0 + 40, cy0 + 260, t, at('l22') + .2, { size: 20 });
  hand(g, 'func', '면역기능 증진에 도움을 줄 수 있음', cx0 + 40, cy0 + 330, t, at('l22') + 2.0, { size: 50, color: P.red, d: 1.6 });
  line(g, 'funcu', [[cx0 + 40, cy0 + 350], [cx0 + 680, cy0 + 352]], t, at('l22') + 3.7, .5, { color: P.red, width: 2.4 });
  reg('card', '표고버섯균사체 AHCC 인정번호 제2008-78호', at('l20') + 1.0, S.qa, [cx0, cy0, cw, 200]);
  reg('func', '면역기능 증진에 도움을 줄 수 있음', at('l22') + 2.0, S.qa, [cx0, cy0 + 280, cw, 80]);
  // the recognition process
  const fx = cx0 + cw + 80;
  ['안전성·기능성 자료 제출', '식약처 심사', '그 원료에만 인정'].forEach((s, i) => {
    hand(g, 'pr' + i, s, fx, cy0 + 60 + i * 120, t, at('l21') + .6 + i * 1.4, { size: 38, color: i === 2 ? P.blue : P.ink });
    if (i < 2) line(g, 'pra' + i, [[fx + 30, cy0 + 80 + i * 120], [fx + 30, cy0 + 140 + i * 120]], t, at('l21') + 1.4 + i * 1.4, .3, { color: P.inkSoft, width: 1.6, passes: 1 });
  });
  reg('proc2', '안전성·기능성 자료 제출 식약처 심사 그 원료에만 인정', at('l21') + .6, S.qa, [fx, cy0 + 20, 450, 300]);
  hand(g, 'same', '같은 표고버섯이라도 → 인정 원료인지 확인', fx, cy0 + 430, t, at('l21b') + .5, { size: 34, color: P.blue });
  reg('same', '같은 표고버섯이라도 → 인정 원료인지 확인', at('l21b') + .5, S.qa, [fx, cy0 + 400, 600, 40]);
  // the human study: a note, not a chart (no numbers are drawn that the viewer cannot check)
  const ny = cy0 + ch + 120;
  hand(g, 'hs', '건강한 성인 · 인체시험', cx0, ny, t, at('l23') + .5, { size: 44, color: P.ink });
  hand(g, 'hs2', '섭취 뒤 수지상세포 수 증가 보고', cx0, ny + 60, t, at('l23') + 2.2, { size: 44, color: P.blue });
  line(g, 'hsa', [[cx0 + 640, ny + 72], [cx0 + 640, ny + 10], [cx0 + 625, ny + 28], [cx0 + 640, ny + 10], [cx0 + 655, ny + 28]], t, at('l23') + 4.0, .4, { color: P.blue, width: 2.6, passes: 1 });
  type(g, 'Terakawa 외, 2008 · 건강한 성인 대상', cx0, ny + 110, t, at('l23') + 2.6, { size: 18 });
  reg('hs', '건강한 성인 · 인체시험 섭취 뒤 수지상세포 수 증가 보고', at('l23') + .5, S.qa, [cx0, ny - 40, 700, 160]);
}

// Q&A — five questions as handwritten cards; the first one draws the line
const QS = [
  ['l25', '암 같은 질병에 도움이 되나요?', '건강기능식품은 의약품이 아닙니다 · 질병 예방·치료 목적 ✕', P.red],
  ['l26', '약을 먹고 있다면?', '섭취 전 의사·약사와 상담하세요', P.red],
  ['l27', '누구에게나 같을까요?', '아니요 · 사람마다 차이가 있습니다', P.blue],
  ['l27b', '얼마나 먹어야 하나요?', '제품에 표시된 섭취량·방법을 따르세요', P.blue],
  ['l28', '어떻게 고르나요?', '원료명 · 식약처 인정 정보 · 건강기능식품 마크', P.blue],
];
function qa(g, t) {
  const [x, y] = QA;
  type(g, '자주 받는 질문', x - 760, y - 520, t, at('l24') + .2, { size: 44, font: SERIF, weight: 700, color: P.ink, d: .8 });
  reg('qah', '자주 받는 질문', at('l24') + .2, S.end, [x - 760, y - 560, 400, 50]);
  QS.forEach(([id, q, a, col], i) => {
    const qy = y - 400 + i * 170, t0 = at(id);
    hand(g, 'qq' + i, 'Q. ' + q, x - 760, qy, t, t0 + .1, { size: 44, color: P.ink, d: .9 });
    hand(g, 'qa' + i, 'A. ' + a, x - 700, qy + 62, t, t0 + 1.4, { size: 40, color: col, d: 1.3 });
    reg('qa' + i, 'Q. ' + q + ' A. ' + a, t0 + .1, S.end, [x - 760, qy - 40, 1300, 120]);
  });
  type(g, '인정 정보 확인: 식품안전나라 (foodsafetykorea.go.kr)', x - 700, y + 470, t, at('l29') + .3, { size: 24, color: P.ink });
  reg('fsk', '인정 정보 확인: 식품안전나라 (foodsafetykorea.go.kr)', at('l29') + .3, S.end, [x - 700, y + 440, 700, 30]);
}

// ---------- the pencil ----------
function lastTip(t) {        // latest recorded drawing position at or before t
  let lo = 0, hi = PT.length - 1, k = -1;
  while (lo <= hi) { const m = (lo + hi) >> 1; if (PT[m][0] <= t) { k = m; lo = m + 1; } else hi = m - 1; }
  return k < 0 ? null : PT[k];
}
function pencil(g, t) {
  const L = TIP ? [t, TIP] : lastTip(t), idle = L ? t - L[0] : 99;
  const base = L ? E.w2s(CAM, L[1][0], L[1][1]) : [W * .8, H * 1.2];
  const away = clamp((idle - .6) / .9);                     // after a pause the hand withdraws to the lower right
  const tip = [lerp(base[0], W * .86, ease(away)), lerp(base[1], H * 1.05, ease(away))];
  const lift = idle < .05 ? .05 + .08 * Math.abs(Math.sin(t * 9)) : .2 + .9 * away;
  if (tip[1] > H + 40) return;
  E.drawPencil(g, { tip, s: .85, lift, flip: 0 });
}

// ---------- frame ----------
export function render(g, t, record = false) {
  CAM = camAt(t);
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1;
  if (!record) E.drawPaper(g, CAM, { dots: .8 });
  E.applyCam(g, CAM);
  TIP = null;
  hook(g, t);
  if (t > S.immune - 1) immune(g, t);
  if (t > S.ahcc - 1) ahcc(g, t);
  if (t > S.history - 1) history(g, t);
  if (t > S.korea - 1) korea(g, t);
  if (t > S.qa - 1) qa(g, t);
  if (record) { if (TIP) PT.push([t, TIP]); return; }      // the pre-pass only registers texts, sounds and the pencil's track
  pencil(g, t);
  // the caption: the narration line, word by word across its time
  // one caption at a time: each holds until just before the next line begins
  const ids = Object.keys(V);
  ids.forEach((id, k) => {
    const [t0, t1, text] = V[id], next = k + 1 < ids.length ? V[ids[k + 1]][0] : DUR, hold = Math.min(t1 + .6, next - .35);
    if (t < t0 - .1 || t > hold + .3) return;
    const words = text.split(' '), n = words.length;
    E.caption(g, words.map((w, i) => ({ w, t: t0 + (t1 - t0) * i / n })), t, { t0, t1: hold, x: 180, y: 1010, size: 38, maxW: 1560 });
  });
}

// sound events (the score reads these)
export function events() {
  const out = EVS.slice();
  Object.entries(S).forEach(([k, t]) => { if (t > 1) out.push({ t: t + .2, type: 'sweep' }); });
  out.push({ t: S.end + 1.4, type: 'strike' });
  return out.sort((a, b) => a.t - b.t);
}
