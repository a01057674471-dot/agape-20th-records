// 내가 숨은 곳까지 — the shot plan on the song's clock (film seconds). Sections (from the song's energy):
// intro 0–13 · verse 1 13–57 · pre 57–64 · chorus 1 64–98 · interlude 98–106 · verse 2 106–134 · chorus 2 134–176 ·
// interlude 176–196 · bridge 196–214 · breakdown (no bass) 214–236, voice returns 222 · final chorus 236–258 · outro 258–277.6
import { aim } from './stage.js';
import { room, R } from './room.js';
import { POSE, walk, blend, poseAt } from './rig.js';
import { phase } from './look.js';
import { hands, doorCU, teaCU, deskTop, sing, alley, ALLEY } from './closeups.js';
import { clamp, lerp, eio, ss, seg, vnoise } from './lib.js';
export const DUR = 277.6;
const ENV = await (await fetch('src/env.json')).json();
const voice = t => { const i = Math.max(0, Math.min(ENV.v.length - 1, Math.round(t * 24))); return ENV.v[i]; };

// keyframes: keys [[t, v], ...] → eased value (holds outside); v may be a number or an array
function K(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i + 1 < keys.length; i++) { const [a, va] = keys[i], [b, vb] = keys[i + 1];
    if (t < b) { const k = eio((t - a) / (b - a)); return Array.isArray(va) ? va.map((v, j) => lerp(v, vb[j], k)) : lerp(va, vb, k); } }
  return keys[keys.length - 1][1];
}
const WIDE = [-.02, .0, .56, -.02, .0, -.1];
const breathe = (t, k = 1) => ({ torso: .025 * k * Math.sin(t * 1.4), head: .015 * k * Math.sin(t * 1.4 - .6) });
const add = (p, d) => { const o = { ...p }; for (const k in d) o[k] = (o[k] ?? 0) + d[k]; return o; };
const STEP = R.H * .5;   // one step's length: the walk phase follows distance so the feet don't slide
const walking = (x, x0, amp = 1) => walk(Math.abs(x - x0) / STEP * Math.PI, amp);

function make(build, script, o = {}) {
  return E => { const set = build(); let f = .5;
    return { S: set.S, update(t) { const r = script(t, E); set.apply({ p: phase(t), ...r.st }, t); aim(set.S.cam, r.cam, t, { hand: r.hand ?? .0004 }); f = r.cam[2] - (r.fz ?? -.078); this.r = r; },
      post() { return { focus: f, aper: this.r.aper ?? 7, maxCoc: 10, bloom: { strength: this.r.bloom ?? .35, radius: .5, threshold: this.r.thr ?? 1.0 } }; },
      grade() { return { vig: .42, contrast: .1, lift: [0, .003, .01], gain: [1, 1, 1], expo: this.r.expo ?? 1, ...(o.grade || {}) }; } }; };
}
const RM = s => make(room, s), HD = s => make(hands, s), DR = s => make(doorCU, s), DRO = s => make(() => doorCU({ out: true }), s), TEA = s => make(teaCU, s), DK = s => make(deskTop, s), SG = s => make(sing, s), AL = s => make(alley, s);

// ——— intro: the cloth goes under the door ———
const s01 = DR(t => {
  const push = K(t, [[2.4, -.3], [4.6, -.01], [5.2, 0]]);
  return { st: { p: 0, shadowX: lerp(-.3, .3, seg(t, 1.0, 2.6)), cloth: push, cover: K(t, [[3.9, 0], [5.0, 1]]), hand: [push - .055 + K(t, [[5.9, 0], [6.9, -.3]]), -.03 + .002 * Math.sin(t * 3), -.06], lit: .6 },
    cam: K(t, [[0, [0, -.025, .3, 0, -.04, -.1]], [7, [-.01, -.03, .25, -.01, -.045, -.1]]]), fz: -.105, aper: 9 };
});
const s02 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, gap: 1, title: K(t, [[8.2, 0], [11.2, 1]]), titleXY: [.135, .045], her: { x: -.2, face: 1, ...add(POSE.sitBack, breathe(t, 1.6)) } },
  cam: K(t, [[7, [.0, -.01, .5, .0, -.01, -.1]], [13, [-.01, -.015, .48, -.01, -.015, -.1]]]) }));
