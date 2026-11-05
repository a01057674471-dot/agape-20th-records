// 「あなたが隠れている場所まで」 — a watercolour picture book in seventeen spreads.
// Timing comes from cues.json (one entry per narration line); every scene is anchored to its lines,
// so replacing cues.json with the recorded narration's timings retimes the whole film.
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
let PAPER_IMG, GRAIN, CUES, LN, SC = [];
const TR = 1.4, LEAD = .9, JP = '"Noto Serif JP"';

// ---------- helpers ----------
const cam = (c, x, y, z = 1) => c.setTransform(z, 0, 0, z, W / 2 - x * z, H / 2 - y * z);
const reset = c => c.setTransform(1, 0, 0, 1, 0, 0);
function paper(c) { reset(c); c.globalAlpha = 1; c.drawImage(PAPER_IMG, 0, 0); }
function fullWash(col, a, x0 = -300, y0 = -300, x1 = W + 300, y1 = H + 300) { return wash(rect(x0, y0, x1 - x0, y1 - y0, 6), col, a, 3, 10); }
function band(y0, y1, col, a, x0 = -400, x1 = W + 400, wob = 16) {   // a horizontal band with a wobbly top edge
  const pts = []; for (let x = x0; x <= x1; x += 40) pts.push([x, y0 + (vnoise(x * .01 + y0) - .5) * wob * 2]);
  pts.push([x1, y1], [x0, y1]); return wash(pts, col, a, 3, 5);
}
function hills(x0, x1, base, amp, f, col, a, bottom = 1400) {
  const pts = []; for (let x = x0; x <= x1; x += 30) pts.push([x, base - amp * fbm(x * f + base * .01)]);
  pts.push([x1, bottom], [x0, bottom]); return wash(pts, col, a, 3, 4);
}
function wavyClip(c, p, kind = 'wipe') {
  c.beginPath();
  if (kind === 'mist') {
    const top = H + 120 - p * (H + 420);
    c.moveTo(-10, H + 10); for (let x = -10; x <= W + 40; x += 40) c.lineTo(x, top + (vnoise(x * .006 + 3) - .5) * 220);
    c.lineTo(W + 10, H + 10);
  } else {
    const X = -260 + p * (W + 520);
    c.moveTo(-10, -10); for (let y = -10; y <= H + 40; y += 40) c.lineTo(X + (vnoise(y * .006 + 7) - .5) * 260, y);
    c.lineTo(-10, H + 10);
  }
  c.closePath(); c.clip();
}
function mistOver(c, p, a = 1) {           // paper rising over the picture
  if (p <= 0) return; reset(c); c.save(); wavyClip(c, p, 'mist'); c.globalAlpha = a; c.drawImage(PAPER_IMG, 0, 0); c.restore(); c.globalAlpha = 1;
}
function writeText(c, txt, x, y, p, size = 50, w = 500, a = .9, align = 'center') {
  if (p <= 0) return;
  c.save(); reset(c); c.font = `${w} ${size}px ${JP}`; c.textAlign = align; c.textBaseline = 'middle';
  const tw = c.measureText(txt).width, x0 = align === 'center' ? x - tw / 2 : x;
  c.beginPath(); c.rect(x0 - 10, y - size, (tw + 20) * eo(p), size * 2); c.clip();
  c.shadowColor = rgba(PAPER, .95); c.shadowBlur = 14; c.fillStyle = rgba(INK, a); c.fillText(txt, x, y); c.shadowBlur = 0; c.fillText(txt, x, y);
  c.restore();
}
const walkers = [];   // per-frame figures (built under a fixed seed)
function figAt(c, seed, o, x, y, sc = 1, am = 1) {
  const L = withSeed(seed, () => fig(o)); c.save(); c.translate(x, y); c.scale(sc, sc); drawL(c, L, 1, null, am); c.restore();
}

// ---------- the scenes ----------
// each: { line, kind (transition into it), build(), draw(c, lt, A, E) }  A(k)/E(k): line k start/end in scene time
const SCENES = [];
const scene = (line, kind, build, draw) => SCENES.push({ line, kind, build, draw });

