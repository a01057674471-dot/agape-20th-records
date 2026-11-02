// Close-up stacks: each is its own small box at a larger scale than the room. apply(st, t) sets one frame; st.p is the colour phase.
import * as THREE from 'three';
import { sheet, skyPanel, burst, text } from './paper.js';
import { stage } from './stage.js';
import { mulberry, clamp, lerp, TAU, vnoise } from './lib.js';
import { PAPER, tint, cut, piece, openHand, herHand, woman } from './rig.js';
import { col, WARM } from './look.js';
import { glowDisc } from './bits.js';

const light = (S, U, st, p) => { U.uLightCol.value.set(col('light', p)); U.uLit.value = st.lit ?? (.85 + .15 * p); S.key.color.set(col('key', p)); S.key.intensity = st.key ?? (.7 + .2 * p); S.amb.color.set(col('amb', p)); S.amb.intensity = st.amb ?? (.32 + .08 * p); };
const frontBand = (U, y, z, w = 1.2) => sheet({ U, w, h: .3, y: y - .15, z, trans: .02, ppm: 1500, shadow: false, draw: x => { x.fillStyle = PAPER; x.beginPath(); x.moveTo(-w / 2, -.15); x.lineTo(-w / 2, .15); for (let u = -w / 2; u <= w / 2; u += .01) x.lineTo(u, .15 - .004 + .004 * Math.sin(u * 13)); x.lineTo(w / 2, -.15); x.fill(); } });

// — HANDS: his open hand waiting (fingers up, palm to us, thumb toward her); hers comes in from the left and lays her fingertips in his palm —
export function hands() {
  const S = stage({ light: [.04, .0, -.14], lightR: .2, lightCol: '#e8e6e2', key: .8, amb: .3, floor: .3, keyPos: [0, .3, .3], keyTarget: [0, -.02, -.1] });
  const { U } = S;
  const back = S.add(sheet({ U, w: .9, h: .5, z: -.13, trans: .4, ppm: 2400, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5);
    cut(x, () => { x.globalAlpha = .1; for (let u = -.45; u < .45; u += .03) x.fillRect(u, -.25, .002, .5); }); } }));
  const glow = S.add(glowDisc(.22, WARM)); glow.position.set(.04, .0, -.09);
  const his = openHand(S, .07, -.06, { arm: 5, flip: true });
  const hers = herHand(S, .06, -.057);
  const front = S.add(frontBand(U, -.13, -.02));
  return { S, U, his, hers, glow, apply(st, t) { const p = st.p ?? 0;
    tint(back, col('wall', p), 1.0); tint(front, col('front', p)); his.tint('#e6cfb4'); tint(hers.m, col('fig', p), 1.1);
    light(S, U, st, p); glow.userData.set(st.glow ?? .6);
    his.set(st.hx ?? .05, st.hy ?? -.06, -Math.PI / 2 + (st.hrot ?? 0), st.close ?? 0, st.hglow ?? 1);
    hers.set(st.sx ?? -.3, st.sy ?? .03, st.srot ?? -.2); } };
}