// ——— verse 1: she crosses the room and folds herself into the gap ———
const s03 = RM(t => {
  const x = K(t, [[14.6, -.2], [24.6, R.GAP]]);
  const pose = t < 14.6 ? blend(POSE.sitBack, POSE.stand, seg(t, 13.2, 14.6)) : t < 24.6 ? walking(x, -.2) : blend(POSE.stand, POSE.curl, seg(t, 24.8, 27.2));
  return { st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, her: { x, face: 1, ...pose } }, cam: K(t, [[13, [-.04, -.01, .5, -.04, -.01, -.1]], [27.5, [.06, -.02, .48, .06, -.02, -.1]]]) };
});
const s04 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, her: { x: R.GAP, face: 1, ...add(POSE.curl, breathe(t, .6)) } },
  cam: K(t, [[27.5, [.17, -.04, .34, .17, -.05, -.1]], [42, [.215, -.07, .16, .215, -.075, -.1]]]) }));
const s05 = TEA(t => ({ st: { p: 0, steam: K(t, [[42.5, 1], [47.3, .05]]) }, cam: K(t, [[42, [-.05, -.01, .26, -.05, -.02, -.1]], [47.5, [-.055, -.015, .22, -.055, -.02, -.1]]]), fz: -.068, aper: 9 }));
const s06 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, dust: 1 }, cam: K(t, [[47.5, [-.15, .035, .07, -.15, .03, -.124]], [51.5, [-.152, .03, .045, -.152, .028, -.124]]]), fz: -.124, aper: 6 }));
const s07 = RM(t => {
  const m = K(t, [[53, 0], [54.6, 1]]);
  return { st: { mirror: m, glass: .35, her: { x: -.092, face: 1, ...poseAt(t, [[51.5, add(POSE.stand, { head: -.15 })], [53, { ...POSE.reach, head: -.2, nua: 1.15, nfa: .45 }], [55.2, add(POSE.stand, { head: -.35, torso: -.05 })]]) } },
    cam: K(t, [[51.5, [-.07, -.04, .2, -.07, -.045, -.1]], [57, [-.065, -.045, .17, -.065, -.05, -.1]]]) };
});
// ——— pre-chorus: someone sits down beside her; an open hand waits ———
const handIn = t => ({ x: K(t, [[59, R.GAP + .13], [62, R.GAP + .046]]), y: R.FY + .038, rot: 0, close: 0, glow: K(t, [[59, .2], [62, 1]]) });
const s08 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, pres: K(t, [[57, 0], [60.5, 1.1]]), presX: R.GAP + .04, hand: handIn(t),
  her: { x: R.GAP - .006, face: 1, ...poseAt(t, [[57, add(POSE.curl, breathe(t, .6))], [63.5, POSE.curlUp, 2.2]]) } },
  cam: K(t, [[57, [.235, -.075, .2, .235, -.08, -.1]], [64, [.24, -.078, .17, .24, -.082, -.1]]]) }));
// ——— chorus 1: she lays her fingertips in his palm; his hand closes; the window opens ———
const s09 = HD(t => ({ st: { hx: .03, sx: K(t, [[64.6, -.36], [68.8, -.115], [70.2, -.094]]), sy: K(t, [[64.6, .05], [70.2, -.022]]), srot: K(t, [[64.6, -.25], [70.2, -.12]]), close: K(t, [[71.4, 0], [73.6, 1]]),
  glow: K(t, [[64, .45], [74, .9]]), hglow: K(t, [[64, .8], [74, 1.2]]) }, cam: K(t, [[64, [-.02, -.01, .36, -.02, -.01, -.06]], [76, [-.04, -.02, .29, -.04, -.02, -.06]]]), fz: -.06, aper: 8 }));
const held = { x: R.GAP + .046, y: R.FY + .038, rot: 0, close: 1, glow: 1.1 };
const heldPose = (t, bow) => add(blend(POSE.curlUp, { ...POSE.curlUp, nua: 1.45, nfa: .1 }, 1), { head: -.35 * bow + .02 * Math.sin(t * 1.2), torso: -.12 * bow + .02 * Math.sin(t * 1.2) });
const s10 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, win: K(t, [[77, 0], [80, 1]]), sway: K(t, [[77, 0], [80, 1.2]]), curL: K(t, [[77, .1], [80.5, 0]]), curR: K(t, [[77, .1], [80.5, 0]]),
  lit: K(t, [[77, .85], [81, 1.35]]), skyK: K(t, [[77, 1.25], [81, 1.9]]), pres: 1, presX: R.GAP + .04, hand: held, dust: K(t, [[79, 0], [82, .8]]),
  her: { x: R.GAP - .006, face: 1, ...heldPose(t, seg(t, 80, 84)) } }, cam: K(t, [[76, [.02, .0, .5, .02, .0, -.1]], [88, [.06, -.02, .44, .06, -.02, -.1]]]), bloom: .45 }));
