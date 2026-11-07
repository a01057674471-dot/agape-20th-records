"""AMJ (일본아가페선교회) reel, 9:16: blue picture-book art + a scrapbook collage of the mission's real photos,
timed to the recorded narration (audio/align.json). Photos stick onto painted boards one by one (taped prints),
handwritten tags, Korean subtitles; the map of Japan goes from a few lights at night to many at dawn.
No music or effects -- the narration only.  python3 compose.py out.mp4 [--preview]
"""
import os, sys, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
ART, PH = os.path.join(HERE, 'art'), os.path.join(HERE, 'photos')
W, H, FPS = 1080, 1920, 30
NAVY = (29, 52, 80); CORAL = (232, 87, 74); PAPER = (252, 250, 244); BLUE = (30, 94, 168)
FONT = lambda name, s: ImageFont.truetype(os.path.join(HERE, 'fonts', name), s)
JUA, PEN, GAEGU, GOWUN = 'Jua.ttf', 'NanumPen.ttf', 'Gaegu-Bold.ttf', 'GowunDodum.ttf'
END_HOLD = 6.0
sys.path.insert(0, os.path.join(HERE, 'art_src'))


def ease(u): u = min(max(u, 0.0), 1.0); return 1 - (1 - u) ** 3
def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)


# ---------------------------------------------------------------- printed photos, tape, tags
def cover(im, w, h, focus=(0.5, 0.45)):
    sw, sh = im.size
    s = max(w / sw, h / sh)
    im = im.resize((max(w, round(sw * s)), max(h, round(sh * s))), Image.LANCZOS)
    x0 = int((im.width - w) * focus[0]); y0 = int((im.height - h) * focus[1])
    return im.crop((x0, y0, x0 + w, y0 + h))


def tape(w, h, rng):
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    pts = [(0, rng.integers(0, 4))]
    for x in range(0, w + 1, 8): pts.append((x, rng.integers(0, 5)))
    for x in range(w, -1, -8): pts.append((x, h - rng.integers(0, 5)))
    d.polygon(pts, fill=(238, 228, 200, 185))
    return t


def print_photo(path, w, h, rot, seed, border=18, focus=(0.5, 0.45), tape_on=True):
    """a photo as a taped print: white border, soft drop shadow, a strip of masking tape, rotated"""
    rng = np.random.default_rng(seed)
    ph = cover(Image.open(path).convert('RGB'), w, h, focus)
    card = Image.new('RGBA', (w + 2 * border, h + 2 * border), PAPER + (255,))
    card.paste(ph, (border, border))
    pad = 60
    canvas = Image.new('RGBA', (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 10, pad + 16, pad + card.width + 6, pad + card.height + 14), fill=(20, 30, 50, 110))
    canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(12)))
    canvas.alpha_composite(card, (pad, pad))
    if tape_on:
        tw = int(min(220, card.width * 0.38))
        tp = tape(tw, 54, rng).rotate(float(rng.uniform(-8, 8)), expand=True, resample=Image.BICUBIC)
        canvas.alpha_composite(tp, (pad + card.width // 2 - tp.width // 2, pad - tp.height // 2 + 4))
    return canvas.rotate(rot, expand=True, resample=Image.BICUBIC)


def tag(text, size=54, font=GAEGU, colour=NAVY, bg=PAPER, rot=0.0, pad=(30, 16), seed=0):
    f = FONT(font, size)
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    lines = text.split('\n')
    tw = max(d0.textlength(l, font=f) for l in lines); lh = size * 1.18
    w, h = int(tw + pad[0] * 2), int(lh * len(lines) + pad[1] * 2)
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((26, 30, 20 + w + 6, 20 + h + 8), 14, fill=(20, 30, 50, 70))
    im = im.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), 14, fill=bg + (255,))
    for k, l in enumerate(lines):
        d.text((20 + w / 2, 20 + pad[1] + lh * k + lh / 2), l, font=f, fill=colour, anchor='mm')
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)


