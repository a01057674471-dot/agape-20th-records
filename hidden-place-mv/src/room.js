// Her room, as one paper stack seen from the front. Every room shot is this same box with a different camera and state.
// Layout (metres, y up): door on the left, coat hook, the window over the desk (her chair left, an empty chair right),
// the bed, the gap between bed and wardrobe where she hides. Layers: sky -.146 · rooftops -.142 · hallway -.139 · door -.135 ·
// wall -.13 · floor -.128 · window panes -.127 · curtains -.118 · chairs -.088 · figure -.078 · desk/bed -.064 · front -.036
import * as THREE from 'three';
import { sheet, skyPanel, burst, text } from './paper.js';
import { stage } from './stage.js';
import { mulberry, clamp, lerp, TAU, vnoise } from './lib.js';
import { PAPER, tint, cut, woman, openHand, piece } from './rig.js';
import { col, WARM } from './look.js';
import { glowDisc } from './bits.js';

export const R = {
  FL: -.1, FY: -.112, H: .105,
  WX0: -.1, WX1: .02, WY0: -.005, WY1: .115, WC: -.04,
  DX0: -.265, DX1: -.185, DY1: .085,
  HOOK: [-.155, .07], DESK: [-.13, .035, -.045], CHAIR: -.148, CHAIR2: .058, CUP1: -.09, CUP2: .005, MIRROR: -.048,
  BED: [.09, .205], GAP: .228, WARD: .262,
};
const W = .62, HH = .4;

