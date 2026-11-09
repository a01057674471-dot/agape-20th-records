// 「세포 속 발전소가 조각나고 있다면?」 — 31초 세로 릴스, 과학 다큐 톤 (어두운 남색 + 형광 현미경 빛, 포인트 라임)
// 화면은 사용자 나레이션(audio/narration.mp3)에 맞췄다: 각 문장의 시작·끝은 음성 인식으로 확인한 시간(TREATMENT.md).
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const W = 1080, H = 1920, DUR = 31.0;
const BG = '#050811', LIME = '#B4EC2D', WHITE = '#F4F6FA', MUTE = '#9AA3B5', FONT = '"Noto Sans KR"';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };

// narration lines (seconds in the recording) — the on-screen subtitles
const SUBS = [
  [0.17, 2.13, '세포 속 발전소가 조각나고 있다면?'],
  [2.64, 5.14, '우리 몸의 세포마다 에너지를 만드는 발전소,'],
  [5.39, 6.53, '미토콘드리아가 있어요.'],
  [7.02, 9.57, '건강할 땐 길게 이어진 그물 모양이지만,'],
  [10.04, 12.91, '영양이 끊기는 스트레스를 받으면 조각조각 쪼개지고,'],
  [13.16, 15.45, '단백질 공장인 소포체도 흐트러져요.'],
  [15.65, 18.11, '일본 오사카공립대학교 연구팀이 이 세포에'],
  [18.38, 20.63, '리치 폴리페놀 올리고놀을 넣어 봤더니,'],
  [20.96, 22.48, '이런 모양 변화가 완화됐어요.'],
  [22.95, 24.23, '세포 실험 결과로 확인한,'],
  [24.50, 26.01, '리치 폴리페놀 올리고놀.'],
  [26.38, 27.93, '젤리 스틱, 올리고파.'],
];
// scenes: [start, image, headline lines (words between * are lime)]
const SC = [
  { t0: 0, img: 'break', head: ['세포 속 *발전소*가', '조각나고 있다면?'] },
  { t0: 2.45, img: 'cell', head: ['에너지를 만드는 발전소,', '*미토콘드리아*'] },
  { t0: 6.8, img: 'network', head: ['건강할 땐', '길게 이어진 *그물 모양*'] },
  { t0: 9.85, img: 'fragment', head: ['영양이 끊기는 스트레스를 받으면', '*조각조각*'] },
  { t0: 12.95, img: 'er', head: ['단백질 공장, *소포체*도', '흐트러져요'] },
  { t0: 15.45, img: 'compare', head: ['리치 폴리페놀 *올리고놀*을', '넣었더니'] },
  { t0: 22.75, img: 'end', head: [] },
];
const IMG = {};
const sceneAt = t => { let i = 0; while (i + 1 < SC.length && t >= SC[i + 1].t0) i++; return i; };