const s11 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, win: 1, sway: 1.2, curL: 0, curR: 0, lit: 1.35, skyK: 1.9, pres: 1, presX: R.GAP + .04, hand: held, dust: .8,
  her: { x: R.GAP - .006, face: 1, ...heldPose(t, 1 - .5 * seg(t, 92, 96)) } }, cam: K(t, [[88, [.2, -.06, .22, .2, -.065, -.1]], [98, [.225, -.07, .17, .225, -.075, -.1]]]), bloom: .45 }));
// ——— interlude: the window, night turning to morning ———
const s12 = RM(t => ({ st: { cloth: (R.DX0 + R.DX1) / 2, clothCover: 1, win: K(t, [[99, 1], [104, .2]]), sway: .6, curL: .25, curR: .25, skyK: K(t, [[98, 1.6], [106, 1.3]]), cup2: 0 },
  cam: [-.04, .03, .3, -.04, .03, -.13], fz: -.13, aper: 5 }));
// ——— verse 2: the next day: the curtain closed, but not all the way; two cups; the empty chair ———
const s13 = RM(t => {
  const c = K(t, [[107.2, .1], [110.2, .78]]);
  return { st: { curL: c, curR: K(t, [[110.6, .1], [112.2, .35]]), sway: .2, dust: .5, her: { x: -.075, face: 1,
      ...poseAt(t, [[106, add(POSE.stand, { head: .1 })], [107.2, { ...POSE.stand, nua: 2.6, nfa: .2, fua: 2.4, ffa: .3, head: .15 }], [110.8, { ...POSE.stand, nua: 2.5, nfa: .3, fua: .1, head: .05 }, 1.2], [113, add(POSE.stand, { head: -.05 }), 1.4]]) } },
    cam: K(t, [[106, [-.04, .01, .3, -.04, .0, -.1]], [116, [-.045, .0, .26, -.045, -.005, -.1]]]) };
});
const s14 = RM(t => ({ st: { curL: .78, curR: .35, cup2: 1, steam: .6, pres: K(t, [[118, 0], [122, .5]]), presX: R.CHAIR2, presY: R.FY + .05,
  her: { x: R.CHAIR + .006, face: 1, ...poseAt(t, [[116, add(POSE.sitChair, breathe(t, .5))], [119, add(POSE.sitChair, { head: .12, torso: .03 }), 1.5]]) } },
  cam: K(t, [[116, [-.05, -.03, .32, -.05, -.04, -.1]], [127, [-.04, -.035, .27, -.04, -.04, -.1]]]) }));
const s15 = RM(t => ({ st: { curL: .78, curR: .35, box: K(t, [[129, 0], [131.5, 1]]),
  her: { x: R.GAP + .008, face: -1, ...poseAt(t, [[127, POSE.stand], [128.4, POSE.kneel, 1.3], [131.5, { ...POSE.kneel, nua: .3, nfa: .3, fua: .25, ffa: .3 }, 2.4]]) } },
  cam: K(t, [[127, [.17, -.05, .26, .17, -.06, -.1]], [134, [.19, -.065, .21, .19, -.07, -.1]]]) }));
// ——— chorus 2: what was in the box; smoothing the notebook; writing; singing at the window ———
const s16 = DK(t => {
  const sm = K(t, [[141.4, 0], [144.4, 1]]);
  return { st: { box: K(t, [[134, .6], [135, 1], [140.5, 1], [141.5, 0]]), items: [K(t, [[134.5, 0], [136.2, 1]]), K(t, [[136.6, 0], [138.2, 1]]), K(t, [[138.6, 0], [140.2, 1]])], smooth: sm,
      hand: t > 140.6 ? [lerp(-.2, .05, sm) + K(t, [[140.6, -.25], [141.4, 0]]), -.01, -.15] : null },
    cam: K(t, [[134, [0, 0, .62, 0, 0, -.1]], [145, [.01, 0, .55, .01, 0, -.1]]]), fz: -.1, aper: 4 };
});
const s17 = DK(t => {
  const w1 = K(t, [[146.2, 0], [150, 1]]), w2 = K(t, [[150.6, 0], [155.4, 1]]);
  const NX = -.02, NW = .2, px = NX + .01 + (w2 > 0 ? w2 : w1) * (NW / 2 - .02), py = w2 > 0 ? -.008 : .028;
  return { st: { box: 0, items: [1, 1, 1], smooth: 1, write: [w1, w2], pen: [px + .001 * Math.sin(t * 24), py - .002, .55], hand: [px + .062 + .001 * Math.sin(t * 24), py - .052, 2.35] },
    cam: K(t, [[145, [.02, .01, .4, .02, .01, -.1]], [156, [.035, .01, .3, .035, .01, -.1]]]), fz: -.1, aper: 4 };
});
const s18 = SG(t => { const v = voice(t);
  return { st: { jaw: .02 + .16 * clamp((v - .25) / .6), head: .06 + .05 * K(t, [[156, 0], [166, 1]]) + .04 * v, lean: -.02, pres: K(t, [[160, 0], [168, .35]]), curtain: .55 },
    cam: K(t, [[156, [.0, -.01, .48, .0, -.01, -.1]], [176, [-.015, .0, .34, -.015, .0, -.1]]]), fz: -.08, aper: 6 };
});
// ——— interlude: beside the window; then before the turned mirror ———
const s19 = RM(t => ({ st: { curL: .78, curR: .35, sway: .5, dust: .6, book: 1, flip: 0, her: { x: .045, face: -1, ...add(POSE.stand, { head: .12 + .02 * Math.sin(t * .8) }) } },
  cam: K(t, [[176, [-.01, .02, .34, -.01, .01, -.1]], [186, [.0, .015, .3, .0, .01, -.1]]]) }));
