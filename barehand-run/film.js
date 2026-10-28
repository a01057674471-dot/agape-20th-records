// 만약 겨울 내내 영하에서 맨손으로 달린다면? — 35 s portrait reel in the Pictogram Motion style.
// Eight cards on a 120 bpm grid (1 beat = 0.5 s): the hook, the wind a run makes, the finger at 15 °C, the 3-week lab study,
// its results, the twist, a runner's checklist, and a split-screen question. Every cut is a band-slide on a beat.
const G = window.G;
const { W, H, E, clamp, lerp, inv } = G;
export const BPM = 120, BEAT = .5, DUR = 35;
const C0 = G.CREAM, INK = G.INK;

// ---------- edit list (seconds) ----------
export const CARDS = [
  { id: 'hook',   t0: 0,    t1: 4.625,    pal: 'night', ch: 'WHAT IF',        en: 'BARE HANDS, ALL WINTER' },
  { id: 'wind',   t0: 4.625, t1: 10.5, pal: 'ice',   ch: 'WIND CHILL',     en: 'YOUR PACE IS A HEADWIND' },
  { id: 'finger', t0: 10.5, t1: 13.75, pal: 'frost', ch: 'ONE RUN',        en: 'FINGER SKIN 15°C' },
  { id: 'study',  t0: 13.75, t1: 17.5, pal: 'night', ch: 'ALL WINTER',     en: '3-WEEK LAB STUDY' },
  { id: 'result', t0: 17.5, t1: 22.75,   pal: 'snow',  ch: 'RESULT',         en: 'AFTER 15 SESSIONS' },
  { id: 'twist',  t0: 22.75, t1: 26.75, pal: 'heat',  ch: 'THE TWIST',      en: 'NUMB, NOT ADAPTED' },
  { id: 'check',  t0: 26.75, t1: 31.5, pal: 'night', ch: 'RUNNER CHECK',   en: 'BEFORE YOU GO OUT' },
  { id: 'cta',    t0: 31.5, t1: 35,   pal: 'ice',   ch: 'YOUR CALL',      en: 'GLOVES OR BARE?' },
];
const N = CARDS.length;
export const K = {
  wind: [4.75, 6.0, 7.25], warn: 7.3,
  gauge: [10.75, 12.0], studyLine: 14.0, count: [14.5, 16.5],
  rows: [17.75, 18.25, 18.75, 19.25], silence: [22.5, 22.75],
  checks: [27.0, 27.5, 28.0], cta: 31.75,
};

// ---------- text registry (reading check) ----------
const TXT = [];
function reg(id, text, t0, t1, box) { if (!TXT.some(x => x.id === id)) TXT.push({ id, text, t0, t1, box }); }
export function texts(t) { return TXT.filter(x => t >= x.t0 && t <= x.t1); }
// mask slide-up line, registered for the reading check
function line(ctx, id, s, x, y, font, col, t, t0, t1, o = {}) {
  ctx.save(); ctx.font = font; const m = ctx.measureText(s); ctx.restore();
  const asc = o.asc ?? m.actualBoundingBoxAscent;
  reg(id, o.text ?? s, t0, t1, [x - (o.align === 'right' ? m.width : 0), y - asc, m.width, asc + 10]);
  if (t < t0) return 0;
  return G.maskText(ctx, s, x, y, font, col, clamp((t - t0) / .35), { align: o.align, ls: o.ls });
}

