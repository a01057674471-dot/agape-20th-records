// Painted elements for 「あなたが隠れている場所まで」: washes, the woman, people, hands, sheep, lantern, props.
// Every generator works in local coordinates and returns a list of elements (strokes from mk, or washes from wash).
// Build them at init (or inside withSeed): they consume the RNG.

const ACC = '#d9822b', ACC2 = '#f2b45e';        // the one accent: the light that comes looking (lantern, cross dawn, gift)
const C = {
  night: '#4f5f7c', night2: '#38455e', night3: '#2b3549', dusk: '#7486a2', mist: '#aab6c7',
  bldg: '#5f6b81', bldg2: '#48546a', lamp: '#eadba8',
  skin: '#e9c5a2', skinS: '#c99a78', blush: '#e2a088', hair: '#352b27', hair2: '#4a3c35',
  coat: '#4a5670', coatS: '#323c53', shirt: '#e8e0d2', pants: '#5a6275', shoe: '#3a3330',
  linen: '#dcd2c2', linenS: '#b9ac98',
  grassN: '#3f5653', hillN: '#46596a', sheepN: '#c3c8d0',
  dawn1: '#f3d3aa', dawn2: '#eab08e', dawn3: '#cdb8cf', sky: '#a9c0d5', skyN: '#40506d',
  wallN: '#7a8599', wallD: '#ddd2c1', floorN: '#5d6679', floorD: '#c9b49a', bedN: '#a9b0bd', bedD: '#ece4d6',
  wood: '#866a55', woodN: '#4f4a4f',
};

// ---------- washes ----------
function wash(pts, col, a = .7, passes = 3, jit = 4) {
  const P = [];
  const cols = [];
  for (let p = 0; p < passes; p++) { P.push(pts.map(([x, y]) => [x + rnd(-jit, jit), y + rnd(-jit, jit)])); cols.push(mixc(col, rnd() < .5 ? '#000000' : '#ffffff', rnd(0, .07))); }
  return { w: 1, P, col, cols, a, passes, edge: mixc(col, '#000000', .25) };
}
function ell(cx, cy, rx, ry, n = 28, rot = 0) {
  const o = []; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, r = 1 + (vnoise(i * .7 + cx * .01) - .5) * .08;
    const x = Math.cos(a) * rx * r, y = Math.sin(a) * ry * r; o.push([cx + x * Math.cos(rot) - y * Math.sin(rot), cy + x * Math.sin(rot) + y * Math.cos(rot)]); }
  return o;
}
function rect(x, y, w, h, n = 3) {           // a hand-wobbly rectangle
  const o = [], side = (x0, y0, x1, y1) => { for (let i = 0; i < n; i++) { const t = i / n; o.push([lerp(x0, x1, t), lerp(y0, y1, t)]); } };
  side(x, y, x + w, y); side(x + w, y, x + w, y + h); side(x + w, y + h, x, y + h); side(x, y + h, x, y); return o;
}
function drawW(c, e, am = 1, col = null) {
  const a = e.a / e.passes * 1.6 * am;
  e.P.forEach((P, k) => {
    c.fillStyle = col || e.cols[k]; c.globalAlpha = clamp(a); c.beginPath(); P.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.closePath(); c.fill();
    if (k === 0) { c.strokeStyle = col || e.edge; c.globalAlpha = clamp(a * .55); c.lineWidth = 2.2; c.lineJoin = 'round'; c.stroke(); }
  });
  c.globalAlpha = 1;
}
function drawE(c, e, p = 1, col = null, am = 1) { if (p <= 0) return; if (e.w) drawW(c, e, am * ss(p), col); else drawS(c, e, p, col, am); }
function drawL(c, L, p = 1, col = null, am = 1) {
  const N = L.length; if (!N) return;
  if (p >= 1) { for (const e of L) drawE(c, e, 1, col, am); return; }
  const dur = Math.min(.5, Math.max(.12, 4 / N));
  for (let j = 0; j < N; j++) drawE(c, L[j], (p - j / N * (1 - dur)) / dur, col, am);
}
function bboxL(L, pad = 8) {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const e of L) {
    if (e.w) { for (const P of e.P) for (const [x, y] of P) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } }
    else for (let i = 0; i < e.pts.length; i++) { const [x, y] = e.pts[i], w = e.ws[i]; x0 = Math.min(x0, x - w); y0 = Math.min(y0, y - w); x1 = Math.max(x1, x + w); y1 = Math.max(y1, y + w); }
  }
  return [Math.floor(x0 - pad), Math.floor(y0 - pad), Math.ceil(x1 + pad), Math.ceil(y1 + pad)];
}
function spr(L, col = null) {
  const [x0, y0, x1, y1] = bboxL(L), cv = document.createElement('canvas');
  cv.width = Math.max(1, x1 - x0); cv.height = Math.max(1, y1 - y0);
  const c = cv.getContext('2d'); c.translate(-x0, -y0); drawL(c, L, 1, col); return { cv, x0, y0 };
}
// an item: elements at (x, y) that paint themselves in between local times a and b, then are a cached sprite
function item(L, x = 0, y = 0, a = 0, b = 1.5, o = {}) { return { L, x, y, a, b, s: spr(L), sc: o.sc || 1, am: o.am ?? 1 }; }
function drawIt(c, it, lt, am = 1, dx = 0, dy = 0) {
  const p = seg(lt, it.a, it.b); if (p <= 0) return;
  c.save(); c.translate(it.x + dx, it.y + dy); if (it.sc !== 1) c.scale(it.sc, it.sc);
  if (p >= 1) { c.globalAlpha = it.am * am; c.drawImage(it.s.cv, it.s.x0, it.s.y0); c.globalAlpha = 1; }
  else drawL(c, it.L, p, null, it.am * am);
  c.restore();
}
const S_ = (pts, w, col, o = {}) => mk(pts, w, col, Object.assign({ prof: 'even', nb: 0, a: .85 }, o));
const T = (pts, f) => pts.map(p => f(p[0], p[1]));
const rot = (a, cx = 0, cy = 0) => (x, y) => { const dx = x - cx, dy = y - cy, c = Math.cos(a), s = Math.sin(a); return [cx + dx * c - dy * s, cy + dx * s + dy * c]; };