// 1 — the night train: her tired face at the window, the city running past
scene(0, 'wipe', function () {
  const B = this;
  B.bg = item([fullWash('#56627a', .85), band(760, 1400, '#3e4860', .7)], 0, 0, 0, 1.2);
  B.city1 = spr(withSeed(11, () => blocks(0, 3000, { h0: 120, h1: 330, col: '#55627c', on: .45 })));
  B.city2 = spr(withSeed(12, () => blocks(0, 3000, { h0: 220, h1: 520, col: '#3a465d', on: .3, w0: 180, w1: 320 })));
  B.sky = spr([fullWash(C.night3, .9, 0, 0, 1200, 700), band(380, 700, '#46557a', .5, 0, 1200)]);
  B.frame = item([
    S_(rect(150, 170, 1080, 560, 1).concat([[150, 170]]), 30, '#2f384b', { a: .9, nb: 5 }),
    S_([[690, 170], [690, 730]], 22, '#2f384b', { a: .9, nb: 4 }),
    wash(rect(100, 730, 1240, 70, 2), '#6f7a90', .8),
    S_([[1330, -20], [1330, 1100]], 16, '#9aa3b3', { a: .85, nb: 4 }),
    S_([[100, 60], [1500, 60]], 10, '#9aa3b3', { a: .7 }),
    ...[300, 560, 820, 1080].map(x => S_([[x, 60], [x, 120], [x - 14, 150], [x, 176], [x + 14, 150], [x, 120]], 5, '#c7ccd5', { a: .75 })),
    wash([[1360, 600], [1960, 560], [1960, 1100], [1360, 1100]], '#4c5a78', .8),
  ], 0, 0, .5, 2.2);
  B.her = item(withSeed(13, () => bust({ face: -1, eyes: 'down', tilt: .1 })), 1580, 740, 1.1, 3.4, { sc: 1.4 });
  B.ghost = spr(withSeed(13, () => bust({ face: -1, eyes: 'down', tilt: .08 })));
}, function (c, lt) {
  paper(c); const B = this, z = 1 + .05 * ss(lt / 18);
  cam(c, 960, 540, z);
  drawIt(c, B.bg, lt);
  const wp = eo(seg(lt, .3, 1.6));
  if (wp > 0) {
    c.save(); c.beginPath(); c.rect(150, 170, 1080 * wp, 560); c.clip();
    c.drawImage(B.sky.cv, 150 + B.sky.x0, 170 + B.sky.y0);
    const o2 = (lt * 90) % 1500, o1 = (lt * 260) % 1500;
    for (const k of [0, 1]) c.drawImage(B.city2.cv, 150 + B.city2.x0 - o2 + k * 1500, 640 + B.city2.y0);
    for (const k of [0, 1]) c.drawImage(B.city1.cv, 150 + B.city1.x0 - o1 + k * 1500, 760 + B.city1.y0);
    for (let i = 0; i < 6; i++) {           // passing light streaks
      const x = 1300 - ((lt * 900 + i * 397) % 1600), y = 260 + i * 70;
      c.fillStyle = rgba(C.lamp, .35); c.beginPath(); c.ellipse(x, y, 80, 3, 0, 0, 7); c.fill();
    }
    c.globalAlpha = .2 * ss(seg(lt, 2.4, 4)); c.drawImage(B.ghost.cv, 900 + B.ghost.x0 * 1.1, 660 + B.ghost.y0 * 1.1, B.ghost.cv.width * 1.1, B.ghost.cv.height * 1.1); c.globalAlpha = 1;
    c.restore();
  }
  drawIt(c, B.frame, lt); drawIt(c, B.her, lt);
});

// 2 — the crossing: grey people stream past; she stands still among them
scene(2, 'wipe', function () {
  const B = this;
  B.bg = item([fullWash(C.night2, .75, -400, -300, 2800, 1400), band(600, 1400, '#3b4357', .8, -400, 2800)], 0, 0, 0, 1);
  B.city = item(withSeed(21, () => blocks(-300, 2700, { h0: 240, h1: 560, col: C.bldg, on: .4 })), 0, 620, .2, 1.6);
  B.road = item(withSeed(22, () => [band(640, 1400, '#464f63', .8, -400, 2800),
    ...Array.from({ length: 18 }, (_, i) => wash([[-200 + i * 160, 820], [-120 + i * 160, 820], [-60 + i * 160 + 40, 1000], [-160 + i * 160 + 40, 1000]], '#c8ccd4', .55, 2, 3))]), 0, 0, .4, 1.8);
  B.lamps = item(withSeed(23, () => [180, 1100, 2000].flatMap(x => [S_([[x, 860], [x, 300], [x + 50, 280]], 10, '#2d3445', { a: .9 }), wash(ell(x + 56, 292, 20, 10, 14), C.lamp, .9, 2)])), 0, 0, .8, 2);
  B.people = Array.from({ length: 13 }, (_, i) => ({
    seed: 200 + i, x0: -400 + i * 230 + (i % 3) * 40, y: i % 2 ? 900 : 960, dir: i % 3 === 1 ? -1 : 1, sp: 70 + (i % 4) * 14, sc: i % 2 ? 1.05 : 1.2,
    coat: ['#8a909a', '#9aa0a8', '#7f8590', '#a3a7ae', '#8f949c'][i % 5], hair: ['#2f2a28', '#3d3734', '#4a4440'][i % 3] }));
}, function (c, lt) {
  paper(c); const B = this, cx = 960 + 240 * eio(seg(lt, 0, 26));
  cam(c, cx, 540, 1);
  drawIt(c, B.bg, lt); drawIt(c, B.city, lt); drawIt(c, B.road, lt); drawIt(c, B.lamps, lt);
  const vis = ss(seg(lt, 1, 2.6));
  const L = B.people.map(p => ({ p, x: p.x0 + p.dir * p.sp * lt })).sort((a, b) => a.p.y - b.p.y);
  let herDrawn = false;
  for (const { p, x } of L) {
    if (!herDrawn && p.y > 930) { figAt(c, 7, { face: 1, coat: C.coat }, 1200, 935, 1.3, vis); herDrawn = true; }
    const xx = ((x + 600) % 3400 + 3400) % 3400 - 600;
    figAt(c, p.seed, { face: p.dir, ph: lt * 5.2 + p.seed, amp: .32, coat: p.coat, pants: '#4d5363', hair: p.hair, bob: .3 }, xx, p.y, p.sc, vis * .5);
  }
});

// 3 — a wall of windows; one stays dark
scene(6, 'wipe', function () {
  const B = this, L = [fullWash('#556179', .9, -200, -200, 2200, 1300)];
  B.win = [];
  withSeed(31, () => {
    for (let r = 0; r < 6; r++) for (let k = 0; k < 8; k++) {
      const x = 120 + k * 220, y = 40 + r * 175, hers = r === 3 && k === 5, on = !hers && rnd() < .78;
      L.push(wash(rect(x, y, 150, 112, 2), on ? mixc(C.lamp, '#f0c890', rnd(0, .5)) : C.night3, on ? rnd(.6, .9) : .85, 2, 2));
      L.push(S_([[x - 6, y + 128], [x + 156, y + 128]], 7, '#3a4559', { a: .8 }));
      L.push(S_([[x + 75, y], [x + 75, y + 112]], 3, '#3a4559', { a: .6 }));
      if (hers) B.hers = [x + 75, y + 56];
    }
  });
  B.wall = item(L, 0, 0, 0, 2.2);
}, function (c, lt, A, E) {
  paper(c); const B = this, p = eio(seg(lt, 1.5, E(6) + .4)), z = 1 + 1.3 * p;
  cam(c, lerp(960, B.hers[0], p), lerp(540, B.hers[1], p), z);
  drawIt(c, B.wall, lt);
});

