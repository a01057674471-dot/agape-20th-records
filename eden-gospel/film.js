// 동산의 동편 (East of the Garden) — timeline: camera, performances, colour fields, handwriting, sound events
import { clamp, lerp, ss, TAU, n2, hex, mix3, INK, PAPER, rgba, rough, ellipse, spline, arrivalField, sampleField, compositor, figure, drawPrims, penStroke, drawPen, dab, foliage, handwrite, R3, LEAF } from './engine.js';
import { buildWorld, W, H, FRUIT, TRUNK, EDEN_Y, SWORD, CROSS, BUSH, C } from './world.js';
import { walk, stand, mixPose } from './poses.js';
const { V, ry } = R3;

export const BPM = 72, BEAT = 60 / BPM, BAR = BEAT * 3;
const DUR = 66;
const SW = innerWidth, SH = innerHeight;            // 1080 × 1920
const FONT = '"Nanum Pen Script"';
await document.fonts.load(`80px ${FONT}`);

// ---------------- helpers ----------------
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const eo = t => 1 - Math.pow(1 - clamp(t), 3), ei = t => Math.pow(clamp(t), 3);
const seg = (t, a, b) => clamp((t - a) / (b - a));
const boilOf = t => Math.floor(t * 12) % 3;
const lerp2 = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u)];
function keys(K, ease = eio) {           // [[t, [..values]], ...] → eased piecewise interpolation
  return t => {
    if (t <= K[0][0]) return K[0][1].slice(); if (t >= K[K.length - 1][0]) return K[K.length - 1][1].slice();
    let i = 0; while (t > K[i + 1][0]) i++;
    const u = ease((t - K[i][0]) / (K[i + 1][0] - K[i][0]));
    return K[i][1].map((v, j) => lerp(v, K[i + 1][1][j], u));
  };
}
function curve(K) {                      // Catmull-Rom over time (for paths)
  const n = K.length, T = K.map(k => k[0]);
  const m = K.map((k, i) => { const a = K[Math.max(0, i - 1)], b = K[Math.min(n - 1, i + 1)]; const dt = b[0] - a[0] || 1; return [(b[1][0] - a[1][0]) / dt, (b[1][1] - a[1][1]) / dt]; });
  return t => {
    if (t <= T[0]) return K[0][1].slice(); if (t >= T[n - 1]) return K[n - 1][1].slice();
    let i = 0; while (t > T[i + 1]) i++;
    const h = T[i + 1] - T[i], u = (t - T[i]) / h, u2 = u * u, u3 = u2 * u;
    const h00 = 2 * u3 - 3 * u2 + 1, h10 = u3 - 2 * u2 + u, h01 = -2 * u3 + 3 * u2, h11 = u3 - u2;
    return [0, 1].map(j => h00 * K[i][1][j] + h10 * h * m[i][j] + h01 * K[i + 1][1][j] + h11 * h * m[i + 1][j]);
  };
}

// ---------------- world and colour fields ----------------
const world = buildWorld();
const gw = 432, gh = 1296;
const edenMask = (x, y) => y < EDEN_Y;
const A1 = arrivalField(W, H, gw, gh, [{ x: FRUIT[0], y: FRUIT[1], t: 3.6, v: 650, mask: edenMask }], { amp: 150 });
const DEP = arrivalField(W, H, gw, gh, [{ x: FRUIT[0], y: FRUIT[1], t: 15.3, v: 560, mask: edenMask }], { amp: 150 });
const A2 = arrivalField(W, H, gw, gh, [{ x: CROSS.x, y: CROSS.bar, t: 48.8, v: 540, sy: .92 }], { amp: 170 });
const arr = new Float32Array(gw * gh * 4);
for (let i = 0; i < gw * gh; i++) { arr[i * 4] = Math.min(A1[i], 9999); arr[i * 4 + 1] = Math.min(DEP[i], 9999); arr[i * 4 + 2] = Math.min(A2[i], 9999); arr[i * 4 + 3] = 0; }
const glc = document.createElement('canvas'); glc.width = SW; glc.height = SH;
const comp = compositor(glc, { ...world, arr, gw, gh });
const cvs = document.getElementById('c'); cvs.width = SW; cvs.height = SH;
const ctx = cvs.getContext('2d');
const fld = (F, x, y) => sampleField(F, W, H, gw, gh, x, y);
// how much colour a dynamic thing at (x, y) has: Eden arrival, drained by sin, restored from the cross
function colorAt(x, y, t) {
  const a1 = clamp((t - fld(A1, x, y) - .05) / .45), d = clamp((t - fld(DEP, x, y)) / .5), a2 = clamp((t - fld(A2, x, y) - .05) / .45);
  return Math.max(a1 * (1 - d), a2);
}
// paper tooth pattern (multiplied over everything, figures included)
const toothPat = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); const img = x.createImageData(256, 256); for (let i = 0; i < 256 * 256; i++) { const px = i % 256, py = i / 256 | 0; const v = 255 - 14 * Math.pow(n2(px * .35, py * .35, 3), 3) - 6 * n2(px * .9, py * .12, 5); img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = v; img.data[i * 4 + 3] = 255; } x.putImageData(img, 0, 0); return ctx.createPattern(c, 'repeat'); })();