// — DOOR: the bottom of a door, the slit of light under it, the floor; a folded cloth pushed into the slit by her hand.
// out = the same kind of door seen from the alley: the slit is dark (someone inside has blocked it) and the cloth's edge shows.
export function doorCU(o = {}) {
  const out = !!o.out;
  const S = stage({ light: [0, -.02, -.15], lightR: .18, lightCol: '#e8e6e2', key: .7, amb: .3, floor: .3, keyPos: [-.05, .3, .3], keyTarget: [0, -.05, -.1] });
  const { U } = S, GY = -.04, FY = -.047;
  const hall = S.add(skyPanel({ w: .8, h: .2, y: GY, z: -.145, stops: [[0, '#fff0dc'], [1, '#ffe6c4']], ppm: 500 }));
  const wall = S.add(sheet({ U, w: .9, h: .5, z: -.125, trans: out ? .25 : .3, ppm: 3000, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5);
    cut(x, () => x.fillRect(-.16, -.2, .32, .5));
    x.fillRect(-.175, -.2, .015, .5); x.fillRect(.16, -.2, .015, .5);
    if (out) { cut(x, () => { x.globalAlpha = .9; x.lineWidth = .0015; for (let r = 0; r < 14; r++) { const yy = FY + .01 + r * .025; x.beginPath(); x.moveTo(-.45, yy); x.lineTo(-.18, yy); x.moveTo(.18, yy); x.lineTo(.45, yy); x.stroke();
      for (let c = 0; c < 8; c++) { const xx = (r % 2 ? .012 : 0) + .19 + c * .04; x.beginPath(); x.moveTo(xx, yy); x.lineTo(xx, yy + .025); x.moveTo(-xx, yy); x.lineTo(-xx, yy + .025); x.stroke(); } } }); }
  } }));
  const door = S.add(sheet({ U, w: .36, h: .4, y: GY + .2, z: -.13, trans: .12, ppm: 3500, draw: x => { x.fillStyle = PAPER; x.fillRect(-.18, -.2, .36, .4);
    x.fillRect(-.18, -.2, .36, .012);   // the threshold strip of the door's bottom rail
    x.strokeStyle = 'rgba(0,0,0,.35)'; x.lineWidth = .0015; x.strokeRect(-.13, -.17, .26, .3); } }));
  const floor = S.add(sheet({ U, w: .9, h: .3, y: FY - .15, z: -.11, trans: .1, ppm: 3000, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.15, .9, .3);
    if (!out) { x.fillStyle = 'rgba(0,0,0,.3)'; for (let k = 1; k < 9; k++) x.fillRect(-.45, .15 - k * k * .0026, .9, .0012); } } }));
  const spill = S.add(burst(.5, .12, WARM)); spill.rotation.z = Math.PI; spill.position.set(0, FY + .001 - .06, -.105);
  const slit = S.add(glowDisc(.2, WARM)); slit.scale.set(1, .04, 1); slit.position.set(0, (GY + FY) / 2, -.1045);
  const shadowBar = S.add(sheet({ U, w: .06, h: .02, y: (GY + FY) / 2, z: -.14, trans: 0, ppm: 1500, draw: x => { x.fillStyle = PAPER; x.fillRect(-.03, -.01, .06, .02); } }));
  const CL = .2;
  const cloth = S.add(sheet({ U, w: CL, h: .03, z: -.104, trans: .3, ppm: 6000, finish: { rim: .4, under: .25 }, draw: x => { x.fillStyle = PAPER;
    x.beginPath(); x.moveTo(-CL / 2, -.012); x.lineTo(CL / 2 - .006, -.012); x.quadraticCurveTo(CL / 2, -.012, CL / 2, -.004); x.lineTo(CL / 2, .004); x.quadraticCurveTo(CL / 2, .012, CL / 2 - .008, .012); x.lineTo(-CL / 2 + .01, .012); x.quadraticCurveTo(-CL / 2 - .002, .0, -CL / 2, -.012); x.fill();
    cut(x, () => { x.lineWidth = .001; x.beginPath(); x.moveTo(-CL / 2 + .01, .001); x.quadraticCurveTo(0, -.001, CL / 2 - .01, .002); x.stroke(); for (let u = -CL / 2 + .02; u < CL / 2; u += .05) { x.beginPath(); x.moveTo(u, .011); x.lineTo(u + .01, .006); x.stroke(); } }); } }));
  const hand = herHand(S, .03, -.1, { arm: 8 });
  const front = S.add(frontBand(U, -.135, -.03));
  return { S, U, apply(st, t) { const p = st.p ?? 0;
    tint(wall, out ? col('wall', p) : col('wall', p), out ? .9 : 1); tint(door, col('furn', p), out ? 1.5 : 1.25); tint(floor, col('floor', p)); tint(cloth, col('cloth', p), .85); tint(front, col('front', p)); tint(hand.m, col('fig', p)); tint(shadowBar, '#000000');
    light(S, U, st, p);
    const g = (st.gap ?? 1) * (1 - clamp(st.cover ?? 0));
    hall.material.color.set(WARM).multiplyScalar(out ? 0 : 1.6 * (st.gap ?? 1)); spill.userData.set(.9 * g); slit.userData.set(1.3 * g);
    shadowBar.visible = st.shadowX !== undefined; if (shadowBar.visible) shadowBar.position.x = st.shadowX;
    cloth.visible = st.cloth !== undefined; if (cloth.visible) cloth.position.set(st.cloth, st.clothY ?? (FY + .0105), st.clothZ ?? -.104);
    hand.m.visible = st.hand !== undefined; if (hand.m.visible) hand.set(st.hand[0], st.hand[1], st.hand[2] ?? 0); } };
}

