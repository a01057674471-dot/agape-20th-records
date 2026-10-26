// The static page: one tall sketchbook page, 2160×6480 world px.
// Top: Eden (tree of knowledge, tree of life, river, lawn). Middle: the wall and the east gate. Below: the thorny land, the path, the hill and the cross.
// Layers: color (washes, white = paper), inkA/timeA (Eden, drawn outward from the fruit at the start), inkB/timeB (gate → land → hill → cross, drawn as the camera arrives).
import { rng, fbm, n2, hex, mix3, lerp, clamp, ellipse, spline, resample, penStroke, rasterPen, wash, reserve, dab, foliage, TAU, LEAF } from './engine.js';

export const W = 2160, H = 6480;
export const WIN_A = [0.3, 5.0], WIN_B = [38.4, 10.4];
export const FRUIT = [1262, 1702];                 // the forbidden fruit, hanging under the crown
export const TRUNK = { x: 1080, base: 2235, top: 1640 };
export const EDEN_Y = 2735;                         // Eden (and its colour) ends here
export const WALL = { y0: 2800, y1: 2905, gx0: 1005, gx1: 1250 };
export const SWORD = [1128, 2610];
export const CHERUBS = [[850, 2935], [1405, 2935]];
export const CROSS = { x: 1080, top: 4600, base: 5230, bar: 4775, hw: 180 };
export const HILL_TOP = 5020;
export const PATHC = [[1128, 2960], [1060, 3200], [960, 3480], [900, 3760], [940, 4060], [1000, 4400], [1050, 4560]];

export const C = {
  sky: hex('#9fbcd6'), skyDeep: hex('#86a6c8'), cloud: hex('#b7b3c9'),
  lawn: hex('#c3c96f'), lawnLit: hex('#dcd98b'), lawnShade: hex('#7f9c52'),
  river: hex('#8fb6c4'), riverD: hex('#5f8ea3'),
  bark: hex('#8a735e'), barkD: hex('#5d4c40'),
  gold: { sun: hex('#ecd47a'), light: hex('#d8c45f'), mid: hex('#b3b552'), dark: hex('#7f9445'), deep: hex('#5d7a3d') },
  flower: [hex('#e7a0a8'), hex('#f0d36a'), hex('#c9a4d8'), hex('#f2efe4')],
  stone: hex('#c7b396'), stoneD: hex('#9a8a78'),
  earth: hex('#d6bf93'), earthD: hex('#b49a72'), thorn: hex('#8c7a5a'),
  hill: hex('#b9b77a'), hillD: hex('#8f915e'), wood: hex('#9a6f4e'), woodD: hex('#6e4c36'),
};