export function room(o = {}) {
  const S = stage({ light: [R.WC, .05, -.145], lightR: .16, lightCol: '#e8e6e2', key: .9, amb: .35, floor: .25, fov: 26, keyPos: [.0, .34, .32], keyTarget: [0, -.05, -.1], keyAngle: .9 });
  const { U } = S, ppm = o.ppm ?? 7000;
  const sky = S.add(skyPanel({ w: .5, h: .3, x: R.WC, y: .06, z: -.146, stops: [[0, '#d8dce2'], [.6, '#f2f2f2'], [1, '#ffffff']], ppm: 1400 }));
  const roofs = S.add(sheet({ U, w: .34, h: .2, x: R.WC, y: .02, z: -.142, trans: .45, ppm: 5000, draw: x => {
    x.fillStyle = PAPER; const R2 = mulberry(4); let u = -.17;
    while (u < .17) { const w = .02 + R2() * .03, h = .0 + R2() * .035; x.beginPath(); x.moveTo(u, -.1); x.lineTo(u, h); x.lineTo(u + w / 2, h + .012); x.lineTo(u + w, h); x.lineTo(u + w, -.1); x.fill();
      if (R2() < .5) x.fillRect(u + w * .7, h + .004, .003, .012); u += w + .002; }
    cut(x, () => { const R3 = mulberry(9); for (let k = 0; k < 18; k++) x.fillRect(-.16 + R3() * .32, -.06 + R3() * .07, .004, .005); }); },
    glowDraw: g => { const R3 = mulberry(9); for (let k = 0; k < 18; k++) g.fillRect(-.16 + R3() * .32, -.06 + R3() * .07, .004, .005); }, glow: 1.4, glowCol: '#ffd9a0' }));
  // the hallway beyond the door: plain warm light
  const hall = S.add(skyPanel({ w: .11, h: .2, x: (R.DX0 + R.DX1) / 2, y: R.FL + .08, z: -.139, stops: [[0, '#ffe2bc'], [1, '#fff4e4']], ppm: 600 }));
  const wall = S.add(sheet({ U, w: W, h: HH, y: .03, z: -.13, trans: .32, ppm, draw: x => {
    x.translate(0, -.03); x.fillStyle = PAPER; x.fillRect(-W / 2, R.FL, W, .3);
    cut(x, () => { x.fillRect(R.WX0, R.WY0, R.WX1 - R.WX0, R.WY1 - R.WY0); x.fillRect(R.DX0, R.FL - .01, R.DX1 - R.DX0, R.DY1 - R.FL + .01); });
    // door frame, skirting, the curtain rod, the hook
    x.fillRect(R.DX0 - .006, R.DY1, R.DX1 - R.DX0 + .012, .006); x.fillRect(R.DX0 - .006, R.FL, .006, R.DY1 - R.FL); x.fillRect(R.DX1, R.FL, .006, R.DY1 - R.FL);
    x.fillRect(-W / 2, R.FL, R.DX0 - .006 + W / 2, .008); x.fillRect(R.DX1 + .006, R.FL, W, .008);
    x.fillRect(R.WX0 - .03, R.WY1 + .012, R.WX1 - R.WX0 + .06, .0025); x.beginPath(); x.arc(R.WX0 - .03, R.WY1 + .013, .003, 0, TAU); x.arc(R.WX1 + .03, R.WY1 + .013, .003, 0, TAU); x.fill();
    x.fillRect(R.HOOK[0] - .004, R.HOOK[1], .008, .003); x.fillRect(R.HOOK[0] - .001, R.HOOK[1] - .006, .002, .008);
    x.fillRect(R.WX0 - .006, R.WY0 - .006, R.WX1 - R.WX0 + .012, .006);   // sill
    // a faint paper texture of wallpaper stripes
    cut(x, () => { x.globalAlpha = .12; for (let u = -W / 2; u < W / 2; u += .016) x.fillRect(u, R.FL + .01, .0012, .3); });
  } }));
  const floor = S.add(sheet({ U, w: W, h: .1, y: R.FL - .05, z: -.128, trans: .1, ppm: 4500, draw: x => { x.fillStyle = PAPER; x.fillRect(-W / 2, -.05, W, .1);
    x.fillStyle = 'rgba(0,0,0,.25)'; for (let k = 1; k < 8; k++) x.fillRect(-W / 2, -k * k * .0009, W, .0005); } }));
  // the door: hinged on its left edge; a gap of light under it
  const DW = R.DX1 - R.DX0, DH = R.DY1 - R.FL - .004;
  const door = S.add(sheet({ U, w: DW, h: DH, ax: -DW / 2, ay: 0, x: R.DX0 + DW / 2, y: R.FL + .004 + DH / 2, z: -.135, trans: .14, ppm, draw: x => {
    x.fillStyle = PAPER; x.fillRect(-DW / 2, -DH / 2, DW, DH);
    x.beginPath(); x.arc(DW / 2 - .01, -.004, .0035, 0, TAU); x.fill(); } }));
  const gapGlow = S.add(burst(.16, .05, WARM)); gapGlow.rotation.z = Math.PI; gapGlow.position.set((R.DX0 + R.DX1) / 2, R.FL + .002 - .025, -.1275);
  const gapLine = S.add(glowDisc(.05, WARM)); gapLine.scale.set(1, .05, 1); gapLine.position.set((R.DX0 + R.DX1) / 2, R.FL + .002, -.1272);
  const doorGlow = S.add(burst(.3, .3, WARM)); doorGlow.position.set((R.DX0 + R.DX1) / 2, R.FL - .03 + .15, -.126);
  // the folded cloth that blocks the gap
  const cloth = S.add(sheet({ U, w: .085, h: .012, z: -.1268, trans: .25, ppm: 9000, draw: x => { x.fillStyle = PAPER; x.beginPath(); x.roundRect(-.042, -.006, .084, .01, .003); x.fill();
    cut(x, () => { x.lineWidth = .0006; x.beginPath(); x.moveTo(-.04, -.001); x.lineTo(.04, .0); x.stroke(); }); } }));
  // window panes (casements hinged at the outer edges) and the curtains
  const PW = (R.WX1 - R.WX0) / 2, PH = R.WY1 - R.WY0;
  const pane = side => sheet({ U, w: PW, h: PH, ax: side * PW / 2, ay: 0, x: R.WC + side * PW / 2 - side * PW / 2 + (side < 0 ? -PW / 2 : PW / 2), y: R.WY0 + PH / 2, z: -.127, trans: .3, ppm, draw: x => {
    x.fillStyle = PAPER; x.fillRect(-PW / 2, -PH / 2, PW, PH);
    cut(x, () => { const f = .004; x.fillRect(-PW / 2 + f, f * .5, PW - 2 * f, PH / 2 - f * 1.5); x.fillRect(-PW / 2 + f, -PH / 2 + f, PW - 2 * f, PH / 2 - f * 1.5); }); } });
  const paneL = S.add(pane(-1)), paneR = S.add(pane(1));
  paneL.position.set(R.WX0, R.WY0 + PH / 2, -.127); paneR.position.set(R.WX1, R.WY0 + PH / 2, -.1269);
  const CW = .085, CH = R.WY1 - R.WY0 + .045;
  const curtain = side => sheet({ U, w: CW, h: CH, ax: side * CW / 2, ay: CH / 2, z: -.118, trans: .78, ppm: 6000, finish: { rim: .15, under: .1 }, draw: x => {
    x.fillStyle = PAPER; x.beginPath(); x.moveTo(-CW / 2, CH / 2);
    for (let u = -CW / 2; u <= CW / 2 + 1e-4; u += CW / 10) x.lineTo(u, CH / 2 - .001 * Math.sin(u * 300));
    x.lineTo(CW / 2, -CH / 2); for (let u = CW / 2; u >= -CW / 2; u -= CW / 10) x.lineTo(u, -CH / 2 + .0025 * Math.sin(u * 260 + 1)); x.closePath(); x.fill();
    cut(x, () => { x.globalAlpha = .35; x.lineWidth = .0007; for (let u = -CW / 2 + .006; u < CW / 2; u += CW / 10) { x.beginPath(); x.moveTo(u, CH / 2 - .006); x.lineTo(u + .001, -CH / 2 + .008); x.stroke(); } }); } });
  const curL = S.add(curtain(-1)), curR = S.add(curtain(1));
  const ROD = R.WY1 + .013;
  // the coat on its hook (dust in the window light later), the desk, two chairs, cups, the mirror
  const coat = S.add(piece(U, [-.022, .022, -.085, .004], x => {
    x.beginPath(); x.moveTo(0, 0); x.lineTo(-.01, -.006); x.quadraticCurveTo(-.017, -.01, -.018, -.03); x.lineTo(-.02, -.08); x.lineTo(.02, -.08); x.lineTo(.018, -.03); x.quadraticCurveTo(.017, -.01, .01, -.006); x.closePath(); x.fill();
    cut(x, () => { x.lineWidth = .0008; x.beginPath(); x.moveTo(0, -.008); x.lineTo(.002, -.078); x.stroke(); x.fillRect(-.016, -.05, .01, .0008); });
  }, { trans: .12, ppm }));
  coat.position.set(R.HOOK[0], R.HOOK[1] - .004, -.124);
  const [dx0, dx1, dy] = R.DESK;
  const desk = S.add(sheet({ U, w: .2, h: .08, x: (dx0 + dx1) / 2, y: (dy + R.FY) / 2, z: -.064, trans: .06, ppm, draw: x => {
    x.fillStyle = PAPER; const L = (dx0 - dx1) / 2, Rr = -L, T = (dy - R.FY) / 2, B = -T;
    x.fillRect(L, T - .006, Rr - L, .006); x.fillRect(L + .004, B, .005, T - B); x.fillRect(Rr - .009, B, .005, T - B);
    x.fillRect(L + .03, T - .022, .06, .016); cut(x, () => x.fillRect(L + .056, T - .015, .008, .0015)); } }));
  const chair = (face) => piece(U, [-.022, .022, 0, .09], x => { x.scale(face, 1);
    x.fillRect(-.016, .035, .034, .004); x.fillRect(-.016, 0, .003, .036); x.fillRect(.014, 0, .003, .036); x.fillRect(-.016, .036, .003, .05); x.fillRect(-.016, .08, .004, .006);
    x.fillRect(-.016, .05, .003, .002); x.fillRect(-.016, .062, .003, .002); }, { trans: .06, ppm });
  const chair1 = S.add(chair(1)); chair1.position.set(R.CHAIR, R.FY, -.088);
  const chair2 = S.add(chair(-1)); chair2.position.set(R.CHAIR2, R.FY, -.088);
  const cupDraw = x => { x.beginPath(); x.moveTo(-.006, .0085); x.lineTo(.006, .0085); x.quadraticCurveTo(.006, .0, .003, 0); x.lineTo(-.003, 0); x.quadraticCurveTo(-.006, 0, -.006, .0085); x.fill();
    x.lineWidth = .0012; x.strokeStyle = PAPER; x.beginPath(); x.arc(.0068, .005, .0022, -1.4, 1.4); x.stroke(); x.fillRect(-.008, -.0008, .016, .0012); };
  const cup1 = S.add(piece(U, [-.01, .011, -.002, .01], cupDraw, { ppm: 20000 })); cup1.position.set(R.CUP1, dy, -.0635);
  const cup2 = S.add(piece(U, [-.01, .011, -.002, .01], cupDraw, { ppm: 20000 })); cup2.position.set(R.CUP2, dy, -.0635);
  const steam = S.add(sheet({ U, w: .014, h: .03, z: -.0634, ppm: 12000, trans: .9, glow: .6, glowRes: .25, glowCol: '#ffffff', finish: { rim: 0, under: 0 }, draw: x => {
      x.strokeStyle = PAPER; x.lineWidth = .0007; for (const s of [-1, 1]) { x.beginPath(); for (let v = -.014; v < .014; v += .001) x.lineTo(s * .002 + .0025 * Math.sin(v * 380 + s), v); x.stroke(); } },
    glowDraw: g => { g.strokeStyle = '#fff'; g.lineWidth = .0012; for (const s of [-1, 1]) { g.beginPath(); for (let v = -.014; v < .014; v += .001) g.lineTo(s * .002 + .0025 * Math.sin(v * 380 + s), v); g.stroke(); } } }));
  steam.position.set(R.CUP1, dy + .026, -.0634);
  // the mirror on its stand: front (a pale glass that catches the window) and back (plain board); a turn swaps them
  const MW = .03, MH = .04;
  const mirrorDraw = back => x => { x.beginPath(); x.ellipse(0, MH / 2 + .008, MW / 2, MH / 2, 0, 0, TAU); x.fill(); x.fillRect(-.0015, 0, .003, .01); x.fillRect(-.009, 0, .018, .0025);
    if (!back) cut(x, () => { x.beginPath(); x.ellipse(0, MH / 2 + .008, MW / 2 - .003, MH / 2 - .003, 0, 0, TAU); x.fill(); }); };
  const mirFront = S.add(piece(U, [-MW / 2 - .002, MW / 2 + .002, -.001, MH + .012], mirrorDraw(false), { ppm: 14000 })); mirFront.position.set(R.MIRROR, dy, -.0636);
  const mirBack = S.add(piece(U, [-MW / 2 - .002, MW / 2 + .002, -.001, MH + .012], mirrorDraw(true), { ppm: 14000 })); mirBack.position.set(R.MIRROR, dy, -.0636);
  const glass = S.add(piece(U, [-MW / 2, MW / 2, -.001, MH + .012], x => { x.beginPath(); x.ellipse(0, MH / 2 + .008, MW / 2 - .0025, MH / 2 - .0025, 0, 0, TAU); x.fill(); },
    { ppm: 10000, trans: .5, glow: .9, glowCol: '#eef2ff', glowDraw: g => { const gr = g.createLinearGradient(-MW / 2, MH, MW / 2, 0); gr.addColorStop(0, '#fff'); gr.addColorStop(.5, '#777'); gr.addColorStop(1, '#bbb'); g.fillStyle = gr; g.beginPath(); g.ellipse(0, MH / 2 + .008, MW / 2 - .0025, MH / 2 - .0025, 0, 0, TAU); g.fill(); } }));
  glass.position.set(R.MIRROR, dy, -.0638);
  // her reflection in the glass (a tiny head-and-shoulders silhouette, facing out), shown when she stands before it
  const refl = S.add(piece(U, [-.014, .014, -.002, .035], x => { x.beginPath(); x.ellipse(0, .022, .0065, .0085, 0, 0, TAU); x.fill(); x.beginPath(); x.moveTo(-.014, .0); x.quadraticCurveTo(-.012, .012, -.003, .013); x.lineTo(.003, .013); x.quadraticCurveTo(.012, .012, .014, 0); x.fill();
    x.beginPath(); x.ellipse(0, .026, .0078, .0075, 0, Math.PI * .95, Math.PI * 2.05); x.fill(); x.fillRect(-.0078, .012, .003, .014); x.fillRect(.0048, .012, .003, .014); }, { ppm: 14000, trans: .1 }));
  refl.position.set(R.MIRROR, dy + .009, -.06375);
  // the bed and the box under it; the wardrobe
  const [bx0, bx1] = R.BED;
  const bed = S.add(sheet({ U, w: .16, h: .07, x: (bx0 + bx1) / 2, y: R.FY + .035, z: -.06, trans: .06, ppm, draw: x => {
    x.fillStyle = PAPER; const L = -(bx1 - bx0) / 2, Rr = -L, B = -.035;
    x.fillRect(L, B, .005, .03); x.fillRect(Rr - .006, B, .006, .068);   // foot post, headboard
    x.fillRect(L, B + .022, Rr - L, .008);   // rail
    x.beginPath(); x.moveTo(L, B + .03); x.lineTo(L, B + .045); x.quadraticCurveTo(L + .01, B + .052, L + .04, B + .05); x.quadraticCurveTo(L + .09, B + .056, Rr - .03, B + .05); x.quadraticCurveTo(Rr - .02, B + .058, Rr - .006, B + .055); x.lineTo(Rr - .006, B + .03); x.closePath(); x.fill();   // blanket
    x.fillRect(Rr - .006 - .002, B, .003, .068); } }));
  const box = S.add(piece(U, [-.025, .025, 0, .016], x => { x.fillRect(-.024, 0, .048, .013); x.fillRect(-.025, .011, .05, .004); cut(x, () => x.fillRect(-.024, .0105, .048, .0007)); }, { ppm, trans: .1 }));
  const ward = S.add(sheet({ U, w: .1, h: .24, x: R.WARD + .05, y: R.FY + .12, z: -.062, trans: .05, ppm: 5000, draw: x => { x.fillStyle = PAPER; x.fillRect(-.05, -.12, .1, .24);
    x.strokeStyle = 'rgba(0,0,0,.35)'; x.lineWidth = .0008; x.strokeRect(-.044, -.11, .042, .2); x.strokeRect(.004, -.11, .042, .2); } }));
  const front = S.add(sheet({ U, w: W + .2, h: .2, y: -.235, z: -.036, trans: .02, ppm: 2500, shadow: false, draw: x => { x.fillStyle = PAPER; x.fillRect(-.5, -.1, 1, .2); } }));
  front.position.y = R.FY - .1 - .016;
  // her, and the hand that waits
  const her = woman(S, R.H, -.078);
  const presence = S.add(glowDisc(.05, WARM)); presence.position.z = -.0755;
  const hand = openHand(S, .011, -.058, { arm: 7 });
  const motes = S.add(dust(U));
  const title = S.add(sheet({ U, w: .2, h: .04, x: -.02, y: .135, z: -.05, trans: .1, ppm: 12000, shadow: false, recv: false, finish: { rim: .3, under: 0 }, glow: .9, glowCol: '#fff1de', glowRes: 1,
    draw: x => text(x, '내가 숨은 곳까지', 0, 0, .019, 'Myeongjo', { fill: PAPER, weight: 700 }), glowDraw: g => { g.fillStyle = '#000'; g.fillRect(-.1, -.02, .2, .04); text(g, '내가 숨은 곳까지', 0, 0, .019, 'Myeongjo', { fill: '#fff', weight: 700 }); } }));
  const BK = [R.DESK[0] + .05, R.DESK[2] + .0012];
  const book = S.add(piece(U, [-.026, .026, -.002, .004], x => { x.fillRect(-.024, 0, .048, .0018); x.beginPath(); x.moveTo(-.024, .0018); x.quadraticCurveTo(-.012, .0042, 0, .0022); x.quadraticCurveTo(.012, .0042, .024, .0018); x.fill(); }, { ppm: 20000, trans: .5 }));
  book.position.set(BK[0], BK[1], -.0633);
  const leaf = S.add(piece(U, [-.001, .025, -.001, .004], x => { x.beginPath(); x.moveTo(0, .0022); x.quadraticCurveTo(.012, .0045, .024, .002); x.lineTo(.024, .0012); x.quadraticCurveTo(.012, .0035, 0, .0012); x.fill(); }, { ppm: 20000, trans: .6 }));
  leaf.position.set(BK[0], BK[1], -.0632);
  const ALL = { wall, floor, door, paneL, paneR, curL, curR, coat, desk, chair1, chair2, cup1, cup2, mirFront, mirBack, bed, box, ward, front, roofs, cloth, glass, refl };

  return {
    S, U, her, hand, presence, ALL,
    // st: the room's state for this frame (every field optional)
    apply(st, t) {
      const p = st.p ?? 0;
      tint(wall, col('wall', p)); tint(floor, col('floor', p)); tint(door, col('wall', p), .78); tint(roofs, col('far', p));
      for (const m of [paneL, paneR]) tint(m, col('wall', p), .9);
      for (const m of [curL, curR]) tint(m, col('cloth', p));
      tint(cloth, col('cloth', p), .8); tint(coat, col('furn', p), 1.15);
      for (const m of [desk, chair1, chair2, cup1, cup2, mirBack, bed, box, ward]) tint(m, col('furn', p));
      tint(mirFront, col('furn', p)); tint(glass, col('cloth', p), .9); tint(refl, col('fig', p), 1.3); tint(front, col('front', p)); tint(steam, '#ffffff');
      her.tint(col('fig', p)); hand.tint('#e6cfb4');
      sky.material.color.set(col('sky', p)).multiplyScalar(st.skyK ?? 1.25);
      U.uLightCol.value.set(col('light', p)); U.uLit.value = st.lit ?? (.85 + .15 * p);
      S.key.color.set(col('key', p)); S.key.intensity = st.key ?? (.7 + .2 * p); S.amb.color.set(col('amb', p)); S.amb.intensity = st.amb ?? (.32 + .08 * p);
      // door, its gap of light, the cloth
      const dOpen = clamp(st.door ?? 0); door.scale.x = 1 - .9 * dOpen;
      hall.material.color.set(WARM).multiplyScalar((st.hall ?? 1) * 1.6);
      const gl = (st.gap ?? 1) * (1 - clamp(st.clothCover ?? 0));
      gapGlow.userData.set(.55 * gl + 1.4 * dOpen); gapLine.userData.set(1.6 * gl); doorGlow.userData.set(1.6 * dOpen);
      cloth.visible = st.cloth !== undefined; if (cloth.visible) cloth.position.set(st.cloth, R.FL + .001, -.1268);
      // window and curtains (0 open … 1 closed over the window centre)
      paneL.scale.x = 1 - .85 * clamp(st.win ?? 0); paneR.scale.x = 1 - .85 * clamp(st.win ?? 0);
      const sway = st.sway ?? 0, w1 = sway * (vnoise(t * .7) - .5), w2 = sway * (vnoise(t * .7 + 9) - .5);
      const cl = st.curL ?? .1, cr = st.curR ?? .1;
      curL.position.set(R.WX0 - .03, ROD, -.118); curL.scale.x = lerp(.28, (R.WC - R.WX0 + .03) / CW, cl) * (1 + .12 * w1); curL.rotation.z = -.12 * w1 * (1 - cl * .5);
      curR.position.set(R.WX1 + .03, ROD, -.1179); curR.scale.x = lerp(.28, (R.WX1 + .03 - R.WC) / CW, cr) * (1 + .12 * w2); curR.rotation.z = .12 * w2 * (1 - cr * .5);
      // the coat leaves the hook when she wears it
      coat.visible = (st.coat ?? 1) > .5;
      // steam over her cup fades as the tea cools; the second cup only on the second morning
      steam.visible = (st.steam ?? 0) > .01; steam.material.userData.u.uGlowLit.value = (st.steam ?? 0) * .9; steam.position.y = R.DESK[2] + .024 + .002 * Math.sin(t * 1.3);
      steam.material.opacity = 1; cup2.visible = !!st.cup2;
      // the mirror: m = 0 facing the room, 1 turned to the wall; a turn passes through edge-on
      const m = clamp(st.mirror ?? 0), sx = Math.abs(Math.cos(m * Math.PI));
      const showBack = m > .5; mirFront.visible = !showBack; glass.visible = !showBack; mirBack.visible = showBack;
      for (const q of [mirFront, mirBack, glass]) q.scale.x = Math.max(.02, sx);
      glass.material.userData.u.uGlowLit.value = (st.glass ?? .35); refl.visible = !showBack && (st.refl ?? 0) > .01; refl.scale.set(Math.max(.02, sx), 1, 1);
      // the box slides out from under the bed into the gap
      box.position.set(lerp(.17, R.GAP + .005, clamp(st.box ?? 0)), R.FY, -.0665);
      // the presence: a warm light beside her, at her height
      presence.position.x = st.presX ?? (R.GAP + .02); presence.position.y = st.presY ?? (R.FY + .03); presence.userData.set(st.pres ?? 0);
      hand.g.visible = !!st.hand; if (st.hand) hand.set(st.hand.x, st.hand.y, st.hand.rot ?? 0, st.hand.close ?? 0, st.hand.glow ?? 1);
      motes.visible = (st.dust ?? 0) > .01; if (motes.visible) motes.userData.set(st.dust, t);
      tint(title, col('cloth', p), 1.05); title.visible = (st.title ?? 0) > .001; const [tx, ty] = st.titleXY ?? [.155, .07]; title.position.set(tx, ty, -.05); title.material.userData.u.uClip.value.set(tx - .1 - 1, ty, 1 + .2 * clamp(st.title ?? 0), 0);
      tint(book, col('cloth', p), .95); tint(leaf, col('cloth', p), 1.05); book.visible = leaf.visible = !!st.book;
      if (st.book) { const f = (st.flip ?? 0) % 1; leaf.scale.x = Math.cos(f * Math.PI); leaf.position.y = BK[1] + .006 * Math.sin(f * Math.PI); }
      if (st.her) her.set({ ...st.her, y: st.her.y ?? (R.FY + st.her.hy * R.H) }); else her.root.visible = false;
    },
  };
}

// dust in a shaft of window light: tiny additive points drifting
function dust(U) {
  const n = 70, R2 = mulberry(31), pos = new Float32Array(n * 3), base = [];
  for (let i = 0; i < n; i++) base.push([R2(), R2(), R2(), R2()]);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const m = new THREE.PointsMaterial({ color: new THREE.Color('#fff4e0'), size: .0009, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
  const p = new THREE.Points(g, m);
  p.userData.set = (k, t) => { m.opacity = k * .55;
    for (let i = 0; i < n; i++) { const [a, b, c, d] = base[i], u = (a + t * .004 * (b - .5)) % 1, v = (b + t * .006 * (c + .2)) % 1;
      // inside a slanted shaft from the window down to the left
      pos[i * 3] = R.WX0 - .02 - u * .14 + v * .02; pos[i * 3 + 1] = R.WY1 - v * .16 + .01 * Math.sin(t * .3 + d * 9); pos[i * 3 + 2] = -.11 + c * .05; }
    g.attributes.position.needsUpdate = true; };
  return p;
}