// — TEA: her cup on the desk by the window; the steam thins as the tea cools. cups = 2 on the second morning —
export function teaCU() {
  const S = stage({ light: [-.05, .0, -.15], lightR: .16, lightCol: '#e8e6e2', key: .7, amb: .3, floor: .3, keyPos: [-.05, .3, .3], keyTarget: [0, -.05, -.1] });
  const { U } = S, DY = -.05;
  const sky = S.add(skyPanel({ w: .8, h: .5, z: -.148, stops: [[0, '#d8dce2'], [1, '#ffffff']], ppm: 600 }));
  const wall = S.add(sheet({ U, w: .9, h: .5, z: -.13, trans: .32, ppm: 2500, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5); cut(x, () => { x.fillRect(-.14, -.045, .3, .35); }); x.fillRect(.01, -.045, .012, .35); x.fillRect(-.14, .08, .3, .01); } }));
  const desk = S.add(sheet({ U, w: .9, h: .3, y: DY - .15, z: -.07, trans: .06, ppm: 2500, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.15, .9, .3); x.fillRect(-.45, .13, .9, .02); } }));
  const cupDraw = x => { x.beginPath(); x.moveTo(-.03, .04); x.lineTo(.03, .04); x.bezierCurveTo(.03, .006, .02, 0, .012, 0); x.lineTo(-.012, 0); x.bezierCurveTo(-.02, 0, -.03, .006, -.03, .04); x.fill();
    x.lineWidth = .005; x.strokeStyle = PAPER; x.beginPath(); x.ellipse(.034, .024, .009, .011, 0, -1.5, 1.5); x.stroke(); x.beginPath(); x.ellipse(0, -.001, .045, .004, 0, 0, TAU); x.fill(); };
  const cup = S.add(piece(U, [-.05, .05, -.006, .045], cupDraw, { ppm: 9000, trans: .08 })); cup.position.set(-.06, DY, -.068);
  const cup2 = S.add(piece(U, [-.05, .05, -.006, .045], cupDraw, { ppm: 9000, trans: .08 })); cup2.position.set(.12, DY, -.09); cup2.scale.set(-.8, .8, 1);
  const wisp = (seed) => sheet({ U, w: .06, h: .16, z: -.067, ppm: 5000, trans: .9, glow: 1, glowCol: '#ffffff', shadow: false, finish: { rim: 0, under: 0 }, draw: x => {},
    glowDraw: g => { const R2 = mulberry(seed); g.lineCap = 'round'; g.filter = 'blur(2px)'; for (let k = 0; k < 3; k++) { g.strokeStyle = `rgba(255,255,255,${.6 + R2() * .4})`; g.lineWidth = .003 + R2() * .003; g.beginPath(); const o2 = R2() * 9, a = .006 + R2() * .008;
      for (let v = -.075; v < .075; v += .002) g.lineTo((k - 1) * .008 + a * Math.sin(v * 70 + o2) * (1 + (v + .075) * 8), v); g.stroke(); } } });
  const w1 = S.add(wisp(3)), w2 = S.add(wisp(7)), w3 = S.add(wisp(11));
  for (const w of [w1, w2, w3]) { w.material.transparent = true; w.material.alphaTest = 0; w.material.opacity = 0; w.material.alphaToCoverage = false; w.material.depthWrite = false; }
  const front = S.add(frontBand(U, DY - .09, -.03));
  return { S, U, apply(st, t) { const p = st.p ?? 0;
    tint(wall, col('wall', p)); tint(desk, col('furn', p), 1.1); tint(cup, col('furn', p), 1.5); tint(cup2, col('furn', p), 1.5); tint(front, col('front', p));
    sky.material.color.set(col('sky', p)).multiplyScalar(1.2); light(S, U, st, p); cup2.visible = !!st.cup2;
    const k = st.steam ?? 1;
    w1.position.set(-.06 + .003 * Math.sin(t * .9), DY + .12 + (t * .012) % .02, -.067); w2.position.set(-.058 + .004 * Math.sin(t * 1.1 + 2), DY + .11 + ((t + .4) * .012) % .02, -.0665);
    w3.position.set(-.062 + .003 * Math.sin(t * .7 + 4), DY + .13 + ((t + .9) * .01) % .02, -.0668);
    for (const [w, ph] of [[w1, 0], [w2, 1.7], [w3, 3.1]]) { w.material.userData.u.uGlowLit.value = k * (1.3 + .5 * Math.sin(t * 1.3 + ph)); w.visible = k > .01; } } };
}