function drawImg(c, im, cx, cy, w, a = 1, z = 1) {
  const h = w * im.height / im.width; c.globalAlpha = a;
  c.drawImage(im, cx - w * z / 2, cy - h * z / 2, w * z, h * z); c.globalAlpha = 1;
}
function fadeEdges(c) {   // blend the pictures' own dark margins into the background
  for (const [y0, y1] of [[0, 420], [H, H - 380]]) {
    const g = c.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, BG); g.addColorStop(1, 'rgba(5,8,17,0)');
    c.fillStyle = g; c.fillRect(0, Math.min(y0, y1), W, Math.abs(y1 - y0));
  }
}
function headline(c, lines, t, t0, y = 300) {
  const size = 74; c.font = `900 ${size}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
  lines.forEach((ln, i) => {
    const p = eo(seg(t, t0 + .1 + i * .18, t0 + .55 + i * .18)); if (p <= 0) return;
    const parts = ln.split('*'), widths = parts.map(s => c.measureText(s).width), tot = widths.reduce((a, b) => a + b, 0);
    let x = W / 2 - tot / 2; const yy = y + i * 98 + (1 - p) * 30;
    c.save(); c.globalAlpha = p; c.textAlign = 'left';
    parts.forEach((s, k) => {
      c.shadowColor = 'rgba(0,0,0,.75)'; c.shadowBlur = 24; c.fillStyle = k % 2 ? LIME : WHITE; c.fillText(s, x, yy); x += widths[k];
    });
    c.restore();
  });
}
function subtitle(c, t) {
  for (const [k, [a, b, txt]] of SUBS.entries()) {
    const nx = k + 1 < SUBS.length ? SUBS[k + 1][0] - .14 : 1e9, e = Math.min(b + .4, nx);
    const al = ss(seg(t, a - .12, a + .08)) * (1 - ss(seg(t, e - .12, e)));
    if (al <= 0) continue;
    c.save(); c.globalAlpha = al; c.font = `700 46px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle';
    const tw = c.measureText(txt).width, y = 1500;
    c.fillStyle = 'rgba(5,8,17,.62)'; roundRect(c, W / 2 - tw / 2 - 30, y - 42, tw + 60, 84, 18); c.fill();
    c.fillStyle = WHITE; c.fillText(txt, W / 2, y + 2); c.restore();
  }
}
function roundRect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function chip(c, txt, x, y, lime) {
  c.font = `700 36px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'middle'; const w = c.measureText(txt).width + 44;
  c.fillStyle = lime ? LIME : 'rgba(244,246,250,.14)'; roundRect(c, x, y - 30, w, 60, 30); c.fill();
  c.fillStyle = lime ? '#0B1020' : WHITE; c.fillText(txt, x + 22, y + 1);
}

// ---------- one scene's picture ----------
function picture(c, i, t) {
  const s = SC[i], lt = t - s.t0;
  c.fillStyle = BG; c.fillRect(0, 0, W, H);
  if (s.img === 'break') {
    // a push in; the threads snap (light pulses on each break)
    const z = 1.18 - .12 * eo(seg(lt, 0, 2.4)), sx = (hash(Math.floor(t * 24)) - .5) * 10 * Math.max(0, 1 - lt / .6);
    drawImg(c, IMG.break, W / 2 + sx, 980, W, 1, z);
    for (const k of [.35, .8, 1.25]) { const f = Math.max(0, 1 - Math.abs(lt - k) / .12); if (f > 0) { c.fillStyle = `rgba(255,150,60,${.16 * f})`; c.fillRect(0, 0, W, H); } }
  } else if (s.img === 'cell') {
    const z = 1.0 + .16 * ss(seg(lt, 0, 4.4)); drawImg(c, IMG.cell, W / 2 + 60 * ss(seg(lt, 0, 4.4)), 1000 - 80 * ss(seg(lt, 0, 4.4)), W, 1, z);
  } else if (s.img === 'network') {
    const z = 1.04 + .06 * lt / 3; drawImg(c, IMG.network, W / 2, 960, W, 1, z);
    c.globalCompositeOperation = 'lighter'; drawImg(c, IMG.network, W / 2, 960, W, .25 * (0.5 + .5 * Math.sin(lt * 3)), z); c.globalCompositeOperation = 'source-over';
  } else if (s.img === 'fragment') {
    // the network breaks into pieces: network → fragments, with a jolt on "조각조각"
    const k = eio(seg(lt, .2, 1.9)), j = Math.max(0, 1 - Math.abs(t - 11.75) / .18), sx = (hash(Math.floor(t * 30)) - .5) * 22 * j;
    drawImg(c, IMG.network, W / 2 + sx, 960, W, 1 - k, 1.1);
    drawImg(c, IMG.fragment, W / 2 + sx, 960, W, k, 1.1 + .04 * seg(lt, 0, 3));
  } else if (s.img === 'er') {
    const z = 1.05 + .07 * ss(seg(lt, 0, 2.6)); drawImg(c, IMG.er, W / 2 - 40 * ss(seg(lt, 0, 2.6)), 960, W, 1, z);
  } else if (s.img === 'end') {
    endCard(c, lt);
  }
}

// the comparison: stress only (top) / stress + Oligonol (bottom: the fragments ease back into the network)
function comparePanels(c, t, lt) {
  const open = eo(seg(lt, 0, .7)), heal = eio(seg(t, 20.9, 22.6));
  const box = (y, h) => { c.save(); roundRect(c, 50, y, W - 100, h, 24); c.clip(); };
  c.fillStyle = BG; c.fillRect(0, 0, W, H);
  c.globalAlpha = open;
  const Y1 = 420, Y2 = 930, BH = 480;
  box(Y1, BH); drawImg(c, IMG.fragment, W / 2, Y1 + BH / 2, W * .98, 1, 1); c.restore();
  box(Y2, BH); drawImg(c, IMG.fragment, W / 2, Y2 + BH / 2, W * .98, 1 - heal, 1); drawImg(c, IMG.network, W / 2, Y2 + BH / 2, W * .98, heal, 1); c.restore();
  c.lineWidth = 3;
  c.strokeStyle = 'rgba(244,246,250,.22)'; roundRect(c, 50, Y1, W - 100, BH, 24); c.stroke();
  c.strokeStyle = `rgba(180,236,45,${.3 + .6 * heal})`; roundRect(c, 50, Y2, W - 100, BH, 24); c.stroke();
  chip(c, '스트레스만', 80, Y1 + 50, false);
  chip(c, '스트레스 + 올리고놀', 80, Y2 + 50, true);
  c.globalAlpha = open * .75; c.font = `500 26px ${FONT}`; c.textAlign = 'right'; c.fillStyle = MUTE; c.fillText('이해를 돕기 위한 이미지', W - 60, Y2 + BH + 30);
  c.globalAlpha = 1;
}

function endCard(c, lt) {
  c.fillStyle = BG; c.fillRect(0, 0, W, H);
  const g = c.createRadialGradient(W / 2, 860, 0, W / 2, 860, 760); g.addColorStop(0, 'rgba(180,236,45,.16)'); g.addColorStop(1, 'rgba(180,236,45,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H);
  const p = eo(seg(lt, 0, .8)), im = IMG.package, w = 660, h = w * im.height / im.width, y = 380 + (1 - p) * 40;
  c.save(); c.globalAlpha = p; roundRect(c, W / 2 - w / 2, y, w, h, 28); c.clip(); c.drawImage(im, W / 2 - w / 2, y, w, h); c.restore();
  const a1 = eo(seg(lt, 1.6, 2.2)), a2 = eo(seg(lt, 3.4, 4)), a3 = eo(seg(lt, .4, 1));
  c.globalAlpha = a3; c.font = `700 36px ${FONT}`; chip(c, '세포 실험 결과', W / 2 - (c.measureText('세포 실험 결과').width + 44) / 2, 300, true); c.globalAlpha = 1;
  c.textAlign = 'center'; c.textBaseline = 'middle';
  c.globalAlpha = a1; c.font = `900 64px ${FONT}`; c.fillStyle = WHITE; c.fillText('리치 폴리페놀 올리고놀', W / 2, 1330); c.globalAlpha = 1;
  c.globalAlpha = a2; c.font = `900 64px ${FONT}`; c.fillStyle = LIME; c.fillText('젤리 스틱, 올리고파', W / 2, 1420); c.globalAlpha = 1;
  const a4 = eo(seg(lt, 1, 1.6));
  c.globalAlpha = a4; c.font = `500 28px ${FONT}`; c.fillStyle = MUTE;
  c.fillText('출처: ICNIM 2026 PB-5 · 오사카공립대학교', W / 2, 1530);
  c.fillText('※ 세포 실험 결과이며, 본 제품의 효과를 의미하지 않습니다.', W / 2, 1576);
  c.globalAlpha = 1;
}

function frame(c, i, t) {
  const s = SC[i];
  if (s.img === 'compare') comparePanels(c, t, t - s.t0); else picture(c, i, t);
  if (s.img !== 'end' && s.img !== 'compare') fadeEdges(c);
  if (s.head.length) headline(c, s.head, t, s.t0, s.img === 'compare' ? 250 : 300);
}

const BUF = document.createElement('canvas'); BUF.width = W; BUF.height = H; const bctx = BUF.getContext('2d');
const XF = .32;
function render(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  const i = sceneAt(t), s = SC[i], p = i ? seg(t, s.t0, s.t0 + XF) : 1;
  if (p < 1) {
    frame(ctx, i - 1, t); frame(bctx, i, t);
    ctx.globalAlpha = ss(p); const z = 1.04 - .04 * eo(p);
    ctx.drawImage(BUF, W / 2 - W * z / 2, H / 2 - H * z / 2, W * z, H * z); ctx.globalAlpha = 1;
  } else frame(ctx, i, t);
  if (SC[i].img !== 'end') subtitle(ctx, t);
  const f = 1 - ss(seg(t, 0, .25)); if (f > 0) { ctx.fillStyle = `rgba(5,8,17,${f})`; ctx.fillRect(0, 0, W, H); }
  const e = ss(seg(t, DUR - .5, DUR)); if (e > 0) { ctx.fillStyle = `rgba(5,8,17,${e})`; ctx.fillRect(0, 0, W, H); }
}
window.DUR = DUR; window.render = render;
window.EV = [
  ...[.35, .8, 1.25].map(t => ({ t, type: 'snap' })),
  ...SC.slice(1).map(s => ({ t: s.t0, type: 'whoosh' })),
  { t: 7.1, type: 'shimmer' }, { t: 11.75, type: 'shatter' }, { t: 13.2, type: 'drone_dip' },
  { t: 21.0, type: 'heal' }, { t: 26.4, type: 'chime' },
];
window.TEXTS = t => {
  const i = sceneAt(t), s = SC[i], out = [];
  s.head.forEach((ln, k) => out.push({ id: `h${i}_${k}`, text: ln.replace(/\*/g, ''), x0: 60, y0: 240 + k * 98, x1: W - 60, y1: 340 + k * 98 }));
  return out;
};
(async () => {
  const load = (k, src) => new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.src = src; });
  await Promise.all([['break', 'assets/01-break.png'], ['cell', 'assets/02-cell.png'], ['network', 'assets/03-network.png'], ['fragment', 'assets/04-fragment.png'], ['er', 'assets/05-er.png'], ['package', 'assets/package.jpg']].map(([k, s]) => load(k, s)));
  await Promise.all(['500 28px', '700 46px', '900 74px'].map(f => document.fonts.load(`${f} ${FONT}`, '세포발전소')));
  window.READY = true;
})();