// 4 — inside the dark room: she sits on the bed, knees held
function room(dawn, o = {}) {
  const L = [], m = dawn ? 1 : 0, wl = mixc(C.wallN, C.wallD, m), fl = mixc(C.floorN, C.floorD, m);
  L.push(fullWash(wl, .85));
  L.push(band(780, 1400, fl, .85));
  L.push(S_([[-50, 782], [1980, 778]], 8, mixc('#3e4658', '#9a8470', m), { a: .7 }));
  if (o.window !== false) {
    L.push(S_(rect(250, 190, 520, 430, 1).concat([[250, 190]]), 16, mixc('#2f384b', '#8d7b69', m), { a: .9, nb: 4 }));
    L.push(S_([[510, 190], [510, 620]], 10, mixc('#2f384b', '#8d7b69', m), { a: .85 }));
  }
  if (o.bed !== false) {
    L.push(wash(rect(980, 640, 760, 150, 2), mixc(C.bedN, C.bedD, m), .85));
    L.push(wash(rect(980, 600, 160, 60, 2), mixc('#c3c9d3', '#f3ece0', m), .85));
    L.push(wash(rect(960, 560, 26, 300, 1), mixc(C.woodN, C.wood, m), .9, 2));
    L.push(wash(rect(1740, 620, 22, 240, 1), mixc(C.woodN, C.wood, m), .9, 2));
    L.push(wash(rect(980, 780, 780, 30, 1), mixc(C.woodN, C.wood, m), .8, 2));
  }
  return L;
}
function nightOutside() {
  return [fullWash(C.night3, .9, 250, 190, 770, 620), ...withSeed(41, () => blocks(250, 770, { h0: 60, h1: 230, col: '#3b4760', on: .3, w0: 70, w1: 130 })).map(e => { xform([e], (x, y) => [x, y + 620]); return e; })];
}
scene(7, 'wipe', function () {
  const B = this;
  B.room = item(withSeed(42, () => room(false)), 0, 0, 0, 1.6);
  B.out = item(withSeed(43, () => nightOutside()), 0, 0, .3, 1.6);
  B.curt = item(withSeed(44, () => [wash([[200, 160], [290, 160], [270, 660], [190, 660]], '#8c97ad', .75), wash([[730, 160], [820, 160], [830, 660], [750, 660]], '#8c97ad', .75)]), 0, 0, .6, 1.8);
  B.moon = item([wash([[260, 620], [770, 620], [980, 900], [420, 900]], '#c6cee0', .22, 2, 6)], 0, 0, 1, 2.4);
  B.her = item(withSeed(45, () => seated()), 1240, 652, 1.1, 3.2, { sc: 1.9 });
}, function (c, lt) {
  paper(c); const B = this; cam(c, 960, 540, 1 + .04 * ss(lt / 10));
  drawIt(c, B.room, lt); drawIt(c, B.out, lt); drawIt(c, B.curt, lt); drawIt(c, B.moon, lt); drawIt(c, B.her, lt);
});

// 5 — up past the roofs into the night sky; the stars come all at once; one drop
scene(8, 'wipe', function () {
  const B = this;
  B.sky = item(withSeed(51, () => [fullWash(C.night3, .95, -300, -300, 2300, 2400), band(1100, 2400, '#3f4d6c', .6, -300, 2300), band(1700, 2400, '#56648a', .5, -300, 2300)]), 0, 0, 0, 1.2);
  B.roofs = item(withSeed(52, () => blocks(-200, 2200, { h0: 120, h1: 380, col: '#262f42', on: .25, w0: 160, w1: 300 })), 0, 2200, .2, 1.6);
  B.stars = withSeed(53, () => Array.from({ length: 190 }, () => ({ x: rnd(-100, 2000), y: rnd(-100, 1700), r: rnd(1.5, 5) * (rnd() < .1 ? 1.8 : 1), d: rnd(0, 1.4), warm: rnd() < .15 })));
}, function (c, lt, A, E) {
  paper(c); const B = this, ty = eio(seg(lt, .4, A(9) + 1.2)), cy = lerp(1640, 540, ty);
  cam(c, 960, cy, 1);
  drawIt(c, B.sky, lt); drawIt(c, B.roofs, lt);
  const t0 = A(9) + 1.4;
  for (const s of B.stars) {
    const q = ss(seg(lt, t0 + s.d, t0 + s.d + .5)); if (q <= 0) continue;
    c.fillStyle = s.warm ? rgba('#f4e2b8', .9 * q) : rgba(PAPER, .92 * q); c.beginPath(); c.arc(s.x, s.y, s.r * (.6 + .4 * q), 0, 7); c.fill();
  }
  const d = seg(lt, A(10) + .8, A(10) + 1.8);      // a single drop falls and blooms
  if (d > 0) {
    reset(c); const y = lerp(260, 600, ei(Math.min(1, d * 1.6))), b = seg(d, .62, 1);
    if (b <= 0) { c.fillStyle = rgba('#9fbbe0', .85); c.beginPath(); c.ellipse(960, y, 13, 19, 0, 0, 7); c.fill(); }
    const g = seg(lt, A(10) + 1.6, A(10) + 4.5);
    if (g > 0) { c.strokeStyle = rgba('#a9c3e4', .55 * (1 - g)); c.lineWidth = 3; c.beginPath(); c.ellipse(960, 600, 20 + 160 * eo(g), 6 + 40 * eo(g), 0, 0, 7); c.stroke();
      c.fillStyle = rgba('#a9c3e4', .3 * (1 - g)); c.beginPath(); c.ellipse(960, 600, 18 + 60 * eo(g), 5 + 16 * eo(g), 0, 0, 7); c.fill(); }
  }
});