const s20 = RM(t => ({ st: { curL: .78, curR: .35, mirror: 1, book: 1, her: { x: -.095, face: 1, ...add(POSE.stand, { head: -.25 + .02 * Math.sin(t) }) } },
  cam: K(t, [[186, [-.08, -.035, .2, -.08, -.04, -.1]], [196, [-.075, -.04, .16, -.075, -.045, -.1]]]) }));
// ——— bridge: she sets the mirror upright and looks; the coat ———
const s21 = RM(t => ({ st: { curL: .78, curR: .35, mirror: K(t, [[197.2, 1], [199, 0]]), glass: K(t, [[199, .35], [201, .9]]), refl: t > 199 ? 1 : 0, book: 1,
  her: { x: -.092, face: 1, ...poseAt(t, [[196, add(POSE.stand, { head: -.25 })], [197.2, { ...POSE.reach, head: -.15, nua: 1.15, nfa: .45 }, 1.1], [199.6, add(POSE.stand, { head: .05 }), 1.2], [203, add(POSE.stand, { head: .1, torso: .03 }), 2.5]]) } },
  cam: K(t, [[196, [-.07, -.04, .17, -.07, -.045, -.1]], [204, [-.06, -.04, .14, -.06, -.045, -.1]]]) }));
const s22 = RM(t => {
  const x = K(t, [[204.5, -.092], [206.6, -.14]]);
  return { st: { curL: .78, curR: .35, mirror: 0, glass: .7, book: 1, coat: t < 207.6 ? 1 : 0, her: { x, face: t < 204.5 ? 1 : -1, jacket: t > 207.6 ? 1 : 0,
      ...(t > 204.5 && t < 206.6 ? walking(x, -.092) : poseAt(t, [[206.6, POSE.stand], [207.3, { ...POSE.stand, nua: 2.7, nfa: .3, head: .2 }, .7], [208.6, POSE.stand, 1.1], [211, add(POSE.stand, { head: -.05 }), 1.5]])) } },
    cam: K(t, [[204, [-.12, -.01, .3, -.12, -.01, -.1]], [214, [-.15, -.01, .27, -.15, -.015, -.1]]]) };
});
// ——— breakdown: her hand on the cloth; she pulls it away; the door opens into light ———
const s23 = DR(t => { const pull = K(t, [[217.4, 0], [219.6, -.42]]);
  return { st: { p: phase(t), cloth: pull, cover: K(t, [[217.6, 1], [218.8, 0]]), hand: [pull - .055 + .004 * Math.sin(t * 2.2) * (t < 217 ? 1 : 0), -.03, -.06], gap: 1.2 },
    cam: K(t, [[214, [-.04, -.03, .25, -.04, -.045, -.1]], [220, [-.02, -.03, .28, -.02, -.045, -.1]]]), fz: -.105, aper: 9, bloom: .5 };
});
const s24 = RM(t => { const x = K(t, [[222.6, -.17], [225.5, -.25]]);
  return { st: { curL: .78, curR: .35, mirror: 0, book: 1, coat: 0, door: K(t, [[220.6, 0], [222.6, 1]]), hall: K(t, [[220.6, 1], [223, 2.4]]),
      her: { x, face: -1, jacket: 1, ...(t > 222.6 ? walking(x, -.17) : add(POSE.stand, { head: .05 })) } },
    cam: K(t, [[220, [-.15, .0, .36, -.15, -.005, -.1]], [225.5, [-.18, .0, .32, -.18, -.005, -.1]]]), bloom: .55, thr: .9, expo: K(t, [[223.5, 1], [225.5, 1.6]]) };
});
// ——— final chorus: out in the street, walking; the camera keeps her pace beside her; the closed door ———
const AX0 = -.15, AV = (ALLEY.XT - .045 - AX0) / 23;
const ax = t => t < 248.5 ? AX0 + (t - 225.5) * AV * Math.min(1, (t - 225.5) / 2 + .2) : AX0 + (248.5 - 225.5) * AV - .0;
const XS = AX0 + (248.5 - 225.5) * AV;   // where she stops
const s25 = AL(t => { const x = ax(t);
  return { st: { camX: x + .02, pres: .25, presX: x + .03, her: { x, face: 1, jacket: 1, ...walking(x, AX0) } },
    cam: [x + .02, ALLEY.Y + .05, .3, x + .02, ALLEY.Y + .045, -.1], fz: -.085, expo: K(t, [[225.5, 1.6], [227.5, 1]]) };
});
const s26 = AL(t => { const x = Math.min(ax(t), XS), stop = seg(t, 247.5, 249);
  return { st: { camX: x, pres: .25, presX: x + .03, her: { x, face: 1, jacket: 1, ...(t < 248.5 ? walking(x, AX0, 1 - .6 * stop) : poseAt(t, [[248.5, POSE.stand], [251, add(POSE.stand, { head: -.12 }), 1.5]])) } },
    cam: K(t, [[240, [x - .03, ALLEY.Y + .04, .24, x - .03, ALLEY.Y + .04, -.1]], [252, [XS + .06, ALLEY.Y + .04, .28, XS + .06, ALLEY.Y + .04, -.1]], [258, [XS + .07, ALLEY.Y + .035, .25, XS + .07, ALLEY.Y + .035, -.1]]]), fz: -.085 };
});
// ——— outro: the cloth under someone else's door; she sits down beside it and waits; home: the open notebook, the curtain in the wind ———
const s27 = DRO(t => ({ st: { p: 2, gap: 0, cloth: .0, clothY: -.042, clothZ: -.1105 + 0 * t, cover: 1, lit: .9 },
  cam: K(t, [[258, [0, -.03, .3, 0, -.04, -.1]], [265, [0, -.035, .26, 0, -.045, -.1]]]), fz: -.11, aper: 9 }));
