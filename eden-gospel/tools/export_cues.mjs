// Export cues for the sound design (world stroke times, events, text writes): node tools/export_cues.mjs  (LIB must point at the library)
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const LIB = process.env.LIB; if (!LIB) { console.error('set LIB to the library folder'); process.exit(2); }
const { openDemo, closeServer } = await import(path.join(LIB, 'core/render/page.mjs'));
const film = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { browser, page } = await openDemo(film, { w: 1080, h: 1920 });
const r = await page.evaluate(() => ({ strokes: window.STROKES, ev: window.EV, dur: window.DUR, txt: window.TXT }));
fs.writeFileSync(path.join(film, 'audio/cues.json'), JSON.stringify(r));
console.log('cues', r.strokes.length, 'strokes', r.ev.length, 'events');
await browser.close(); closeServer();