def text_img(text, size, font=JUA, colour=NAVY, stroke=0, stroke_col=PAPER, spacing=1.15):
    f = FONT(font, size)
    lines = text.split('\n')
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    tw = max(d0.textlength(l, font=f) for l in lines); lh = size * spacing
    im = Image.new('RGBA', (int(tw + 40 + stroke * 2), int(lh * len(lines) + 40)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, l in enumerate(lines):
        d.text((im.width / 2, 20 + lh * k + lh / 2), l, font=f, fill=colour, anchor='mm', stroke_width=stroke, stroke_fill=stroke_col)
    return im


# ---------------------------------------------------------------- items placed on a board
class Item:
    """an image placed with its centre at (x, y), appearing at t0 with a short 'stick on' settle"""
    def __init__(self, im, x, y, t0, kind='stick', t1=None):
        self.im, self.x, self.y, self.t0, self.kind, self.t1 = im, x, y, t0, kind, t1

    def draw(self, base, t):
        if t < self.t0: return
        u = (t - self.t0) / 0.32
        a = ease(u)
        if self.t1 is not None:
            a = min(a, 1 - smooth((t - self.t1) / 0.25))
            if a <= 0: return
        im = self.im
        if self.kind == 'stick' and u < 1:
            s = 1.08 - 0.08 * ease(u)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
            dy = -18 * (1 - ease(u))
        elif self.kind == 'pop' and u < 1:
            s = 0.7 + 0.3 * ease(u) + 0.05 * math.sin(min(u, 1) * math.pi)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
            dy = 0
        else:
            dy = 0
        if a < 1:
            im = im.copy(); im.putalpha(Image.eval(im.getchannel('A'), lambda v: int(v * a)))
        base.alpha_composite(im, (int(self.x - im.width / 2), int(self.y - im.height / 2 + dy)))


def subtitle(lines, y1=1560):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = FONT(JUA, 52); lh = 72
    bw = max(d.textlength(l, font=f) for l in lines) + 76
    y0 = y1 - lh * len(lines) - 36
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 30, fill=PAPER + (238,))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 18 + lh * k + lh / 2), l.replace('…', '...').replace('....', '...'), font=f, fill=NAVY, anchor='mm')
    return im


SUB_SPLIT = {2: ['크리스마스가 누구의 생일인지', '모르는 나라,'], 7: ['일본을 위해 함께', '예배하고 기도합니다.'],
             9: ['일본 현지에서', '선교사님들과 함께합니다.'], 12: ['선교사님들이', '복음을 전하고 있습니다.'],
             14: ['당신의 기도와 손길이', '필요합니다.'], 15: ['일본 선교,', '이제 당신 차례입니다.']}


