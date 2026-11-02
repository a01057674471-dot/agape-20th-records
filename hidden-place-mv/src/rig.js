// The jointed paper figures: the woman (profile, facing +x; joints rotate only) and the open hand that waits beside her.
import * as THREE from 'three';
import { sheet } from './paper.js';
import { lerp, clamp, eio, TAU } from './lib.js';

export const PAPER = '#9a9a9a', BASE = new THREE.Color(PAPER).r;
export const tint = (m, hex, k = 1) => m.material.color.set(hex).multiplyScalar(k / BASE);
export const cut = (x, fn) => { x.save(); x.globalCompositeOperation = 'destination-out'; x.fillStyle = '#000'; x.strokeStyle = '#000'; fn(); x.restore(); };
const C = new THREE.Color(), D = new THREE.Color();
export const mixHex = (a, b, k) => '#' + C.set(a).lerp(D.set(b), clamp(k)).getHexString();

// one jointed part: drawn in its own coordinates with the joint at the origin; box = [x0, x1, y0, y1] around the joint (metres).
// The mesh's origin is the joint; its position starts at 0 (the parent places it).
export function piece(U, box, fn, o = {}) {
  const [x0, x1, y0, y1] = box, w = x1 - x0, h = y1 - y0, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const m = sheet({ U, w, h, ax: -cx, ay: -cy, trans: o.trans ?? .06, ppm: o.ppm ?? 5200, glow: o.glow, glowCol: o.glowCol, glowRes: o.glowRes, finish: o.finish ?? { rim: .25, under: .2, rimPx: 2, underPx: 2 },
    draw: x => { x.translate(-cx, -cy); x.fillStyle = PAPER; fn(x); },
    glowDraw: o.glowDraw ? gx => { gx.fillStyle = '#000'; gx.fillRect(-9, -9, 18, 18); gx.translate(-cx, -cy); gx.fillStyle = '#fff'; o.glowDraw(gx); } : null });
  m.position.set(0, 0, 0); return m;
}
function part(U, H, box, fn, o = {}) { return piece(U, box.map(v => v * H), x => { x.scale(H, H); fn(x); }, { ppm: Math.min(26000, 2600 / H), ...o }); }
const rr = (x, a, b, c, d, r) => { x.beginPath(); x.roundRect(a, b, c - a, d - b, r); x.fill(); };
function limb(x, len, w0, w1) { x.beginPath(); x.moveTo(-w0 / 2, 0); x.quadraticCurveTo(-w0 * .62, -len * .5, -w1 / 2, -len); x.arc(0, -len, w1 / 2, Math.PI, 0); x.quadraticCurveTo(w0 * .62, -len * .5, w0 / 2, 0); x.arc(0, 0, w0 / 2, 0, Math.PI); x.fill(); }