// ---------------- camera ----------------
const camKeys = keys([
  [0, [1262, 1700, 2.4]], [3.4, [1262, 1700, 2.5]], [7.6, [1080, 1470, .62]], [10.3, [1080, 1440, .645]],
  [11.4, [1255, 1830, 1.15]], [14.95, [1262, 1845, 1.22]], [15.0, [1262, 1860, 1.4]], [18.0, [1228, 1890, 1.0]], [21.6, [1225, 1885, 1.0]],
  [22.7, [1080, 690, 1.0]], [26.45, [1080, 670, 1.03]], [26.95, [910, 2330, 1.5]], [33.2, [930, 2330, 1.56]],
  [34.0, [1450, 2030, 1.1]], [39.0, [1440, 2040, 1.12]], [41.0, [1200, 2920, .9]], [46.5, [1200, 2940, .9]],
  [48.0, [1080, 4840, .85]], [54.4, [1080, 4830, .9]], [56.8, [1080, 4300, .6]], [59.4, [1080, 3240, .29]], [60.6, [1080, 3240, .29]], [66, [1080, 4420, .40]],
]);
function camera(t) {
  let [cx, cy, z] = camKeys(t); let rot = 0;
  if (t >= 15.0 && t < 15.12) z = lerp(1.22, 1.4, eo(seg(t, 15.0, 15.08)));          // punch-in on the bite
  if (t >= 15.0 && t < 15.45) { const k = Math.exp(-(t - 15.0) / .11); cx += Math.sin(t * 93) * 13 * k / z; cy += Math.cos(t * 77) * 10 * k / z; }
  if (t > 26.45 && t < 26.95) rot = .07 * Math.sin(seg(t, 26.45, 26.95) * Math.PI);   // whip-tilt with a slight roll
  return { cx, cy, z, rot };
}
const toScreen = (cam, x, y) => { const c = Math.cos(cam.rot), s = Math.sin(cam.rot), dx = (x - cam.cx) * cam.z, dy = (y - cam.cy) * cam.z; return [SW / 2 + c * dx - s * dy, SH / 2 + s * dx + c * dy]; };

// ---------------- the couple ----------------
const SKIN_E = hex('#e9c2a2'), SKIN_A = hex('#d29c7c'), HAIR_E = hex('#6b4a32'), HAIR_A = hex('#3a2a22');
const LOOK = {
  eve: { skin: SKIN_E, top: SKIN_E, bottom: SKIN_E, hair: HAIR_E, hairLong: 1, torso: [.08, .066, .09], shoe: SKIN_E },
  adam: { skin: SKIN_A, top: SKIN_A, bottom: SKIN_A, hair: HAIR_A, curly: 1, torso: [.078, .086, .108], shoe: SKIN_A },
  eve2: { skin: SKIN_E, top: hex('#a77b54'), hair: HAIR_E, hairLong: 1, dress: 1, sleeve: 'none', flare: .16, torso: [.082, .07, .094], shoe: hex('#7a5a40') },
  adam2: { skin: SKIN_A, top: hex('#93684a'), bottom: hex('#7d5a40'), sleeve: 'none', hair: HAIR_A, curly: 1, torso: [.08, .088, .11], shoe: hex('#6a4a35') },
};
const EVE0 = { x: 1335, y: 2240, S: 520, yaw: -1.25 }, ADAM0 = { x: 1585, y: 2252, S: 540, yaw: -2.05 };
// screen point (world) → body coordinates for a hand target (q2 = depth in front of the body)
function toBody(place, X, Y, q2 = .12) { const q = [(X - place.x) / place.S, (place.y - Y) / place.S - q2 * .28, q2]; return ry(q, -place.yaw); }
const crouch = o => ({ hipY: .27, lean: .72, nod: -.55, headYaw: 0, footL: V(-.09, .03, .16), footR: V(.09, .03, .12), handL: V(-.07, .36, .3), handR: V(.07, .38, .3), elbL: V(-1, -.4, .2), elbR: V(1, -.4, .2), ...o });
const COUPLE = curve([[39.0, [1445, 2245]], [40.4, [1290, 2440]], [42.4, [1128, 2960]], [44.0, [1060, 3220]], [45.6, [960, 3520]], [46.8, [905, 3900]], [47.9, [990, 4330]], [48.2, [1000, 4350]]]);
// footfalls land on the beat: a foot plants at sin(ph) = ±1, half a beat after each multiple of π
const WALK0 = 39 + 1 / 6 - BEAT / 2;
const walkPh = t => (t - WALK0) * Math.PI / BEAT * clamp(1 - seg(t, 47.9, 48.25));
export const STEPS = []; for (let t = WALK0 + BEAT / 2; t < 47.95; t += BEAT) STEPS.push(+t.toFixed(3));

