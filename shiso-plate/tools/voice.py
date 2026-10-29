# Narration: the user's recording (voices/source.mp3, 26.1 s) cut at its pauses into the script's phrases and laid
# on the film's timeline so each phrase lands with its plate. Boundaries from silencedetect. → voices/narration.wav
# run: python3 tools/voice.py
import os, subprocess, numpy as np, wave
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, 'voices', 'source.mp3'); SR = 48000; DUR = 30.0
# (source start, source end, film time, text)
P = [
  (0.00, 1.80, 0.20, '둘 중, 깻잎은 뭘까요?'),
  (1.90, 2.95, 2.60, '이건 자소예요.'),
  (3.15, 5.20, 4.05, '일본 식탁에 늘 오르는 잎이죠.'),
  (5.45, 6.50, 6.20, '초밥 옆 그 잎,'),
  (6.65, 8.62, 7.35, '우메보시의 붉은색도 자소랍니다.'),
  (8.98, 12.00, 9.75, '자소잎에는 로즈마린산과 루테올린이 들어 있어요.'),
  (12.38, 14.08, 13.25, '일본에선 면역 반응의 균형,'),
  (14.30, 16.10, 15.05, 'TNF 조절 작용이 연구됐어요.'),
  (16.22, 17.30, 16.95, '생쥐 실험에서요.'),
  (17.32, 21.12, 18.55, '주스로, 밥에, 샐러드로. 일본 식탁의 단골 잎이에요.'),
  (21.16, 23.12, 22.75, '이제 깻잎과 헷갈리지 마세요.'),
  (23.33, 26.15, 24.80, '몰랐던 건강 소재, 팔로우하고 더 알아가요.'),
]
out = np.zeros(int(DUR * SR), np.float32); prev = 0
for a, b, at, text in P:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-to', str(b), '-i', SRC, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; k = int(.01 * SR); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k)
    i = int(at * SR); assert at >= prev - 1e-6, f'overlap at {text}'; out[i:i + len(x)] += x[:len(out) - i]; prev = at + len(x) / SR
    print(f'{at:6.2f}–{prev:6.2f}  {text}')
with wave.open(os.path.join(HERE, 'voices', 'narration.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