// — the woman. H = standing height in metres. Units below are fractions of H. —
const TH = .30, NK = .045, UA = .165, FA = .15, THI = .245, SHI = .235;
export function woman(S, H, z, o = {}) {
  const U = S.U, root = new THREE.Group(); root.position.z = z; S.scene.add(root);
  const torsoDraw = (jacket) => x => {
    x.beginPath(); x.moveTo(-.055, jacket ? -.13 : -.02); x.bezierCurveTo(-.07, .08, -.06, .2, -.05, TH - .01);
    x.quadraticCurveTo(-.02, TH + .03, .02, TH + .015); x.quadraticCurveTo(.06, TH - .02, .068, .2);
    x.quadraticCurveTo(.08, .17, .06, .14); x.bezierCurveTo(.045, .09, .05, .03, .058, jacket ? -.13 : -.02);
    x.closePath(); x.fill();
    if (jacket) { x.beginPath(); x.moveTo(-.02, TH + .02); x.lineTo(.035, TH + .035); x.lineTo(.028, TH - .03); x.closePath(); x.fill();
      cut(x, () => { x.lineWidth = .004; x.beginPath(); x.moveTo(.03, TH - .01); x.lineTo(.045, -.12); x.stroke(); x.fillRect(-.03, .02, .03, .004); }); }
    rr(x, -.06, -.06, .062, .02, .03);   // hips
  };
  const torso = part(U, H, [-.09, .1, -.15, TH + .06], torsoDraw(false));
  const jacket = part(U, H, [-.09, .1, -.15, TH + .06], torsoDraw(true)); jacket.visible = false;
  const head = part(U, H, [-.1, .1, -.02, .2], x => {
    x.fillRect(-.022, -.01, .04, .05);   // neck
    x.beginPath(); x.moveTo(.01, .03); x.lineTo(.03, .045);
    x.bezierCurveTo(.05, .05, .055, .06, .056, .075);   // chin
    x.lineTo(.06, .082); x.lineTo(.056, .086); x.lineTo(.063, .092); x.lineTo(.058, .097);   // lips
    x.lineTo(.062, .108); x.lineTo(.072, .118); x.lineTo(.06, .127);   // nose
    x.quadraticCurveTo(.058, .14, .06, .15);   // brow
    x.bezierCurveTo(.055, .19, .0, .205, -.035, .19);   // crown
    x.bezierCurveTo(-.07, .17, -.075, .12, -.07, .07);   // back of the head, hair falling
    x.bezierCurveTo(-.068, .03, -.06, -.005, -.07, -.03); x.lineTo(-.04, -.025); x.lineTo(-.02, .03);
    x.closePath(); x.fill();
  });
  head.position.set(.0 * H, (TH + .01) * H, .0003);
  const mkArm = (dz) => {
    const ua = part(U, H, [-.035, .035, -UA - .02, .03], x => limb(x, UA, .05, .04));
    const fa = part(U, H, [-.04, .05, -FA - .07, .03], x => { limb(x, FA, .04, .03); x.beginPath(); x.ellipse(.004, -FA - .03, .02, .034, -.1, 0, TAU); x.fill(); x.beginPath(); x.ellipse(.018, -FA - .012, .008, .02, -.6, 0, TAU); x.fill(); });
    fa.position.set(0, -UA * H, .0002); ua.add(fa); ua.position.set(.0, (TH - .025) * H, dz); torso.add(ua); return [ua, fa];
  };
  const mkLeg = (dz) => {
    const th = part(U, H, [-.05, .05, -THI - .03, .04], x => limb(x, THI, .085, .055));
    const sh = part(U, H, [-.045, .11, -SHI - .05, .03], x => { limb(x, SHI, .055, .038); x.beginPath(); x.moveTo(-.022, -SHI + .01); x.lineTo(-.024, -SHI - .03); x.lineTo(.085, -SHI - .03); x.quadraticCurveTo(.08, -SHI - .005, .02, -SHI + .0); x.closePath(); x.fill(); });
    sh.position.set(0, -THI * H, .0002); th.add(sh); th.position.z = dz; root.add(th); return [th, sh];
  };
  const [fua, ffa] = mkArm(-.0025), [fth, fsh] = mkLeg(-.0015);
  root.add(torso); torso.add(head, jacket);
  const [nth, nsh] = mkLeg(.0015), [nua, nfa] = mkArm(.0025);
  const all = [torso, jacket, head, fua, ffa, nua, nfa, fth, fsh, nth, nsh];
  return {
    root, all, H, torso, head,
    tint(hex) { all.forEach(m => tint(m, hex)); },
    // p: { x, y (hip), face (1 right / -1 left), torso, head, nua, nfa, fua, ffa, nth, nsh, fth, fsh, jacket }
    set(p) {
      root.position.x = p.x; root.position.y = p.y; root.scale.x = p.face ?? 1; root.visible = p.vis ?? true;
      torso.rotation.z = p.torso ?? 0; head.rotation.z = p.head ?? 0;
      nua.rotation.z = p.nua ?? 0; nfa.rotation.z = p.nfa ?? 0; fua.rotation.z = p.fua ?? 0; ffa.rotation.z = p.ffa ?? 0;
      nth.rotation.z = p.nth ?? 0; nsh.rotation.z = p.nsh ?? 0; fth.rotation.z = p.fth ?? 0; fsh.rotation.z = p.fsh ?? 0;
      jacket.visible = (p.jacket ?? 0) > .5;
    },
  };
}
// the woman's poses (angles in radians; the hip height y is in units of H above the floor)
export const POSE = {
  stand: { torso: 0, head: 0, nua: .05, nfa: .1, fua: -.05, ffa: .1, nth: 0, nsh: 0, fth: 0, fsh: 0, hy: THI + SHI + .035 },
  // hugging her knees on the floor, head down on them
  curl: { torso: -.5, head: -.6, nua: .8, nfa: 1.3, fua: .7, ffa: 1.4, nth: 2.25, nsh: -2.2, fth: 2.1, fsh: -2.05, hy: .055 },
  // the same, head lifted
  curlUp: { torso: -.3, head: .1, nua: .6, nfa: 1.3, fua: .5, ffa: 1.4, nth: 2.25, nsh: -2.2, fth: 2.1, fsh: -2.05, hy: .055 },
  // on the floor, back to the door, legs out, head back: relief
  sitBack: { torso: .22, head: .35, nua: .2, nfa: .5, fua: .1, ffa: .4, nth: 1.5, nsh: -.2, fth: 1.45, fsh: -.35, hy: .055 },
  sitChair: { torso: -.05, head: -.05, nua: .55, nfa: .95, fua: .5, ffa: 1.0, nth: 1.55, nsh: -1.55, fth: 1.5, fsh: -1.5, hy: THI + SHI - .02 },
  kneel: { torso: -.35, head: -.3, nua: .9, nfa: .4, fua: .7, ffa: .5, nth: .25, nsh: -1.75, fth: .2, fsh: -1.7, hy: THI * .97 + .03 },
  reach: { torso: -.1, head: .0, nua: 1.3, nfa: .25, fua: .2, ffa: .3, nth: 0, nsh: 0, fth: 0, fsh: 0, hy: THI + SHI + .035 },
};
export function walk(ph, amp = 1) {   // a step cycle, ph in radians
  const s = Math.sin(ph), s2 = Math.sin(ph + Math.PI);
  return { torso: -.04, head: .02, nth: .38 * s * amp, fth: .38 * s2 * amp, nsh: -.75 * Math.max(0, Math.sin(ph - .9)) * amp, fsh: -.75 * Math.max(0, Math.sin(ph + Math.PI - .9)) * amp,
    nua: -.28 * s * amp, nfa: .25, fua: -.28 * s2 * amp, ffa: .25, hy: THI + SHI + .035 - .012 * Math.abs(Math.cos(ph)) * amp };
}
export function blend(a, b, k) { k = eio(k); const o = {}; for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) { const va = a[key] ?? b[key], vb = b[key] ?? a[key]; o[key] = typeof va === 'number' ? lerp(va, vb, k) : (k < .5 ? va : vb); } return o; }
// keyed poses: keys = [[t, poseObj], ...] → pose at t
export function poseAt(t, keys, dur = .9) {
  let i = 0; while (i + 1 < keys.length && t >= keys[i + 1][0]) i++;
  const [t0, p0] = keys[i]; if (i + 1 >= keys.length) return p0;
  const [t1, p1] = keys[i + 1], d = keys[i + 1][2] ?? dur;
  return blend(p0, p1, clamp((t - (t1 - d)) / d));
}

