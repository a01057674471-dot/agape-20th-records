// Korean lettering for the whiteboard: there is no single-stroke Hangul font, so each glyph is
// rendered from a bold sans font, thinned to a 1-px skeleton (Zhang–Suen), traced into polylines,
// split at junctions and re-joined where a line runs straight through, then ordered roughly as a hand
// writes Hangul (top-left first; horizontals left→right, verticals top→bottom).
// Output goes into HANGUL in wb.js in the same units as the EMS font (y up, cap height ≈ 677). The strokes only set the
// writing order and pace: wb.js reveals the real glyph through them, so every letter ends up whole and legible.
import { HANGUL } from './wb.js';

const F = 150, PAD = 18, N = F + PAD * 2, UNIT = 850 / F;   // px → font units (Gaegu's Hangul sits small in its em box: scaled up to match the Latin cap height)

function thin(img, w, h) {                       // Zhang–Suen thinning, in place on a 0/1 array
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h) ? 0 : img[y * w + x];
  let changed = true;
  while (changed) {
    changed = false;
    for (let pass = 0; pass < 2; pass++) {
      const del = [];
      for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
        if (!img[y * w + x]) continue;
        const p = [at(x, y - 1), at(x + 1, y - 1), at(x + 1, y), at(x + 1, y + 1), at(x, y + 1), at(x - 1, y + 1), at(x - 1, y), at(x - 1, y - 1)];
        const B = p.reduce((a, b) => a + b, 0); if (B < 2 || B > 6) continue;
        let A = 0; for (let i = 0; i < 8; i++) if (!p[i] && p[(i + 1) % 8]) A++;
        if (A !== 1) continue;
        if (pass === 0 ? (p[0] * p[2] * p[4] || p[2] * p[4] * p[6]) : (p[0] * p[2] * p[6] || p[0] * p[4] * p[6])) continue;
        del.push(y * w + x);
      }
      for (const k of del) img[k] = 0;
      if (del.length) changed = true;
    }
  }
}

const NB = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]];
function trace(img, w, h) {
  const on = (x, y) => x >= 0 && y >= 0 && x < w && y < h && img[y * w + x];
  const deg = (x, y) => NB.reduce((a, [dx, dy]) => a + (on(x + dx, y + dy) ? 1 : 0), 0);
  const nodes = new Set(), used = new Set(), paths = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (on(x, y) && deg(x, y) !== 2) nodes.add(y * w + x);
  const key = (a, b) => a < b ? a + ',' + b : b + ',' + a;
  const walk = (sx, sy, nx, ny) => {
    const pts = [[sx, sy]]; let px = sx, py = sy, x = nx, y = ny;
    for (let guard = 0; guard < 4000; guard++) {
      used.add(key(py * w + px, y * w + x)); pts.push([x, y]);
      if (nodes.has(y * w + x)) break;
      let next = null;
      for (const [dx, dy] of NB) { const qx = x + dx, qy = y + dy; if (!on(qx, qy) || (qx === px && qy === py)) continue; if (used.has(key(y * w + x, qy * w + qx))) continue; next = [qx, qy]; break; }
      if (!next) break;
      px = x; py = y; [x, y] = next;
      if (x === sx && y === sy) { pts.push([x, y]); break; }
    }
    return pts;
  };
  for (const n of nodes) { const x = n % w, y = n / w | 0; for (const [dx, dy] of NB) if (on(x + dx, y + dy) && !used.has(key(n, (y + dy) * w + x + dx))) paths.push(walk(x, y, x + dx, y + dy)); }
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {        // closed loops (ㅇ) have no nodes
    if (!on(x, y)) continue;
    for (const [dx, dy] of NB) if (on(x + dx, y + dy) && !used.has(key(y * w + x, (y + dy) * w + x + dx))) { paths.push(walk(x, y, x + dx, y + dy)); }
  }
  return paths;
}

const plen = p => { let L = 0; for (let i = 1; i < p.length; i++) L += Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]); return L; };
const dirAt = (p, end) => { const k = Math.min(6, p.length - 1); const a = end ? p[p.length - 1 - k] : p[k], b = end ? p[p.length - 1] : p[0]; return Math.atan2(b[1] - a[1], b[0] - a[0]); };