// ---------- pieces ----------
function colors(pal) {
  const P = G.PAL[pal], light = pal === 'snow';
  return { P, fg: P.fg, far: G.mix(P.fg, P.t[1], .45), bg: P.t[1], disc: light ? P.t[4] : P.t[3], line: G.rgba(P.fg, .55), acc: pal === 'heat' ? '#ffd23f' : '#ff5a36' };
}
function background(ctx, pal, seed, t, cardT0, spread = .4) {
  const pat = G.pattern(pal, seed, { spread, density: .5 });
  const beat = Math.floor((t - cardT0) / BEAT);
  // rows breathe in alternating directions; every beat they jump a quarter cell
  G.drawPattern(ctx, pat, j => (j % 2 ? 1 : -1) * (((t - cardT0) * 18) % 90 + (beat % 4) * G.CELL / 4 * (spread > .7 ? 1 : 0)));
}
function sun(ctx, x, y, r, C, t) {
  G.disc(ctx, x, y, r, C.disc);
  ctx.save(); ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.clip();      // one soft light sweep
  const sx = x - r * 1.6 + ((t * .35) % 1) * r * 3.2;
  const g = ctx.createLinearGradient(sx - 120, 0, sx + 120, 0);
  g.addColorStop(0, G.rgba(C0, 0)); g.addColorStop(.5, G.rgba(C0, .09)); g.addColorStop(1, G.rgba(C0, 0));
  ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2); ctx.restore();
}
// a figure on the stage: (x, y) = hip in px, s = body height in px; asm = assembly progress (bands slide into register)
function figure(ctx, pose, x, y, s, C, asm = 1, extra) {
  const J = G.joints(pose);
  const draw = () => { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); G.drawFigure(ctx, J, C.fg, C.far); if (extra) extra(ctx, J); ctx.restore(); };
  if (asm >= 1) { draw(); return J; }
  const bands = 6, top = y - s * .62, h = s * 1.1 / bands;
  for (let i = 0; i < bands; i++) {
    const p = E.oExp(clamp(asm * 1.6 - i * .12)); if (p <= 0) continue;
    ctx.save(); ctx.beginPath(); ctx.rect(0, top + i * h, W, h + 1); ctx.clip();
    ctx.translate((1 - p) * (i % 2 ? 1 : -1) * W * .6, 0); draw(); ctx.restore();
  }
  return J;
}
const run = (t, k = 1) => Object.assign(G.runCycle(t / BEAT / 2, k), { x: 0 });      // one stride cycle every two beats
// bare hands: two warm discs; mittens: bigger amber capsules
function hands(ctx, J, col, r = .045) { G.disc(ctx, J.aL[2][0], J.aL[2][1], r, col); G.disc(ctx, J.aR[2][0], J.aR[2][1], r, col); }
// a pictogram hand (unit = palm height), fingers coloured by temperature
function handIcon(ctx, x, y, s, palm, finger) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = palm; ctx.beginPath(); ctx.roundRect(-.36, -.1, .72, .62, .16); ctx.fill();
  [[-.27, .78], [-.09, .92], [.09, .88], [.27, .72]].forEach(([fx, L]) => G.seg(ctx, [fx, 0], [fx, -L * .62], .15, finger));
  G.seg(ctx, [-.3, .28], [-.62, -.02], .17, finger);
  ctx.restore();
}
function arrow(ctx, x, y, s, col, down = true) {      // a pictogram arrow: one capsule and a triangle
  const d = down ? 1 : -1;
  G.seg(ctx, [x, y - d * s * .5], [x, y + d * s * .15], s * .22, col);
  G.poly(ctx, [[x - s * .32, y + d * s * .05], [x + s * .32, y + d * s * .05], [x, y + d * s * .5]], col);
}
function chip(ctx, s, x, y, bg, fg, px = 34) {
  ctx.save(); ctx.font = G.F.kr(800, px); const w = ctx.measureText(s).width;
  ctx.fillStyle = bg; ctx.fillRect(x, y - px * 1.05, w + px * .9, px * 1.45);
  ctx.fillStyle = fg; ctx.fillText(s, x + px * .45, y); ctx.restore(); return w + px * .9;
}
function snow(ctx, t, C, seed = 3, n = 26) {
  const r = G.rng(seed);
  for (let i = 0; i < n; i++) {
    const x0 = r() * W, sp = 60 + r() * 120, y = (r() * H + t * sp) % (H * .62), x = x0 + Math.sin(t * 1.3 + i) * 18;
    G.disc(ctx, x, y + 120, 3 + r() * 6, G.rgba(C0, .55));
  }
}