// apply a point transform to elements already built (for mirroring / tilting whole groups)
function xform(L, f) {
  for (const e of L) {
    if (e.w) e.P = e.P.map(P => P.map(([x, y]) => f(x, y)));
    else {
      e.pts = e.pts.map(([x, y]) => f(x, y));
      const n = e.pts.length;
      for (let i = 0; i < n; i++) { const a = e.pts[Math.max(0, i - 1)], b = e.pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L2 = Math.hypot(dx, dy) || 1; e.nx[i] = -dy / L2; e.ny[i] = dx / L2; }
    }
  }
  return L;
}
const mirror = L => xform(L, (x, y) => [-x, y]);
const scaleL = (L, s) => xform(L, (x, y) => [x * s, y * s]);

// ---------- the woman: head-and-shoulders, profile facing right; origin at the base of the neck ----------
// o.tilt: head bowed (radians), o.pray: folded hands, o.eyes: 'down' | 'closed' | 'open', o.light: warm side light
function bust(o = {}) {
  const tilt = o.tilt || 0, L = [], head = [], hr = rot(tilt, -5, -88);
  const H = (pts) => T(pts, hr);
  // body
  L.push(wash([[-38, -48], [-150, 6], [-205, 120], [-222, 330], [190, 330], [168, 120], [118, 10], [42, -44]], C.coat, .78));
  L.push(wash([[-150, 6], [-205, 120], [-222, 330], [-110, 330], [-95, 120], [-60, 20]], C.coatS, .45));
  L.push(wash([[-6, -48], [42, -44], [22, 52], [-2, 10]], C.shirt, .85, 2));
  L.push(S_(qcurve(44, -42, 34, 110, 14, 10), 7, C.coatS, { a: .8 }));
  L.push(S_(qcurve(-36, -46, -6, 70, -12, 10), 6, C.coatS, { a: .7 }));
  // neck
  L.push(wash([[-30, -100], [14, -100], [18, -40], [-26, -42]], C.skin, .75, 2));
  L.push(wash([[-28, -96], [10, -100], [12, -80], [-24, -74]], C.skinS, .4, 2));
  // face, nose, cheek, eye, brow, mouth
  head.push(wash(H(ell(10, -158, 58, 70)), C.skin, .62));
  head.push(wash(H(ell(34, -128, 14, 9)), C.blush, .28, 2));
  head.push(S_(H(qcurve(62, -168, 70, -138, -6, 6)), 5, C.skinS, { a: .55 }));
  if ((o.eyes || 'down') === 'open') head.push(S_(H(qcurve(30, -162, 46, -162, -3, 6)), 3.4, INK, { a: .9 }), S_(H(qcurve(40, -164, 42, -158, 0, 3)), 4.2, INK, { a: .95 }));
  else head.push(S_(H(qcurve(30, -158, 48, -156, o.eyes === 'closed' ? 3 : 4, 6)), 3.2, INK, { a: .88 }));
  head.push(S_(H(qcurve(28, -180, 50, -182, -3, 6)), 3, C.hair2, { a: .55 }));
  head.push(S_(H(qcurve(50, -114, 60, -115, 1, 4)), 2.6, '#a8645a', { a: .7 }));
  // hair: a bob with a fringe
  head.push(wash(H([[68, -178], [56, -208], [16, -230], [-40, -222], [-78, -186], [-86, -128], [-76, -88], [-34, -84], [-12, -98], [-16, -140], [8, -168], [42, -176]]), C.hair, .86));
  head.push(wash(H([[-40, -222], [-78, -186], [-86, -128], [-76, -88], [-50, -90], [-56, -150], [-30, -200]]), C.hair, .35, 2));
  for (let i = 0; i < 8; i++) {
    const a = -1.75 - i * .16, x0 = -4 + Math.cos(a) * 62, y0 = -158 + Math.sin(a) * 62;
    head.push(mk(H(qcurve(x0, y0, x0 - 20 - i * 3, y0 + 70 + i * 4, 6, 8)), 6, C.hair2, { prof: 'tip', nb: 2, a: .45 }));
  }
  head.push(mk(H(qcurve(66, -178, 30, -168, -6, 6)), 9, C.hair, { prof: 'tip', nb: 2, a: .7 }));
  L.push(...head);
  if (o.pray) {
    L.push(S_([[-90, 250], [-10, 190], [70, 128]], 44, mixc(C.coat, '#000000', .08), { a: .85 }));
    L.push(S_([[30, 280], [80, 200], [96, 132]], 40, C.coat, { a: .85 }));
    L.push(wash([[70, 128], [66, 70], [80, 18], [96, -12], [110, 14], [120, 70], [114, 130]], C.skin, .8));
    L.push(S_([[94, -6], [94, 118]], 2.6, C.skinS, { a: .6 }));
    L.push(S_(qcurve(72, 96, 112, 98, 4, 5), 2.4, C.skinS, { a: .5 }));
  }
  if (o.face === -1) mirror(L);
  return L;
}