// 6 — the field at night: a lantern goes looking for the one sheep
scene(11, 'mist', function () {
  const B = this, X1 = 3900;
  B.bg = item(withSeed(61, () => [fullWash(C.skyN, .9, -300, -300, X1, 1400), hills(-300, X1, 520, 160, .0016, '#3b4a62', .8), hills(-300, X1, 660, 120, .0024, C.hillN, .85), band(720, 1400, C.grassN, .85, -300, X1)]), 0, 0, 0, 1.6);
  B.flock = withSeed(62, () => Array.from({ length: 58 }, () => ({ x: rnd(-200, 2700), y: rnd(740, 1000) })).sort((a, b) => a.y - b.y).map((s, i) => item(sheep(mixc(C.sheepN, '#8f98a8', rnd(0, .3)), rnd() < .5 ? 1 : -1), s.x, s.y, 1 + i * .015, 1.6 + i * .015, { sc: .8 + (s.y - 740) / 260 * .6 })));
  const mound = (x, y, w, h) => [[x - w, y], [x - w * .8, y - h * .6], [x - w * .3, y - h], [x + w * .4, y - h * .9], [x + w * .85, y - h * .4], [x + w, y]];
  B.rocks = item(withSeed(63, () => [wash(mound(3230, 900, 130, 110), '#6a7384', .85), wash(mound(3500, 910, 100, 80), '#5c6576', .85), wash(mound(3230, 900, 130, 50), '#4c5566', .4, 2)]), 0, 0, .8, 2);
  B.lost = item(withSeed(64, () => sheep('#b7bdc8', -1)), 3360, 915, 1.2, 2.2, { sc: 1.25 });
  B.lan = spr(withSeed(65, () => lantern()));
}, function (c, lt, A, E) {
  paper(c); const B = this, lp = eio(seg(lt, A(11) + .6, A(13) + .4)), lx = lerp(260, 3290, lp), ly = 790 + Math.sin(lt * 3.1) * 6;
  const cx = clamp(lx + 260, 960, 3900 - 960 - 300);
  cam(c, cx, 540, 1);
  drawIt(c, B.bg, lt);
  const found = ss(seg(lt, A(13) + .2, A(13) + 1.6)), lv = ss(seg(lt, A(11), A(11) + 1.2));
  lanternGlow(c, lx, ly - 40, 260 + 140 * found, lv);
  drawIt(c, B.rocks, lt); for (const s of B.flock) drawIt(c, s, lt); drawIt(c, B.lost, lt);
  if (lv > 0) { c.save(); c.globalAlpha = lv; c.translate(lx, ly + Math.sin(lt * 3.1) * 4); c.rotate(Math.sin(lt * 3.1) * .05); c.drawImage(B.lan.cv, B.lan.x0, B.lan.y0); c.restore(); }
});

// 7 — she walks away from the light into the dark
scene(14, 'wipe', function () {
  const B = this;
  B.bg = item(withSeed(71, () => [fullWash(C.skyN, .9, -400, -300, 4200, 1400), hills(-400, 4200, 600, 140, .002, '#3a465c', .8), band(760, 1400, '#3b4652', .85, -400, 4200),
    band(820, 900, '#56606c', .5, -400, 4200, 8)]), 0, 0, 0, 1.4);
  B.lan = spr(withSeed(72, () => lantern()));
}, function (c, lt, A, E) {
  paper(c); const B = this, hx = 700 + 74 * lt, cx = Math.max(960, hx - 300);
  cam(c, cx, 540, 1);
  drawIt(c, B.bg, lt);
  const g = c.createLinearGradient(900, 0, 3000, 0); g.addColorStop(0, rgba(C.night3, 0)); g.addColorStop(1, rgba(C.night3, .7)); c.fillStyle = g; c.fillRect(800, -400, 3600, 1900);
  lanternGlow(c, 320, 760, 300, 1); c.drawImage(B.lan.cv, 320 + B.lan.x0, 800 + B.lan.y0);
  figAt(c, 7, { face: 1, ph: lt * 4.6, amp: .3, coat: C.coat }, hx, 880, 1.4, ss(seg(lt, .6, 1.6)));
});

// 8 — a mark painted, an arrow that misses
scene(16, 'wipe', function () {
  const B = this;
  B.bg = item([fullWash('#e3e1dc', .5), band(780, 1400, '#c7ccd4', .5)], 0, 0, 0, 1);
  B.target = item(withSeed(81, () => [wash(ell(1340, 470, 190, 190, 34), '#b4bfcd', .8), wash(ell(1340, 470, 135, 135, 30), '#8d9fb6', .8), wash(ell(1340, 470, 80, 80, 26), '#c4a76d', .85), wash(ell(1340, 470, 32, 32, 18), '#9c7c55', .9),
    S_([[1340, 660], [1300, 860]], 10, INK2, { a: .8 }), S_([[1340, 660], [1390, 860]], 10, INK2, { a: .8 })]), 0, 0, .6, 2.6);
  B.path = qctrl(220, 620, 900, 120, 1720, 250, 40);
  B.trail = withSeed(82, () => mk(B.path, 5, INK2, { prof: 'even', nb: 3, a: .35 }));
  B.arrow = spr(withSeed(83, () => [S_([[-110, 0], [0, 0]], 5, INK, { a: .9 }), wash([[0, -11], [26, 0], [0, 11]], INK, .95, 2, 1), mk(qcurve(-110, 0, -134, -18, 2, 4), 9, '#9c3b2c', { prof: 'leaf', nb: 2 }), mk(qcurve(-110, 0, -134, 18, -2, 4), 9, '#9c3b2c', { prof: 'leaf', nb: 2 })]));
}, function (c, lt, A, E) {
  paper(c); const B = this; cam(c, 960, 540, 1);
  drawIt(c, B.bg, lt); drawIt(c, B.target, lt);
  const f = ei(seg(lt, A(17) + .1, A(17) + 1.3)) * .999;
  if (f > 0) {
    drawS(c, B.trail, f);
    const n = B.path.length - 1, m = n * f, k = Math.floor(m), u = m - k, P = B.path, x = lerp(P[k][0], P[k + 1][0], u), y = lerp(P[k][1], P[k + 1][1], u);
    const a = Math.atan2(P[k + 1][1] - P[k][1], P[k + 1][0] - P[k][0]);
    c.save(); c.translate(x, y); c.rotate(a); c.drawImage(B.arrow.cv, B.arrow.x0, B.arrow.y0); c.restore();
  }
  const q = seg(lt, A(17) + 1.5, A(17) + 2.6);
  if (q > 0) {
    c.strokeStyle = rgba(INK, .7); c.lineWidth = 1.8; c.beginPath(); c.moveTo(1420, 300); c.quadraticCurveTo(1470, 220, 1540, 200 + 0 * q); c.stroke();
    writeText(c, '的を外す', 1560, 196, seg(q, .3, 1), 40, 500, .85, 'left');
  }
});