// — DESK, seen from above: what came out of the box. A crumpled notebook (smoothed by her hand), an old photo, an unsent letter; then she writes. —
export function deskTop() {
  const S = stage({ light: [.0, .02, -.15], lightR: .25, lightCol: '#e8e6e2', key: .9, amb: .35, floor: .4, keyPos: [-.12, .25, .3], keyTarget: [0, 0, -.1] });
  const { U } = S;
  const top = S.add(sheet({ U, w: .9, h: .5, z: -.13, trans: .25, ppm: 2400, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5);
    cut(x, () => { x.globalAlpha = .55; x.lineWidth = .0009; const R2 = mulberry(5); for (let k = 0; k < 9; k++) { const y = -.25 + k * .06; x.beginPath(); x.moveTo(-.45, y); for (let u = -.45; u < .45; u += .01) x.lineTo(u, y + .002 * Math.sin(u * 20 + k) ); x.stroke(); }
      for (let k = 0; k < 40; k++) { const y = -.25 + R2() * .5, u = -.45 + R2() * .9; x.beginPath(); x.moveTo(u, y); x.quadraticCurveTo(u + .03, y + .004, u + .07, y); x.stroke(); } }); } }));
  const NW = .2, NH = .14, NX = -.02, NY = .0;
  const page = (crumple) => piece(U, [-NW / 2, NW / 2, -NH / 2, NH / 2], x => {
    x.fillRect(-NW / 2, -NH / 2, NW, NH);
    x.strokeStyle = 'rgba(70,80,100,.45)'; x.lineWidth = .0005; for (let y = -NH / 2 + .016; y < NH / 2 - .008; y += .013) { x.beginPath(); x.moveTo(-NW / 2 + .012, y); x.lineTo(-.006, y); x.moveTo(.008, y); x.lineTo(NW / 2 - .01, y); x.stroke(); }
    x.fillStyle = 'rgba(0,0,0,.35)'; x.fillRect(-.0012, -NH / 2, .0024, NH);
    if (crumple) { const R2 = mulberry(12); for (let k = 0; k < 34; k++) { let u = (R2() - .5) * NW, v = (R2() - .5) * NH; x.lineWidth = .0004 + R2() * .0006; x.strokeStyle = R2() < .5 ? 'rgba(0,0,0,.28)' : 'rgba(255,255,255,.35)'; x.beginPath(); x.moveTo(u, v); for (let j = 0; j < 2; j++) { u += (R2() - .5) * .06; v += (R2() - .5) * .04; x.lineTo(clamp(u, -NW / 2, NW / 2), clamp(v, -NH / 2, NH / 2)); } x.stroke(); }
      const g = x.createRadialGradient(0, 0, .01, 0, 0, .12); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.25)'); x.fillStyle = g; x.fillRect(-NW / 2, -NH / 2, NW, NH); }
  }, { ppm: 9000, trans: .5, finish: { rim: .3, under: .2 } });
  const crumpled = S.add(page(true)), smooth = S.add(page(false));
  crumpled.position.set(NX, NY, -.1); smooth.position.set(NX - NW / 2, NY, -.0995);
  smooth.geometry.translate(NW / 2, 0, 0);   // anchored at its left edge: the smoothing wipes left → right
  // the writing: two handwritten lines, revealed left → right by a clip circle centred far to the left
  const LINES = [['내가 숨은 곳까지', .036], ['주님은 버리지 않으셨죠', .01]];
  const lines = LINES.map(([s, y]) => { const m = sheet({ U, w: NW / 2 - .01, h: .024, x: NX + NW / 4 + .002, y: NY + y, z: -.099, trans: .1, ppm: 12000, shadow: false, finish: { rim: 0, under: 0 },
      draw: x => text(x, s, -(NW / 2 - .01) / 2 + .004, 0, s.length > 9 ? .0105 : .0125, 'Pen', { fill: PAPER, align: 'left' }) }); S.add(m); m.userData.y = NY + y; return m; });
  const photo = S.add(piece(U, [-.042, .042, -.032, .032], x => { x.fillRect(-.04, -.03, .08, .06); cut(x, () => { x.fillRect(-.034, -.024, .068, .048); }); }, { ppm: 9000, trans: .3 }));
  const photoImg = S.add(piece(U, [-.036, .036, -.026, .026], x => { x.globalAlpha = 1; x.fillRect(-.035, -.025, .07, .05); x.fillStyle = '#000';
    // two figures side by side on a bench, one smaller: herself as a child and someone beside her
    cut(x, () => { x.beginPath(); x.arc(-.008, .006, .0045, 0, TAU); x.fill(); x.fillRect(-.013, -.02, .01, .022); x.beginPath(); x.arc(.012, .0, .0035, 0, TAU); x.fill(); x.fillRect(.008, -.02, .008, .016); x.fillRect(-.03, -.022, .06, .003); }); }, { ppm: 9000, trans: .7 }));
  const letter = S.add(piece(U, [-.05, .05, -.032, .032], x => { x.fillRect(-.048, -.03, .096, .06); cut(x, () => { x.lineWidth = .0008; x.beginPath(); x.moveTo(-.048, .03); x.lineTo(0, -.004); x.lineTo(.048, .03); x.stroke(); }); x.fillRect(.03, .012, .012, .014); }, { ppm: 9000, trans: .35 }));
  const box = S.add(piece(U, [-.12, .12, -.08, .08], x => { x.fillRect(-.115, -.075, .23, .15); cut(x, () => x.fillRect(-.105, -.065, .21, .13)); }, { ppm: 4000, trans: .1 }));
  const handS = herHand(S, .045, -.09, { arm: 8 });
  const pen = S.add(piece(U, [-.006, .1, -.004, .004], x => { x.beginPath(); x.moveTo(0, 0); x.lineTo(.012, .0028); x.lineTo(.1, .0028); x.lineTo(.1, -.0028); x.lineTo(.012, -.0028); x.closePath(); x.fill(); }, { ppm: 12000 }));
  pen.position.z = -.088;
  const front = S.add(sheet({ U, w: .9, h: .5, z: -.02, trans: 0, ppm: 800, shadow: false, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5); cut(x, () => { x.beginPath(); x.ellipse(0, 0, .28, .2, 0, 0, TAU); x.fill(); }); } }));
  return { S, U, NW, NX, NY, lines, apply(st, t) { const p = st.p ?? 1;
    tint(top, col('furn', p), 2.0); tint(crumpled, col('cloth', p), .95); tint(smooth, col('cloth', p), .95); tint(photo, '#d8d0c0'); tint(photoImg, '#8a7a66'); tint(letter, col('cloth', p), .9); tint(box, col('furn', p), 1.4);
    tint(handS.m, col('fig', p), 1.2); tint(pen, col('fig', p)); tint(front, col('front', p)); lines.forEach(m => tint(m, '#2a2a30'));
    light(S, U, st, p); front.visible = (st.vig ?? 1) > .5;
    const it = st.items ?? [0, 0, 0];   // 0 hidden in the box … 1 laid out
    box.visible = (st.box ?? 0) > .01; box.position.set(.0, lerp(-.42, -.22, clamp(st.box ?? 0)), -.115);
    const lay = (m, k, tx, ty, r) => { m.visible = k > .001; m.position.set(lerp(0, tx, k), lerp(-.25, ty, k), m.position.z); m.rotation.z = lerp(.6, r, k); };
    lay(crumpled, it[0], NX, NY, 0); lay(photo, it[1], .17, .07, .12); lay(photoImg, it[1], .17, .07, .12); lay(letter, it[2], .16, -.085, -.08);
    photo.position.z = -.1; photoImg.position.z = -.0998; letter.position.z = -.1;
    const sm = clamp(st.smooth ?? 0); smooth.visible = sm > .002 && it[0] > .99; smooth.scale.x = Math.max(.002, sm);
    if (sm > .995) crumpled.visible = false;
    const wr = st.write ?? [0, 0];
    lines.forEach((m, i) => { const k = clamp(wr[i]); m.visible = k > .001; const x0 = NX + .006; m.material.userData.u.uClip.value.set(x0 - 1, m.userData.y, 1 + k * (NW / 2 - .01), 0); });
    handS.m.visible = !!st.hand; if (st.hand) handS.set(...st.hand);
    pen.visible = !!st.pen; if (st.pen) { pen.position.x = st.pen[0]; pen.position.y = st.pen[1]; pen.rotation.z = st.pen[2] ?? .5; } } };
}