// a finger: from its knuckle at the origin toward -x; rounded tip, slight taper
function finger(x, len, w) { x.beginPath(); x.moveTo(.04, w / 2); x.quadraticCurveTo(-len * .5, w * .5, -len + w * .42, w * .4); x.arc(-len + w * .42, 0, w * .4, Math.PI / 2, Math.PI * 1.5); x.quadraticCurveTo(-len * .5, -w * .5, .04, -w / 2); x.closePath(); x.fill(); }
// — the open hand: palm toward the viewer, fingers pointing left toward her, the arm coming in from the right edge.
// L = palm length (wrist → knuckles, metres). Warm cream paper, lit through: the only thing in the box that glows from itself.
// close 0 → 1: the fingers curl (shorten from the knuckles) and the thumb folds down over whatever lies in the palm.
export function openHand(S, L, z, o = {}) {
  const U = S.U, g = new THREE.Group(); g.position.z = z; S.scene.add(g); if (o.flip) g.scale.y = -1;
  const ppm = Math.min(16000, 1500 / L), arm = o.arm ?? 6, gl = { trans: .85, glow: o.glow ?? .55, glowCol: '#ffd8a8', ppm, finish: { rim: .55, under: .12 }, glowRes: .35 };
  const sc = fn => x => { x.scale(L, L); fn(x); };
  const palmShape = x => { x.beginPath(); x.moveTo(-.98, .4); x.quadraticCurveTo(-.55, .47, -.3, .42);
    x.quadraticCurveTo(-.05, .5, .12, .36); x.quadraticCurveTo(.25, .3, .4, .3); x.lineTo(arm, .36); x.lineTo(arm, -.36); x.lineTo(.4, -.3);
    x.quadraticCurveTo(.1, -.36, -.3, -.42); x.quadraticCurveTo(-.8, -.46, -1.0, -.3); x.quadraticCurveTo(-1.04, .05, -.98, .4); x.closePath(); x.fill(); };
  const palm = piece(U, [-1.1 * L, arm * L, -.55 * L, .6 * L], sc(x => { palmShape(x);
    x.beginPath(); x.moveTo(arm, -.46); x.lineTo(1.0, -.42); x.quadraticCurveTo(.96, 0, 1.0, .44); x.lineTo(arm, .48); x.closePath(); x.fill();   // a plain sleeve
    cut(x, () => { x.globalAlpha = .7; x.lineWidth = .012; x.lineCap = 'round';
      x.beginPath(); x.moveTo(-.92, .2); x.quadraticCurveTo(-.6, .1, -.28, .2); x.stroke();          // heart line
      x.beginPath(); x.moveTo(-.9, -.02); x.quadraticCurveTo(-.55, .0, -.35, -.12); x.stroke();      // head line
      x.beginPath(); x.moveTo(-.4, .3); x.quadraticCurveTo(-.2, .0, .05, -.15); x.stroke(); });      // the thumb's crease
  }), { ...gl, glowDraw: sc(gx => { const r = gx.createRadialGradient(-.5, 0, 0, -.5, 0, 1.2); r.addColorStop(0, '#fff'); r.addColorStop(1, '#333'); gx.fillStyle = r; palmShape(gx); }) });
  g.add(palm);
  const F = [[.3, .82, .2, .07], [.1, .92, .21, .02], [-.1, .86, .2, -.03], [-.29, .68, .18, -.1]];
  const fingers = F.map(([y, len, w, a]) => {
    const f = piece(U, [-len * L - .02 * L, .06 * L, -w * .6 * L, w * .6 * L], sc(x => { finger(x, len, w);
      cut(x, () => { x.globalAlpha = .6; x.lineWidth = .01; for (const k of [.3, .6]) { x.beginPath(); x.moveTo(-len * k, w * .3); x.lineTo(-len * k - .01, -w * .3); x.stroke(); } }); }),
      { ...gl, glowDraw: sc(gx => { gx.fillStyle = '#aaa'; finger(gx, len, w); }) });
    f.position.set(-.95 * L, y * L, -.0002); f.rotation.z = a; f.userData.a = a; palm.add(f); return f;
  });
  const thumb = piece(U, [-.06 * L, .72 * L, -.18 * L, .18 * L], sc(x => { x.save(); x.scale(-1, 1); finger(x, .68, .27); x.restore(); }),
    { ...gl, glowDraw: sc(gx => { gx.save(); gx.scale(-1, 1); gx.fillStyle = '#aaa'; finger(gx, .68, .27); gx.restore(); }) });
  thumb.position.set(-.18 * L, .3 * L, .004); palm.add(thumb);
  const all = [palm, thumb, ...fingers];
  return { g, palm, fingers, thumb, all, tint(hex) { all.forEach(m => tint(m, hex)); },
    set(x, y, rot = 0, close = 0, glow = 1) { g.position.x = x; g.position.y = y; g.rotation.z = rot; const c = clamp(close);
      fingers.forEach((f, i) => { f.scale.x = 1 - .42 * c; f.rotation.z = f.userData.a * (1 - c); });
      thumb.rotation.z = lerp(2.25, 3.4, c);   // open: up and back; closed: folded down across the palm
      for (const m of all) m.material.userData.u.uGlowLit.value = glow; } };
}