// 9 — hiding: behind the curtain, the room washing away
scene(18, 'wipe', function () {
  const B = this;
  B.room = item(withSeed(91, () => room(false, { bed: true })), 0, 0, 0, 1.4);
  B.curt = item(withSeed(92, () => [wash([[210, 150], [810, 150], [830, 820], [190, 820]], '#8a94aa', .85),
    ...Array.from({ length: 9 }, (_, i) => S_(qcurve(240 + i * 66, 160, 230 + i * 70, 810, (i % 2 ? 10 : -10), 10), 6, '#6f7990', { a: .5 })),
    wash([[430, 300], [520, 280], [600, 330], [620, 820], [410, 820]], '#5b647a', .45)]), 0, 0, .4, 2);
  B.feet = item([S_(qcurve(470, 838, 510, 840, 1, 4), 12, C.shoe, { a: .85 }), S_(qcurve(540, 840, 584, 842, 1, 4), 12, C.shoe, { a: .85 })], 0, 0, 1.6, 2.2);
}, function (c, lt, A, E) {
  paper(c); const B = this; cam(c, 960, 540, 1);
  drawIt(c, B.room, lt); drawIt(c, B.curt, lt); drawIt(c, B.feet, lt);
  mistOver(c, eio(seg(lt, A(18) + 1.6, E(18) + 1.4)) * .82, .78);
});

// 10 — footsteps coming through the dark, a lantern above them, to a closed door
scene(19, 'mist', function () {
  const B = this, X1 = 3400;
  B.bg = item(withSeed(101, () => [fullWash(C.night3, .9, -300, -300, X1 + 300, 1400), band(640, 1400, '#343d4c', .9, -300, X1 + 300), band(760, 900, '#4a5361', .55, -300, X1 + 300, 10)]), 0, 0, 0, 1.4);
  B.door = item(withSeed(102, () => [wash(rect(2900, 240, 300, 560, 2), '#2a2f3b', .9), wash(rect(2930, 270, 240, 520, 2), C.woodN, .9), S_([[2940, 798], [3160, 798]], 6, ACC2, { a: .8 }), wash(ell(3140, 540, 10, 10, 10), '#9a8a70', .9, 2), wash(rect(2700, 160, 700, 80, 2), '#2b3241', .8)]), 0, 0, .4, 1.8);
  B.steps = withSeed(103, () => Array.from({ length: 22 }, (_, i) => ({ x: 120 + i * 122, y: 830 + (i % 2 ? 26 : -18), L: [wash(ell(0, 0, 22, 9, 14), INK2, .5, 2), wash(ell(-34, 0, 11, 8, 12), INK2, .45, 2)] })).map(s => item(s.L, s.x, s.y, 0, .3)));
  B.lan = spr(withSeed(104, () => lantern()));
}, function (c, lt, A, E) {
  paper(c); const B = this, n = B.steps.length, t1 = A(21) - 1.6, k = seg(lt, .9, t1) * n;
  const lx = 120 + Math.min(k, n - 1) * 122 + 30, cx = clamp(lx + 200, 960, 3400 - 960);
  cam(c, cx, 540, 1);
  drawIt(c, B.bg, lt); drawIt(c, B.door, lt);
  const glow = ss(seg(lt, .6, 1.6)) * (1 + .4 * ss(seg(k, n - 2, n)));
  lanternGlow(c, lx, 620, 280 * glow, Math.min(1, glow));
  B.steps.forEach((s, i) => drawIt(c, s, k - i));
  if (glow > 0) { c.save(); c.globalAlpha = Math.min(1, glow); c.translate(lx, 660 + Math.sin(lt * 3) * 5); c.drawImage(B.lan.cv, B.lan.x0, B.lan.y0); c.restore(); }
});

