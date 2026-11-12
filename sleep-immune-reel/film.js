// 「잠 못 잔 다음 날, 면역세포는 무슨 일을?」 — 47.5초 세로 릴스. 과학 다큐 톤의 모션 그래픽:
// 밤 남색에서 시작해 결론(실천법)에서 아침빛으로 바뀐다. 숫자는 모두 연구 원문 값(TREATMENT.md).
// 나레이션 자막은 자막 모션 스킬로 따로 얹는다(captions/). 화면 아래 1330~1560 은 자막 자리라 비워 둔다.
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = 1080, H = 1920, DUR = 47.5, FONT = '"Noto Sans KR"';
const NIGHT = '#0B1430', NIGHT2 = '#14224A', INK = '#EAF0FF', MUTE = '#8E9BC0', CYAN = '#7FD1FF', AMBER = '#FFB547', RED = '#FF6B6B', CREAM = '#FFF6E8', DARK = '#1B2440';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = t => { t = clamp(t); const s = 1.7; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
let PRODUCT; const IMG = {};
function photo(c, k, z = 1, dx = 0, dy = 0) { const im = IMG[k], h = H * z, w = h * im.width / im.height; c.drawImage(im, W / 2 - w / 2 + dx, H / 2 - h / 2 + dy, w, h); }
function veil(c, col, a) { c.fillStyle = col; c.globalAlpha = a; c.fillRect(0, 0, W, H); c.globalAlpha = 1; }
function foot(c, a = .7) { const g = c.createLinearGradient(0, H, 0, H - 760); g.addColorStop(0, `rgba(8,14,34,${a})`); g.addColorStop(1, 'rgba(8,14,34,0)'); c.fillStyle = g; c.fillRect(0, H - 760, W, 760); }

// scene starts (seconds), anchored to the narration lines
const S = [0, 3.35, 7.85, 10.05, 17.35, 21.6, 28.0, 40.35];
function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function text(c, s, x, y, size, w = 700, col = INK, align = 'center', a = 1) {
  c.save(); c.globalAlpha *= a; c.font = `${w} ${size}px ${FONT}`; c.textAlign = align; c.textBaseline = 'middle'; c.fillStyle = col; c.fillText(s, x, y); c.restore();
}
function label(c, s, y, a, col = MUTE) {   // small caps-like kicker above a graphic
  c.save(); c.globalAlpha = a; c.font = `700 30px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  const w = c.measureText(s).width + 48; c.strokeStyle = col; c.lineWidth = 2; rr(c, W / 2 - w / 2, y - 26, w, 52, 26); c.stroke(); c.fillStyle = col; c.fillText(s, W / 2, y + 1); c.restore();
}
function source(c, s, a) { text(c, s, W / 2, 370, 24, 500, MUTE, 'center', a * .9); }   // under the kicker: the bottom of the frame is for the captions
function stars(c, t, a) {
  for (let i = 0; i < 70; i++) { const x = hash(i) * W, y = hash(i + 99) * 900, tw = .5 + .5 * Math.sin(t * 1.3 + i);
    c.fillStyle = `rgba(234,240,255,${(.15 + .35 * tw) * a})`; c.beginPath(); c.arc(x, y, 1.2 + hash(i + 7) * 1.8, 0, 7); c.fill(); }
}
function bg(c, t) {             // night → morning across the film
  const m = ss(seg(t, 27.6, 29.2));
  const g = c.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, m < 1 ? NIGHT : '#FFE3B8'); g.addColorStop(1, m < 1 ? NIGHT2 : CREAM);
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  if (m > 0 && m < 1) { const h = c.createLinearGradient(0, 0, 0, H); h.addColorStop(0, '#FFE3B8'); h.addColorStop(1, CREAM); c.globalAlpha = m; c.fillStyle = h; c.fillRect(0, 0, W, H); c.globalAlpha = 1; }
  if (m < 1) stars(c, t, 1 - m);
}
function virus(c, x, y, r, rot, col = RED, a = 1) {
  c.save(); c.globalAlpha = a; c.translate(x, y); c.rotate(rot); c.fillStyle = col; c.strokeStyle = col; c.lineWidth = r * .14; c.lineCap = 'round';
  for (let k = 0; k < 10; k++) { const an = k / 10 * Math.PI * 2; c.beginPath(); c.moveTo(Math.cos(an) * r, Math.sin(an) * r); c.lineTo(Math.cos(an) * r * 1.45, Math.sin(an) * r * 1.45); c.stroke(); c.beginPath(); c.arc(Math.cos(an) * r * 1.5, Math.sin(an) * r * 1.5, r * .16, 0, 7); c.fill(); }
  c.beginPath(); c.arc(0, 0, r, 0, 7); c.fill(); c.globalAlpha = a * .35; c.fillStyle = '#fff'; c.beginPath(); c.arc(-r * .3, -r * .3, r * .3, 0, 7); c.fill(); c.restore();
}
function moon(c, x, y, r, col = AMBER) { c.save(); c.fillStyle = col; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); c.globalCompositeOperation = 'destination-out'; c.beginPath(); c.arc(x + r * .45, y - r * .3, r * .85, 0, 7); c.fill(); c.restore(); }

// ---------- scenes ----------
function s1(c, t, lt) {   // 3 a.m.: the phone's glow in the dark
  photo(c, 'night', 1.08 - .05 * ss(lt / 3.4)); foot(c);
  label(c, '새벽 3시', 300, eo(seg(lt, .2, .7)), '#C9D6FF');
}
function s2(c, t, lt) {   // 164 people, 7 nights measured
  photo(c, 'band', 1.04 + .04 * ss(lt / 4.5)); veil(c, NIGHT, .72); foot(c, .5);
  const a = eo(seg(lt, 0, .5)); label(c, '연구 ① 2015 · 학술지 Sleep', 300, a);
  const n = Math.round(164 * eo(seg(lt, .3, 1.6)));
  text(c, String(n), 320, 520, 200, 900, INK, 'center', a); text(c, '명', 320, 650, 52, 700, MUTE, 'center', a);
  text(c, '×', 590, 530, 90, 300, MUTE, 'center', a);
  const d = Math.round(7 * eo(seg(lt, .8, 2.0))); text(c, String(d), 780, 520, 200, 900, CYAN, 'center', a); text(c, '일', 780, 650, 52, 700, MUTE, 'center', a);
  // a week of sleep, night by night (bars = hours slept, illustrative)
  const hrs = [7.4, 5.6, 6.8, 5.2, 7.9, 6.1, 4.9];
  hrs.forEach((h, i) => { const q = eo(seg(lt, 1.2 + i * .14, 1.7 + i * .14)), x = 190 + i * 110, bh = h * 42 * q;
    c.fillStyle = h < 6 ? RED : CYAN; c.globalAlpha = a; rr(c, x, 1040 - bh, 70, bh, 12); c.fill(); c.globalAlpha = 1;
    text(c, '월화수목금토일'[i], x + 35, 1080, 30, 700, MUTE, 'center', a); });
  text(c, '손목 측정기 + 수면 일기 (그림은 예시)', W / 2, 1140, 26, 500, MUTE, 'center', a * .9);
}
function s3(c, t, lt) {   // a drop of cold virus, into the nose
  photo(c, 'drop', 1.04 + .05 * ss(lt / 2.3)); foot(c, .75);
  const tg = c.createLinearGradient(0, 0, 0, 520); tg.addColorStop(0, 'rgba(8,14,34,.55)'); tg.addColorStop(1, 'rgba(8,14,34,0)'); c.fillStyle = tg; c.fillRect(0, 0, W, 520);
  const a = eo(seg(lt, 0, .4)); label(c, '그리고 격리 상태에서', 300, a, '#EAF0FF');
  for (let i = 0; i < 6; i++) { const q = eo(seg(lt, .5 + i * .08, 1.0 + i * .08)), an = -2.4 + i * .55, x = 735 + Math.cos(an) * 150 * q, y = 870 + Math.sin(an) * 120 * q;
    virus(c, x, y, 14 + (i % 3) * 5, t * .8 + i, RED, a * q * .95); }
  c.save(); c.shadowColor = 'rgba(0,0,0,.6)'; c.shadowBlur = 20;
  text(c, '감기 바이러스', W / 2, 440, 64, 900, '#FF8A8A', 'center', eo(seg(lt, .9, 1.4)));
  text(c, '5일 동안 감기에 걸리는지 관찰', W / 2, 515, 34, 700, '#EAF0FF', 'center', eo(seg(lt, 1.1, 1.6)));
  c.restore();
}
function ei2(t) { return t * t; }
function s4(c, t, lt) {   // the result: odds of a cold by nightly sleep
  const a = eo(seg(lt, 0, .4)); label(c, '감기에 걸릴 확률 (7시간 이상 = 1)', 300, a);
  const B = [['7시간\n이상', 1.0, CYAN, 1.2], ['6~7\n시간', 1.0, CYAN, 1.6], ['6시간\n미만', 4.2, RED, 2.3], ['5시간\n미만', 4.5, RED, 3.0]];
  const base = 1060, unit = 140, x0 = 150, bw = 150, gap = 70;
  c.strokeStyle = 'rgba(234,240,255,.25)'; c.lineWidth = 2; c.beginPath(); c.moveTo(110, base); c.lineTo(970, base); c.stroke();
  B.forEach(([nm, v, col, at], i) => {
    const q = eio(seg(lt, at, at + .7)), x = x0 + i * (bw + gap), h = v * unit * q;   // bars
    const hl = i === 2 ? Math.max(0, 1 - Math.abs(t - 15.9) / .5) : 0;
    c.save(); c.globalAlpha = a; c.fillStyle = col; rr(c, x - hl * 6, base - h - hl * 6, bw + hl * 12, h + hl * 6, 16); c.fill(); c.restore();
    nm.split('\n').forEach((s, k) => text(c, s, x + bw / 2, base + 44 + k * 38, 32, 700, MUTE, 'center', a));
    if (q > .05) {
      const lab = i === 1 ? '차이 없음' : v.toFixed(1) + (i ? '배' : '');
      text(c, lab, x + bw / 2, base - h - 46, i >= 2 ? 64 : 40, 900, i >= 2 ? RED : INK, 'center', a * eo(seg(lt, at + .4, at + .8)));
    }
  });
  source(c, '출처: Prather 외, Sleep 2015 (성인 164명) · 나이·스트레스·소득·흡연 보정', a);
}
function s5(c, t, lt) {   // what predicted the cold best
  const a = eo(seg(lt, 0, .4)); label(c, '감기를 가장 잘 예측한 것은?', 300, a);
  const P = [['나이', 230, 560], ['스트레스', 850, 520], ['소득', 220, 1000], ['흡연', 860, 1040]];
  P.forEach(([s, x, y], i) => { const q = eo(seg(lt, .2 + i * .12, .6 + i * .12)), fade = 1 - .55 * ss(seg(lt, 1.8, 2.6));
    c.save(); c.globalAlpha = a * q * fade; c.strokeStyle = MUTE; c.lineWidth = 3; c.beginPath(); c.arc(x, y, 92, 0, 7); c.stroke(); c.restore();
    text(c, s, x, y, 38, 700, MUTE, 'center', a * q * fade); });
  const g = back(seg(lt, 1.7, 2.5));
  c.save(); c.translate(540, 790); c.scale(g, g);
  const h = c.createRadialGradient(0, 0, 0, 0, 0, 260); h.addColorStop(0, 'rgba(255,181,71,.35)'); h.addColorStop(1, 'rgba(255,181,71,0)'); c.fillStyle = h; c.beginPath(); c.arc(0, 0, 260, 0, 7); c.fill();
  moon(c, -10, -30, 110); text(c, '잠', 0, 150, 96, 900, AMBER);
  c.restore();
}
function s6(c, t, lt) {   // vaccine study: antibodies after a night's sleep vs a night awake
  photo(c, 'arm', 1.04 + .05 * ss(lt / 6.4)); veil(c, NIGHT, .25 + .55 * ss(seg(lt, 1.4, 2.1))); foot(c, .6);
  const a = eo(seg(lt, 0, .4)); label(c, '연구 ② 2003 · 독일 뤼베크대', 300, a);
  c.save(); c.shadowColor = 'rgba(0,0,0,.6)'; c.shadowBlur = 18; text(c, 'A형 간염 백신 접종 → 그날 밤', W / 2, 1180, 44, 900, INK, 'center', a * (1 - ss(seg(lt, 1.4, 2.0)))); c.restore();
  const q = ss(seg(lt, 1.6, 2.2)); if (q <= 0) return;
  const base = 1040, unit = 230, bw = 230;
  [['밤새운 사람', 1.0, MUTE, 2.4, 260], ['푹 잔 사람', 2.0, AMBER, 4.6, 590]].forEach(([nm, v, col, at, x]) => {
    const p = eio(seg(lt, at, at + .8)), h = v * unit * p;
    c.save(); c.globalAlpha = q; c.fillStyle = col; rr(c, x, base - h, bw, h, 18); c.fill(); c.restore();
    text(c, nm, x + bw / 2, base + 50, 36, 700, INK, 'center', q);
    if (p > .05) text(c, v === 1 ? '1' : '약 2배', x + bw / 2, base - h - 50, v === 1 ? 44 : 72, 900, v === 1 ? INK : AMBER, 'center', q * eo(seg(lt, at + .4, at + .8)));
  });
  text(c, '4주 뒤 항체', W / 2, 470, 34, 700, MUTE, 'center', q);
  source(c, '출처: Lange 외, Psychosomatic Medicine 2003', q);
}
function s7(c, t, lt) {   // three things to do (morning)
  photo(c, 'morning', 1.04 + .03 * ss(lt / 12)); veil(c, CREAM, .38);
  const sun = eo(seg(lt, 0, 1.2));
  const g = c.createRadialGradient(540, 180, 0, 540, 180, 520); g.addColorStop(0, `rgba(255,181,71,${.55 * sun})`); g.addColorStop(1, 'rgba(255,181,71,0)'); c.fillStyle = g; c.fillRect(0, 0, W, 800);
  text(c, '그래서 이렇게 하세요', W / 2, 300, 74, 900, DARK, 'center', eo(seg(lt, .1, .6)));
  const T = [[29.6, '최소 6시간,', '가능하면 7시간 이상 자기'], [33.45, '백신 맞은 날 밤은', '꼭 푹 자기'], [36.75, '잠과 함께', '꾸준한 면역 습관 챙기기']];
  T.forEach(([at, a1, a2], i) => {
    const p = back(seg(t, at, at + .45)); if (p <= 0) return;
    const cur = t >= at && (i === 2 || t < T[i + 1][0]), y = 470 + i * 250;
    c.save(); c.translate(540, y + 105); c.scale(p, p); c.translate(-540, -(y + 105));
    c.shadowColor = 'rgba(80,50,10,.18)'; c.shadowBlur = 40; c.fillStyle = '#FFFFFF'; rr(c, 80, y, 920, 210, 34); c.fill(); c.shadowBlur = 0;
    if (cur) { c.strokeStyle = AMBER; c.lineWidth = 5; rr(c, 80, y, 920, 210, 34); c.stroke(); }
    c.fillStyle = cur ? AMBER : '#F1E4CF'; c.beginPath(); c.arc(190, y + 105, 56, 0, 7); c.fill();
    text(c, String(i + 1), 190, y + 108, 62, 900, cur ? '#FFFFFF' : '#B79B70');
    text(c, a1, 290, y + 72, 40, 700, '#6B6152', 'left'); text(c, a2, 290, y + 138, 52, 900, DARK, 'left');
    c.restore();
  });
}
function s8(c, t, lt) {   // the product, kept apart from the studies
  c.fillStyle = CREAM; c.fillRect(0, 0, W, H);
  const p = eo(seg(lt, 0, .6)), w = 960, h = w * PRODUCT.height / PRODUCT.width, y = 430 + (1 - p) * 40;
  c.save(); c.globalAlpha = p; c.shadowColor = 'rgba(80,50,10,.2)'; c.shadowBlur = 40; c.fillStyle = '#fff'; rr(c, 40, y - 30, 1000, h + 60, 34); c.fill(); c.shadowBlur = 0;
  rr(c, 60, y, w, h, 22); c.clip(); c.drawImage(PRODUCT, 60, y, w, h); c.restore();
  const q = eo(seg(lt, .5, 1.1)), q2 = eo(seg(lt, 1.2, 1.8));
  text(c, '면역기능 증진에 도움을 줄 수 있는', W / 2, 920, 46, 700, '#6B6152', 'center', q);
  text(c, '라파힐 AHCC', W / 2, 1010, 96, 900, DARK, 'center', q);
  c.save(); c.globalAlpha = q2; c.font = `700 32px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; const tw = c.measureText('식약처 개별인정 제2008-78호').width + 56;
  c.fillStyle = '#1F4FA3'; rr(c, W / 2 - tw / 2, 1085, tw, 60, 30); c.fill(); c.fillStyle = '#fff'; c.fillText('식약처 개별인정 제2008-78호', W / 2, 1116); c.restore();
  text(c, '출처: Prather 외, Sleep 2015 · Lange 외, Psychosomatic Medicine 2003', W / 2, 1230, 24, 500, '#8C8070', 'center', q2);
  text(c, '※ 수면 연구는 본 제품의 효과를 보여 주는 연구가 아닙니다.', W / 2, 1270, 24, 500, '#8C8070', 'center', q2);
}
const SCN = [s1, s2, s3, s4, s5, s6, s7, s8];
const at = t => { let i = 0; while (i + 1 < S.length && t >= S[i + 1]) i++; return i; };
const BUF = document.createElement('canvas'); BUF.width = W; BUF.height = H; const b = BUF.getContext('2d');
function frame(c, i, t) { c.save(); bg(c, t); SCN[i](c, t, t - S[i]); c.restore(); }
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  const i = at(t), q = i ? seg(t, S[i], S[i] + .35) : 1;
  if (q < 1) { frame(ctx, i - 1, t); frame(b, i, t); const z = 1.05 - .05 * eo(q); ctx.globalAlpha = ss(q); ctx.drawImage(BUF, W / 2 - W * z / 2, H / 2 - H * z / 2, W * z, H * z); ctx.globalAlpha = 1; }
  else frame(ctx, i, t);
  const f = 1 - ss(seg(t, 0, .25)); if (f > 0) { ctx.fillStyle = `rgba(11,20,48,${f})`; ctx.fillRect(0, 0, W, H); }
}
window.DUR = DUR; window.render = render;
window.EV = S.slice(1).map(t => ({ t, type: 'cut' }));
(async () => {
  PRODUCT = await new Promise(r => { const im = new Image(); im.onload = () => r(im); im.src = 'assets/product.jpg'; });
  await Promise.all([['night', 'p1-night'], ['band', 'p2-band'], ['drop', 'p3-drop'], ['arm', 'p6-arm'], ['morning', 'p7-morning']].map(([k, f]) => new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.src = `assets/${f}.png`; })));
  await Promise.all(['500 24px', '700 40px', '900 96px'].map(f => document.fonts.load(`${f} ${FONT}`, '잠면역')));
  window.READY = true;
})();
