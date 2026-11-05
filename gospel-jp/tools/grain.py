# grain.png: a mid-grey texture (paper fibres + pigment granulation) laid over every frame with 'overlay'
import numpy as np
from PIL import Image, ImageFilter
W, H = 1920, 1080; rng = np.random.default_rng(9)
p = np.asarray(Image.open('paper.jpg').convert('L'), np.float32)
hp = p - np.asarray(Image.fromarray(p.astype(np.uint8)).filter(ImageFilter.GaussianBlur(18)), np.float32)
def blob(s):
    n = rng.standard_normal((H // s + 2, W // s + 2)).astype(np.float32)
    im = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W + 2 * s, H + 2 * s), Image.BICUBIC)
    return np.asarray(im, np.float32)[s:s + H, s:s + W] / 255 - .5
gran = rng.normal(0, 1, (H, W)).astype(np.float32)
gran = np.asarray(Image.fromarray(np.clip(gran * 40 + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7)), np.float32) - 128
g = 128 + hp * 2.2 + gran * .9 + blob(60) * 26 + blob(14) * 10
Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).save('grain.png')