// the fruit's position is tied to hands; keep the hand targets here
const HANDOFF = lerp2([1450, 1890], [1470, 1880], 0);
function evePose(t) {
  let p = stand({ nod: -.05, headYaw: .1 });
  // reach for the fruit, pluck, bring it to the mouth, hand it to Adam
  const reach = ss(seg(t, 11.3, 11.9)) * (1 - ss(seg(t, 12.05, 12.45)));
  const toMouth = ss(seg(t, 12.35, 12.75)) * (1 - ss(seg(t, 12.95, 13.25)));
  const give = ss(seg(t, 13.05, 13.55)) * (1 - ss(seg(t, 13.75, 14.2)));
  if (reach + toMouth + give > 0) {
    const rest = [EVE0.x + 60, EVE0.y - 260];
    let tgt = rest;
    tgt = lerp2(tgt, [FRUIT[0] + 6, FRUIT[1] + 14], reach);
    tgt = lerp2(tgt, [EVE0.x - 18, EVE0.y - 470], toMouth);
    tgt = lerp2(tgt, HANDOFF, give);
    p.handR = toBody(EVE0, tgt[0], tgt[1], .18); p.elbR = V(1, -.6, -.3);
    p.headYaw = .1 - .35 * reach; p.nod = -.05 + .3 * reach - .1 * give;
  }
  // after the fall: crouch behind the bush, hands to the face
  const hide = ss(seg(t, 16.9, 17.9)) * (1 - ss(seg(t, 31.9, 32.8)));
  if (hide > 0) p = mixPose(p, crouch({ headYaw: -.3 }), hide);
  // standing, head bowed, then turned toward the path
  if (t > 32.8) { p.nod = -.38; p.headYaw = .2; }
  return p;
}
function adamPose(t) {
  let p = stand({ nod: -.05 });
  const take = ss(seg(t, 13.2, 13.6)) * (1 - ss(seg(t, 13.95, 14.3)));
  const eat = ss(seg(t, 14.25, 14.85)) * (1 - ss(seg(t, 15.25, 15.85)));
  const drop = ss(seg(t, 15.85, 16.1)) * (1 - ss(seg(t, 16.3, 16.8)));
  if (take + eat + drop > 0) {
    let tgt = [ADAM0.x - 70, ADAM0.y - 270];
    tgt = lerp2(tgt, [HANDOFF[0] + 12, HANDOFF[1] - 4], take);
    tgt = lerp2(tgt, [ADAM0.x - 26, ADAM0.y - 480], eat);
    tgt = lerp2(tgt, [ADAM0.x - 80, ADAM0.y - 330], drop);
    p.handL = toBody(ADAM0, tgt[0], tgt[1], .2); p.elbL = V(-1, -.6, -.2);
    p.nod = -.05 + .12 * eat;
  }
  const hide = ss(seg(t, 16.7, 17.7)) * (1 - ss(seg(t, 31.9, 32.8)));
  if (hide > 0) p = mixPose(p, crouch({ headYaw: .3, lean: .8 }), hide);
  if (t > 32.8) { p.nod = -.4; p.headYaw = -.15; }
  return p;
}
// both figures at time t → [{place, pose, look}]
function couple(t) {
  if (t < 39.0) {
    const hideShift = ss(seg(t, 16.9, 17.9)) * (1 - ss(seg(t, 31.9, 32.8)));
    const turn = ss(seg(t, 37.4, 38.9));
    const e = { ...EVE0, x: EVE0.x + 40 * hideShift, yaw: lerp(EVE0.yaw, Math.PI - .25, turn) };
    const a = { ...ADAM0, x: ADAM0.x - 40 * hideShift, yaw: lerp(ADAM0.yaw, Math.PI - .35, turn) };
    return [{ who: 'eve', place: e, pose: evePose(t) }, { who: 'adam', place: a, pose: adamPose(t) }];
  }
  // exile: walking down the page, side by side, heads bowed; at the hill they stop and look up at the cross
  const c = COUPLE(t), c2 = COUPLE(t + .05), dx = c2[0] - c[0], dy = c2[1] - c[1], mv = Math.hypot(dx, dy) > .5;
  const yaw = Math.PI + clamp(Math.atan2(dx, dy) * .6, -.6, .6) * (mv ? 1 : 0);
  const k = ss(seg(t, 39.0, 39.8)), ph = walkPh(t), stop = seg(t, 47.9, 48.25);
  const look = ss(seg(t, 50.0, 51.2));
  const poseE = mixPose(walk(ph, { nod: -.35 }), stand({ nod: lerp(-.38, .12, look) }), Math.max(1 - k, ss(stop)));
  const poseA = mixPose(walk(ph + Math.PI, { nod: -.38 }), stand({ nod: lerp(-.4, .1, look) }), Math.max(1 - k, ss(stop)));
  const e = { x: lerp(EVE0.x, c[0] - 100, k), y: lerp(EVE0.y, c[1], k), S: 520, yaw: lerp(Math.PI - .25, yaw, k) };
  const a = { x: lerp(ADAM0.x, c[0] + 105, k), y: lerp(ADAM0.y, c[1] - 26, k), S: 540, yaw: lerp(Math.PI - .35, yaw, k) };
  if (stop > 0) { e.yaw = lerp(e.yaw, Math.PI, ss(stop)); a.yaw = lerp(a.yaw, Math.PI, ss(stop)); }
  return [{ who: 'eve', place: e, pose: poseE }, { who: 'adam', place: a, pose: poseA }];
}
const GARB = 34.9;    // the pen draws the garments of skin, colour blooms after
function figureColor(x, y, t) { if (t < 15) return colorAt(x, y - 260, t); const g = clamp((t - 35.3) / 1.1); return Math.max(g, t < 17 ? colorAt(x, y - 260, t) : 0); }