// — SING: her head and shoulders in profile at the window; her jaw follows the voice —
export function sing() {
  const S = stage({ light: [.12, .03, -.15], lightR: .18, lightCol: '#e8e6e2', key: .8, amb: .35, floor: .3, keyPos: [.1, .3, .3], keyTarget: [0, -.02, -.1] });
  const { U } = S, HS = .05;
  const sky = S.add(skyPanel({ w: .8, h: .5, z: -.148, stops: [[0, '#d0d6dc'], [1, '#ffffff']], ppm: 600 }));
  const roofs = S.add(sheet({ U, w: .5, h: .2, x: .1, y: -.08, z: -.144, trans: .5, ppm: 2500, draw: x => { x.fillStyle = PAPER; const R2 = mulberry(4); let u = -.25;
    while (u < .25) { const w = .04 + R2() * .05, h = R2() * .06; x.beginPath(); x.moveTo(u, -.1); x.lineTo(u, h); x.lineTo(u + w / 2, h + .02); x.lineTo(u + w, h); x.lineTo(u + w, -.1); x.fill(); u += w + .003; } } }));
  const wall = S.add(sheet({ U, w: .9, h: .5, z: -.13, trans: .32, ppm: 2500, draw: x => { x.fillStyle = PAPER; x.fillRect(-.45, -.25, .9, .5); cut(x, () => x.fillRect(.05, -.1, .17, .22)); x.fillRect(.13, -.1, .007, .22); x.fillRect(.05, .02, .17, .006); x.fillRect(.04, -.11, .19, .01); } }));
  const curtain = S.add(sheet({ U, w: .12, h: .34, ax: -.06, ay: .17, z: -.115, trans: .78, ppm: 3000, finish: { rim: .15, under: .1 }, draw: x => { x.fillStyle = PAPER; x.fillRect(-.06, -.17, .12, .34);
    cut(x, () => { x.globalAlpha = .35; x.lineWidth = .001; for (let u = -.05; u < .06; u += .012) { x.beginPath(); x.moveTo(u, .16); x.lineTo(u + .002, -.16); x.stroke(); } }); } }));
  // the head: crown, brow, nose, upper lip, long hair down her back; the jaw (lower lip, chin) is its own piece hinged under the ear
  const sc = x => x.scale(HS, HS);
  const head = piece(U, [-.8 * HS, .75 * HS, -1.3 * HS, .75 * HS], x => { sc(x);
    x.beginPath(); x.moveTo(.14, -.45); x.quadraticCurveTo(.3, -.43, .35, -.34); x.lineTo(.40, -.245); x.lineTo(.50, -.235); x.quadraticCurveTo(.545, -.215, .535, -.19);
    x.quadraticCurveTo(.51, -.15, .515, -.12); x.lineTo(.53, -.095); x.quadraticCurveTo(.56, -.08, .605, -.04); x.quadraticCurveTo(.61, -.015, .585, .0);
    x.quadraticCurveTo(.53, .08, .52, .14); x.quadraticCurveTo(.545, .19, .52, .23); x.quadraticCurveTo(.5, .33, .46, .38);
    x.quadraticCurveTo(.5, .42, .42, .48);   // a fringe of hair over the brow
    x.bezierCurveTo(.3, .64, .02, .7, -.22, .62); x.bezierCurveTo(-.5, .5, -.6, .2, -.58, -.1);
    x.bezierCurveTo(-.58, -.5, -.66, -.9, -.74, -1.25); x.lineTo(-.3, -1.25); x.quadraticCurveTo(-.26, -.8, -.22, -.55);
    x.quadraticCurveTo(-.05, -.47, .14, -.45); x.closePath(); x.fill();
    x.beginPath(); x.moveTo(-.24, -.5); x.quadraticCurveTo(0, -.45, .2, -.44); x.quadraticCurveTo(.16, -.75, .22, -1.3); x.lineTo(-.3, -1.3); x.closePath(); x.fill();   // neck
  }, { ppm: 9000, trans: .08 });
  const jaw = piece(U, [-.05 * HS, .6 * HS, -.56 * HS, .02 * HS], x => { sc(x);
    x.beginPath(); x.moveTo(.3, -.36); x.lineTo(.40, -.245); x.lineTo(.5, -.245); x.quadraticCurveTo(.54, -.26, .53, -.29); x.quadraticCurveTo(.51, -.32, .49, -.33);
    x.quadraticCurveTo(.51, -.37, .5, -.42); x.quadraticCurveTo(.48, -.5, .38, -.51); x.quadraticCurveTo(.3, -.5, .25, -.46); x.closePath(); x.fill();
  }, { ppm: 9000, trans: .08 });
  const body = piece(U, [-1.0 * HS, .9 * HS, -3.2 * HS, -.6 * HS], x => { sc(x);
    // shoulders and chest in profile, the hair falling over the back
    x.beginPath(); x.moveTo(-.25, -.8); x.quadraticCurveTo(-.7, -.95, -.78, -1.3); x.lineTo(-.85, -3.2); x.lineTo(.7, -3.2); x.quadraticCurveTo(.72, -2.2, .6, -1.85);
    x.quadraticCurveTo(.66, -1.6, .45, -1.25); x.quadraticCurveTo(.3, -1.0, .2, -.85); x.closePath(); x.fill();
  }, { ppm: 7000, trans: .06 });
  const fig = new THREE.Group(); fig.position.z = -.08; S.scene.add(fig);
  fig.add(body); body.add(head); head.position.set(0, 0, .0005); head.add(jaw); jaw.position.z = .0003;
  const glow = S.add(glowDisc(.12, WARM)); glow.position.set(-.12, -.02, -.1);
  const front = S.add(frontBand(U, -.15, -.03));
  return { S, U, apply(st, t) { const p = st.p ?? 1;
    tint(wall, col('wall', p)); tint(roofs, col('far', p)); tint(curtain, col('cloth', p)); for (const m of [head, jaw, body]) tint(m, col('fig', p)); tint(front, col('front', p));
    sky.material.color.set(col('sky', p)).multiplyScalar(1.25); light(S, U, st, p); glow.userData.set(st.pres ?? 0);
    curtain.position.set(.235 + .004 * Math.sin(t * .5), .14, -.115); curtain.rotation.z = .02 * Math.sin(t * .4); curtain.scale.x = st.curtain ?? .55;
    fig.position.x = st.x ?? -.035; fig.position.y = st.y ?? .01;
    body.rotation.z = (st.lean ?? 0) + .006 * Math.sin(t * 1.6); head.rotation.z = st.head ?? 0; jaw.rotation.z = -(st.jaw ?? 0); } };
}