// 11 — the cross on the hill; then the dawn breaks out from behind it
function calvary(dawn) {
  const L = [];
  if (dawn) L.push(fullWash(C.sky, .7), band(160, 1400, C.dawn3, .6), band(380, 1400, C.dawn1, .75), band(560, 1400, C.dawn2, .45));
  else L.push(fullWash(C.night3, .95), band(380, 1400, '#3c4864', .6));
  L.push(hills(-300, 2300, 700, 260, .0016, dawn ? '#7f9579' : '#2a3342', .92));
  L.push(hills(-300, 2300, 860, 120, .003, dawn ? '#93a585' : '#323b4b', .7));
  L.push(wash([[1310, 760], [1320, 690], [1360, 662], [1400, 690], [1410, 760]], dawn ? '#4a4038' : '#151a24', .95, 2));
  L.push(wash(ell(dawn ? 1480 : 1366, 742, 34, 36, 18), dawn ? '#9d968c' : '#3c4352', .9, 2));
  return L;
}
scene(21, 'wipe', function () {
  const B = this;
  B.night = item(withSeed(111, () => calvary(false)), 0, 0, 0, 1.6);
  B.dawn = spr(withSeed(111, () => calvary(true)));
  B.post = withSeed(112, () => mk(qcurve(960, 330, 962, 646, 2, 12), 26, '#2b2420', { prof: 'even', nb: 7, a: .95 }));
  B.beam = withSeed(113, () => mk(qcurve(872, 414, 1050, 410, -2, 10), 22, '#2b2420', { prof: 'even', nb: 6, a: .95 }));
  B.burst = withSeed(114, () => Array.from({ length: 48 }, (_, i) => vnoise(i * .7) * .35 + .82));
}, function (c, lt, A, E) {
  paper(c); const B = this, z = 1 + .07 * ss(lt / (E(23) + 3)); cam(c, 960, 520, z);
  drawIt(c, B.night, lt);
  const tb = A(23) + 1.6, b = eo(seg(lt, tb, tb + 3.2));
  if (b > 0) {
    c.save(); c.beginPath();
    for (let i = 0; i <= 48; i++) { const a = i / 48 * Math.PI * 2, r = b * 2300 * B.burst[i % 48]; i ? c.lineTo(960 + Math.cos(a) * r, 700 + Math.sin(a) * r * .8) : c.moveTo(960 + Math.cos(a) * r, 700 + Math.sin(a) * r * .8); }
    c.closePath(); c.clip(); c.drawImage(B.dawn.cv, B.dawn.x0, B.dawn.y0); c.restore();
    lanternGlow(c, 960, 690, 900 * b, .9 * (1 - .4 * seg(lt, tb + 3, tb + 6)));
    lanternGlow(c, 1360, 720, 140 * b, .9);
  }
  drawS(c, B.post, eio(seg(lt, A(21) + .8, A(21) + 4.4)));
  drawS(c, B.beam, eio(seg(lt, A(22) + .2, A(22) + 1.5)));
});

// 12 — the light goes back through the town, up the wall, to her window
scene(24, 'wipe', function () {
  const B = this, L = [fullWash('#c9c4c4', .7, -200, -200, 2200, 1300), band(-300, 120, C.dawn1, .6, -200, 2200)];
  withSeed(121, () => {
    for (let r = 0; r < 6; r++) for (let k = 0; k < 8; k++) {
      const x = 120 + k * 220, y = 40 + r * 175, hers = r === 3 && k === 5;
      L.push(wash(rect(x, y, 150, 112, 2), hers ? '#3c4660' : mixc('#a9b6c8', C.dawn1, rnd(0, .6)), hers ? .85 : .7, 2, 2));
      L.push(S_([[x - 6, y + 128], [x + 156, y + 128]], 7, '#857b78', { a: .7 }));
      if (hers) B.hers = [x + 75, y + 56];
    }
  });
  B.wall = item(L, 0, 0, 0, 1.6);
}, function (c, lt, A, E) {
  paper(c); const B = this, z = 1 + .35 * ss(seg(lt, 2, E(24) + 1.4));
  cam(c, lerp(960, B.hers[0], ss(seg(lt, 2, E(24) + 1.4)) * .6), lerp(540, B.hers[1], ss(seg(lt, 2, E(24) + 1.4)) * .6), z);
  drawIt(c, B.wall, lt);
  const g = eio(seg(lt, .8, A(24) + 3)), gy = lerp(1300, B.hers[1], g), gx = lerp(B.hers[0] - 300, B.hers[0], g);
  lanternGlow(c, gx, gy, 200, ss(seg(lt, .6, 1.4)));
  const on = ss(seg(lt, A(24) + 2.6, A(24) + 4));
  if (on > 0) { c.fillStyle = rgba(ACC2, .8 * on); c.fillRect(B.hers[0] - 72, B.hers[1] - 53, 144, 106); lanternGlow(c, B.hers[0], B.hers[1], 260, on); }
});

// 13 — the verse, written on an empty page
const VERSE = ['神はそのひとり子を賜わったほどに、この世を愛して下さった。', 'それは御子を信じる者がひとりも滅びないで、', '永遠の命を得るためである。'], VREF = 'ヨハネによる福音書 3章16節（口語訳）';
scene(25, 'mist', function () {
  this.bg = item(withSeed(131, () => [band(-300, 90, C.dawn1, .45), band(960, 1400, C.dawn3, .35)]), 0, 0, 0, 1.6);
}, function (c, lt, A, E) {
  paper(c); cam(c, 960, 540, 1); drawIt(c, this.bg, lt);
  const t0 = A(25) + .1, t1 = E(25) - .6, tot = VERSE.reduce((s, v) => s + v.length, 0); let acc = 0;
  VERSE.forEach((v, i) => { const a = t0 + (t1 - t0) * acc / tot, b = t0 + (t1 - t0) * (acc + v.length) / tot; acc += v.length; writeText(c, v, 960, 380 + i * 104, seg(lt, a, b), 52, 500, .92); });
  writeText(c, VREF, 960, 720, seg(lt, t1 - .4, t1 + .8), 28, 500, .65);
});