// ---------------- props ----------------
// the fruit: position, bites, colour
function fruitState(t, hands) {
  let p = [FRUIT[0] + 3 * Math.sin(t * 1.3), FRUIT[1] + 2 * Math.sin(t * 1.7)];
  if (t >= 12.0 && t < 13.75) p = hands.eve;
  else if (t >= 13.75 && t < 16.15) p = hands.adam;
  else if (t >= 16.15) { const u = clamp((t - 16.15) / .38); const drop0 = [ADAM0.x - 80, ADAM0.y - 330]; p = [drop0[0] + 18 * u, lerp(drop0[1], ADAM0.y + 8, u * u)]; }
  const bites = (t >= 12.8 ? 1 : 0) + (t >= 15.0 ? 1 : 0);
  const col = clamp((t - 1.0) / .5) * (1 - clamp((t - 15.15) / .9));
  return { p, bites, col };
}
const RED = hex('#c4373a');
function fruitPrims(p, bites, b) {
  const [x, y] = p, r = 21;
  let body = ellipse(x, y, r * 1.02, r, 18);
  const prims = [{ k: 'knock', poly: ellipse(x, y, r * 1.15, r * 1.1, 14), a: .9 }, { k: 'wash', poly: body, col: RED, a: .85, seed: 3 + b, dx: 2, dy: 1, j: 2 },
    { k: 'wash', poly: ellipse(x + 6, y + 7, r * .6, r * .45, 12), col: mix3(RED, [70, 30, 60], .45), a: .4, seed: 4 + b }];
  if (bites > 0) prims.push({ k: 'knock', poly: ellipse(x + r * .95, y - r * .3, r * .45, r * .5, 12), a: 1 });
  if (bites > 1) prims.push({ k: 'knock', poly: ellipse(x - r * .9, y + r * .2, r * .42, r * .48, 12), a: 1 });
  prims.push({ k: 'ink', st: penStroke(ellipse(x, y, r, r * .98, 16, -1.2).slice(0, 15), { w: 2.2, wob: .5, seed: 7 + b, over: 3, smooth: false }) });
  prims.push({ k: 'ink', st: penStroke([[x, y - r], [x + 2, y - r - 14]], { w: 2, wob: .3, seed: 8, over: 1 }) });
  const leaf = [[x + 2, y - r - 8], [x + 18, y - r - 22], [x + 36, y - r - 16], [x + 16, y - r - 6]];
  prims.push({ k: 'wash', poly: leaf, col: LEAF.mid, a: .6, seed: 9 }, { k: 'ink', st: penStroke(leaf, { w: 1.6, wob: .3, seed: 10, over: 2 }) });
  return prims;
}
// the serpent: a tapered body along a path, olive wash, ink edges, a head
const OLIVE = hex('#7d8a4a');
function serpentPrims(path, w, seed) {
  const P = spline(path, 8), n = P.length, L = [], Rr = [];
  for (let i = 0; i < n; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(n - 1, i + 1)]; let nx = -(b[1] - a[1]), ny = b[0] - a[0]; const l = Math.hypot(nx, ny) || 1; nx /= l; ny /= l; const ww = w * (.25 + .75 * Math.sin(Math.PI * Math.min(1, (i / (n - 1)) * 1.08 + .04))); L.push([P[i][0] + nx * ww, P[i][1] + ny * ww]); Rr.push([P[i][0] - nx * ww, P[i][1] - ny * ww]); }
  const body = [...L, ...Rr.slice().reverse()], h = P[n - 1], h0 = P[n - 3], ang = Math.atan2(h[1] - h0[1], h[0] - h0[0]);
  const head = ellipse(h[0] + Math.cos(ang) * w * .8, h[1] + Math.sin(ang) * w * .8, w * 1.5, w * 1.05, 12, ang);
  const prims = [{ k: 'knock', poly: body, a: .85 }, { k: 'wash', poly: body, col: OLIVE, a: .7, seed, dx: 1.5, j: 1.5 }, { k: 'knock', poly: head, a: .85 }, { k: 'wash', poly: head, col: OLIVE, a: .75, seed: seed + 1, j: 1 }];
  for (let i = 4; i < n - 6; i += 7) prims.push({ k: 'wash', poly: ellipse(P[i][0], P[i][1], w * .45, w * .3, 8), col: mix3(OLIVE, [40, 40, 30], .5), a: .5, seed: seed + i });
  prims.push({ k: 'ink', st: penStroke(L, { w: 2, wob: .5, seed: seed + 2, over: 2, smooth: false }) }, { k: 'ink', st: penStroke(Rr, { w: 2.2, wob: .5, seed: seed + 3, over: 2, smooth: false, gap: .4 }) });
  prims.push({ k: 'ink', st: penStroke(head.slice(0, 11), { w: 2, wob: .3, seed: seed + 4, over: 1, smooth: false }) });
  const ex = h[0] + Math.cos(ang) * w * 1.1 - Math.sin(ang) * w * .4, ey = h[1] + Math.sin(ang) * w * 1.1 + Math.cos(ang) * w * .4;
  prims.push({ k: 'fn', fn: c => { c.fillStyle = rgba(INK, .9); c.beginPath(); c.arc(ex, ey, w * .18, 0, TAU); c.fill(); } });
  return prims;
}
function serpentOnBranch(t) {
  const sw = Math.sin(t * 2.1) * 6, lift = ss(seg(t, 10.6, 11.4)) * (1 - ss(seg(t, 15.0, 16.0)));
  return [[930, 1555], [985, 1600], [1040, 1585], [1090, 1612], [1140, 1590], [1180, 1615], [1215 + sw * .3, 1598 - 18 * lift], [1238 + sw, 1580 - 40 * lift], [1262 + sw, 1572 - 52 * lift]];
}
function serpentOnGround(t) {
  const u = eo(seg(t, 26.6, 28.7)), x0 = lerp(1010, 760, u), ph = t * 3.2 * (1 - seg(t, 28.4, 28.9));
  const pts = []; for (let i = 0; i < 10; i++) { const s = 1 - i / 9; pts.push([x0 + s * 300, 2448 + Math.sin(ph + s * 7) * 16 * (.4 + s * .6)]); }
  return pts;
}
// heel of the woman's seed (3:15): a foot drawn in profile, pressing down on the serpent's head
function heelPrims(t) {
  const press = ss(seg(t, 29.1, 29.35)) * 12, x = 742, y = 2392 + press;
  const foot = [[x - 46, y - 120], [x - 40, y - 40], [x - 28, y + 6], [x + 10, y + 16], [x + 90, y + 20], [x + 140, y + 14], [x + 150, y], [x + 110, y - 14], [x + 40, y - 34], [x + 18, y - 70], [x + 20, y - 120]];
  return [{ k: 'knock', poly: foot, a: .95 }, { k: 'wash', poly: foot, col: SKIN_E, a: .45, seed: 31, dx: 2 }, { k: 'ink', st: penStroke(foot, { w: 2.6, wob: .6, seed: 32, over: 4, smooth: true }) }];
}
// the lamb (3:21): drawn by the pen, a red drop, then lying down
const LAMB = [1770, 2440];
function lambPrims(t) {
  const lie = ss(seg(t, 36.6, 37.6)), [x, y0] = LAMB, y = y0 + 34 * lie, legL = 54 * (1 - lie * .8);
  const body = []; for (let i = 0; i < 16; i++) { const a = i / 16 * TAU, r = 1 + .12 * Math.sin(i * 3.1); body.push([x + Math.cos(a) * 92 * r, y - legL - 50 + Math.sin(a) * 52 * r]); }
  const head = ellipse(x - 98, y - legL - 74 + 20 * lie, 30, 22, 12, -.35), ear = [[x - 100, y - legL - 92], [x - 72, y - legL - 104 + 10 * lie], [x - 82, y - legL - 86]];
  const prims = [{ k: 'knock', poly: body, a: .95 }, { k: 'wash', poly: body, col: hex('#efe8d8'), a: .5, seed: 41 }, { k: 'wash', poly: body.slice(2, 9).concat([[x, y - legL - 50]]), col: hex('#b8b3cc'), a: .35, seed: 42 },
    { k: 'knock', poly: head, a: .95 }, { k: 'wash', poly: head, col: hex('#d9cbb6'), a: .55, seed: 43 }];
  prims.push({ k: 'ink', st: penStroke([...body, body[0], body[1]], { w: 2.2, wob: .8, seed: 44, over: 3, smooth: true, gap: .4 }) });
  prims.push({ k: 'ink', st: penStroke(head.slice(0, 11), { w: 2, wob: .4, seed: 45, over: 2 }) }, { k: 'ink', st: penStroke(ear, { w: 1.6, wob: .3, seed: 46, over: 1 }) });
  for (const lx of [-50, -26, 30, 56]) prims.push({ k: 'ink', st: penStroke([[x + lx, y - legL - 8], [x + lx + 2, y]], { w: 2, wob: .4, seed: 47 + lx, over: 1, smooth: false }) });
  for (let k = 0; k < 6; k++) { const a = k * 1.1, cx2 = x + Math.cos(a) * 46, cy2 = y - legL - 52 + Math.sin(a) * 22; prims.push({ k: 'ink', st: penStroke(ellipse(cx2, cy2, 12, 9, 8, a).slice(0, 6), { w: 1.3, wob: .3, seed: 60 + k, over: 0 }), alpha: .6 }); }
  return prims;
}
// the flaming sword (3:24), turning every way above the gate
function swordPrims(t, life) {
  const ang = (t - 42.6) * 1.5, [cx, cy] = SWORD, L = 250 * life;
  const d = [Math.cos(ang), Math.sin(ang) * .55], nrm = [-d[1], d[0]];
  const tip = [cx + d[0] * L, cy + d[1] * L], hilt = [cx - d[0] * L * .55, cy - d[1] * L * .55];
  const blade = [[hilt[0] + nrm[0] * 9, hilt[1] + nrm[1] * 9], [tip[0], tip[1]], [hilt[0] - nrm[0] * 9, hilt[1] - nrm[1] * 9]];
  return { blade, hilt, tip, d, nrm, ang };
}

