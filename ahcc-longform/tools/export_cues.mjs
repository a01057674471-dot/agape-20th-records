// Export cues for the sound design (picture events and the film length): node tools/export_cues.mjs  (LIB must point at the library)
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const LIB = process.env.LIB; if (!LIB) { console.error('set LIB to the library folder'); process.exit(2); }
const { openDemo, closeServer } = await import(path.join(LIB, 'core/render/page.mjs'));
const film = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { browser, page } = await openDemo(film, { w: 1920, h: 1080 });
const r = await page.evaluate(() => ({ ev: window.EV, dur: window.DUR }));
fs.writeFileSync(path.join(film, 'audio/cues.json'), JSON.stringify(r));
console.log('cues', r.ev.length, 'events, dur', r.dur);
await browser.close(); closeServer();
