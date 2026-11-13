// 「표고버섯, 4주 매일 먹었더니 면역세포가?」 — 44.5초 세로 릴스. 따뜻한 푸드 다큐:
// 실사 사진 + 숫자 모션 그래픽. 숫자는 연구 원문 값(Dai 외, J Am Coll Nutr 2015). 나레이션 자막은 자막 모션 스킬로
// 따로 얹는다(captions/). 화면 아래 1300~1560 은 자막 자리라 비워 둔다.
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = 1080, H = 1920, DUR = 44.5, FONT = '"Noto Sans KR"';
const NAVY = '#0E1A33', INK = '#FFFFFF', MUTE = '#C9C2B6', BROWN = '#6B4A2E', CREAM = '#FFF6E8', GOLD = '#FFC56B', SKY = '#7EC8F0', ROSE = '#FF8A6B', DARK = '#2B2118';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = t => { t = clamp(t); const s = 1.7; return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); };
const IMG = {};
const S = [0, 4.35, 8.3, 12.7, 15.65, 21.95, 25.8, 37.05];

function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function photo(c, k, z = 1, dx = 0, dy = 0) { const im = IMG[k], h = H * z, w = h * im.width / im.height; c.drawImage(im, W / 2 - w / 2 + dx, H / 2 - h / 2 + dy, w, h); }
function veil(c, col, a) { c.fillStyle = col; c.globalAlpha = a; c.fillRect(0, 0, W, H); c.globalAlpha = 1; }
function shade(c, top = .55, foot = .7) {
  let g = c.createLinearGradient(0, 0, 0, 640); g.addColorStop(0, `rgba(20,14,8,${top})`); g.addColorStop(1, 'rgba(20,14,8,0)'); c.fillStyle = g; c.fillRect(0, 0, W, 640);
  g = c.createLinearGradient(0, H, 0, H - 760); g.addColorStop(0, `rgba(20,14,8,${foot})`); g.addColorStop(1, 'rgba(20,14,8,0)'); c.fillStyle = g; c.fillRect(0, H - 760, W, 760);
}
function text(c, s, x, y, size, w = 700, col = INK, align = 'center', a = 1, sh = true) {
  if (a <= 0) return; c.save(); c.globalAlpha *= a; c.font = `${w} ${size}px ${FONT}`; c.textAlign = align; c.textBaseline = 'middle';
  if (sh) { c.shadowColor = 'rgba(0,0,0,.55)'; c.shadowBlur = 22; } c.fillStyle = col; c.fillText(s, x, y); c.restore();
}
function label(c, s, y, a, col = '#FFFFFF', bg = 'rgba(20,14,8,.45)') {
  if (a <= 0) return; c.save(); c.globalAlpha = a; c.font = `700 30px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  const w = c.measureText(s).width + 52; c.fillStyle = bg; rr(c, W / 2 - w / 2, y - 28, w, 56, 28); c.fill(); c.fillStyle = col; c.fillText(s, W / 2, y + 1); c.restore();
}
function arrow(c, x, y, len, up, col, p, wdt = 26) {   // a fat arrow that grows from its tail
  const L = len * eo(p), d = up ? -1 : 1; if (L <= 1) return;
  c.save(); c.fillStyle = col; c.translate(x, y);
  c.fillRect(-wdt / 2, up ? -L + 40 : 0, wdt, L - 40);
  c.beginPath(); c.moveTo(-wdt * 1.9, d * (L - 54)); c.lineTo(wdt * 1.9, d * (L - 54)); c.lineTo(0, d * (L + 6)); c.closePath(); c.fill(); c.restore();
}

// ---------- scenes ----------
function s0(c, t, lt) {   // dried shiitake, picked up
  photo(c, 'dried', 1.10 - .07 * ss(lt / 4.3)); shade(c, .35, .65);
  label(c, '말린 표고버섯 · 4주 매일', 300, eo(seg(lt, .3, .8)));
}
function s1(c, t, lt) {   // 52 healthy adults
  photo(c, 'hand', 1.04 + .04 * ss(lt / 4)); shade(c, .6, .7); veil(c, '#14100A', .18);
  label(c, '미국 플로리다대 · 2015 · J Am Coll Nutr', 300, eo(seg(lt, 0, .4)));
  const n = Math.round(52 * eo(seg(lt, .4, 1.5))), a = eo(seg(lt, .3, .7));
  text(c, String(n), 470, 520, 230, 900, INK, 'center', a); text(c, '명', 660, 560, 72, 800, GOLD, 'left', a);
  text(c, '건강한 성인 · 21~41세', W / 2, 700, 44, 700, INK, 'center', eo(seg(lt, 1.2, 1.7)));
}
function s2(c, t, lt) {   // 5–10 g a day, 28 days
  photo(c, 'pan', 1.04 + .05 * ss(lt / 4.4)); shade(c, .65, .7);
  const a = eo(seg(lt, .1, .5)); label(c, '하루 말린 표고', 300, a);
  text(c, '5~10', 470, 480, 190, 900, INK, 'center', a); text(c, 'g', 700, 510, 110, 900, GOLD, 'left', a);
  // a 4-week calendar filling day by day
  const x0 = 250, y0 = 640, cs = 72, d = Math.floor(28 * seg(lt, 1.0, 3.6));
  c.save(); c.globalAlpha = a; c.fillStyle = 'rgba(20,14,8,.62)'; rr(c, 210, 600, 660, 470, 36); c.fill(); c.restore();
  for (let i = 0; i < 28; i++) { const cx = x0 + (i % 7) * (cs + 12), cy = y0 + Math.floor(i / 7) * (cs + 12), on = i < d;
    c.save(); c.globalAlpha = a * (on ? 1 : .35); c.fillStyle = on ? GOLD : 'rgba(255,255,255,.5)'; rr(c, cx, cy, cs, cs, 14); c.fill();
    if (on) { c.strokeStyle = DARK; c.lineWidth = 6; c.lineCap = 'round'; c.beginPath(); c.moveTo(cx + 20, cy + 38); c.lineTo(cx + 32, cy + 50); c.lineTo(cx + 54, cy + 24); c.stroke(); }
    c.restore(); }
  text(c, `${Math.max(1, Math.ceil(d / 7))}주째 · ${d}일`, W / 2, 1020, 40, 800, INK, 'center', a * ss(seg(lt, 1.0, 1.4)));
}
function s3(c, t, lt) {   // blood and saliva, before vs after
  photo(c, 'tubes', 1.04 + .04 * ss(lt / 3)); veil(c, '#0E1A33', .25); shade(c, .5, .6);
  const a = eo(seg(lt, .1, .5)); label(c, '먹기 전 vs 4주 후', 300, a);
  [['피', 340, '#C0392B'], ['침', 740, SKY]].forEach(([s, x, col], i) => {
    const p = back(seg(lt, .4 + i * .3, .8 + i * .3)); if (p <= 0) return;
    c.save(); c.translate(x, 470); c.scale(p, p); c.fillStyle = '#FFFFFF'; c.beginPath(); c.arc(0, 0, 92, 0, 7); c.fill();
    c.fillStyle = col; c.beginPath(); c.moveTo(0, -50); c.bezierCurveTo(40, 0, 44, 30, 0, 52); c.bezierCurveTo(-44, 30, -40, 0, 0, -50); c.fill(); c.restore();
    text(c, s, x, 610, 56, 900, INK, 'center', p > 0 ? 1 : 0);
  });
}
function s4(c, t, lt) {   // the immune cells that multiplied
  photo(c, 'cells', 1.04 + .06 * ss(lt / 6.3)); veil(c, NAVY, .3); shade(c, .5, .6);
  label(c, '4주 뒤, 면역세포 증식', 300, eo(seg(lt, 0, .4)), '#FFFFFF', 'rgba(14,26,51,.6)');
  const card = (y, at, name, sub, val, suf, to) => {
    const p = back(seg(t, at, at + .45)); if (p <= 0) return;
    c.save(); c.translate(540, y + 120); c.scale(p, p); c.translate(-540, -(y + 120));
    c.fillStyle = 'rgba(14,26,51,.72)'; rr(c, 90, y, 900, 240, 36); c.fill(); c.strokeStyle = 'rgba(126,200,240,.6)'; c.lineWidth = 3; rr(c, 90, y, 900, 240, 36); c.stroke();
    text(c, name, 140, y + 82, 46, 900, INK, 'left', 1, false); text(c, sub, 140, y + 150, 30, 500, '#AFC6E0', 'left', 1, false);
    const v = to * eo(seg(t, at + .2, at + 1.0)), shown = to >= 10 ? '+' + Math.round(v) : (v < 1.05 ? '1' : v.toFixed(v >= 1.95 ? 0 : 1));
    text(c, shown, 860, y + 112, 120, 900, SKY, 'right', 1, false); text(c, suf, 950, y + 130, 54, 900, SKY, 'right', 1, false);
    c.restore();
  };
  card(470, 17.6, '감마델타 T세포', 'γδ T cell · 증식', 60, '%', 60);
  card(760, 19.85, 'NKT세포', 'NKT cell · 증식', 2, '배', 2);
}
function s5(c, t, lt) {   // antibodies up, inflammation down
  c.fillStyle = NAVY; c.fillRect(0, 0, W, H);
  const g = c.createRadialGradient(540, 760, 0, 540, 760, 900); g.addColorStop(0, '#1C2E57'); g.addColorStop(1, NAVY); c.fillStyle = g; c.fillRect(0, 0, W, H);
  label(c, '면역은 강화, 염증은 감소', 300, eo(seg(lt, 0, .4)), '#FFFFFF', 'rgba(255,255,255,.12)');
  const up = seg(t, 22.2, 23.0), dn = seg(t, 23.95, 24.75);
  arrow(c, 300, 1010, 430, true, SKY, up, 40);
  text(c, '침 속 면역 항체', 300, 1080, 40, 800, INK, 'center', eo(seg(t, 22.3, 22.8)), false);
  text(c, 'sIgA', 300, 1132, 30, 500, '#AFC6E0', 'center', eo(seg(t, 22.3, 22.8)), false);
  text(c, '늘었어요', 300, 520, 50, 900, SKY, 'center', eo(seg(t, 22.8, 23.2)), false);
  arrow(c, 780, 560, 430, false, ROSE, dn, 40);
  text(c, '혈액 속 염증 수치', 780, 1080, 40, 800, INK, 'center', eo(seg(t, 24.0, 24.5)), false);
  text(c, 'CRP', 780, 1132, 30, 500, '#AFC6E0', 'center', eo(seg(t, 24.0, 24.5)), false);
  text(c, '줄었어요', 780, 500, 50, 900, ROSE, 'center', eo(seg(t, 24.6, 25.0)), false);
  text(c, '출처: Dai 외, J Am Coll Nutr 2015 · 건강한 성인 52명', W / 2, 1210, 24, 500, '#8EA0C0', 'center', eo(seg(lt, .5, 1)), false);
}
function s6(c, t, lt) {   // three ways to eat it (the breakfast table)
  photo(c, 'meal', 1.03 + .03 * ss(lt / 11)); veil(c, CREAM, .25);
  text(c, '그래서 이렇게 드세요', W / 2, 300, 74, 900, DARK, 'center', eo(seg(lt, .1, .6)), false);
  const T = [[27.45, '하루 조금씩,', '4주 이상 꾸준히'], [30.85, '표고버섯은', '반드시 익혀서'], [33.5, '국 · 볶음 · 밥에 넣어', '하루 한 끼']];
  T.forEach(([at, a1, a2], i) => {
    const p = back(seg(t, at, at + .45)); if (p <= 0) return;
    const cur = t >= at && (i === 2 || t < T[i + 1][0]), y = 440 + i * 240;
    c.save(); c.translate(540, y + 100); c.scale(p, p); c.translate(-540, -(y + 100));
    c.shadowColor = 'rgba(80,50,10,.2)'; c.shadowBlur = 40; c.fillStyle = 'rgba(255,255,255,.96)'; rr(c, 80, y, 920, 200, 34); c.fill(); c.shadowBlur = 0;
    if (cur) { c.strokeStyle = '#C8873A'; c.lineWidth = 5; rr(c, 80, y, 920, 200, 34); c.stroke(); }
    c.fillStyle = cur ? '#C8873A' : '#F1E4CF'; c.beginPath(); c.arc(185, y + 100, 54, 0, 7); c.fill();
    text(c, String(i + 1), 185, y + 103, 60, 900, cur ? '#FFFFFF' : '#B79B70', 'center', 1, false);
    text(c, a1, 280, y + 68, 38, 700, '#6B6152', 'left', 1, false); text(c, a2, 280, y + 132, 52, 900, DARK, 'left', 1, false);
    c.restore();
  });
  const wq = ss(seg(t, 31.2, 31.8)); if (wq > 0) { c.save(); c.globalAlpha = wq; c.fillStyle = 'rgba(255,255,255,.92)'; rr(c, 150, 1150, 780, 56, 28); c.fill(); c.restore(); }
  text(c, '※ 덜 익힌 표고버섯은 피부염(발진)을 일으킬 수 있어요', W / 2, 1179, 26, 600, '#6B5A44', 'center', wq, false);
}
function s7(c, t, lt) {   // the ingredient, kept apart from the study
  c.fillStyle = CREAM; c.fillRect(0, 0, W, H);
  const P = IMG.product, p = eo(seg(lt, 0, .6)), w = 960, h = w * P.height / P.width, y = 430 + (1 - p) * 40;
  c.save(); c.globalAlpha = p; c.shadowColor = 'rgba(80,50,10,.2)'; c.shadowBlur = 40; c.fillStyle = '#fff'; rr(c, 40, y - 30, 1000, h + 60, 34); c.fill(); c.shadowBlur = 0;
  rr(c, 60, y, w, h, 22); c.clip(); c.drawImage(P, 60, y, w, h); c.restore();
  const q = eo(seg(lt, .4, 1.0)), q2 = eo(seg(lt, 1.6, 2.2));
  text(c, '표고버섯 균사체에서 얻은 원료', W / 2, 920, 46, 700, '#6B6152', 'center', q, false);
  text(c, '라파힐 AHCC', W / 2, 1010, 96, 900, DARK, 'center', q, false);
  c.save(); c.globalAlpha = q2; c.font = `700 30px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  const s = '면역기능 증진에 도움을 줄 수 있음 · 식약처 개별인정 제2008-78호', tw = c.measureText(s).width + 56;
  c.fillStyle = '#1F4FA3'; rr(c, W / 2 - tw / 2, 1085, tw, 58, 29); c.fill(); c.fillStyle = '#fff'; c.fillText(s, W / 2, 1115); c.restore();
  text(c, '출처: Dai 외, J Am Coll Nutr 2015 (연구비: 미국·호주 버섯 단체 지원)', W / 2, 1220, 24, 500, '#8C8070', 'center', q2, false);
  text(c, '※ 위 연구는 표고버섯을 먹은 연구로, 본 제품으로 한 연구가 아닙니다.', W / 2, 1260, 24, 500, '#8C8070', 'center', q2, false);
}
const SCN = [s0, s1, s2, s3, s4, s5, s6, s7];
const at = t => { let i = 0; while (i + 1 < S.length && t >= S[i + 1]) i++; return i; };
const BUF = document.createElement('canvas'); BUF.width = W; BUF.height = H; const b = BUF.getContext('2d');
function frame(c, i, t) { c.save(); c.fillStyle = '#000'; c.fillRect(0, 0, W, H); SCN[i](c, t, t - S[i]); c.restore(); }
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  const i = at(t), q = i ? seg(t, S[i], S[i] + .35) : 1;
  if (q < 1) { frame(ctx, i - 1, t); frame(b, i, t); const z = 1.05 - .05 * eo(q); ctx.globalAlpha = ss(q); ctx.drawImage(BUF, W / 2 - W * z / 2, H / 2 - H * z / 2, W * z, H * z); ctx.globalAlpha = 1; }
  else frame(ctx, i, t);
  const f = 1 - ss(seg(t, 0, .25)); if (f > 0) { ctx.fillStyle = `rgba(20,14,8,${f})`; ctx.fillRect(0, 0, W, H); }
}
window.DUR = DUR; window.render = render;
window.EV = S.slice(1).map(t => ({ t, type: 'cut' }));
(async () => {
  const L = (k, f) => new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.src = `assets/${f}`; });
  await Promise.all([['dried', 'p1-dried.png'], ['hand', 'p2-hand.png'], ['pan', 'p3-pan.png'], ['tubes', 'p4-tubes.png'], ['cells', 'p5-cells.png'], ['meal', 'p7-meal.png'], ['product', 'product.jpg']].map(([k, f]) => L(k, f)));
  await Promise.all(['500 24px', '700 40px', '900 96px'].map(f => document.fonts.load(`${f} ${FONT}`, '표고면역')));
  window.READY = true;
})();