// ---------------- dynamic drawing helpers ----------------
function inkProgress(prims, t, t0, t1) {
  const inks = prims.filter(p => p.k === 'ink'), n = inks.length, u = seg(t, t0, t1);
  const map = new Map(); inks.forEach((p, i) => map.set(p, clamp(u * n - i * .75)));
  return p => map.get(p) ?? 1;
}
const bloomClip = (cx, cy, R, seed) => c => { c.beginPath(); const n = 24; for (let i = 0; i <= n; i++) { const a = i / n * TAU, r = R * (.8 + .4 * n2(Math.cos(a) * 2 + seed, Math.sin(a) * 2, seed)); const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r; i ? c.lineTo(x, y) : c.moveTo(x, y); } c.closePath(); };
function shadow(x, y, S, a) { if (a <= 0) return; ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = rgba(hex('#7a7a6a'), a); ctx.beginPath(); ctx.ellipse(x + S * .06, y + 4, S * .2, S * .04, 0, 0, TAU); ctx.fill(); ctx.restore(); }

// the flowering bush in front of the couple (dynamic so it can hide them)
const BUSH_KNOCK = BUSH.map(c => rough(ellipse(c.x, c.y, c.r * 1.02, c.r * .9, 20), c.r * .08, c.x));
const BUSH_INK = BUSH.flatMap((c, i) => { const frags = []; let cur = []; for (let k = 0; k <= 30; k++) { const a = k / 30 * TAU, rr = c.r * (1 + .07 * Math.sin(k * 2.3)), p = [c.x + Math.cos(a) * rr, c.y + Math.sin(a) * rr * .9]; const inside = BUSH.some(o => o !== c && Math.hypot(p[0] - o.x, (p[1] - o.y) / .9) < o.r * .96) || a > .25 * Math.PI && a < .75 * Math.PI; if (inside) { if (cur.length > 2) frags.push(cur); cur = []; } else cur.push(p); } if (cur.length > 2) frags.push(cur); return frags.map((f, k) => penStroke(f, { w: 2.2, wob: .8, over: 3, gap: .4, seed: 300 + i * 7 + k })); });
const BUSH_FLOWERS = (() => { const out = []; let s = 7; for (const c of BUSH) for (let k = 0; k < 9; k++) { s = (s * 9301 + 49297) % 233280; const a = s / 233280 * TAU, r = c.r * (.25 + ((s * 7) % 100) / 100 * .6); out.push([c.x + Math.cos(a) * r, c.y + Math.sin(a) * r * .8, k % 3]); } return out; })();
function drawBush(t) {
  const inkT = 3.3; if (t < inkT) return;
  const col = colorAt(1480, 2150, t), ip = seg(t, inkT, inkT + .5);
  ctx.save(); ctx.fillStyle = rgba(PAPER, .97); for (const p of BUSH_KNOCK) { ctx.beginPath(); p.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fill(); } ctx.restore();
  if (col > 0) {
    ctx.save(); ctx.globalAlpha = col;
    foliage(ctx, BUSH, { seed: 501, dens: 1.2, scale: .8 });
    ctx.globalCompositeOperation = 'multiply';
    for (const [x, y, k] of BUSH_FLOWERS) for (let j = 0; j < 4; j++) dab(ctx, x + Math.cos(j * 1.6) * 6, y + Math.sin(j * 1.6) * 4, 6, j, [hex('#e7a0a8'), hex('#f2efe4'), hex('#e9c46a')][k], .6, 800 + x + j | 0);
    ctx.restore();
  }
  for (const st of BUSH_INK) drawPen(ctx, st, ip);
}