// 14 — a hand holds out a gift; hers come to receive it
scene(26, 'mist', function () {
  const B = this;
  B.bg = item(withSeed(141, () => [fullWash('#efe1cb', .45), band(760, 1400, '#e3cdb0', .45)]), 0, 0, 0, 1.2);
  B.giver = spr(withSeed(142, () => palm(C.linen, C.linenS)));
  B.hers = spr(withSeed(143, () => palm(C.coat, C.coatS, { flip: true })));
  B.hers2 = spr(withSeed(144, () => palm(C.coat, C.coatS, { flip: true })));
  B.gift = spr(withSeed(145, () => gift()));
}, function (c, lt, A, E) {
  paper(c); const B = this; cam(c, 960, 540, 1 + .05 * ss(lt / 20)); drawIt(c, B.bg, lt);
  lanternGlow(c, 900, 560, 620, .55 * ss(seg(lt, .4, 2)));
  const gx = lerp(-700, 0, eo(seg(lt, .3, A(26) + 1.8))), hx = lerp(800, 0, eo(seg(lt, A(27) - .6, A(27) + 1.2)));
  const K = 1.55, D = (s, x, y, a = 1) => { c.save(); c.translate(x, y); c.scale(K, K); c.globalAlpha = a; c.drawImage(s.cv, s.x0, s.y0); c.restore(); };
  D(B.giver, 560 + gx, 640);
  D(B.hers2, 1400 + hx, 700, .9); D(B.hers, 1360 + hx, 660);
  const m = eio(seg(lt, A(27) + 1.4, A(27) + 3.2)), x = lerp(620 + gx, 1290 + hx, m), y = lerp(600, 630, m) - Math.sin(m * Math.PI) * 90;
  c.save(); c.translate(x, y); c.scale(1.3, 1.3); c.drawImage(B.gift.cv, B.gift.x0, B.gift.y0); c.restore();
});

// 15 — she bows her head and prays
scene(28, 'wipe', function () {
  const B = this;
  B.bg = item(withSeed(151, () => [fullWash(mixc(C.wallN, C.wallD, .65), .7), wash(rect(1380, 120, 420, 520, 2), C.dawn1, .7), S_(rect(1380, 120, 420, 520, 1).concat([[1380, 120]]), 14, '#8d7b69', { a: .85 }), band(820, 1400, mixc(C.floorN, C.floorD, .6), .8)]), 0, 0, 0, 1.4);
  B.her = item(withSeed(152, () => bust({ tilt: .32, eyes: 'closed', pray: true })), 880, 700, .6, 2.6, { sc: 1.5 });
}, function (c, lt, A, E) {
  paper(c); const B = this; cam(c, 960, 560, 1 + .07 * ss(lt / 16)); drawIt(c, B.bg, lt);
  lanternGlow(c, 1590, 380, 700, .45 * ss(seg(lt, 1, 4)) + .25 * ss(seg(lt, A(30), E(30))));
  drawIt(c, B.her, lt);
});

// 16 — she draws the curtain back: the dawn comes in
scene(31, 'wipe', function () {
  const B = this;
  B.night = spr(withSeed(161, () => room(false, { bed: false })));
  B.dawn = spr(withSeed(161, () => room(true, { bed: false })));
  B.out = spr(withSeed(162, () => [fullWash(C.sky, .7, 250, 190, 770, 620), band(380, 640, C.dawn1, .8, 250, 770), band(500, 640, C.dawn2, .5, 250, 770), ...blocks(250, 770, { h0: 50, h1: 160, col: '#9aa3b4', windows: false, w0: 70, w1: 130 }).map(e => { xform([e], (x, y) => [x, y + 622]); return e; })]));
  B.curt = spr(withSeed(163, () => [wash([[0, 0], [300, 0], [310, 640], [-10, 640]], '#9aa1b2', .85), ...Array.from({ length: 5 }, (_, i) => S_(qcurve(30 + i * 60, 10, 24 + i * 62, 630, i % 2 ? 8 : -8, 10), 6, '#7a8296', { a: .5 }))]));
  B.up = spr(withSeed(164, () => fig({ face: -1, armUp: true })));
  B.down = spr(withSeed(164, () => fig({ face: -1 })));
}, function (c, lt, A, E) {
  paper(c); const B = this, op = eio(seg(lt, A(31) + .3, A(31) + 2.6)), z = 1 + .03 * ss(lt / 12);
  cam(c, 960, 540, z);
  c.drawImage(B.night.cv, B.night.x0, B.night.y0);
  c.globalAlpha = op; c.drawImage(B.dawn.cv, B.dawn.x0, B.dawn.y0); c.globalAlpha = 1;
  c.save(); c.beginPath(); c.rect(250, 190, 520, 430); c.clip(); c.fillStyle = rgba(C.night3, .85); c.fillRect(250, 190, 520, 430); c.globalAlpha = op; c.drawImage(B.out.cv, B.out.x0, B.out.y0); c.restore(); c.globalAlpha = 1;
  if (op > 0) { c.fillStyle = rgba(ACC2, .28 * op); c.beginPath(); c.moveTo(250, 620); c.lineTo(770, 620); c.lineTo(1500, 1100); c.lineTo(500, 1100); c.fill(); lanternGlow(c, 510, 420, 700, .6 * op); }
  // the curtain: closed over the window, drawn to the left
  const cw = lerp(1, .22, op); c.save(); c.translate(240, 180); c.scale(cw * 1.8, 1); c.drawImage(B.curt.cv, B.curt.x0, B.curt.y0); c.restore();
  const arm = 1 - ss(seg(lt, A(31) + 2.4, A(31) + 3.2)) * (lt > A(31) ? 1 : 0), vis = ss(seg(lt, .4, 1.4));
  const fx = 860, fy = 900, sc = 2.3;
  c.save(); c.translate(fx, fy); c.scale(sc, sc);
  c.globalAlpha = vis * (lt < A(31) - .4 ? 0 : arm); c.drawImage(B.up.cv, B.up.x0, B.up.y0);
  c.globalAlpha = vis * (lt < A(31) - .4 ? 1 : 1 - arm); c.drawImage(B.down.cv, B.down.x0, B.down.y0);
  c.restore(); c.globalAlpha = 1;
});