// ---------- a full figure; origin at the feet; height ≈ 270 at scale 1 ----------
// o: face (1 right, -1 left), back (seen from behind), ph (walk phase), amp (stride), coat, pants, hair, bob, armUp
function fig(o = {}) {
  const L = [], amp = o.amp ?? 0, ph = o.ph ?? 0, coat = o.coat || C.coat, pants = o.pants || C.pants, hair = o.hair || C.hair;
  const sw = Math.sin(ph) * amp, hipY = -120;
  const leg = (s, front) => {
    const a = s, kx = Math.sin(a) * 60, ky = hipY + Math.cos(a) * 60, bend = front ? 0 : Math.max(0, -s) * .9 + .1;
    const fx = kx + Math.sin(a - bend) * 60, fy = ky + Math.cos(a - bend) * 60;
    return [[0, hipY], [kx * .5, (hipY + ky) / 2], [kx, ky], [(kx + fx) / 2, (ky + fy) / 2], [fx, fy]];
  };
  for (const [s, front, col] of [[-sw, false, mixc(pants, '#000000', .18)], [sw, true, pants]]) {
    const P = leg(s, front); L.push(S_(P, 17, col, { a: .85 }));
    const [fx, fy] = P[4]; L.push(S_(qcurve(fx - 6, fy - 2, fx + 18, fy, 1, 4), 9, C.shoe, { a: .9 }));
  }
  L.push(wash([[-24, -222], [22, -222], [32, o.long ? -78 : -108], [-30, o.long ? -78 : -108]], coat, .82));
  L.push(wash([[-24, -222], [-6, -222], [-12, o.long ? -78 : -108], [-30, o.long ? -78 : -108]], mixc(coat, '#000000', .25), .35, 2));
  const arm = o.armUp ? [[4, -212], [22, -250], [40, -290], [52, -316]] : (() => {
    const a = -sw * .8; return [[2, -214], [Math.sin(a) * 30, -214 + Math.cos(a) * 46], [Math.sin(a) * 52 + 4, -214 + Math.cos(a) * 88]]; })();
  L.push(S_(arm, 14, mixc(coat, '#000000', .1), { a: .85 }));
  const hd = arm[arm.length - 1]; L.push(wash(ell(hd[0], hd[1] + 4, 7, 8, 12), C.skin, .8, 2));
  L.push(wash([[-7, -236], [7, -236], [8, -220], [-7, -220]], C.skin, .8, 2));
  L.push(wash(ell(3, -256, 21, 24, 20), C.skin, .7));
  if (o.back) L.push(wash(ell(2, -258, 24, 26, 20), hair, .88));
  else {
    const b = o.bob ?? 1;
    L.push(wash([[16, -276], [-6, -284], [-24, -270], [-28, -246], [-24, -228 - (1 - b) * 14], [-6, -228 - (1 - b) * 14], [-4, -250], [10, -262], [22, -264]], hair, .88));
    L.push(S_(qcurve(14, -254, 20, -254, 0, 3), 2.2, INK, { a: .8 }));
  }
  if (o.face === -1) mirror(L);
  return L;
}