// ---------------- handwriting ----------------
// every text: lines [text, x, y, size, align], written on from w0 over wd seconds (line after line), gone at t1
const TXT = [
  { id: 'forbid', w0: 6.3, wd: 1.3, t1: 10.35, lines: [['단 하나의 열매만 금하셨다', 1080, 420, 100, 'center']] },
  { id: 'ate', w0: 11.0, wd: 1.8, t1: 16.75, halo: 1, lines: [['여자가 그 실과를 따먹고 …', 1255, 2405, 56, 'center'], ['그도 먹은지라 (창 3:6)', 1255, 2480, 56, 'center']] },
  { id: 'hid', w0: 17.25, wd: 1.1, t1: 21.4, lines: [['그들은 나무 사이에 숨었다', 1228, 2600, 70, 'center']] },
  { id: 'where', w0: 22.75, wd: .9, t1: 26.42, lines: [['네가 어디 있느냐', 1080, 640, 150, 'center'], ['창 3:9', 1080, 760, 64, 'center']] },
  { id: 'seed', w0: 27.1, wd: 1.6, t1: 33.15, lines: [['여자의 후손은 네 머리를', 930, 2720, 56, 'center'], ['상하게 할 것이요', 930, 2800, 56, 'center'], ['창 3:15', 930, 2872, 44, 'center']] },
  { id: 'garment', w0: 34.3, wd: 1.1, t1: 38.95, halo: 1, lines: [['가죽옷을 지어 입히시니라', 1450, 2690, 64, 'center'], ['창 3:21', 1450, 2770, 48, 'center']] },
  { id: 'guard', w0: 41.1, wd: 1.4, t1: 46.5, lines: [['생명나무의 길을 지키게', 1500, 3250, 54, 'center'], ['하시니라 (창 3:24)', 1500, 3330, 54, 'center']] },
  { id: 'cross', w0: 49.6, wd: 1.4, t1: 55.3, halo: 1, lines: [['여자의 후손 예수,', 1080, 5480, 66, 'center'], ['우리 대신 상하셨다', 1080, 5570, 66, 'center']] },
  { id: 'open', w0: 55.4, wd: 1.2, t1: 60.0, halo: 1, lines: [['닫혔던 생명의 길이 다시 열렸다', 1080, 5745, 76, 'center']] },
  { id: 'way', w0: 60.9, wd: 1.8, t1: 99, lines: [['내가 곧 길이요', 1080, 6070, 150, 'center'], ['진리요 생명이니', 1080, 6230, 150, 'center'], ['요 14:6', 1080, 6335, 64, 'center']] },
  { id: 'note', w0: 61.6, wd: .8, t1: 99, lines: [['창세기 3장 · 동산의 동편에서', 2050, 6430, 54, 'right']] },
];
const measure = (() => { const c = document.createElement('canvas').getContext('2d'); return (s, size) => { c.font = `400 ${size}px ${FONT}`; return c.measureText(s).width; }; })();
for (const T of TXT) { const chars = T.lines.reduce((a, l) => a + l[0].length, 0); let acc = 0; T.lines.forEach(l => { l.s0 = T.w0 + T.wd * acc / chars; acc += l[0].length; l.s1 = T.w0 + T.wd * acc / chars; l.w = measure(l[0], l[3]); }); }
const lineBox = l => { const [s, x, y, size, al] = l, x0 = al === 'center' ? x - l.w / 2 : al === 'right' ? x - l.w : x; return [x0, y - size * .82, x0 + l.w, y + size * .25]; };
function drawTexts(t) {
  for (const T of TXT) {
    if (t < T.w0 || t > T.t1 + .4) continue;
    const fade = 1 - clamp((t - T.t1) / .4);
    if (T.halo) {
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const l of T.lines) { const b = lineBox(l); x0 = Math.min(x0, b[0]); y0 = Math.min(y0, b[1]); x1 = Math.max(x1, b[2]); y1 = Math.max(y1, b[3]); }
      const k = eo(seg(t, T.w0 - .2, T.w0 + .3)) * fade, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      drawPrims(ctx, [{ k: 'knock', poly: rough(ellipse(cx, cy, (x1 - x0) / 2 + 60, (y1 - y0) / 2 + 40, 26), 14, T.w0 * 10 | 0), a: .62 * k }], {});
    }
    for (const l of T.lines) handwrite(ctx, l[0], l[1], l[2], l[3], seg(t, l.s0, l.s1), { font: FONT, align: l[4], alpha: .92 * fade, col: INK });
  }
}
window.TEXTS = t => {
  const cam = camera(t), out = [];
  for (const T of TXT) {
    if (t < T.w0 || t > T.t1) continue;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const l of T.lines) { const b = lineBox(l); for (const [px, py] of [[b[0], b[1]], [b[2], b[3]], [b[0], b[3]], [b[2], b[1]]]) { const [sx, sy] = toScreen(cam, px, py); x0 = Math.min(x0, sx); y0 = Math.min(y0, sy); x1 = Math.max(x1, sx); y1 = Math.max(y1, sy); } }
    out.push({ id: T.id, text: T.lines.map(l => l[0]).join(' / '), x0, y0, x1, y1 });
  }
  return out;
};