// — ALLEY: a long street of house fronts in soft daylight, travelled alongside her; it ends at a closed door with a cloth under it —
export const ALLEY = { XT: 1.05, Y: -.07, H: .1 };
export function alley() {
  const S = stage({ light: [0, .1, -.15], lightR: .35, lightCol: '#fbf1e2', key: 1.0, amb: .4, floor: .45, keyPos: [-.1, .35, .3], keyTarget: [0, -.05, -.1], shadowR: 8 });
  const { U } = S, Y = ALLEY.Y, XT = ALLEY.XT, X0 = -.4, X1 = 2.1, LW = X1 - X0, LC = (X0 + X1) / 2;
  const sky = S.add(skyPanel({ w: .8, h: .5, z: -.148, stops: [[0, '#cfd8e0'], [.7, '#f4f4f2'], [1, '#ffffff']], ppm: 600 }));
  const far = S.add(sheet({ U, w: LW, h: .3, x: LC, y: Y + .08, z: -.14, trans: .55, ppm: 1600, draw: x => { x.fillStyle = PAPER; const R2 = mulberry(21); let u = -LW / 2;
    while (u < LW / 2) { const w = .03 + R2() * .06, h = .0 + R2() * .07; x.beginPath(); x.moveTo(u, -.15); x.lineTo(u, h); if (R2() < .6) { x.lineTo(u + w / 2, h + .025); } x.lineTo(u + w, h); x.lineTo(u + w, -.15); x.fill(); if (R2() < .4) x.fillRect(u + w * .2, h, .006, .02); u += w; } } }));
  // house fronts: a run of facades with doors and windows; one door (at XT) is the one she stops at
  const doors = [], wins = [];
  { const R2 = mulberry(8); let u = X0; while (u < X1) { const w = .12 + R2() * .08; if (Math.abs(u + w / 2 - XT) < .12) { doors.push([XT, 1]); u = XT + .09; continue; } doors.push([u + w * (.25 + R2() * .5), 0]); wins.push([u + w * .5, R2()]); u += w; } }
  const DW = .036, DH = .07;
  const houses = S.add(sheet({ U, w: LW, h: .34, x: LC, y: Y + .17, z: -.11, trans: .22, ppm: 2600, draw: x => { x.translate(-LC, -(Y + .17)); x.fillStyle = PAPER;
    const R2 = mulberry(15); let u = X0;
    while (u < X1) { const w = .1 + R2() * .12, h = .12 + R2() * .1; x.beginPath(); x.moveTo(u, Y); x.lineTo(u, Y + h); x.lineTo(u + w * .5, Y + h + .02 * R2()); x.lineTo(u + w, Y + h); x.lineTo(u + w, Y); x.fill(); x.fillRect(u - .002, Y + h - .002, w + .004, .004); u += w; }
    cut(x, () => { for (const [dx] of doors) x.fillRect(dx - DW / 2, Y, DW, DH);
      for (const [wx, r] of wins) { x.fillRect(wx - .012, Y + .085, .024, .028); }
      x.lineWidth = .0006; for (let k = 0; k < 60; k++) { const yy = Y + .006 + k * .009; x.beginPath(); x.moveTo(X0, yy); x.lineTo(X1, yy); x.globalAlpha = .18; x.stroke(); } x.globalAlpha = 1; });
    for (const [wx] of wins) { x.fillRect(wx - .0008, Y + .085, .0016, .028); x.fillRect(wx - .012, Y + .099, .024, .0016); x.fillRect(wx - .015, Y + .083, .03, .003); }
    for (const [dx] of doors) { x.fillRect(dx - DW / 2 - .004, Y + DH, DW + .008, .004); x.fillRect(dx - DW / 2 - .006, Y, DW + .012, .003); } } }));
  const interiors = S.add(sheet({ U, w: LW, h: .2, x: LC, y: Y + .1, z: -.118, trans: .5, ppm: 1500, draw: x => { x.fillStyle = PAPER; x.fillRect(-LW / 2, -.1, LW, .2); } }));
  const doorSheets = S.add(sheet({ U, w: LW, h: DH, x: LC, y: Y + DH / 2 + .0015, z: -.114, trans: .1, ppm: 2600, draw: x => { x.translate(-LC, -(Y + DH / 2 + .0015)); x.fillStyle = PAPER;
    for (const [dx] of doors) { x.fillRect(dx - DW / 2, Y + .0015, DW, DH - .0015); cut(x, () => { x.lineWidth = .0006; x.globalAlpha = .7; x.strokeRect(dx - DW / 2 + .005, Y + .008, DW - .01, DH - .02); }); x.beginPath(); x.arc(dx + DW / 2 - .006, Y + DH / 2, .0018, 0, TAU); x.fill(); } } }));
  // the cloth under the target door, seen from outside: a pale fold in the dark slit
  const tcloth = S.add(sheet({ U, w: DW - .004, h: .004, x: XT, y: Y + .0018, z: -.1135, trans: .3, ppm: 9000, finish: { rim: .3, under: 0 }, draw: x => { x.fillStyle = PAPER; x.fillRect(-DW / 2, -.002, DW, .0032); } }));
  const lane = S.add(sheet({ U, w: LW, h: .2, x: LC, y: Y - .1, z: -.1, trans: .12, ppm: 1600, draw: x => { x.fillStyle = PAPER; x.fillRect(-LW / 2, -.1, LW, .2);
    cut(x, () => { x.globalAlpha = .6; x.lineWidth = .0008; for (let k = 1; k < 5; k++) { x.beginPath(); x.moveTo(-LW / 2, .1 - k * k * .004); x.lineTo(LW / 2, .1 - k * k * .004); x.stroke(); } }); } }));
  // a washing line across the lane with a few cloths that move in the wind
  const lineY = Y + .125, cloths = [];
  const wline = S.add(sheet({ U, w: LW, h: .03, x: LC, y: lineY, z: -.07, trans: .1, ppm: 1600, shadow: false, draw: x => { x.translate(-LC, -lineY); x.fillStyle = PAPER; for (let s = X0; s < X1; s += .5) { x.beginPath(); x.moveTo(s, lineY + .01); x.quadraticCurveTo(s + .25, lineY - .01, s + .5, lineY + .01); x.lineTo(s + .5, lineY + .0115); x.quadraticCurveTo(s + .25, lineY - .0085, s, lineY + .0115); x.fill(); } } }));
  { const R2 = mulberry(3); for (let s = X0 + .2; s < X1; s += .5) for (let k = 0; k < 2; k++) { const w = .025 + R2() * .02, h = .03 + R2() * .02, cx = s + .1 + k * .14;
      const m = S.add(piece(U, [-w / 2, w / 2, -h, .002], x => { x.fillRect(-w / 2, -h, w, h + .002); cut(x, () => { x.globalAlpha = .5; x.lineWidth = .0006; x.beginPath(); x.moveTo(-w / 2, -h * .3); x.lineTo(w / 2, -h * .3); x.stroke(); }); }, { ppm: 5000, trans: .75 }));
      m.position.set(cx, lineY + .01 - .02 * (1 - Math.pow((cx - s - .25) / .25, 2)) + .001, -.069); m.userData.ph = R2() * 9; cloths.push(m); } }
  const her = woman(S, ALLEY.H, -.085);
  const pres = S.add(glowDisc(.07, WARM)); pres.position.z = -.088;
  // near occluders: lamp posts and plant pots rushing past
  const near = S.add(sheet({ U, w: LW * 1.2, h: .4, x: LC, y: Y, z: -.035, trans: .02, ppm: 1200, shadow: false, draw: x => { x.translate(-LC, -Y); x.fillStyle = PAPER;
    x.fillRect(X0 - .3, Y - .25, LW * 1.4, .19);
    const R2 = mulberry(44); for (let u = X0; u < X1 + .3; u += .35 + R2() * .25) { if (R2() < .5) { x.fillRect(u, Y - .1, .006, .3); x.beginPath(); x.ellipse(u + .003, Y + .2, .014, .007, 0, 0, TAU); x.fill(); }
      else { x.beginPath(); x.moveTo(u - .02, Y - .06); x.lineTo(u + .02, Y - .06); x.lineTo(u + .016, Y - .03); x.lineTo(u - .016, Y - .03); x.fill(); for (let k = 0; k < 7; k++) { x.beginPath(); x.ellipse(u + (k - 3) * .006, Y - .02 + .01 * Math.sin(k * 2), .007, .014, (k - 3) * .2, 0, TAU); x.fill(); } } } } }));
  return { S, U, her, apply(st, t) { const p = st.p ?? 2;
    tint(far, col('far', p), 1.08); tint(houses, col('wall', p), .92); tint(interiors, '#1a1a1c'); tint(doorSheets, col('furn', p), 1.3); tint(tcloth, col('cloth', p), .9); tint(lane, col('floor', p), 1.15); tint(wline, col('fig', p));
    cloths.forEach(m => tint(m, col('cloth', p))); her.tint(col('fig', p)); tint(near, col('front', p), 1.2);
    sky.material.color.set(col('sky', p)).multiplyScalar(1.2); sky.position.x = st.camX ?? 0; U.uLight.value.x = (st.camX ?? 0) + .05;
    light(S, U, st, p);
    for (const m of cloths) m.rotation.z = .12 * (vnoise(t * .6 + m.userData.ph) - .5) + .05 * Math.sin(t * 1.3 + m.userData.ph);
    pres.visible = (st.pres ?? 0) > .01; pres.userData.set(st.pres ?? 0); pres.position.x = st.presX ?? 0; pres.position.y = Y + .045;
    tcloth.position.x = XT + (st.clothShift ?? 0);
    if (st.her) her.set({ ...st.her, y: st.her.y ?? (Y + st.her.hy * ALLEY.H) }); } };
}