function cv(w, h, fill) { const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d', { willReadFrequently: true }); if (fill) { x.fillStyle = fill; x.fillRect(0, 0, w, h); } return [c, x]; }

// Page edge: frays at the left, right and bottom; the bottom margin stays blank for the last words
export function pageMask(x, y) {
  const n = (fbm(x * .004, y * .004, 5, 3) - .5) * 140 + (n2(x * .03, y * .03, 8) - .5) * 36;
  return Math.min(x - 50 + n, W - 50 - x + n, H - 60 - y + n, y - 40 + n);
}
export const inPage = (x, y, m = 0) => pageMask(x, y) > m;

export const CROWN = [{ x: 1080, y: 1290, r: 330 }, { x: 830, y: 1400, r: 250 }, { x: 1330, y: 1410, r: 260 }, { x: 960, y: 1130, r: 230 }, { x: 1220, y: 1150, r: 220 }, { x: 1080, y: 1520, r: 220 }];
export const LIFE = [{ x: 400, y: 1330, r: 190 }, { x: 290, y: 1420, r: 140 }, { x: 520, y: 1420, r: 150 }, { x: 400, y: 1200, r: 140 }];
export const BUSH = [{ x: 1310, y: 2110, r: 140 }, { x: 1470, y: 2090, r: 150 }, { x: 1630, y: 2105, r: 145 }, { x: 1225, y: 2215, r: 105 }, { x: 1745, y: 2210, r: 110 }, { x: 1390, y: 2245, r: 115 }, { x: 1560, y: 2250, r: 120 }, { x: 1470, y: 2200, r: 120 }];

export function buildWorld() {
  const [colorC, cx] = cv(W, H, '#fff');
  const [inkAC, ia] = cv(W, H), [timeAC, ta] = cv(W, H, '#fff'), [inkBC, ib] = cv(W, H), [timeBC, tb] = cv(W, H, '#fff');
  ta.globalCompositeOperation = 'darken'; tb.globalCompositeOperation = 'darken';
  const R = rng(1203);
  const strokes = [];
  // Eden ink: the farther from the fruit, the later it is drawn
  const penA = (pts, o = {}, t0) => {
    const st = penStroke(pts, o); if (st.P.length < 2) return st;
    const m = st.P[st.P.length >> 1], d = Math.hypot(m[0] - FRUIT[0], m[1] - FRUIT[1]);
    const t = t0 ?? (0.45 + d / 620 + R() * .1), du = clamp(st.L / 2200, .04, .3);
    rasterPen(ia, ta, st, t, du, WIN_A); strokes.push([+t.toFixed(3), +du.toFixed(3), Math.round(st.L), 0]); return st;
  };
  // Lower-page ink at an explicit time
  const penB = (pts, o, t0, dur) => { const st = penStroke(pts, o); if (st.P.length < 2) return st; const du = dur ?? clamp(st.L / 1800, .05, .4); rasterPen(ib, tb, st, t0, du, WIN_B); strokes.push([+t0.toFixed(3), +du.toFixed(3), Math.round(st.L), 1]); return st; };
  const W1 = 2.6;

  // ================= Sky =================
  for (let i = 0; i < 46; i++) {
    const x = 150 + R() * 1860, y = 140 + R() * 900;
    if (!inPage(x, y, 160)) continue;
    const rx = 160 + R() * 260, ry = rx * (.3 + R() * .25), k = clamp(1 - y / 1200);
    wash(cx, ellipse(x, y, rx, ry, 22, R()), R() < .3 ? C.skyDeep : C.sky, { a: .1 + .1 * k, j: rx * .18, layers: 3, edge: .1, seed: 100 + i, freq: .006 });
  }
  for (const [x, y, rx, ry] of [[560, 640, 210, 70], [1600, 520, 250, 80], [1280, 760, 150, 50]]) {
    const puff = []; for (let k = 0; k < 9; k++) { const a = Math.PI + k / 8 * Math.PI; puff.push([x + Math.cos(a) * rx * (.85 + .3 * R()), y + Math.sin(a) * ry * (1.2 + .6 * R())]); }
    puff.push([x + rx * .9, y + ry * .35], [x - rx * .9, y + ry * .35]);
    reserve(cx, spline(puff, 4, true), .8, 12, x);
    wash(cx, ellipse(x, y + ry * .25, rx * .8, ry * .32, 18), C.cloud, { a: .2, j: 9, edge: .1, seed: x | 0 });
    penA(puff.slice(0, 7), { w: 1.6, wob: .8, over: 4, seed: x | 0 });
  }
  // birds: two-stroke ticks
  for (let i = 0; i < 7; i++) { const x = 1300 + R() * 600, y = 300 + R() * 300, s = 12 + R() * 10; penA([[x - s, y - s * .4], [x - s * .4, y - s * .1], [x, y + s * .15]], { w: 1.6, wob: .3, over: 1, seed: 40 + i }); penA([[x, y + s * .15], [x + s * .5, y - s * .2], [x + s * 1.1, y - s * .5]], { w: 1.6, wob: .3, over: 1, seed: 60 + i }); }

  // ================= Distant hills of Eden =================
  const ridge = []; for (let x = 0; x <= W; x += 60) ridge.push([x, 1560 - 120 * Math.sin(x / 520 + .6) - 60 * fbm(x * .004, 3, 9, 3)]);
  wash(cx, [...ridge, [W, 1900], [0, 1900]], mix3(C.lawn, hex('#b9c0cc'), .45), { a: .35, j: 14, layers: 2, edge: .08, seed: 7 });
  visible(ridge, behindTree).forEach((f, k) => penA(f, { w: 1.6, wob: 1, over: 5, gap: .5, seed: 8 + k }));

  // ================= River (behind the tree, flowing left to right) =================
  const rv = []; for (let x = -40; x <= W + 40; x += 80) rv.push([x, 1870 + 40 * Math.sin(x / 330) + (x - 1080) * .03]);
  const rvB = rv.map(([x, y]) => [x, y + 70 + 18 * Math.sin(x / 210)]);
  wash(cx, [...rv, ...rvB.slice().reverse()], C.river, { a: .55, j: 8, layers: 3, edge: .3, seed: 21 });
  for (let i = 0; i < 26; i++) { const x = R() * W, y = 1900 + R() * 50 + (x - 1080) * .03; reserve(cx, ellipse(x, y, 30 + R() * 50, 4, 10), .6, 2, i); }
  visible(rv, behindTree).forEach((f, k) => penA(f, { w: 2, wob: 1, over: 6, gap: .5, seed: 22 + k * 3 })); visible(rvB, behindTree).forEach((f, k) => penA(f, { w: 2.2, wob: 1, over: 6, gap: .5, seed: 23 + k * 3 }));
  for (let i = 0; i < 12; i++) { const x = 120 + R() * 1900, y = 1905 + R() * 30 + (x - 1080) * .03; if (behindTree(x, y) || behindTree(x + 80, y)) continue; penA([[x, y], [x + 40, y - 3], [x + 80, y + 1]], { w: 1.4, wob: .6, over: 2, seed: 30 + i }); }

  // ================= Lawn =================
  const lawnTop = x => 1985 + 18 * Math.sin(x / 260);
  const lawnPoly = [...[...Array(28)].map((_, i) => { const x = i / 27 * W; return [x, lawnTop(x)]; }), [W, EDEN_Y - 30], [0, EDEN_Y - 30]];
  wash(cx, lawnPoly, C.lawn, { a: .45, j: 20, layers: 3, edge: .05, seed: 31 });
  for (let i = 0; i < 16; i++) { const y = 2050 + i * 42, x = R() * W; wash(cx, ellipse(x, y, 260 + R() * 360, 22 + R() * 14, 18), R() < .5 ? C.lawnLit : C.lawnShade, { a: .14 + R() * .12, j: 10, layers: 2, edge: 0, seed: 40 + i }); }
  // ragged lower edge of Eden's lawn: dabs fraying into the paper above the wall
  for (let i = 0; i < 420; i++) { const x = R() * W, y = EDEN_Y - 90 + R() * 110; if (R() > .6) continue; dab(cx, x, y, 5 + R() * 12, R() * TAU, R() < .5 ? LEAF.light : C.lawn, .25 + R() * .3, 500 + i); }
  // grass flicks
  for (let i = 0; i < 260; i++) {
    const x = 60 + R() * (W - 120), y = 2030 + R() * 680; if (Math.abs(x - TRUNK.x) < 90 && y < 2280) continue;
    const s = 10 + R() * 14 * (y - 1900) / 800; penA([[x, y], [x + (R() - .5) * 8, y - s]], { w: 1.4 + (y - 2000) / 900, wob: .4, over: 1, seed: 100 + i, smooth: false });
  }
  // flowers: small dabs with an ink tick
  for (let i = 0; i < 110; i++) {
    const x = 80 + R() * (W - 160), y = 2040 + R() * 640; if (Math.abs(x - TRUNK.x) < 120 && y < 2300) continue;
    const col = C.flower[(R() * 4) | 0], r = 6 + R() * 7;
    for (let k = 0; k < 4; k++) dab(cx, x + Math.cos(k * 1.6) * r * .7, y + Math.sin(k * 1.6) * r * .5, r * .6, k, col, .55, 900 + i * 4 + k);
    if (R() < .5) penA([[x, y + r * .6], [x + 2, y + r * 2.2]], { w: 1.2, wob: .3, over: 0, seed: 300 + i, smooth: false });
  }

  // ================= Tree of life (back left, golden) =================
  for (const c of LIFE) scallop(c, R, .9, LIFE).forEach((f, k) => penA(f, { w: 1.8, wob: .7, over: 3, gap: .3, seed: (c.x + c.y | 0) + k }));
  foliage(cx, LIFE, { seed: 77, pal: C.gold, dens: 1.1 });
  wash(cx, [[388, 1460], [372, 1980], [430, 1980], [414, 1460]], C.bark, { a: .5, j: 4, layers: 2, edge: .2, seed: 78 });
  penA([[386, 1470], [376, 1985]], { w: 2, wob: .6, over: 3, seed: 79 }); penA([[416, 1470], [428, 1985]], { w: 2.2, wob: .6, over: 3, seed: 80 });
  for (let i = 0; i < 18; i++) { const a = R() * TAU, r = R() * 160; dab(cx, 400 + Math.cos(a) * r, 1320 + Math.sin(a) * r * .8, 7, 0, hex('#e9b84a'), .6, 1200 + i); }

  // ================= Tree of knowledge =================
  const trunk = [[1040, TRUNK.base], [1048, 2000], [1052, 1800], [1035, TRUNK.top], [1125, TRUNK.top], [1110, 1800], [1114, 2000], [1128, TRUNK.base]];
  wash(cx, trunk, C.bark, { a: .55, j: 4, layers: 3, edge: .25, seed: 90 });
  wash(cx, trunk.slice(4).concat([[1095, 2000], [1092, 1800], [1090, TRUNK.top]].reverse()), C.barkD, { a: .3, j: 3, layers: 2, edge: .1, seed: 91 });
  penA([[1040, TRUNK.base + 8], [1048, 2000], [1052, 1800], [1035, TRUNK.top]], { w: W1, wob: .9, over: 4, seed: 92 });
  penA([[1128, TRUNK.base + 8], [1114, 2000], [1110, 1800], [1125, TRUNK.top]], { w: W1 * 1.1, wob: .9, over: 4, seed: 93 });
  for (let i = 0; i < 6; i++) { const y = 1700 + i * 90; penA([[1062, y], [1070 + R() * 10, y + 30]], { w: 1.4, wob: .4, over: 1, seed: 94 + i }); }
  // roots
  for (const [a, b] of [[[1040, 2225], [980, 2250]], [[1128, 2225], [1190, 2252]], [[1085, 2232], [1080, 2258]]]) penA([a, [(a[0] + b[0]) / 2, a[1] + 14], b], { w: 2, wob: .5, over: 2, seed: a[0] + b[1] });
  // branches into the crown (the fruit hangs from the lower right one)
  for (const br of [[[1080, 1660], [1180, 1600], [1262, 1640]], [[1060, 1670], [960, 1580], [880, 1520]], [[1085, 1640], [1100, 1460], [1150, 1350]]]) { penA(br, { w: 2.2, wob: .7, over: 3, seed: br[2][0] }); wash(cx, thick(br, 9), C.bark, { a: .45, j: 2, layers: 2, edge: .1, seed: br[2][1] | 0 }); }
  foliage(cx, CROWN, { seed: 11, dens: 1.15 });
  for (const c of CROWN) scallop(c, R, 1, CROWN).forEach((f, k) => penA(f, { w: 2.2, wob: .8, over: 3, gap: .35, seed: (c.x * 3 + c.y | 0) + k }));
  // reserve a halo around the forbidden fruit so it reads over the leaves
  reserve(cx, ellipse(FRUIT[0], FRUIT[1], 50, 48, 18), .45, 8, 5);
  // other fruits on the tree: small pale dabs (only the one fruit is red)
  for (let i = 0; i < 9; i++) { const c = CROWN[i % CROWN.length], a = R() * TAU, r = c.r * (.4 + R() * .45); const x = c.x + Math.cos(a) * r, y = c.y + Math.sin(a) * r; if (Math.hypot(x - FRUIT[0], y - FRUIT[1]) < 140) continue; dab(cx, x, y, 14, 0, hex('#e2c07a'), .5, 1500 + i); penA(ellipse(x, y, 13, 12, 10), { w: 1.5, wob: .3, over: 2, seed: 1600 + i }); }

  // ================= Wall and the gate (ink B, drawn as the couple arrives) =================
  const wallT = x => 38.6 + Math.abs(x - 1128) / 1100 * 1.2;
  for (const [x0, x1] of [[0, WALL.gx0], [WALL.gx1, W]]) {
    const top = [[x0, WALL.y0 + 6], [x1, WALL.y0 - 4]], bot = [[x0, WALL.y1], [x1, WALL.y1 + 4]];
    wash(cx, [top[0], top[1], bot[1], bot[0]], C.stone, { a: .45, j: 6, layers: 3, edge: .2, seed: x0 + 7 });
    wash(cx, [[x0, WALL.y1 - 30], [x1, WALL.y1 - 30], [x1, WALL.y1 + 4], [x0, WALL.y1]], C.stoneD, { a: .25, j: 4, layers: 2, edge: .1, seed: x0 + 9 });
    penB(top, { w: 2.6, wob: 1, over: 6, gap: .5, seed: x0 + 11 }, wallT((x0 + x1) / 2), .5);
    penB(bot, { w: 2.8, wob: 1, over: 6, gap: .5, seed: x0 + 12 }, wallT((x0 + x1) / 2) + .1, .5);
    for (let x = x0 + 40; x < x1 - 20; x += 70 + R() * 40) { const y = WALL.y0 + 20 + R() * 50; penB([[x, y], [x + 40 + R() * 20, y + (R() - .5) * 6]], { w: 1.5, wob: .5, over: 2, seed: x | 0, smooth: false }, wallT(x), .08); if (R() < .6) penB([[x + 20, y], [x + 22, y + 34]], { w: 1.4, wob: .4, over: 1, seed: x + 1 | 0, smooth: false }, wallT(x) + .05, .05); }
  }
  for (const gx of [WALL.gx0, WALL.gx1]) {   // gate posts
    const s = gx === WALL.gx0 ? -1 : 1, p = [[gx, WALL.y1 + 6], [gx, WALL.y0 - 58], [gx + s * 60, WALL.y0 - 58], [gx + s * 60, WALL.y1 + 8]];
    wash(cx, p, C.stone, { a: .5, j: 4, layers: 3, edge: .25, seed: gx });
    wash(cx, [p[0], p[1], [gx + s * 22, WALL.y0 - 58], [gx + s * 22, WALL.y1 + 6]], C.stoneD, { a: .3, j: 3, layers: 2, edge: .1, seed: gx + 1 });
    penB(p, { w: 2.8, wob: .8, over: 5, seed: gx + 2, smooth: false }, 38.5, .55);
    penB([[gx - s * 8, WALL.y0 - 66], [gx + s * 68, WALL.y0 - 66]], { w: 3, wob: .6, over: 4, seed: gx + 3 }, 39.0, .2);
  }
  // cherubim: robed winged figures in ink, faces left blank
  CHERUBS.forEach(([x, y], i) => {
    const s = i ? -1 : 1, t0 = 39.0 + i * .35, h = 560;
    const robe = [[x - 70, y], [x - 48, y - h * .62], [x - 22, y - h * .74], [x + 22, y - h * .74], [x + 48, y - h * .62], [x + 70, y]];
    penB(robe, { w: 2.4, wob: .8, over: 4, seed: 720 + i }, t0, .5);
    penB([[x - 8, y - h * .7], [x - 4, y - h * .3], [x - 12, y]], { w: 1.3, wob: .6, over: 2, seed: 725 + i }, t0 + .3, .25);
    penB(ellipse(x, y - h * .82, 34, 38, 16), { w: 2.2, wob: .5, over: 3, seed: 730 + i }, t0 + .45, .2);
    // two tall wings rising behind the shoulders, feathers as scalloped arcs
    for (const ws of [-1, 1]) {
      const sx = x + ws * 30, sy = y - h * .68;
      const wing = [[sx, sy], [sx + ws * 90, sy - 110], [sx + ws * 200, sy - 170], [sx + ws * 270, sy - 150], [sx + ws * 250, sy - 90], [sx + ws * 280, sy - 40], [sx + ws * 220, sy + 10], [sx + ws * 230, sy + 70], [sx + ws * 140, sy + 60], [sx + ws * 40, sy + 40]];
      penB(wing, { w: 2.1, wob: .8, over: 3, seed: 750 + i * 2 + (ws > 0 ? 1 : 0) }, t0 + .6, .45);
      for (let k = 0; k < 4; k++) { const u = .2 + k * .2, a = [sx + ws * (40 + 190 * u), sy - 120 * Math.sin(u * 2.4) + 30]; penB([a, [a[0] + ws * 26, a[1] + 26], [a[0] + ws * 30, a[1] + 54]], { w: 1.4, wob: .5, over: 1, seed: 760 + i * 10 + k + (ws > 0 ? 5 : 0) }, t0 + .9 + k * .06, .1); }
    }
    // arms raised toward the sword
    penB([[x - s * 30, y - h * .62], [x + s * 20, y - h * .5], [x + s * 70, y - h * .78]], { w: 2, wob: .6, over: 2, seed: 790 + i }, t0 + 1.1, .25);
  });

  // ================= The land east of Eden (ink only until the end) =================
  const landT = y => 40.6 + (y - 2950) / 1900 * 5.2;
  for (let i = 0; i < 24; i++) {
    const x = 120 + R() * 1920, y = 3000 + R() * 2100; if (!inPage(x, y, 120)) continue;
    wash(cx, ellipse(x, y, 260 + R() * 340, 70 + R() * 70, 18, R()), R() < .5 ? C.earth : C.earthD, { a: .1 + R() * .08, j: 20, layers: 2, edge: .08, seed: 1800 + i, freq: .008 });
  }
  // path: two wobbly lines along PATHC
  const pathL = spline(PATHC.map(([x, y]) => [x - 80 - (y - 2960) * .012, y]), 6), pathR = spline(PATHC.map(([x, y]) => [x + 80 + (y - 2960) * .012, y]), 6);
  wash(cx, [...pathL, ...pathR.slice().reverse()], hex('#e3d4b4'), { a: .35, j: 6, layers: 2, edge: .1, seed: 1900 });
  for (let k = 0; k < pathL.length - 6; k += 6) { const y = pathL[k][1]; penB(pathL.slice(k, k + 7), { w: 2, wob: .9, over: 3, gap: .3, seed: 1910 + k, smooth: false }, landT(y), .25); penB(pathR.slice(k, k + 7), { w: 2.2, wob: .9, over: 3, gap: .3, seed: 1960 + k, smooth: false }, landT(y) + .05, .25); }
  // cracks in dry ground
  for (let i = 0; i < 40; i++) { const x = 100 + R() * 1960, y = 3050 + R() * 2000; if (Math.abs(x - pathX(y)) < 160 || !inPage(x, y, 80)) continue; const pts = [[x, y]]; for (let k = 0; k < 4; k++) { const p = pts[pts.length - 1]; pts.push([p[0] + 20 + R() * 30, p[1] + (R() - .5) * 26]); } penB(pts, { w: 1.4, wob: .5, over: 1, seed: 2000 + i, smooth: false }, landT(y), .15); }
  // thorns and thistles (3:18): spiky ink scribbles with a dull wash
  for (let i = 0; i < 34; i++) {
    const x = 120 + R() * 1920, y = 3060 + R() * 1950; if (Math.abs(x - pathX(y)) < 190 || !inPage(x, y, 110) || (y > 4500 && Math.abs(x - 1080) < 600)) continue;
    const s = 40 + R() * 50; wash(cx, ellipse(x, y - s * .4, s * .9, s * .5, 12), C.thorn, { a: .25, j: s * .2, layers: 2, edge: .15, seed: 2100 + i });
    const t0 = landT(y);
    for (let k = 0; k < 6; k++) { const a = -Math.PI / 2 + (k - 2.5) * .38 + (R() - .5) * .2, L = s * (.7 + R() * .6), tip = [x + Math.cos(a) * L, y + Math.sin(a) * L]; penB([[x, y], [lerp(x, tip[0], .5) + (R() - .5) * 6, lerp(y, tip[1], .5)], tip], { w: 1.6, wob: .5, over: 2, seed: 2200 + i * 10 + k }, t0 + k * .04, .08); for (let b = 0; b < 2; b++) { const u = .4 + b * .25, p = [lerp(x, tip[0], u), lerp(y, tip[1], u)], sd = b ? 1 : -1; penB([p, [p[0] + Math.cos(a + sd * .9) * 12, p[1] + Math.sin(a + sd * .9) * 12]], { w: 1.2, wob: .2, over: 0, seed: 2300 + i * 10 + k * 2 + b, smooth: false }, t0 + .2 + k * .04, .04); } }
  }
  // rocks
  for (let i = 0; i < 14; i++) { const x = 140 + R() * 1880, y = 3100 + R() * 1900; if (Math.abs(x - pathX(y)) < 170 || !inPage(x, y, 120)) continue; const r = 26 + R() * 30, rock = [[x - r, y], [x - r * .7, y - r * .7], [x + r * .2, y - r * .9], [x + r, y - r * .3], [x + r * .9, y]]; wash(cx, rock, C.stoneD, { a: .35, j: 3, layers: 2, edge: .2, seed: 2400 + i }); penB(rock, { w: 1.8, wob: .5, over: 2, seed: 2450 + i, smooth: false }, landT(y), .12); }

  // ================= The hill and the cross =================
  const hill = []; for (let i = 0; i <= 30; i++) { const u = i / 30, x = lerp(330, 1830, u); hill.push([x, HILL_TOP + 40 + 640 * Math.pow(Math.abs(u - .5) * 2, 2.4) - 24 * Math.sin(u * 9)]); }
  const hillPoly = [...hill, [1830, 5880], [330, 5880]];
  wash(cx, hillPoly, C.hill, { a: .42, j: 18, layers: 3, edge: .1, seed: 2500 });
  wash(cx, [...hill.slice(15), [1830, 5880], [1080, 5880]], C.hillD, { a: .2, j: 14, layers: 2, edge: .05, seed: 2501 });
  for (let i = 0; i < 300; i++) { const x = 330 + R() * 1500, y = 5560 + R() * 380; if (R() > .5) continue; dab(cx, x, y, 5 + R() * 10, R() * TAU, R() < .5 ? C.hill : C.hillD, .25 + R() * .25, 2600 + i); }
  const behindCross = (x, y) => Math.abs(x - CROSS.x) < 30 && y < CROSS.base + 10; visible(hill, behindCross).forEach((f, k) => penB(f, { w: 2.4, wob: 1, over: 6, seed: 2510 + k }, 46.5 + k * .25, .45));
  for (let i = 0; i < 26; i++) { const x = 420 + R() * 1320, y = 5420 + R() * 380; if (y < hillY(hill, x) + 30) continue; penB([[x, y], [x + 3, y - 14 - R() * 10]], { w: 1.3, wob: .3, over: 0, seed: 2520 + i, smooth: false }, 46.9 + R() * .3, .04); }
  // the cross: wood, drawn last (vertical, then the crossbar)
  const { x: X, top, base, bar, hw } = CROSS, vw = 34;
  const vert = [[X - vw / 2, base], [X - vw / 2, top], [X + vw / 2, top], [X + vw / 2, base]], hor = [[X - hw, bar - 16], [X + hw, bar - 16], [X + hw, bar + 18], [X - hw, bar + 18]];
  for (const p of [vert, hor]) { wash(cx, p, C.wood, { a: .6, j: 3, layers: 3, edge: .3, seed: p.length + p[0][0] | 0 }); }
  wash(cx, [[X + 4, base], [X + 4, top], [X + vw / 2, top], [X + vw / 2, base]], C.woodD, { a: .3, j: 2, layers: 2, edge: .1, seed: 2700 });
  penB([[X - vw / 2, top], [X - vw / 2 - 1, base + 6]], { w: 3.2, wob: .7, over: 6, seed: 2710, smooth: false }, 47.3, .55);
  penB([[X + vw / 2, top - 4], [X + vw / 2 + 1, base + 8]], { w: 3.4, wob: .7, over: 6, seed: 2711, smooth: false }, 47.42, .55);
  penB([[X - vw / 2, top], [X + vw / 2, top]], { w: 3, wob: .4, over: 3, seed: 2712, smooth: false }, 48.0, .06);
  penB([[X - hw, bar - 16], [X + hw + 4, bar - 17]], { w: 3.2, wob: .7, over: 6, seed: 2713, smooth: false }, 48.1, .32);
  penB([[X - hw - 3, bar + 18], [X + hw, bar + 18]], { w: 3.4, wob: .7, over: 6, seed: 2714, smooth: false }, 48.24, .32);
  penB([[X - hw, bar - 16], [X - hw, bar + 18]], { w: 2.8, wob: .4, over: 2, seed: 2715, smooth: false }, 48.5, .05);
  penB([[X + hw, bar - 16], [X + hw, bar + 18]], { w: 2.8, wob: .4, over: 2, seed: 2716, smooth: false }, 48.55, .05);
  for (let k = 0; k < 4; k++) penB([[X - 6 + k * 4, top + 60 + k * 140], [X - 5 + k * 4, top + 120 + k * 140]], { w: 1.2, wob: .4, over: 0, seed: 2720 + k, smooth: false }, 48.6, .04);

  // ================= Page edge =================
  {
    const [mc, mx] = cv(W, H); const img = mx.createImageData(W, H), d = img.data;
    for (let y = 0; y < H; y += 2) for (let x = 0; x < W; x += 2) { if (pageMask(x, y) < 0) for (const [ox, oy] of [[0, 0], [1, 0], [0, 1], [1, 1]]) { const k = ((y + oy) * W + x + ox) * 4; d[k] = d[k + 1] = d[k + 2] = d[k + 3] = 255; } }
    mx.putImageData(img, 0, 0);
    cx.save(); cx.globalCompositeOperation = 'source-over'; cx.drawImage(mc, 0, 0); cx.restore();   // white (= paper) outside the page
    for (const c of [ia, ib]) { c.save(); c.globalCompositeOperation = 'destination-out'; c.drawImage(mc, 0, 0); c.restore(); }
    const Rm = rng(77); cx.globalCompositeOperation = 'multiply';
    for (let i = 0; i < 9000; i++) { const x = Rm() * W, y = Rm() * H, m = pageMask(x, y); if (m < 0 && m > -60 && Rm() < (1 + m / 60) * .6) { const col = y < EDEN_Y ? (Rm() < .5 ? LEAF.light : C.lawn) : (Rm() < .5 ? C.earth : C.hill); dab(cx, x, y, 4 + Rm() * 10, Rm() * TAU, col, .25 + Rm() * .3, 40000 + i); } }
    cx.globalCompositeOperation = 'source-over';
  }

  // ================= Pack into textures =================
  const pack = (r, g) => { const out = new Uint8Array(W * H * 4); const A = r.getImageData(0, 0, W, H).data; for (let i = 0, n = W * H; i < n; i++) out[i * 4] = A[i * 4 + 3]; const B = g.getImageData(0, 0, W, H).data; for (let i = 0, n = W * H; i < n; i++) { out[i * 4 + 1] = B[i * 4 + 3]; out[i * 4 + 3] = 255; } return out; };
  const packT = (r, g) => { const out = new Uint8Array(W * H * 4); const A = r.getImageData(0, 0, W, H).data, B = g.getImageData(0, 0, W, H).data; for (let i = 0, n = W * H; i < n; i++) { out[i * 4] = A[i * 4]; out[i * 4 + 1] = B[i * 4]; out[i * 4 + 3] = 255; } return out; };
  const ink = pack(ia, ib), time = packT(ta, tb);
  return { W, H, color: colorC, ink, time, winA: WIN_A, winB: WIN_B, strokes };
}

// scalloped crown outline fragments (only part of the outline is inked)
function scallop(c, R, k, all) {
  const out = []; let cur = []; const n = 40; const a0 = R() * TAU;
  for (let i = 0; i <= n; i++) {
    const a = a0 + i / n * TAU, rr = c.r * (.98 + .08 * Math.sin(i * 1.1)), p = [c.x + Math.cos(a) * rr, c.y + Math.sin(a) * rr * .92];
    const inside = (all || []).some(o => o !== c && Math.hypot(p[0] - o.x, (p[1] - o.y) / .92) < o.r * .97);
    if (inside || (i % 9 === 8 && R() < .5 * k)) { if (cur.length > 2) out.push(cur); cur = []; } else cur.push(p);
  }
  if (cur.length > 2) out.push(cur);
  return out;
}
// split a polyline where it passes behind an occluder (static ink cannot be hidden by later washes)
function visible(pl, hidden) { const out = []; let cur = []; for (const p of resample(pl, 12)) { if (hidden(p[0], p[1])) { if (cur.length > 1) out.push(cur); cur = []; } else cur.push(p); } if (cur.length > 1) out.push(cur); return out; }
const inCrown = (x, y, crowns, m = .95) => crowns.some(o => Math.hypot(x - o.x, (y - o.y) / .92) < o.r * m);
const behindTree = (x, y) => inCrown(x, y, CROWN) || inCrown(x, y, LIFE) || (x > 1030 && x < 1135 && y > 1600 && y < 2240) || (x > 365 && x < 440 && y > 1450 && y < 1990);
function thick(pl, w) { const L = pl.map(([x, y]) => [x, y - w]), Rr = pl.map(([x, y]) => [x, y + w]); return [...L, ...Rr.reverse()]; }
function hillY(hill, x) { let best = hill[0]; for (const p of hill) if (Math.abs(p[0] - x) < Math.abs(best[0] - x)) best = p; return best[1]; }
export function pathX(y) { for (let i = 1; i < PATHC.length; i++) { const [x0, y0] = PATHC[i - 1], [x1, y1] = PATHC[i]; if (y <= y1) return lerp(x0, x1, clamp((y - y0) / (y1 - y0))); } return PATHC[PATHC.length - 1][0]; }