// ---------- HUD ----------
function hud(ctx, card, i, t, C) {
  const p = clamp((t - card.t0) / .4);
  ctx.save(); ctx.fillStyle = C.fg; ctx.font = G.F.mono(24); ctx.letterSpacing = '4px';
  G.typeText(ctx, 'WHAT IF —', 72, 96, G.F.mono(24), C.fg, 1, { ls: '4px', caret: false });
  G.typeText(ctx, 'BARE-HAND WINTER RUN', 72, 130, G.F.mono(24), C.fg, 1, { ls: '4px', caret: false });
  G.typeText(ctx, `CH.0${i + 1}  ${card.ch}`, W - 72, 96, G.F.mono(24), C.fg, p, { ls: '4px', align: 'right', caret: false });
  G.typeText(ctx, '연구 기반 시뮬레이션', W - 72, 130, G.F.mono(24), C.fg, 1, { ls: '2px', align: 'right', caret: false });
  // progress: N ticks, current tall
  const x0 = 72, w = W - 144;
  for (let k = 0; k < N; k++) {
    const x = x0 + (w * k) / (N - 1), cur = k === i;
    ctx.fillStyle = G.rgba(C.fg, k < i ? .45 : cur ? 1 : .22);
    ctx.fillRect(x - 2, cur ? 1812 : 1826, 4, cur ? 40 : 14);
  }
  ctx.restore();
}
function index(ctx, i, x, y, C, t, t0) {
  G.maskText(ctx, `0${i + 1} / 0${N}`, x, y, G.F.mono(30), C.fg, clamp((t - t0) / .3), { ls: '6px' });
}

