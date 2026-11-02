// 내가 숨은 곳까지 — one plan of shots on the song's clock. Each shot: build(E) → { S, update(t), post(), grade() }, t = film seconds.
import * as THREE from 'three';
import { Pipe } from './post.js';
import { dispose } from './stage.js';
import { ss, clamp } from './lib.js';
import { PLAN, DUR } from './shots.js';

const Q = new URLSearchParams(location.search), SSAA = +(Q.get('ssaa') || 2);
const FROM = Q.has('from') ? +Q.get('from') : 0, TO = Q.has('to') ? +Q.get('to') : DUR;
window.DUR = +(TO - FROM).toFixed(3);
const plan = PLAN.map(([build, start, dis], i) => ({ build, start, dis: dis ?? 0 }));
plan.forEach((s, i) => { s.end = i + 1 < plan.length ? plan[i + 1].start : DUR; });

const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(SSAA); renderer.setSize(1920, 1080, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.VSMShadowMap;
renderer.toneMapping = THREE.NoToneMapping; renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
const pipe = new Pipe(renderer, 1920, 1080, SSAA);
await Promise.all([document.fonts.load('700 40px Myeongjo', '내가'), document.fonts.load('400 40px Myeongjo', '내가'), document.fonts.load('40px Pen', '주님')]);

const live = new Map();
function get(i) { if (!live.has(i)) live.set(i, plan[i].build({ T0: plan[i].start, T1: plan[i].end })); return live.get(i); }
function gc(keep) { for (const [i, s] of live) if (!keep.includes(i)) { dispose(s.S.scene); live.delete(i); } }
function draw(i, t, target) { const s = get(i); s.update(t); pipe.shot(s.S.scene, s.S.cam, s.post(), target); return s.grade(t); }
function R(t) {
  let i = plan.findIndex(p => t >= p.start && t < p.end); if (i < 0) i = plan.length - 1;
  const p = plan[i], tl = t - p.start;
  let g, mixB = 0;
  if (i > 0 && p.dis > 0 && tl < p.dis) { draw(i - 1, t, pipe.rtA); g = draw(i, t, pipe.rtB); mixB = ss(tl / p.dis); gc([i - 1, i]); }
  else { g = draw(i, t, pipe.rtA); gc([i]); }
  const fadeIn = ss(clamp(t / 1.2)), fadeOut = 1 - ss(clamp((t - (DUR - 2.5)) / 2.5));
  pipe.final({ ...g, mixB, fade: (g.fade ?? 1) * fadeIn * fadeOut });
}
window.render = t => R(FROM + t);
window.READY = true;
