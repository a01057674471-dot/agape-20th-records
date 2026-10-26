# subtitles from the film's own handwriting timeline (audio/cues.json → subs.json), then srt.py writes the .srt
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); c = json.load(open(os.path.join(D, '../audio/cues.json'), encoding='utf-8'))
cues = [{'t0': x['t0'], 't1': x['t1'], 'text': x['text']} for x in c['txt']]
json.dump(cues, open(os.path.join(D, '../subs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('subs.json', len(cues))