// — her hand: the back of her hand toward the viewer, fingers pointing right, arm (sweater cuff) from the left edge —
export function herHand(S, L, z, o = {}) {
  const arm = o.arm ?? 5;
  const m = piece(S.U, [-arm * L, 1.95 * L, -.6 * L, .55 * L], x => { x.scale(L, L);
    // back of the hand from the wrist (x=0) to the knuckles (x=.9), then four fingers together, slightly spread
    x.beginPath(); x.moveTo(-arm, .3); x.lineTo(-.1, .3); x.quadraticCurveTo(.4, .42, .88, .38); x.lineTo(.92, -.34); x.quadraticCurveTo(.4, -.4, -.05, -.3); x.lineTo(-arm, -.32); x.closePath(); x.fill();
    for (const [y, len, w, a] of [[.27, .8, .19, .05], [.09, .9, .2, .01], [-.09, .84, .19, -.03], [-.26, .66, .17, -.08]]) { x.save(); x.translate(.86, y); x.rotate(a); x.scale(-1, 1); finger(x, len, w); x.restore(); }
    x.save(); x.translate(.2, -.3); x.rotate(-.55); x.scale(-1, 1); finger(x, .62, .25); x.restore();   // thumb, below
    x.beginPath(); x.moveTo(-arm, .42); x.lineTo(-.55, .4); x.quadraticCurveTo(-.5, 0, -.55, -.42); x.lineTo(-arm, -.44); x.closePath(); x.fill();   // sweater cuff
    cut(x, () => { x.globalAlpha = .5; x.lineWidth = .014; for (let k = 0; k < 6; k++) { x.beginPath(); x.moveTo(-.62 - k * .1, .38); x.lineTo(-.62 - k * .1, -.4); x.stroke(); } });
  }, { ppm: Math.min(16000, 1500 / L), trans: .08, finish: { rim: .3, under: .2 } });
  S.add(m); m.position.z = z;
  return { m, set(x, y, rot = 0) { m.position.x = x; m.position.y = y; m.rotation.z = rot; } };
}