const s28 = AL(t => ({ st: { camX: XS + .06, pres: K(t, [[266, .25], [269, .7]]), presX: ALLEY.XT + .105, clothShift: .0008 * Math.sin(t * 3) * seg(t, 267, 268) * (1 - seg(t, 269, 270)),
  her: { x: ALLEY.XT + .055, face: 1, jacket: 1, ...poseAt(t, [[265, POSE.stand], [267.4, { ...POSE.curlUp, torso: -.05, head: .12 }, 2.2]]) } },
  cam: K(t, [[265, [ALLEY.XT + .05, ALLEY.Y + .03, .26, ALLEY.XT + .05, ALLEY.Y + .03, -.1]], [271, [ALLEY.XT + .055, ALLEY.Y + .03, .23, ALLEY.XT + .055, ALLEY.Y + .03, -.1]]]), fz: -.085 }));
const s29 = RM(t => ({ st: { p: 2, curL: .1, curR: .1, win: 1, sway: 1.6, book: 1, flip: K(t, [[272, 0], [276, 2]]), mirror: 0, glass: .7, coat: 0, dust: .6, skyK: 1.6, title: K(t, [[273.4, 0], [276, 1]]), titleXY: [-.035, -.068] },
  cam: K(t, [[271, [-.035, -.0, .2, -.035, -.01, -.1]], [277.6, [-.035, .0, .3, -.035, -.005, -.1]]]) }));

export const PLAN = [
  [s01, 0], [s02, 7, .8], [s03, 13, .6], [s04, 27.5, .8], [s05, 42, .6], [s06, 47.5, .6], [s07, 51.5, .6],
  [s08, 57, .7], [s09, 64, .6], [s10, 76, .8], [s11, 88, .8], [s12, 98, 1.2],
  [s13, 106, 1.0], [s14, 116, .8], [s15, 127, .7],
  [s16, 134, .7], [s17, 145, .7], [s18, 156, .9],
  [s19, 176, 1.0], [s20, 186, .9], [s21, 196, .8], [s22, 204, .7],
  [s23, 214, .7], [s24, 220, .6], [s25, 225.5, 1.0], [s26, 240, .8],
  [s27, 258, .8], [s28, 265, .8], [s29, 271, 1.2],
];