# ---------------------------------------------------------------- the reel
def build(seg0, total):
    from common_amj import CITIES
    L = lambda i: seg0[i]
    scenes = []          # (t0, t1, board image name, [items], extra flags)
    P = lambda n: os.path.join(PH, n)
    # 1  the night map, "1%"
    it = [Item(text_img('일본의 그리스도인', 72, JUA, PAPER), 540, 210, L(0) + 0.1, 'pop'),
          Item(text_img('1%', 300, JUA, (242, 212, 136)), 420, 390, L(1) + 0.05, 'pop'),
          Item(text_img('도 안 됩니다', 76, JUA, PAPER), 760, 440, L(1) + 0.45, 'pop')]
    scenes.append((0.0, L(2), 'map_night.jpg', it, {}))
    # 2  Christmas street (subtitles carry the words)
    it = [Item(tag('누구의 생일?', 58, GAEGU, CORAL, rot=6), 790, 230, L(2) + 0.9, 'pop')]
    scenes.append((L(2), L(4), 'xmas.jpg', it, {}))
    # 3  2018: founded
    it = [Item(print_photo(P('f_speech.jpg'), 820, 546, -3, 1, focus=(0.5, 0.3)), 520, 560, L(4) + 0.05),
          Item(print_photo(P('f_group.jpg'), 820, 546, 3.5, 2, focus=(0.5, 0.4)), 560, 1130, L(4) + 0.6),
          Item(tag('2018. 1. 16\n일본아가페선교회 창립', 50, GAEGU, NAVY, rot=-4), 300, 850, L(5) + 0.2, 'pop'),
          Item(ImageOps.contain(Image.open(P('logo_blue.jpg')).convert('RGBA'), (300, 200)).rotate(5, expand=True, resample=Image.BICUBIC),
               860, 230, L(5) + 0.5, 'pop')]
    scenes.append((L(4), L(6), 'board_1.jpg', it, {}))
    # 4  every Monday evening
    it = [Item(print_photo(P('w_easter.jpg'), 800, 534, 2.5, 3), 540, 470, L(6) + 0.05),
          Item(print_photo(P('w_2025.jpg'), 760, 506, -3, 4), 520, 960, L(6) + 0.7),
          Item(print_photo(P('w_room.jpg'), 560, 316, 4, 5), 640, 1330, L(7) + 0.3),
          Item(tag('매주 월요일 저녁 7:30\n정기예배와 중보기도', 48, GAEGU, NAVY, rot=-5), 300, 1200, L(7) + 0.9, 'pop')]
    scenes.append((L(6), L(8), 'board_2.jpg', it, {}))
    # 5  finding and training; with the missionaries in Japan
    it = [Item(print_photo(P('w_praise.jpg'), 780, 520, -2.5, 6), 520, 430, L(8) + 0.05),
          Item(print_photo(P('t_ordination.jpg'), 600, 404, 3.5, 7, focus=(0.5, 0.3)), 640, 830, L(8) + 0.8),
          Item(tag('선교사 발굴과 훈련', 50, GAEGU, NAVY, rot=-3), 290, 700, L(8) + 1.2, 'pop'),
          Item(print_photo(P('r_aso.jpg'), 820, 546, -2, 8, focus=(0.5, 0.6)), 540, 1170, L(9) + 0.05),
          Item(tag('일본 현지 선교사 수양회', 48, GAEGU, NAVY, rot=3), 740, 930, L(9) + 0.7, 'pop')]
    scenes.append((L(8), L(10), 'board_3.jpg', it, {}))
    # 6  city names light up on the night map
    names = ['도쿄', '후쿠오카', '교토', '고베', '아키타']
    d = (L(11) - L(10)) * 0.8
    it = []
    for k, nm in enumerate(names):
        x, y = CITIES[nm]
        t = L(10) + 0.1 + d * k / len(names)
        glow = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((40, 40, 120, 120), fill=(242, 212, 136, 150)); glow = glow.filter(ImageFilter.GaussianBlur(14))
        ImageDraw.Draw(glow).ellipse((68, 68, 92, 92), fill=(231, 179, 76, 255))
        it.append(Item(glow, x, y, t, 'pop'))
        tx = x + (140 if nm in ('도쿄', '아키타') else -20 if nm == '후쿠오카' else -130 if nm == '고베' else 0)
        ty = y + (110 if nm in ('후쿠오카', '고베') else -90 if nm == '교토' else 0)
        it.append(Item(tag(nm, 48, GAEGU, NAVY, rot=float(np.random.default_rng(k).uniform(-5, 5))), tx, ty, t + 0.05, 'pop'))
    scenes.append((L(10), L(11), 'map_night.jpg', it, {}))
    # 7  the missionary families: 13 prints, one after another
    it = []
    cols = [(200, 0), (540, 0), (880, 0)]
    pos = []
    for r_ in range(4):
        for c in range(3):
            pos.append((200 + c * 340 + (20 if r_ % 2 else -20), 330 + r_ * 300))
    order = list(range(13))
    span = (L(13) - L(11)) * 0.72
    for k in order:
        x, y = pos[k] if k < 12 else (540, 780)
        rot = float(np.random.default_rng(40 + k).uniform(-6, 6))
        it.append(Item(print_photo(P(f'm{k + 1:02d}.jpg'), 270, 270, rot, 40 + k, border=12, tape_on=k % 3 == 0), x, y,
                       L(11) + span * k / 13))
    it.append(Item(tag('일본 곳곳의 선교사님들', 52, GAEGU, PAPER, bg=BLUE, rot=-3), 540, 130, L(11) + 0.2, 'pop'))
    scenes.append((L(11), L(13), 'board_1.jpg', it, {}))
    # 8  dawn: lights everywhere -- your prayer and your hands
    it = [Item(tag('기도', 64, GAEGU, CORAL, rot=-6), 250, 240, L(14) + 0.1, 'pop'),
          Item(tag('후원', 64, GAEGU, CORAL, rot=4), 540, 200, L(14) + 0.45, 'pop'),
          Item(tag('동역', 64, GAEGU, CORAL, rot=-3), 830, 250, L(14) + 0.8, 'pop')]
    scenes.append((L(13), L(15), 'map_dawn.jpg', it, {'from': 'map_night.jpg'}))
    # 9  your turn: a scattered wall of photos and the big handwriting
    picks = [('w_2023.jpg', 230, 380, -7), ('m05.jpg', 820, 330, 6), ('w_may.jpg', 300, 1250, 5), ('m10.jpg', 840, 1300, -5),
             ('r_aso.jpg', 760, 760, 4), ('m03.jpg', 220, 820, -4)]
    it = []
    for k, (n, x, y, r) in enumerate(picks):
        sq = n.startswith('m')
        it.append(Item(print_photo(P(n), 320 if sq else 440, 320 if sq else 294, r, 70 + k, border=12), x, y, L(15) - 0.05 + 0.08 * k))
    it.append(Item(tag('일본 선교,\n이제 당신 차례!', 100, PEN.replace('NanumPen', 'Gaegu-Bold') if False else GAEGU, CORAL, rot=-3,
                       pad=(50, 26)), 540, 860, L(15) + 0.4, 'pop'))
    scenes.append((L(15), seg0[-1], 'board_2.jpg', it, {}))
    # 10 end card
    it = [Item(ImageOps.contain(Image.open(P('logo_blue.jpg')).convert('RGBA'), (460, 320)), 540, 330, seg0[-1] + 0.1, 'pop')]
    info = [('Agape Mission for Japan', 46, JUA, NAVY, 590),
            ('매주 월요일 오후 7:30 정기예배', 50, JUA, NAVY, 720), ('사랑의교회 9층 브라질예배실', 44, GOWUN, NAVY, 790),
            ('후원계좌', 44, JUA, CORAL, 920), ('국민은행 596401-01-331197', 60, JUA, NAVY, 1000),
            ('예금주 일본아가페선교회', 42, GOWUN, NAVY, 1070),
            ('미션펀드 정기후원', 44, JUA, CORAL, 1190), ('go.missionfund.org/agapemissionforjapan', 36, GOWUN, NAVY, 1255),
            ('amj.or.kr', 56, JUA, BLUE, 1380)]
    card = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((70, 140, 1010, 1470), 44, fill=PAPER + (246,))
    for (txt, s, fnt, col, y) in info:
        cd.text((540, y), txt, font=FONT(fnt, s), fill=col, anchor='mm')
    cd.line((200, 860, 880, 860), fill=(185, 210, 234), width=3); cd.line((200, 1130, 880, 1130), fill=(185, 210, 234), width=3)
    it = [Item(card, 540, 960, seg0[-1] + 0.05, 'fade')] + it
    scenes.append((seg0[-1], total, 'board_3.jpg', it, {'end': True}))
    return scenes


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv
    al = json.load(open(os.path.join(HERE, 'audio', 'align.json')))
    segs = al['segs']
    seg0 = [0.0] + [s[1] for s in segs[:-1]] + [al['total']]
    total = al['total'] + END_HOLD
    scenes = build(seg0, total)
    boards = {}
    def board(n):
        if n not in boards: boards[n] = Image.open(os.path.join(ART, n)).convert('RGBA')
        return boards[n]
    subs = {i: subtitle(SUB_SPLIT.get(i, [LINES[i]])) for i in range(len(LINES))}
    subs_hi = {i: subtitle(SUB_SPLIT.get(i, [LINES[i]]), 1330) for i in (2, 3)}     # above the two people in the street
    XF = 0.3

    def render_scene(k, t):
        t0, t1, bn, items, fl = scenes[k]
        im = board(bn).copy()
        if 'from' in fl:                                 # night -> dawn over the first 1.2 s
            a = smooth((t - t0) / 1.2)
            if a < 1: im = Image.blend(board(fl['from']), im, a)
        for itm in items: itm.draw(im, t)
        return im

    nfr = int(total * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-shortest', '-movflags', '+faststart', out]
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if preview: os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    for fi in range(nfr):
        t = fi / FPS
        if preview and fi % 15: continue
        k = max(i for i, s in enumerate(scenes) if s[0] <= t + 1e-6)
        im = render_scene(k, t)
        if k > 0 and t - scenes[k][0] < XF and 'from' not in scenes[k][4]:
            im = Image.blend(render_scene(k - 1, t), im, smooth((t - scenes[k][0]) / XF))
        if t < seg0[-1]:
            i = max(i for i in range(len(LINES)) if seg0[i] <= t + 1e-6)
            im.alpha_composite(subs_hi[i] if scenes[k][2] == 'xmas.jpg' and i in subs_hi else subs[i])
        rgb = im.convert('RGB')
        if preview: rgb.resize((360, 640)).save(os.path.join(HERE, 'preview', f'{fi:05d}.jpg'), quality=80)
        else: proc.stdin.write(rgb.tobytes())
    if proc: proc.stdin.close(); proc.wait()
    print('done', out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
