#!/bin/sh
# Noto Serif JP (OFL), subset to the characters the film uses (cues.json + film.js) -> fonts/ + fonts.css
set -e
cd "$(dirname "$0")/.."
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
CH=$(python3 -c "
import re
s=open('cues.json',encoding='utf-8').read()+open('film.js',encoding='utf-8').read()
print(''.join(sorted(set(c for c in s if ord(c)>0x2e7f)))+'。、「」・（）')")
ENC=$(python3 -c "import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))" "$CH")
mkdir -p fonts; : > fonts.css; n=0
for W in 500 700; do
  CSS=$(curl -sS -A "$UA" "https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@$W&text=$ENC&display=block")
  for U in $(echo "$CSS" | grep -o 'https://[^)]*' | sort -u); do
    curl -sS -o fonts/jp$n.woff2 "$U"
    CSS=$(echo "$CSS" | sed "s#$U#fonts/jp$n.woff2#g"); n=$((n+1))
  done
  echo "$CSS" >> fonts.css
done
echo "font files $n, chars ${#CH}"