// ---------------- render ----------------
window.DUR = DUR;
window.render = t => {
  const cam = camera(t);
  comp(cam, t);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  ctx.drawImage(glc, 0, 0);
  const c = Math.cos(cam.rot), s = Math.sin(cam.rot);
  ctx.setTransform(cam.z * c, cam.z * s, -cam.z * s, cam.z * c, SW / 2 - cam.z * (c * cam.cx - s * cam.cy), SH / 2 - cam.z * (s * cam.cx + c * cam.cy));
  const bo = boilOf(t);

  // the flaming sword over the gate
  if (t > 42.6 && t < 57) {
    const life = eo(seg(t, 42.6, 43.2)) * (1 - ss(seg(t, 55.6, 56.8)));
    const flame = eo(seg(t, 42.8, 43.4)) * (1 - ss(seg(t, 55.4, 56.4)));
    const sw = swordPrims(t, Math.max(life, .001)), [cx0, cy0] = SWORD;
    if (life > .01) {
      ctx.save(); ctx.globalAlpha = Math.min(1, life * 1.4);
      // flames: orange and gold dabs licking along the blade, re-seeded at 12 fps
      if (flame > 0) { ctx.globalCompositeOperation = 'multiply'; drawPrims(ctx, [{ k: 'wash', poly: rough(ellipse(cx0, cy0, 300 * flame, 150 * flame, 22), 30, bo + 3), col: hex('#f0b45a'), a: .22, seed: 70 + bo, edge: 0 }], { color: 1 }); for (let k = 0; k < 22; k++) { const u = k / 21, px = lerp(sw.hilt[0], sw.tip[0], u), py = lerp(sw.hilt[1], sw.tip[1], u), rr = (16 + 14 * Math.sin(u * Math.PI)) * flame; const j = n2(k, bo * 3.1, 4) - .5; dab(ctx, px - 6 + j * 18, py - rr * .8, rr, -1.4 + j, k % 3 ? hex('#e8892f') : hex('#efc24a'), .6, 900 + k + bo * 31); if (k % 2) dab(ctx, px + j * 10, py - rr * 1.6, rr * .55, -1.5 + j, hex('#d9562c'), .5, 950 + k + bo * 17); } ctx.globalCompositeOperation = 'source-over'; }
      drawPrims(ctx, [{ k: 'knock', poly: sw.blade, a: .8 }, { k: 'wash', poly: sw.blade, col: hex('#c9ccd6'), a: .5, seed: 5 }, { k: 'ink', st: penStroke([...sw.blade, sw.blade[0]], { w: 2.2, wob: .4, seed: 11 + bo, over: 2, smooth: false }) }], { color: 1 });
      drawPen(ctx, penStroke([[sw.hilt[0] + sw.nrm[0] * 30, sw.hilt[1] + sw.nrm[1] * 30], [sw.hilt[0] - sw.nrm[0] * 30, sw.hilt[1] - sw.nrm[1] * 30]], { w: 3, wob: .3, seed: 12, over: 2 }), 1);
      drawPen(ctx, penStroke([sw.hilt, [sw.hilt[0] - sw.d[0] * 40, sw.hilt[1] - sw.d[1] * 40]], { w: 4, wob: .3, seed: 13, over: 1 }), 1);
      // ink flame curls rising off the blade
      if (flame > 0) for (let k = 0; k < 5; k++) { const ph = ((t * 1.6 + k / 5) % 1), u = .2 + k * .17, bx = lerp(sw.hilt[0], sw.tip[0], u), by = lerp(sw.hilt[1], sw.tip[1], u) - 20 - ph * 70; const pts = []; for (let i = 0; i <= 8; i++) pts.push([bx + Math.sin(i * .9 + k) * 9, by - i * 6]); drawPen(ctx, penStroke(pts, { w: 1.6, wob: .4, seed: 20 + k, over: 0 }), eo(ph / .5), INK, .7 * flame, ei(clamp((ph - .45) / .55))); }
      ctx.restore();
    }
  }

  // serpent on the branch (9.4 → 21.6)
  if (t > 9.4 && t < 21.7) { const sp = serpentPrims(serpentOnBranch(t), 9, 200 + bo * 5); drawPrims(ctx, sp, { color: colorAt(1100, 1600, t), ink: inkProgress(sp, t, 9.4, 10.5) }); }

  // the couple (behind the bush while in Eden) — figures from far to near by y
  const fig = couple(t), hands = {};
  const items = [];
  for (const f of fig) {
    const swap = f.who === 'eve' ? 'eve2' : 'adam2', seedF = f.who === 'eve' ? 50 : 70;
    const prims = figure(LOOK[f.who], f.pose, f.place, { seed: seedF, boil: bo });
    hands[f.who] = f.who === 'eve' ? prims.hand.R : prims.hand.L;
    items.push({ y: f.place.y, draw: () => {
      const colF = figureColor(f.place.x, f.place.y, t);
      shadow(f.place.x, f.place.y, f.place.S, .25 * Math.max(colF, .3));
      if (t < GARB) {
        drawPrims(ctx, prims, { color: colF, ink: inkProgress(prims, t, 3.5, 4.6), clip: t < 9 && colF < 1 ? bloomClip(f.place.x, f.place.y - 280, 420 * eo(colF), seedF) : null });
      } else {
        const u = seg(t, GARB, GARB + .8), p2 = figure(LOOK[swap], f.pose, f.place, { seed: seedF + 3, boil: bo });
        if (u < 1) { ctx.save(); ctx.globalAlpha = 1 - u; drawPrims(ctx, prims, { color: 0 }); ctx.restore(); }
        const g = clamp((t - 35.3) / 1.1);
        drawPrims(ctx, p2, { color: g, ink: inkProgress(p2, t, GARB, GARB + .8), clip: g < 1 ? bloomClip(f.place.x, f.place.y - 270, 380 * eo(g), seedF + 1) : null });
      }
    } });
  }
  items.push({ y: 2290, draw: () => drawBush(t) });
  if (t > 32.7) items.push({ y: LAMB[1], draw: () => {
    const lp = lambPrims(t), lc = colorAt(LAMB[0], LAMB[1], t) || .85;
    drawPrims(ctx, lp, { color: Math.max(lc, .85), ink: inkProgress(lp, t, 32.8, 33.9) });
    // a red drop on its side, falling to the ground
    if (t > 34.2) {
      const u = clamp((t - 34.2) / .35); ctx.save(); ctx.globalCompositeOperation = 'multiply';
      dab(ctx, LAMB[0] + 30, LAMB[1] - 98 + 34 * ss(seg(t, 36.6, 37.6)), 13 * eo(u), .3, RED, .8, 77);
      const fall = clamp((t - 34.55) / .4); if (fall > 0) { dab(ctx, LAMB[0] + 34, lerp(LAMB[1] - 80, LAMB[1] + 4, fall * fall), 6, 0, RED, .85, 78); if (fall >= 1) dab(ctx, LAMB[0] + 36, LAMB[1] + 6, 11 * eo(clamp((t - 34.95) / .3)), 0, RED, .7, 79); }
      ctx.restore();
    }
  } });
  items.sort((a, b) => a.y - b.y);
  for (const it of items) it.draw();

  // the fruit (always on top while held)
  if (t > .2) {
    const fs = fruitState(t, hands); const fp = fruitPrims(fs.p, fs.bites, bo);
    if (!(t > 16.6 && t < 39)) drawPrims(ctx, fp, { color: fs.col, ink: inkProgress(fp, t, .2, .95), clip: fs.col < 1 && t < 3 ? bloomClip(fs.p[0], fs.p[1], 40 * eo(fs.col), 5) : null });
  }

  // 3:15 — the serpent on the ground and the heel
  if (t > 26.4 && t < 33.5) {
    const sp = serpentPrims(serpentOnGround(t), 10, 260 + bo * 5); drawPrims(ctx, sp, { color: 0 });
    if (t > 28.6) { const hp = heelPrims(t); drawPrims(ctx, hp, { color: clamp((t - 29.0) / .6) * .9, ink: inkProgress(hp, t, 28.6, 29.1) }); }
    if (t > 29.3) { const u = seg(t, 29.3, 29.55); for (let k = 0; k < 3; k++) drawPen(ctx, penStroke([[730 + k * 10, 2452], [722 + k * 16, 2470 + k * 4]], { w: 1.6, wob: .3, seed: 90 + k, over: 0 }), u); }
    if (t > 29.5) { ctx.save(); ctx.globalCompositeOperation = 'multiply'; dab(ctx, 726, 2386 + 12, 10 * eo(seg(t, 29.5, 30.0)), .5, RED, .75, 91); ctx.restore(); }
  }

  // the red at the cross: blooms from the centre when the second stroke is done
  if (t > 48.75) {
    const u = eo(seg(t, 48.75, 49.7));
    drawPrims(ctx, [{ k: 'wash', poly: rough(ellipse(CROSS.x, CROSS.bar + 4, 20 + 46 * u, 14 + 30 * u, 18), 6, 9), col: RED, a: .55 * u, seed: 9 }], { color: 1 });
    drawPrims(ctx, [{ k: 'wash', poly: rough(ellipse(CROSS.x, CROSS.bar + 60, 9 + 10 * u, 30 + 160 * u, 14), 4, 10), col: RED, a: .32 * u, seed: 10 }], { color: 1 });
  }

  drawTexts(t);

  // paper tooth over everything
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = toothPat;
  const iz = 1 / cam.z; ctx.fillRect(cam.cx - SW * iz, cam.cy - SH * iz, SW * 2 * iz, SH * 2 * iz); ctx.restore();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
};

