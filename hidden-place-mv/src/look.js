// The film's colour journey: one "phase" number p carries every ladder.
//   p = 0  cool blue-grey night (the hiding room)      p = 1  neutral natural light      p = 2  soft daylight (out in the alley)
// No heavy yellow: the daylight end is only a touch warm. The one accent is the warm light of the hand that waits.
import * as THREE from 'three';
import { clamp, lerp } from './lib.js';

const C = new THREE.Color(), D = new THREE.Color();
const L = {   // back → front
  sky:   ['#56688a', '#c4c8cc', '#e6ecf0'],
  far:   ['#3a4866', '#8c9298', '#a8aaa4'],
  wall:  ['#64718e', '#9a9a98', '#b4aea4'],
  floor: ['#33405a', '#6a6864', '#7e766c'],
  cloth: ['#8c9ab8', '#d6d4ce', '#e8e2d6'],
  furn:  ['#262e40', '#3e3e40', '#4a443e'],
  fig:   ['#141a28', '#202022', '#26221f'],
  front: ['#080b12', '#0e0e0f', '#13110f'],
  light: ['#b4c4e2', '#e8e6e2', '#fbf1e2'],
  key:   ['#b8c4e0', '#f0eeea', '#fff6ea'],
  amb:   ['#5a6a90', '#9a9a9c', '#b0aaa0'],
};
export function col(name, p) {
  const s = L[name], q = clamp(p, 0, 2), i = Math.min(1, Math.floor(q)), k = q - i;
  return '#' + C.set(s[i]).lerp(D.set(s[i + 1]), k).getHexString();
}
export const WARM = '#ffcf98';   // the waiting hand's light, the hallway behind the door
// phase across the film (seconds): night until the hand; greys toward neutral through chorus 1; neutral in verse 2;
// warmer daylight from the bridge; full soft daylight outside.
const KEYS = [[0, 0], [64, 0], [98, .55], [106, 1], [196, 1.15], [222, 1.8], [240, 2]];
export function phase(t) {
  if (t <= KEYS[0][0]) return KEYS[0][1];
  for (let i = 0; i + 1 < KEYS.length; i++) { const [a, pa] = KEYS[i], [b, pb] = KEYS[i + 1]; if (t < b) return lerp(pa, pb, (t - a) / (b - a)); }
  return KEYS[KEYS.length - 1][1];
}