// 17 — the door opens; she walks out into the morning; the page empties to the title
const TITLE = 'あなたが隠れている場所まで';
scene(33, 'wipe', function () {
  const B = this;
  B.room = spr(withSeed(171, () => room(true, { bed: false, window: false })));
  B.door = spr(withSeed(172, () => [wash(rect(0, 0, 300, 560, 2), C.wood, .9), wash(rect(30, 30, 240, 220, 1), mixc(C.wood, '#000000', .12), .5, 2), wash(rect(30, 290, 240, 240, 1), mixc(C.wood, '#000000', .12), .5, 2), wash(ell(262, 300, 10, 10, 10), '#9a8a70', .9, 2)]));
  B.outside = spr(withSeed(173, () => [fullWash(C.sky, .55, 810, 250, 1110, 810), band(560, 810, C.dawn1, .8, 810, 1110), band(680, 810, '#c2c89a', .6, 810, 1110)]));
  B.frame = spr(withSeed(174, () => [S_(rect(800, 240, 320, 580, 1).concat([[800, 240]]), 18, '#8d7b69', { a: .9, nb: 4 })]));
}, function (c, lt, A, E) {
  paper(c); const B = this, op = eio(seg(lt, .6, 2.6)), walk = seg(lt, 1.6, E(33) + .6), z = 1 + .25 * eio(seg(lt, 1.6, E(33) + 1));
  cam(c, 960, 520, z);
  c.drawImage(B.room.cv, B.room.x0, B.room.y0);
  c.drawImage(B.outside.cv, B.outside.x0, B.outside.y0);
  lanternGlow(c, 960, 560, 520 * op, op);
  c.save(); c.translate(810, 250); c.scale(lerp(1, .12, op), 1); c.drawImage(B.door.cv, B.door.x0, B.door.y0); c.restore();
  c.drawImage(B.frame.cv, B.frame.x0, B.frame.y0);
  if (walk < 1) {
    const sc = lerp(2.2, .95, eio(walk)), x = lerp(1250, 960, eio(walk)), y = lerp(1080, 812, eio(walk));
    figAt(c, 7, { back: true, ph: lt * 4.4, amp: .28 * (1 - seg(walk, .85, 1)) }, x, y, sc, ss(seg(lt, .3, 1.2)) * (1 - ss(seg(walk, .82, 1))));
  }
  mistOver(c, eio(seg(lt, E(33) + .5, E(33) + 2.6)));
  writeText(c, TITLE, 960, 500, seg(lt, E(33) + 2, E(33) + 4.4), 68, 700, .9);
});

// ---------- timeline, transitions, subtitles ----------
function setup() {
  LN = CUES.lines; window.DUR = CUES.dur;
  SC = SCENES.map((s, i) => Object.assign(s, { t0: i ? LN[s.line].t0 - LEAD : 0 }));
  for (const s of SC) { s.build(); s.A = k => LN[k].t0 - s.t0; s.E = k => LN[k].t1 - s.t0; }
}
const BUF = [0, 1].map(() => { const b = document.createElement('canvas'); b.width = W; b.height = H; return b.getContext('2d'); });
function drawScene(c, s, t) { c.save(); s.draw.call(s, c, t - s.t0, s.A, s.E); c.restore(); reset(c); c.globalAlpha = 1; }
function subs(t) {
  for (const l of LN) {
    if (l.cue === 6) continue;
    const t1 = Math.max(l.t1 + .4, l.t0 + 1.8), a = ss(seg(t, l.t0 - .15, l.t0 + .15)) * (1 - ss(seg(t, t1 - .2, t1 + .1)));
    if (a <= 0) continue;
    ctx.save(); reset(ctx); ctx.font = `500 44px ${JP}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const tw = ctx.measureText(l.text).width; ctx.save(); ctx.translate(W / 2, H - 86); ctx.scale((tw + 260) / 2 / 70, 1);
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 70); g.addColorStop(0, rgba(PAPER, .82 * a)); g.addColorStop(.6, rgba(PAPER, .62 * a)); g.addColorStop(1, rgba(PAPER, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 70, 0, 7); ctx.fill(); ctx.restore();
    ctx.shadowColor = rgba(PAPER, .95); ctx.shadowBlur = 10; ctx.fillStyle = rgba(INK, .86 * a);
    ctx.fillText(l.text, W / 2, H - 86); ctx.fillText(l.text, W / 2, H - 86); ctx.restore();
  }
}
function render(t) {
  reset(ctx); ctx.globalAlpha = 1;
  let i = 0; while (i + 1 < SC.length && t >= SC[i + 1].t0) i++;
  const s = SC[i], p = i ? seg(t, s.t0, s.t0 + TR) : 1;
  if (p >= 1) drawScene(ctx, s, t);
  else {
    drawScene(BUF[0], SC[i - 1], t); drawScene(BUF[1], s, t);
    ctx.drawImage(BUF[0].canvas, 0, 0);
    ctx.save(); wavyClip(ctx, eio(p), s.kind); ctx.drawImage(BUF[1].canvas, 0, 0); ctx.restore();
  }
  ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = .55; ctx.drawImage(GRAIN, 0, 0); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  subs(t);
  const f = 1 - ss(seg(t, 0, .6)); if (f > 0) { ctx.globalAlpha = f; ctx.drawImage(PAPER_IMG, 0, 0); ctx.globalAlpha = 1; }
}
window.render = render;
window.TEXTS = t => {
  const out = [], s25 = SC.find(s => s.line === 25), s33 = SC.find(s => s.line === 33);
  if (t > LN[25].t0 && t < LN[26].t0 - LEAD) VERSE.forEach((v, i) => out.push({ id: 'v' + i, text: v, x0: 160, y0: 340 + i * 104, x1: 1760, y1: 420 + i * 104 }));
  if (t > LN[33].t1 + 2) out.push({ id: 'title', text: TITLE, x0: 500, y0: 450, x1: 1420, y1: 550 });
  return out;
};
(async () => {
  CUES = await (await fetch('cues.json')).json();
  PAPER_IMG = new Image(); PAPER_IMG.src = 'paper.jpg'; await PAPER_IMG.decode();
  GRAIN = new Image(); GRAIN.src = 'grain.png'; await GRAIN.decode();
  await Promise.all([`500 44px ${JP}`, `700 68px ${JP}`].map(f => document.fonts.load(f, 'あなた神')));
  setup();
  window.READY = true;
})();