// ---------- cards ----------
const TX = 80;      // text column x
function cardHook(ctx, t, c, C) {
  sun(ctx, W / 2, 640, 380, C, t); snow(ctx, t, C);
  figure(ctx, run(t), W / 2, 690, 620, C, 1, (cx, J) => hands(cx, J, C.acc, .05));
  index(ctx, 0, TX, 1090, C, t, c.t0);
  // the title, from the first frame: three lines, the last one in the warm accent
  const L1 = '만약 겨울 내내', L2 = '영하에서 맨손으로', L3 = '달린다면?';
  line(ctx, 'h1', L1, TX, 1250, G.F.kr(900, G.fitFont(ctx, L2, 'kr', 900, 140, W - 160)), C.fg, t, -.3, c.t1, { text: L1 + ' ' + L2 + ' ' + L3 });
  line(ctx, 'h2', L2, TX, 1410, G.F.kr(900, G.fitFont(ctx, L2, 'kr', 900, 140, W - 160)), C.fg, t, -.2, c.t1);
  line(ctx, 'h3', L3, TX, 1610, G.F.kr(900, 190), C.acc, t, -.1, c.t1);
}
const WIND = [['−15°C', '기온 −10°C · 6분 페이스 (시속 10km)'], ['−20°C', '+ 맞바람 시속 20km'], ['−26°C', '−15°C + 맞바람 20km/h']];
function cardWind(ctx, t, c, C) {
  sun(ctx, W / 2, 600, 340, C, t);
  // the runner holds still while the wind streams past: the pace is the headwind
  figure(ctx, run(t), W / 2 + 40, 650, 560, C, clamp((t - c.t0) / .5), (cx, J) => {
    const k = 1 + (t > K.wind[1]) + (t > K.wind[2]);
    for (let i = 0; i < 6 * k; i++) { const ph = ((t * (1.4 + k * .5) + i * .37) % 1); cx.fillStyle = G.rgba(C0, .5); cx.fillRect(.9 - ph * 2.4, -.5 + ((i * 37) % 11) * .1, .35 + (i % 3) * .1, .012); }
    hands(cx, J, t > K.wind[2] ? '#ff5a36' : C0, .045);
  });
  index(ctx, 1, TX, 1030, C, t, c.t0);
  line(ctx, 'w0', '손이 느끼는 체감온도', TX, 1110, G.F.kr(800, 52), C.fg, t, K.wind[0], c.t1);
  // the big number: each new value rises in on its beat, the old one leaves upward
  let i = 0; K.wind.forEach((tk, k) => { if (t >= tk) i = k; });
  const tk = K.wind[i], p = clamp((t - tk) / .3), big = G.F.en(900, 300);
  ctx.save(); ctx.beginPath(); ctx.rect(0, 1130, W, 300); ctx.clip();
  ctx.font = big; ctx.letterSpacing = '-8px'; ctx.fillStyle = i === 2 ? '#ffd9cf' : C.fg;
  if (i && p < 1) ctx.fillText(WIND[i - 1][0], TX - 10, 1400 - E.oExp(p) * 300);
  if (t >= K.wind[0]) ctx.fillText(WIND[i][0], TX - 10, 1400 + (1 - E.oExp(p)) * 300);
  ctx.restore();
  reg('wnum', '−15°C −20°C −26°C', K.wind[0], c.t1, [TX, 1150, 700, 250]);
  WIND.forEach(([, s], k) => line(ctx, 'wl' + k, s, TX, 1500 + k * 62, G.F.kr(k === i ? 800 : 500, 40), k === i ? C.fg : G.rgba(C.fg, .6), t, K.wind[k] + .1, c.t1));
  if (t >= K.warn) {
    const p2 = E.oExp(clamp((t - K.warn) / .3));
    ctx.save(); ctx.beginPath(); ctx.rect(0, 1650, W * p2, 120); ctx.clip();
    chip(ctx, '−27°C부터 동상 위험 급증', TX, 1730, '#ff5a36', C0, 44); ctx.restore();
    reg('warn', '−27°C부터 동상 위험 급증', K.warn, c.t1, [TX, 1680, 700, 60]);
  }
}
function cardFinger(ctx, t, c, C) {
  sun(ctx, W / 2, 620, 360, C, t);
  const g = E.io(clamp((t - K.gauge[0]) / (K.gauge[1] - K.gauge[0]))), temp = Math.round(lerp(32, 15, g));
  const warm = '#ff8a5c', cold = '#bfe6ff';
  handIcon(ctx, W / 2 - 110, 720, 300, C0, G.mix(warm, cold, g));
  // thermometer: a capsule tube, a bulb, the fill falling in steps
  const tx = W / 2 + 230, top = 360, bot = 820;
  G.seg(ctx, [tx, top], [tx, bot], 60, G.rgba(C0, .35)); G.disc(ctx, tx, bot + 40, 62, G.mix(warm, cold, g));
  const fy = lerp(top + 40, bot - 40, inv(32, 10, temp));
  G.seg(ctx, [tx, fy], [tx, bot], 34, G.mix(warm, cold, g));
  ctx.font = G.F.en(900, 64); ctx.fillStyle = C.fg; ctx.fillText(`${temp}°`, tx + 70, fy + 22);
  index(ctx, 2, TX, 1130, C, t, c.t0);
  line(ctx, 'f1', '손가락 15°C', TX, 1320, G.F.kr(900, 170), C.fg, t, c.t0 + .15, c.t1);
  line(ctx, 'f2', '손놀림 급격히 저하', TX, 1460, G.F.kr(900, 96), '#bfe6ff', t, c.t0 + .3, c.t1);
}
function cardStudy(ctx, t, c, C) {
  sun(ctx, W / 2, 620, 360, C, t);
  // a hand dipping into a bowl of 8 °C water on every beat
  const u = (t - c.t0) / BEAT, dip = Math.max(0, Math.sin(u * Math.PI)) ** 2;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, 760); ctx.clip();
  handIcon(ctx, W / 2, 470 + dip * 140, 230, C0, G.mix('#ff8a5c', '#bfe6ff', clamp((t - K.count[0]) / 2)));
  ctx.restore();
  ctx.save(); ctx.beginPath(); ctx.arc(W / 2, 740, 300, 0, Math.PI); ctx.fillStyle = '#3f82dc'; ctx.fill(); ctx.restore();
  for (let i = 0; i < 3; i++) { ctx.fillStyle = G.rgba(C0, .5); ctx.fillRect(W / 2 - 250 + i * 40, 770 + i * 40, 500 - i * 80, 6); }
  ctx.font = G.F.en(900, 56); ctx.fillStyle = C0; ctx.textAlign = 'center'; ctx.fillText('8°C', W / 2, 900); ctx.textAlign = 'left';
  index(ctx, 3, TX, 1060, C, t, c.t0);
  line(ctx, 's1', '겨울 내내 하면?', TX, 1220, G.F.kr(900, 130), C.fg, t, c.t0 + .1, c.t1);
  line(ctx, 's2', '16명 · 8°C 물 · 하루 30분 · 15회', TX, 1310, G.F.kr(700, 44), G.rgba(C.fg, .85), t, K.studyLine, c.t1);
  // day counter: 01 → 15 on sixteenth notes, slam on the downbeat
  const d = Math.max(1, Math.min(15, 1 + Math.floor(inv(K.count[0], K.count[1], t) * 14.999)));
  if (t >= K.count[0]) {
    ctx.font = G.F.en(900, 300); ctx.letterSpacing = '-8px'; ctx.fillStyle = d === 15 ? C.acc : C.fg;
    ctx.fillText(String(d).padStart(2, '0'), TX - 10, 1650); ctx.letterSpacing = '0px';
    ctx.font = G.F.kr(800, 56); ctx.fillStyle = C.fg; ctx.fillText('회째', TX + 380, 1650);
    reg('count', '01 → 15회째', K.count[0], c.t1, [TX, 1420, 600, 230]);
  }
  line(ctx, 's3', 'Daanen 외, 2011 · 실험실 연구', TX, 1730, G.F.kr(500, 30), G.rgba(C.fg, .65), t, K.studyLine + .1, c.t1);
}
const ROWS = [['통증', 'down'], ['손가락 온도', 'down'], ['스스로 데워지는 반응', 'civd'], ['촉각', 'down']];
function cardResult(ctx, t, c, C) {
  index(ctx, 4, TX, 300, C, t, c.t0);
  line(ctx, 'r0', '3주 뒤', TX, 440, G.F.kr(900, 130), C.fg, t, c.t0 + .1, c.t1);
  ROWS.forEach(([s, kind], k) => {
    const t0 = K.rows[k], y = 640 + k * 290;
    if (t < t0) return;
    const p = E.oExp(clamp((t - t0) / .3));
    ctx.fillStyle = G.rgba(INK, .14); ctx.fillRect(TX, y - 120, (W - 2 * TX) * p, 2);
    line(ctx, 'rr' + k, s, TX, y, G.F.kr(900, k === 2 ? 72 : 96), C.fg, t, t0, c.t1);
    if (kind === 'down') { ctx.save(); ctx.globalAlpha = p; arrow(ctx, W - 170, y - 40, 120, k === 0 ? '#0a7d4f' : '#e0382a'); ctx.restore(); }
    else {      // CIVD 52 % → 24 %: two bars, the second shrinks in
      const bw = (W - 2 * TX) * .9;
      ctx.fillStyle = G.rgba(INK, .25); ctx.fillRect(TX, y + 30, bw * .52, 36);
      ctx.fillStyle = '#e0382a'; ctx.fillRect(TX, y + 80, bw * lerp(.52, .24, E.io(clamp((t - t0 - .25) / .6))), 36);
      ctx.font = G.F.en(900, 40); ctx.fillStyle = C.fg; ctx.fillText('52%', TX + bw * .52 + 16, y + 62); ctx.fillText('24%', TX + bw * .24 + 16, y + 112);
      reg('rciv', '52% → 24%', t0, c.t1, [TX, y + 20, 700, 100]);
    }
  });
  line(ctx, 'rnote', '* 손을 8°C 물에 담근 실험실 연구 기준', TX, 1760, G.F.kr(500, 30), G.rgba(C.fg, .7), t, K.rows[0] + .2, c.t1);
}
function cardTwist(ctx, t, c, C) {
  index(ctx, 5, TX, 640, C, t, c.t0);
  line(ctx, 'x1', '덜 아픈 건', TX, 860, G.F.kr(900, 150), C.fg, t, c.t0 + .05, c.t1);
  line(ctx, 'x2', '적응이 아니라', TX, 1040, G.F.kr(900, 150), C.fg, t, c.t0 + .3, c.t1);
  line(ctx, 'x3', '둔해진 것', TX, 1240, G.F.kr(900, 190), '#ffd23f', t, c.t0 + .8, c.t1);
  line(ctx, 'x4', '→ 동상 위험이 커질 수 있다 (연구진)', TX, 1400, G.F.kr(700, 48), C.fg, t, c.t0 + .6, c.t1, { text: '→ 동상 위험이 커질 수 있다' });
}
const CHECKS = ['체감 −27°C 아래면 장갑 필수', '하얗게 질리고 감각 없으면 중단', '얇은 장갑 + 벙어리장갑'];
function cardCheck(ctx, t, c, C) {
  sun(ctx, W / 2, 560, 320, C, t); snow(ctx, t, C, 9, 18);
  figure(ctx, run(t), W / 2, 600, 520, C, clamp((t - c.t0) / .5), (cx, J) => { cx.fillStyle = '#ffb020';
    [J.aL[2], J.aR[2]].forEach(h => { cx.beginPath(); cx.roundRect(h[0] - .05, h[1] - .06, .1, .12, .05); cx.fill(); }); });
  index(ctx, 6, TX, 1000, C, t, c.t0);
  line(ctx, 'c0', '러너 체크', TX, 1150, G.F.kr(900, 120), C.fg, t, c.t0 + .1, c.t1);
  CHECKS.forEach((s, k) => {
    const t0 = K.checks[k], y = 1300 + k * 120;
    if (t >= t0) { const p = E.oBack(clamp((t - t0) / .3)); ctx.save(); ctx.translate(TX + 30, y - 18); ctx.scale(p, p);
      G.disc(ctx, 0, 0, 30, '#ffb020'); ctx.strokeStyle = INK; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-13, 0); ctx.lineTo(-3, 11); ctx.lineTo(14, -10); ctx.stroke(); ctx.restore(); }
    line(ctx, 'ck' + k, s, TX + 84, y, G.F.kr(800, 52), C.fg, t, t0, c.t1);
  });
}
function cardCta(ctx, t, c, C) {
  // split screen along a grid line: gloves (ice) | bare (heat)
  const sp = E.ioExp(clamp((t - c.t0) / .5)), mid = W / 2;
  const R = colors('heat');
  ctx.save(); ctx.beginPath(); ctx.rect(mid + (1 - sp) * mid, 0, W, H); ctx.clip();
  background(ctx, 'heat', 11, t, c.t0, .4); ctx.restore();
  ctx.fillStyle = G.rgba(C0, .9); ctx.fillRect(mid - 2, 200, 4, 1000 * sp);
  const L = { ...C }, Rr = { ...R };
  figure(ctx, run(t), W * .27, 640, 440, L, 1, (cx, J) => { cx.fillStyle = '#ffb020'; [J.aL[2], J.aR[2]].forEach(h => { cx.beginPath(); cx.roundRect(h[0] - .05, h[1] - .06, .1, .12, .05); cx.fill(); }); });
  if (sp > .3) figure(ctx, run(t + .25), W * .75, 640, 440, Rr, clamp((sp - .3) / .7), (cx, J) => hands(cx, J, '#ffd23f', .045));
  line(ctx, 'v1', '장갑파', TX, 1020, G.F.kr(900, 96), C.fg, t, c.t0 + .3, c.t1, { text: '장갑파 vs 맨손파' });
  line(ctx, 'v2', '맨손파', W - TX, 1020, G.F.kr(900, 96), C0, t, c.t0 + .45, c.t1, { align: 'right' });
  index(ctx, 7, TX, 1240, C, t, c.t0);
  line(ctx, 'q1', '당신은?', TX, 1450, G.F.kr(900, 190), C.fg, t, K.cta, c.t1);
  line(ctx, 'q2', '댓글로 알려주세요', TX, 1580, G.F.kr(800, 72), C.fg, t, K.cta + .3, c.t1);
}
const DRAW = { hook: cardHook, wind: cardWind, finger: cardFinger, study: cardStudy, result: cardResult, twist: cardTwist, check: cardCheck, cta: cardCta };