function cleanup(paths) {
  // drop tiny bits and spurs at junctions
  let P = paths.filter(p => plen(p) > 3.5);
  const ends = p => [p[0], p[p.length - 1]];
  const near = (a, b, r = 3.2) => Math.hypot(a[0] - b[0], a[1] - b[1]) <= r;
  const degreeAt = pt => P.reduce((a, q) => a + ends(q).filter(e => near(e, pt)).length, 0);
  P = P.filter(p => { if (plen(p) > F * .045) return true; const [a, b] = ends(p); return !((degreeAt(a) === 1) !== (degreeAt(b) === 1)); });
  // join paths that continue straight through a junction
  let merged = true;
  while (merged) {
    merged = false;
    outer: for (let i = 0; i < P.length; i++) for (let j = 0; j < P.length; j++) {
      if (i === j) continue;
      const a = P[i], b = P[j];
      for (const [ra, rb] of [[false, false], [false, true], [true, false], [true, true]]) {
        const A = ra ? a.slice().reverse() : a, B = rb ? b.slice().reverse() : b;
        if (!near(A[A.length - 1], B[0], 4)) continue;
        const d1 = dirAt(A, true), d2 = Math.atan2(B[Math.min(6, B.length - 1)][1] - B[0][1], B[Math.min(6, B.length - 1)][0] - B[0][0]);
        let dd = Math.abs(d1 - d2); if (dd > Math.PI) dd = 2 * Math.PI - dd;
        if (dd < .5) { P[i] = A.concat(B.slice(1)); P.splice(j, 1); merged = true; break outer; }
      }
    }
  }
  return P;
}
function smooth(p) {
  if (p.length < 5) return p;
  const q = p.map((pt, i) => { if (i === 0 || i === p.length - 1) return pt; const a = p[Math.max(0, i - 2)], b = p[Math.min(p.length - 1, i + 2)]; return [(a[0] + pt[0] * 2 + b[0]) / 4, (a[1] + pt[1] * 2 + b[1]) / 4]; });
  return q.filter((_, i) => i % 3 === 0 || i === q.length - 1);
}
function orient(p) {
  const [a, b] = [p[0], p[p.length - 1]], dx = b[0] - a[0], dy = b[1] - a[1];
  const closed = Math.hypot(dx, dy) < 6;
  if (closed) {                                  // circle: start at the top, go counter-clockwise like a hand
    let k = 0; for (let i = 0; i < p.length; i++) if (p[i][1] < p[k][1]) k = i;
    let q = p.slice(k).concat(p.slice(1, k + 1));
    const s = q[Math.min(5, q.length - 1)]; if (s[0] > q[0][0]) q = q.reverse();
    return q;
  }
  if (Math.abs(dx) > Math.abs(dy) * 1.2) return dx < 0 ? p.slice().reverse() : p;
  return dy < 0 ? p.slice().reverse() : p;
}

let cv;
export async function loadHangul(chars, family = '"Gaegu"', weight = 700) {
  await document.fonts.load(`${weight} ${F}px ${family}`, chars);
  cv = cv || new OffscreenCanvas(N, N); const g = cv.getContext('2d', { willReadFrequently: true });
  for (const ch of new Set(chars)) {
    if (!/[ㄱ-ㆎ가-힣]/.test(ch) || HANGUL[ch]) continue;
    g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, N, N);
    g.font = `${weight} ${F}px ${family}`; g.textBaseline = 'alphabetic'; g.fillStyle = '#000';
    const base = PAD + F * .86; g.fillText(ch, PAD, base);
    const adv = g.measureText(ch).width;
    const d = g.getImageData(0, 0, N, N).data, img = new Uint8Array(N * N);
    for (let i = 0; i < N * N; i++) img[i] = d[i * 4 + 3] > 110 ? 1 : 0;
    thin(img, N, N);
    let P = cleanup(trace(img, N, N)).map(smooth).map(orient);
    P.sort((p, q) => { const c = s => { let x = 0, y = 0; for (const t of s) { x += t[0]; y += t[1]; } return [x / s.length, y / s.length]; }; const [ax, ay] = c(p), [bx, by] = c(q); return (ax + ay * 1.25) - (bx + by * 1.25); });
    // to font units: x from the glyph's left edge, y up from the baseline
    // fill: how to draw the real glyph in the same font units, so the pen can reveal its exact shape (wb.js)
    HANGUL[ch] = { w: adv * .9 * UNIT, s: P.map(p => p.flatMap(([x, y]) => [(x - PAD) * UNIT, (base - y) * UNIT * .92])), fill: { font: `${weight} ${F}px ${family}`, PAD, base, UNIT, sy: .92 } };
  }
}