// ---------------- sound events (for the mixer) ----------------
const EV = [];
EV.push({ t: 0.2, type: 'pen', d: .75 }, { t: 1.0, type: 'bloom', g: .6 }, { t: 3.6, type: 'bloomBig', d: 4.0 }, { t: 3.0, type: 'birdsIn' },
  { t: 9.4, type: 'pen', d: 1.1 }, { t: 9.6, type: 'hiss' }, { t: 11.9, type: 'pluck' }, { t: 12.8, type: 'bite', g: .5 }, { t: 13.6, type: 'handoff' }, { t: 14.6, type: 'silence', d: .4 },
  { t: 15.0, type: 'bite', g: 1 }, { t: 15.3, type: 'drain', d: 4.4 }, { t: 16.35, type: 'drop' }, { t: 16.9, type: 'rustle' }, { t: 21.6, type: 'silence', d: .9 },
  { t: 26.45, type: 'whoosh' }, { t: 26.6, type: 'slither', d: 2.2 }, { t: 28.6, type: 'pen', d: .5 }, { t: 29.3, type: 'thud' }, { t: 29.5, type: 'drip' },
  { t: 32.8, type: 'pen', d: 1.1 }, { t: 34.2, type: 'drip' }, { t: 34.95, type: 'drip', g: .5 }, { t: 34.9, type: 'pen', d: .8 }, { t: 35.3, type: 'cloth' }, { t: 35.4, type: 'bloom', g: .8 },
  { t: 42.6, type: 'flameIn' }, { t: 42.8, type: 'flame', d: 13.4 }, { t: 46.5, type: 'silence', d: .8 }, { t: 48.8, type: 'bloom', g: 1 }, { t: 49.0, type: 'bloomBig', d: 10 },
  { t: 55.6, type: 'flameOut' }, { t: 57.5, type: 'birdsIn' });
for (const T of TXT) for (const l of T.lines) EV.push({ t: +l.s0.toFixed(3), type: 'write', d: +(l.s1 - l.s0).toFixed(3) });
for (const st of STEPS) EV.push({ t: st, type: 'step' });
window.EV = EV;
window.STROKES = world.strokes;
window.TXT = TXT.map(T => ({ id: T.id, t0: T.w0, t1: Math.min(T.t1, window.DUR), text: T.lines.map(l => l[0]).join('\n') }));
window.READY = true;