// ---------- seated on the bed, hugging her knees (facing right); origin at the hip on the bed ----------
function seated() {
  const L = [];
  L.push(S_([[0, -10], [40, -55], [78, -96]], 36, C.pants, { a: .85 }));
  L.push(S_([[78, -96], [88, -50], [96, -6]], 28, mixc(C.pants, '#000000', .12), { a: .85 }));
  L.push(S_(qcurve(92, -2, 126, 0, 2, 4), 12, C.shoe, { a: .7 }));
  L.push(wash([[-30, 0], [-36, -62], [-12, -134], [34, -136], [52, -70], [36, -4]], C.coat, .82));
  L.push(wash([[-30, 0], [-36, -62], [-12, -134], [0, -132], [-14, -60], [-10, 0]], C.coatS, .4, 2));
  L.push(wash(ell(62, -142, 34, 30, 22), C.skin, .5));
  L.push(wash([[30, -170], [70, -176], [100, -150], [96, -118], [74, -108], [48, -112], [24, -130], [22, -156]], C.hair, .88));
  for (let i = 0; i < 6; i++) L.push(mk(qcurve(40 + i * 9, -166, 46 + i * 11, -112 + i * 2, 4, 6), 6, C.hair2, { prof: 'tip', nb: 2, a: .5 }));
  L.push(S_([[20, -122], [60, -112], [104, -86], [112, -66]], 22, mixc(C.coat, '#000000', .06), { a: .88 }));
  L.push(wash(ell(110, -62, 13, 11, 14), C.skin, .8, 2));
  return L;
}

// ---------- an open hand palm up, fingers to the right; origin at the palm centre ----------
function palm(sleeve, sleeveS, o = {}) {
  const L = [];
  L.push(wash([[-420, -66], [-200, -76], [-84, -84], [-66, -20], [-62, 66], [-200, 80], [-420, 70]], sleeve, .82));
  L.push(wash([[-420, 26], [-200, 34], [-62, 30], [-62, 66], [-200, 80], [-420, 70]], sleeveS, .45, 2));
  L.push(S_(qcurve(-96, -80, -76, 70, 12, 8), 8, sleeveS, { a: .6 }));
  L.push(S_(qcurve(-260, -70, -230, 20, 10, 6), 4, sleeveS, { a: .4 }));
  L.push(wash([[-70, -40], [-56, 40], [-40, 40], [-46, -36]], C.skin, .7, 2));
  L.push(wash([[-64, -44], [30, -54], [96, -40], [114, -6], [96, 34], [16, 52], [-62, 44]], C.skin, .72));
  L.push(wash([[-60, 14], [40, 22], [100, 30], [16, 52], [-62, 44]], C.skinS, .3, 2));
  const F = [[[96, -40], [146, -54], [178, -58]], [[110, -16], [160, -24], [196, -24]], [[112, 6], [160, 6], [192, 10]], [[100, 28], [138, 34], [164, 42]]];
  F.forEach((P, i) => { L.push(mk(P, 26 - i * 2, C.skin, { prof: 'even', nb: 0, a: .82, rough: .12 })); L.push(S_(P.map(([x, y]) => [x, y + 11 - i]), 3, C.skinS, { a: .5 })); });
  L.push(mk([[30, -50], [70, -80], [104, -96]], 28, C.skin, { prof: 'even', nb: 0, a: .82, rough: .12 }));
  L.push(S_([[36, -40], [74, -70], [104, -84]], 3, C.skinS, { a: .5 }));
  if (o.flip) mirror(L);
  return L;
}
// the gift: a small box with an accent ribbon; origin at the bottom centre
function gift() {
  const L = [];
  L.push(wash(rect(-60, -86, 120, 86, 2), '#ece4d4', .9));
  L.push(wash([[-60, -86], [-30, -112], [86, -112], [60, -86]], '#f6efe2', .9, 2));
  L.push(wash([[60, -86], [86, -112], [86, -24], [60, 0]], '#cfc3ae', .8, 2));
  L.push(S_([[-60, -2], [60, -2]], 4, '#b4a68f', { a: .6 }));
  L.push(mk([[0, -2], [0, -86], [28, -112]], 13, ACC, { prof: 'even', nb: 3, a: .92 }));
  L.push(mk([[-60, -46], [60, -46], [86, -70]], 12, ACC, { prof: 'even', nb: 3, a: .9 }));
  L.push(mk(qcurve(14, -100, -30, -132, 26, 8), 13, ACC, { prof: 'leaf', nb: 3, a: .9 }));
  L.push(mk(qcurve(14, -100, 54, -138, -24, 8), 13, ACC, { prof: 'leaf', nb: 3, a: .9 }));
  L.push(mk(qcurve(14, -100, -10, -70, 8, 6), 9, ACC, { prof: 'tip', nb: 2, a: .85 }));
  L.push(mk(qcurve(14, -100, 40, -72, -8, 6), 9, ACC, { prof: 'tip', nb: 2, a: .85 }));
  return L;
}

