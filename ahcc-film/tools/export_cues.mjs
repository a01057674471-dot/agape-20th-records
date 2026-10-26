// Export cues for the sound design (world stroke times, events, text writes): node tools/export_cues.mjs  (LIB must point at the library)
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const LIB = process.env.LIB; if (!LIB) { console.error('set LIB to the library folder'); process.exit(2); }
const { openDemo, closeServer } = await import(path.join(LIB, 'core/render/page.mjs'));
const film = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { browser, page } = await openDemo(film, { w: 1080, h: 1920 });
const r = await page.evaluate(() => ({ ev: window.EV, dur: window.DUR, lines: window.LINES.map(l => ({ id: l.id, t0: l.t0, t1: l.t1, d: l.d })), subs: window.SUBS }));
fs.writeFileSync(path.join(film, 'audio/cues.json'), JSON.stringify(r));
console.log('cues', r.ev.length, 'events, dur', r.dur);
await browser.close(); closeServer();