function scene(ctx, i, t) {
  const c = CARDS[i], C = colors(c.pal);
  ctx.save();
  background(ctx, c.pal, i * 7 + 1, t, c.t0, c.id === 'twist' ? .6 : c.pal === 'snow' ? .25 : .4);
  DRAW[c.id](ctx, t, c, C);
  hud(ctx, c, i, t, C);
  ctx.restore();
}

// ---------- frame: band-slide transitions on each cut ----------
let A = null, B = null;
const TR = .25;
export function render(ctx, t) {
  if (!A) { A = G.canvas(W, H); B = G.canvas(W, H); }
  let i = CARDS.findIndex(c => t < c.t1); if (i < 0) i = N - 1;
  const c = CARDS[i], into = t - c.t0;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.letterSpacing = '0px';
  if (i === 0 || into >= TR) { scene(ctx, i, t); return; }
  const a = A.getContext('2d'), b = B.getContext('2d');
  a.setTransform(1, 0, 0, 1, 0, 0); b.setTransform(1, 0, 0, 1, 0, 0);
  scene(a, i - 1, t); scene(b, i, t);
  ctx.drawImage(A, 0, 0);
  const p = E.ioExp(into / TR), rows = 8, h = H / rows;
  for (let j = 0; j < rows; j++) {
    const q = clamp(p * 1.4 - (j % 2) * .15 - j * .02), dx = (1 - E.oExp(q)) * W * (j % 2 ? 1 : -1);
    ctx.drawImage(B, 0, j * h, W, h + 1, dx, j * h, W, h + 1);
  }
}

// ---------- sound events (the score reads these) ----------
export function events() {
  const ev = CARDS.map((c, i) => ({ t: c.t0, type: 'cut', card: c.id, i }));
  K.wind.forEach((t, i) => ev.push({ t, type: 'slam', k: i }));
  ev.push({ t: K.warn, type: 'warn' });
  ev.push({ t: K.gauge[0], type: 'gauge', d: K.gauge[1] - K.gauge[0] });
  for (let d = 0; d < 15; d++) ev.push({ t: K.count[0] + d * (K.count[1] - K.count[0]) / 14.999, type: 'count', d });
  for (let b = 1; b < 7; b++) ev.push({ t: 13.75 + b * BEAT, type: 'dip' });
  K.rows.forEach((t, k) => ev.push({ t, type: 'row', k }));
  ev.push({ t: K.silence[0], type: 'silence', d: K.silence[1] - K.silence[0] });
  K.checks.forEach((t, k) => ev.push({ t, type: 'check', k }));
  ev.push({ t: K.cta, type: 'slam', k: 3 });
  return ev.sort((a, b) => a.t - b.t);
}