// ---------- sheep (local origin at the feet), lantern ----------
function sheep(col = C.sheepN, face = 1) {
  const L = [];
  for (const [x, y] of [[-14, 0], [-6, 0], [10, 0], [17, 0]]) L.push(S_([[x, -14], [x + 1, 0]], 3.4, INK2, { a: .7 }));
  L.push(wash(ell(0, -24, 30, 16, 18), col, .85));
  clump(L, 0, -27, 20, 9, [col, mixc(col, '#ffffff', .3)], { sx: 1.4, sy: .7, l0: 8, l1: 14, w0: 8, w1: 12, a0: .5, a1: .8 });
  L.push(wash(ell(30, -30, 9, 7, 12, .5), INK2, .8, 2));
  if (face === -1) mirror(L);
  return L;
}
function lanternGlow(c, x, y, r, a = 1) {
  const g = c.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, rgba(ACC2, .75 * a)); g.addColorStop(.25, rgba(ACC, .42 * a)); g.addColorStop(.6, rgba(ACC, .14 * a)); g.addColorStop(1, rgba(ACC, 0));
  c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill();
}
function lantern() {
  const L = [];
  L.push(S_(qcurve(0, -70, 0, -150, 4, 6), 2.4, INK2, { a: .6 }));
  L.push(S_(qcurve(-16, -66, 16, -66, -8, 6), 3, INK2, { a: .8 }));
  L.push(wash(rect(-14, -62, 28, 50, 2), '#f7d9a0', .9, 2));
  L.push(wash(ell(0, -36, 7, 13, 12), ACC, .95, 2));
  L.push(S_([[-15, -62], [-15, -12]], 3, INK2, { a: .8 }), S_([[15, -62], [15, -12]], 3, INK2, { a: .8 }), S_([[-18, -10], [18, -10]], 4, INK2, { a: .85 }));
  return L;
}

// ---------- buildings: a row of night (or dawn) blocks with windows; origin at the street line ----------
function blocks(x0, x1, o = {}) {
  const L = [], body = o.col || C.bldg, lit = o.lit || C.lamp, dark = o.dark || C.night2;
  let x = x0;
  while (x < x1) {
    const w = rnd(o.w0 || 140, o.w1 || 260), h = rnd(o.h0 || 200, o.h1 || 520);
    L.push(wash(rect(x, -h, w - rnd(4, 14), h + 40, 2), mixc(body, dark, rnd(0, .35)), rnd(.75, .9)));
    if (o.windows !== false) {
      for (let yy = -h + 26; yy < -30; yy += 34) for (let xx = x + 16; xx < x + w - 34; xx += 30) {
        const on = rnd() < (o.on ?? .35); L.push(wash(rect(xx, yy, 14, 18, 1), on ? lit : dark, on ? rnd(.55, .9) : .35, 1, 1));
      }
    }
    x += w;
  }
  return L;
}
