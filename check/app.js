/* Every Shade monthly skin check.
   Everything stays on this device. No analytics, no uploads, no image analysis.
   Storage: IndexedDB (checks, photos, spots, settings) with an in-memory fallback. */
(function () {
'use strict';

var TOOL_URL = 'https://zainjaffar06.github.io/everyshade/check/';
var AREA_COUNT = 10;

/* ---------- small helpers ---------- */
function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
function pad(n) { return (n < 10 ? '0' : '') + n; }
function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
function monthId(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1); }
function monthLabel(id) { var p = id.split('-'); return new Date(+p[0], +p[1] - 1, 1).toLocaleDateString(undefined, { month: 'long', year: 'numeric' }); }
function dateLabel(iso) {
  var d, m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  d = m ? new Date(+m[1], +m[2] - 1, +m[3]) : new Date(iso);   /* plain dates are local, not UTC */
  if (isNaN(d)) return ''; return d.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
}
function todayISO() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
function prevMonthId(id) { var p = id.split('-'); var y = +p[0], m = +p[1] - 1; if (m === 0) { m = 12; y--; } return y + '-' + pad(m); }
function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function lsSet(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
function download(blob, name) {
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = name; a.style.display = 'none';
  document.body.appendChild(a); a.click();
  setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
}

/* ---------- storage ---------- */
var DB_NAME = 'everyshade-check', DB_VER = 1;
var KEYS = { checks: 'month', photos: 'key', spots: 'id', settings: 'key' };
var db = null, storageOK = true, storageMsg = '';
var mem = { checks: {}, photos: {}, spots: {}, settings: {} };

function setStorageProblem(msg) {
  storageOK = false; storageMsg = msg;
  var b = $('#storageBanner'); $('#storageMsg').textContent = msg; b.classList.add('show');
}
function openDB() {
  return new Promise(function (resolve) {
    var idb; try { idb = window.indexedDB; } catch (e) { idb = null; }
    if (!idb) { setStorageProblem('This browser is not letting the page save anything on this device (this happens in private or incognito mode). You can still do the check, but progress, notes, and photos will be gone when you close this tab.'); return resolve(null); }
    var req, done = false;
    function finish(d) { if (done) return; done = true; resolve(d); }
    try { req = idb.open(DB_NAME, DB_VER); } catch (e) { setStorageProblem('Saving is blocked in this browser mode. You can still do the check, but nothing will be kept after you close this tab.'); return finish(null); }
    req.onupgradeneeded = function (e) {
      var d = e.target.result;
      ['checks', 'photos', 'spots', 'settings'].forEach(function (s) { if (!d.objectStoreNames.contains(s)) d.createObjectStore(s, { keyPath: KEYS[s] }); });
    };
    req.onsuccess = function (e) { db = e.target.result; db.onversionchange = function () { db.close(); db = null; }; finish(db); };
    req.onerror = function () { setStorageProblem('Saving is blocked in this browser mode (often private browsing). You can still do the check, but nothing will be kept after you close this tab.'); finish(null); };
    req.onblocked = function () { setStorageProblem('Another tab is using the saved data. Close other copies of this page and reload.'); finish(null); };
    setTimeout(function () { if (!done) { setStorageProblem('Saved data could not be opened in time. You can still do the check, but it may not be saved.'); finish(null); } }, 5000);
  });
}
function reqP(r) { return new Promise(function (res, rej) { r.onsuccess = function () { res(r.result); }; r.onerror = function () { rej(r.error); }; }); }
var store = {
  get: function (s, key) { if (!db) return Promise.resolve(mem[s][key]); return reqP(db.transaction(s).objectStore(s).get(key)); },
  all: function (s) { if (!db) return Promise.resolve(Object.keys(mem[s]).map(function (k) { return mem[s][k]; })); return reqP(db.transaction(s).objectStore(s).getAll()); },
  put: function (s, val) {
    if (!db) { mem[s][val[KEYS[s]]] = val; return Promise.resolve(); }
    return reqP(db.transaction(s, 'readwrite').objectStore(s).put(val)).catch(function (err) {
      var full = err && /quota/i.test(err.name || '');
      setStorageProblem(full ? 'This device is out of storage space, so the last change could not be saved. Try removing a photo, or export and delete old data.' : 'The last change could not be saved. This browser may be blocking storage.');
      throw err;
    });
  },
  del: function (s, key) { if (!db) { delete mem[s][key]; return Promise.resolve(); } return reqP(db.transaction(s, 'readwrite').objectStore(s)['delete'](key)); },
  clear: function (s) { if (!db) { mem[s] = {}; return Promise.resolve(); } return reqP(db.transaction(s, 'readwrite').objectStore(s).clear()); }
};
function getSetting(k, def) { return store.get('settings', k).then(function (r) { return r ? r.value : def; }); }
function setSetting(k, v) { return store.put('settings', { key: k, value: v }); }

/* ---------- object URLs (photos) ---------- */
var urlCache = {};
function photoURL(key, blob) {
  if (!urlCache[key]) urlCache[key] = URL.createObjectURL(blob);
  return urlCache[key];
}
function dropURL(key) { if (urlCache[key]) { URL.revokeObjectURL(urlCache[key]); delete urlCache[key]; } }

/* Downscale to keep storage small. Falls back to the original file if decoding fails (for example HEIC). */
function processImage(file) {
  return new Promise(function (resolve) {
    var url;
    try { url = URL.createObjectURL(file); } catch (e) { return resolve(file); }
    var img = new Image();
    img.onload = function () {
      try {
        var max = 1400, w = img.naturalWidth, h = img.naturalHeight;
        var scale = Math.min(1, max / Math.max(w, h));
        var c = document.createElement('canvas');
        c.width = Math.round(w * scale); c.height = Math.round(h * scale);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        c.toBlob(function (b) { URL.revokeObjectURL(url); resolve(b || file); }, 'image/jpeg', 0.85);
      } catch (e) { URL.revokeObjectURL(url); resolve(file); }
    };
    img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
    img.src = url;
  });
}

/* ---------- content ---------- */
var GENERAL_SIGNS = [
  'A spot that is new, or that you do not remember.',
  'A spot that has changed in size, shape, color, or how it feels.',
  'A sore that bleeds, crusts, or does not heal in about three weeks.',
  'A spot that itches or hurts.',
  'A spot that looks different from all your other spots. Doctors call this the "ugly duckling."',
  'A bump that is shiny, whether it is pink, brown, or black.'
];
var ABCDE = [
  ['A', 'Asymmetry', 'one half does not match the other.'],
  ['B', 'Border', 'edges are ragged, blurry, or uneven.'],
  ['C', 'Color', 'more than one color, or an uneven mix of brown, black, tan, pink, red, white, or blue.'],
  ['D', 'Diameter', 'bigger than a pencil eraser (about 6 mm), though it can be smaller.'],
  ['E', 'Evolving', 'changing in size, shape, color, or how it feels.']
];
var TONE_NOTE = 'On brown and Black skin, a melanoma may be dark brown, black, or even pink, red, or purple. A basal cell cancer may look like a shiny brown or black bump rather than a pink, pearly one. The place matters too: palms, soles, between the toes, and under the nails are the sites most often missed.';
var NAIL_LOOK = 'A new dark line (brown or black) running from the base of the nail to the tip. See a doctor if the line is new, if it gets wider or darker, if it bleeds, if the nail cracks or lifts, or if the skin next to the nail turns dark. Many people with darker skin have harmless dark lines, often on several nails. A line that is new, on just one nail, or changing is the one to have checked.';

var STEPS = [
  { id: 'ready', title: 'Get ready', info: true,
    where: 'Find a room with bright light. A bathroom with a full-length mirror and a hand mirror works well.',
    how: ['Take off glasses, jewelry, and nail polish if you can.', 'Ask a family member or friend to help with your back and scalp.', 'Go slowly. The whole check takes about ten minutes.', 'Tick each area as you finish it. You can stop and come back later; your progress is saved on this device.'],
    look: 'You are learning what your skin normally looks like. Most spots are harmless. The goal is to notice anything new or changing, and to have a doctor look at it.' },
  { id: 'face', title: 'Face, ears, and neck', map: 'front', regions: ['head', 'neck'],
    where: 'Your whole face, nose, lips, around the eyes, both ears (front, back, and the rim), and your neck.',
    how: ['Use the big mirror.', 'Use the hand mirror to see behind your ears.', 'Lift your chin to see under your jaw.'],
    look: 'A new or changing spot, a sore that does not heal, or a shiny bump. On brown and Black skin that bump may be brown or black rather than pink.' },
  { id: 'scalp', title: 'Scalp', map: 'back', regions: ['head'],
    where: 'Your whole scalp, the part in your hair, and the hairline.',
    how: ['Use a comb, or a hair dryer on the cool setting, to part your hair in rows.', 'A helper makes this much easier.', 'Hairdressers and barbers notice spots too. You can ask them to tell you.'],
    look: 'A sore that does not heal, a new bump, or a dark or changing spot.' },
  { id: 'torso', title: 'Chest and belly', map: 'front', regions: ['torso'],
    where: 'Chest, breasts, the skin under the breasts, the belly, the belly button, and any skin folds.',
    how: ['Lift the breasts and skin folds to see underneath.', 'Use the hand mirror if needed.'],
    look: 'A new or changing spot, a sore that does not heal, or a spot that looks different from the rest.' },
  { id: 'arms', title: 'Arms, armpits, and tops of hands', map: 'front', regions: ['arm-l', 'arm-r', 'hand-l', 'hand-r'],
    where: 'Shoulders, both sides of each arm, elbows, armpits, wrists, and the backs of the hands.',
    how: ['Raise each arm and look in the armpit with the mirror.', 'Bend the elbow to see both sides of the arm.'],
    look: 'A new or changing spot, a scaly patch, or a sore that does not heal.' },
  { id: 'palms', title: 'Palms and between the fingers', map: 'palm',
    where: 'Both palms, each finger, and the skin between the fingers.',
    how: ['Spread your fingers wide.', 'Turn each hand over slowly in good light.'],
    look: 'This is a place where melanoma is often missed, especially on darker skin. Look for a new or changing dark spot, a dark patch with uneven edges, or a sore or bump that does not heal. On brown or Black skin, a melanoma here may be dark brown or black, but it can also be pink, red, or purple.',
    missed: true },
  { id: 'fingernails', title: 'Fingernails', map: 'nail',
    where: 'All ten fingernails and the skin around them.',
    how: ['Take off nail polish.', 'Hold each nail up to the light.'],
    look: NAIL_LOOK, missed: true },
  { id: 'back', title: 'Back, shoulders, and buttocks', map: 'back', regions: ['torso', 'buttocks', 'neck'],
    where: 'Back of the neck, shoulders, upper and lower back, and buttocks.',
    how: ['Stand with your back to the big mirror and hold the hand mirror in front of you.', 'Or ask a helper to look, or to take a photo for you.'],
    look: 'A new or changing spot, or one that looks different from the rest. Many people never see their own back; a helper or a photo makes a real difference.' },
  { id: 'legs', title: 'Legs, front and back', map: 'front', regions: ['leg-l', 'leg-r'],
    where: 'Thighs, knees, shins, calves, the backs of the knees, the groin, and the skin between the legs.',
    how: ['Sit down.', 'Use the hand mirror for the backs of the legs and the groin.'],
    look: 'A new or changing spot, a sore that does not heal, or a scaly patch. On darker skin, squamous cell cancer can show up on the legs, or in an old scar or burn, as a sore or growth that does not heal.' },
  { id: 'feet', title: 'Feet: tops, soles, and between the toes', map: 'sole',
    where: 'The tops of both feet, the soles, the heels, and the skin between every toe.',
    how: ['Sit down and rest one foot on the other knee.', 'Use the hand mirror for the soles.', 'Spread the toes apart to see between them.'],
    look: 'Another place melanoma is often missed. Look for a new or changing dark spot, a sore that does not heal, or a growth. On brown or Black skin it may be dark brown or black, but it can also be pink, red, or purple, or look like a wart or blister that does not go away.',
    missed: true },
  { id: 'toenails', title: 'Toenails', map: 'nail', toe: true,
    where: 'All ten toenails and the skin around them.',
    how: ['Take off nail polish.', 'Toenails are the hardest to see. Take your time, or ask a helper to look.'],
    look: NAIL_LOOK, missed: true },
  { id: 'finish', title: 'Finish', finish: true }
];
var AREA_STEPS = STEPS.filter(function (s) { return !s.info && !s.finish; });

/* ---------- body maps (inline SVG, drawn here) ---------- */
function mirror(pts) { return pts.map(function (p) { return [200 - p[0], p[1]]; }); }
function poly(pts) { return pts.map(function (p) { return p.join(','); }).join(' '); }
var FIG = {
  neck: [[88, 72], [112, 72], [114, 92], [86, 92]],
  torso: [[56, 92], [144, 92], [158, 100], [160, 118], [152, 236], [48, 236], [40, 118], [42, 100]],
  back: [[56, 92], [144, 92], [158, 100], [160, 118], [154, 200], [46, 200], [40, 118], [42, 100]],
  buttocks: [[46, 200], [154, 200], [152, 236], [48, 236]],
  armL: [[36, 100], [56, 100], [48, 172], [32, 234], [12, 230], [24, 170]],
  handL: [[10, 230], [32, 234], [34, 264], [26, 278], [8, 278], [0, 264]],
  legL: [[48, 236], [99, 236], [96, 330], [92, 408], [60, 408], [52, 330]],
  footL: [[58, 408], [94, 408], [98, 430], [52, 430]]
};
function bodyRegions(side) {
  var front = side === 'front';
  var r = [];
  r.push({ id: 'arm-l', label: front ? 'Right arm' : 'Back of right arm', pts: FIG.armL });
  r.push({ id: 'arm-r', label: front ? 'Left arm' : 'Back of left arm', pts: mirror(FIG.armL) });
  r.push({ id: 'hand-l', label: front ? 'Back of right hand' : 'Right hand', pts: FIG.handL });
  r.push({ id: 'hand-r', label: front ? 'Back of left hand' : 'Left hand', pts: mirror(FIG.handL) });
  r.push({ id: 'leg-l', label: front ? 'Right leg' : 'Back of right leg', pts: FIG.legL });
  r.push({ id: 'leg-r', label: front ? 'Left leg' : 'Back of left leg', pts: mirror(FIG.legL) });
  r.push({ id: 'foot-l', label: front ? 'Top of right foot' : 'Right heel', pts: FIG.footL });
  r.push({ id: 'foot-r', label: front ? 'Top of left foot' : 'Left heel', pts: mirror(FIG.footL) });
  if (front) r.push({ id: 'torso', label: 'Chest and belly', pts: FIG.torso });
  else { r.push({ id: 'torso', label: 'Back', pts: FIG.back }); r.push({ id: 'buttocks', label: 'Buttocks', pts: FIG.buttocks }); }
  r.push({ id: 'neck', label: front ? 'Neck' : 'Back of neck', pts: FIG.neck });
  r.push({ id: 'head', label: front ? 'Face' : 'Back of head and scalp', ellipse: [100, 42, 28, 34] });
  return r;
}
var MAPS = {
  front: { vb: '0 0 200 440', title: 'Front of the body', regions: function () { return bodyRegions('front'); } },
  back: { vb: '0 0 200 440', title: 'Back of the body', regions: function () { return bodyRegions('back'); } },
  palm: { vb: '0 0 200 250', title: 'Palm of the hand, fingers spread', regions: function () {
    return [
      { id: 'thumb', label: 'Thumb', rect: [44, 114, 26, 84, 13, 'rotate(40 57 114)'] },
      { id: 'index', label: 'Index finger', rect: [60, 30, 22, 90, 11] },
      { id: 'middle', label: 'Middle finger', rect: [88, 18, 22, 102, 11] },
      { id: 'ring', label: 'Ring finger', rect: [116, 28, 22, 92, 11] },
      { id: 'pinky', label: 'Little finger', rect: [142, 52, 20, 70, 10] },
      { id: 'palm', label: 'Palm', pts: [[58, 112], [164, 112], [166, 200], [142, 244], [76, 244], [52, 200]] }
    ]; } },
  sole: { vb: '0 0 200 300', title: 'Sole of the foot, with toes', regions: function () {
    return [
      { id: 'bigtoe', label: 'Big toe', ellipse: [146, 42, 22, 24] },
      { id: 'toe2', label: 'Second toe', ellipse: [112, 34, 13, 16] },
      { id: 'toe3', label: 'Third toe', ellipse: [86, 40, 12, 15] },
      { id: 'toe4', label: 'Fourth toe', ellipse: [64, 50, 11, 14] },
      { id: 'toe5', label: 'Little toe', ellipse: [46, 64, 10, 13] },
      { id: 'sole', label: 'Sole', path: 'M48 78 C30 95 40 150 56 185 C64 215 46 250 70 278 C95 300 150 292 160 255 C168 220 152 190 158 150 C163 118 172 90 168 72 C150 62 120 70 100 70 C80 70 62 66 48 78 Z' },
      { id: 'heel', label: 'Heel', ellipse: [112, 258, 34, 24] }
    ]; } },
  nail: { vb: '0 0 200 170', title: 'Fingertip with the nail, showing a dark line', regions: function () {
    return [
      { id: 'skin', label: 'Skin around the nail', rect: [36, 14, 128, 150, 56] },
      { id: 'nail', label: 'Nail', rect: [68, 34, 64, 78, 24], cls: 'nail-plate' }
    ]; }, extra: '<rect class="nail-band" x="95" y="34" width="9" height="78" rx="2" pointer-events="none"/>' }
};
function mapSVG(mapName, opts) {
  opts = opts || {};
  var m = MAPS[mapName]; var regs = m.regions();
  var hi = opts.highlight || [];
  var out = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + m.vb + '" ' + (opts.interactive ? 'role="group" aria-label="' + esc(m.title) + '. Pick an area."' : 'role="img" aria-label="' + esc(opts.alt || m.title) + '"') + ' data-map="' + mapName + '">';
  regs.forEach(function (r) {
    var cls = 'region' + (hi.length ? (hi.indexOf(r.id) >= 0 ? ' hi' : ' dim') : '') + (opts.interactive ? ' tap' : '') + (r.cls ? ' ' + r.cls : '');
    var attrs = ' class="' + cls + '" data-region="' + r.id + '" data-label="' + esc(r.label) + '"';
    if (opts.interactive) attrs += ' tabindex="0" role="button" aria-label="' + esc(r.label) + '"';
    if (r.ellipse) out += '<ellipse' + attrs + ' cx="' + r.ellipse[0] + '" cy="' + r.ellipse[1] + '" rx="' + r.ellipse[2] + '" ry="' + r.ellipse[3] + '"/>';
    else if (r.rect) out += '<rect' + attrs + ' x="' + r.rect[0] + '" y="' + r.rect[1] + '" width="' + r.rect[2] + '" height="' + r.rect[3] + '" rx="' + r.rect[4] + '"' + (r.rect[5] ? ' transform="' + r.rect[5] + '"' : '') + '/>';
    else if (r.path) out += '<path' + attrs + ' d="' + r.path + '"/>';
    else out += '<polygon' + attrs + ' points="' + poly(r.pts) + '"/>';
  });
  if (m.extra) out += m.extra;
  if (opts.pins) {
    out += '<g aria-hidden="true">';
    opts.pins.forEach(function (p) {
      out += '<circle class="pin" cx="' + p.x + '" cy="' + p.y + '" r="10"/><text class="pin-label" x="' + p.x + '" y="' + p.y + '">' + p.n + '</text>';
    });
    out += '</g>';
  }
  return out + '</svg>';
}
function svgPoint(svg, evt) {
  var pt = svg.createSVGPoint(); pt.x = evt.clientX; pt.y = evt.clientY;
  var ctm = svg.getScreenCTM(); if (!ctm) return null;
  return pt.matrixTransform(ctm.inverse());
}

/* ---------- views ---------- */
var VIEWS = ['home', 'check', 'spots', 'history', 'settings'];
var currentView = '';
function showView(name, focusHeading) {
  if (VIEWS.indexOf(name) < 0) name = 'home';
  VIEWS.forEach(function (v) { $('#view-' + v).classList.toggle('active', v === name); });
  $$('nav.tabs a').forEach(function (a) { if (a.dataset.view === name) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  var changed = currentView !== name; currentView = name;
  var render = { home: renderHome, check: renderCheck, spots: renderSpots, history: renderHistory, settings: renderSettings }[name];
  Promise.resolve(render()).then(function () {
    if (changed) { window.scrollTo(0, 0); if (focusHeading !== false) { var h = $('#view-' + name + ' [tabindex="-1"]'); if (h) h.focus({ preventScroll: true }); } }
  });
}
function route() { showView((location.hash || '#home').slice(1)); }

/* ---------- checks ---------- */
var stepIndex = 0;
function loadCheck(month) {
  return store.get('checks', month).then(function (c) { return c || null; });
}
function newCheck(month) { return { month: month, started: new Date().toISOString(), completed: null, steps: {} }; }
function areasDone(c) { return c ? AREA_STEPS.filter(function (s) { return c.steps[s.id]; }).length : 0; }
function sentenceStatus(c) {
  if (!c) return 'You have not started this month\'s check yet. It takes about ten minutes.';
  if (c.completed) return 'You finished ' + monthLabel(c.month) + '\'s check on ' + dateLabel(c.completed) + '. You can look back through it any time.';
  var n = areasDone(c);
  return n === 0 ? 'You started this month\'s check but have not ticked any areas yet.' : 'You have checked ' + n + ' of ' + AREA_COUNT + ' areas this month. You can pick up where you left off.';
}
function streakSentence(checks) {
  var done = {}; checks.forEach(function (c) { if (c.completed) done[c.month] = true; });
  var m = monthId(); var n = 0;
  if (!done[m]) m = prevMonthId(m);
  while (done[m]) { n++; m = prevMonthId(m); }
  if (n === 0) return 'No completed checks yet. Finishing this month\'s check will start your record.';
  if (n === 1) return 'You have completed one month. Keep going next month to build the habit.';
  return 'You have completed ' + n + ' months in a row. Well done.';
}

function renderHome() {
  var month = monthId();
  return Promise.all([loadCheck(month), store.all('checks')]).then(function (res) {
    var c = res[0];
    $('#homeStatusText').textContent = sentenceStatus(c);
    var btn = $('#homeStartBtn');
    btn.textContent = !c ? 'Start this month\'s check' : (c.completed ? 'Look through this month\'s check' : 'Continue this month\'s check');
    $('#homeStreak').textContent = streakSentence(res[1]);
    $('#careHome').innerHTML = careBoxHTML();
  });
}

function careBoxHTML() {
  return '<div class="card tint">' +
    '<h2>Finding care</h2>' +
    '<ul>' +
    '<li><strong>See a dermatologist (a skin doctor) or your primary care doctor.</strong> Bring your notes and photos. Say which spot worries you and what has changed.</li>' +
    '<li><strong>Medicare</strong> does not pay for a routine screening of healthy skin, but it does cover a visit to check a spot when it is medically necessary. If a spot worries you, say so when you book.</li>' +
    '<li><strong>No insurance, or a tight budget?</strong> New Jersey\'s Federally Qualified Health Centers see patients regardless of insurance and charge based on what you can pay. Find one near you at <a href="https://findahealthcenter.hrsa.gov" target="_blank" rel="noopener">findahealthcenter.hrsa.gov</a>.</li>' +
    '<li><strong>Free screenings.</strong> The American Academy of Dermatology runs free SPOTme skin cancer screenings. Find one at <a href="https://www.aad.org/public/public-health/skin-cancer-screenings" target="_blank" rel="noopener">aad.org/public/public-health/skin-cancer-screenings</a>.</li>' +
    '</ul>' +
    '<p class="note">Links open in a new tab and leave this page. The tool itself never sends anything.</p>' +
    '</div>';
}

function signsHTML() {
  return '<details><summary>Signs to look for anywhere on the body</summary><div class="stack">' +
    '<ul>' + GENERAL_SIGNS.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ul>' +
    '<h4>The ABCDE check for moles</h4>' +
    '<ul>' + ABCDE.map(function (a) { return '<li><strong>' + a[0] + ' for ' + a[1] + ':</strong> ' + esc(a[2]) + '</li>'; }).join('') + '</ul>' +
    '<h4>On brown and Black skin</h4><p>' + esc(TONE_NOTE) + '</p>' +
    '</div></details>';
}

var currentCheck = null;
function renderCheck() {
  var month = monthId();
  return loadCheck(month).then(function (c) {
    currentCheck = c || newCheck(month);
    /* Resume where the person left off: first area not yet ticked. */
    if (c && !c.completed && stepIndex === 0 && areasDone(c) > 0) {
      var next = STEPS.findIndex(function (s) { return !s.info && !s.finish && !c.steps[s.id]; });
      stepIndex = next > 0 ? next : STEPS.length - 1;
    }
    if (!c) return store.put('checks', currentCheck).catch(function () {});
  }).then(function () { return renderStep(); });
}

function photoKeyFor(month, stepId) { return 'region:' + month + ':' + stepId; }
function latestEarlierPhoto(stepId, month) {
  return store.all('photos').then(function (all) {
    var best = null;
    all.forEach(function (p) { if (p.kind === 'region' && p.region === stepId && p.month < month && (!best || p.month > best.month)) best = p; });
    return best;
  });
}

function renderStep() {
  var c = currentCheck; var s = STEPS[stepIndex]; var area = $('#checkArea');
  var done = areasDone(c);
  var h = '<div class="stack-lg">';
  h += '<div class="stack"><span class="eyebrow">Step ' + (stepIndex + 1) + ' of ' + STEPS.length + ' · ' + monthLabel(c.month) + '</span>';
  h += '<div class="progress" role="progressbar" aria-label="Areas checked" aria-valuemin="0" aria-valuemax="' + AREA_COUNT + '" aria-valuenow="' + done + '" aria-valuetext="' + done + ' of ' + AREA_COUNT + ' areas checked"><i style="width:' + (done / AREA_COUNT * 100) + '%"></i></div>';
  h += '<h2 id="stepTitle" tabindex="-1">' + esc(s.title) + '</h2>';
  h += '<p class="note">' + done + ' of ' + AREA_COUNT + ' areas checked' + (c.completed ? ' · Completed ' + dateLabel(c.completed) : '') + '</p></div>';

  if (s.finish) {
    h += '<div class="card tint"><h3>You checked ' + done + ' of ' + AREA_COUNT + ' areas.</h3>';
    if (done < AREA_COUNT) h += '<p>' + (AREA_COUNT - done) + ' area' + (AREA_COUNT - done === 1 ? ' is' : 's are') + ' not ticked yet: ' + esc(AREA_STEPS.filter(function (x) { return !c.steps[x.id]; }).map(function (x) { return x.title; }).join('; ')) + '. You can go back, or finish anyway and come back later.</p>';
    if (c.completed) h += '<p>This month\'s check was marked complete on ' + dateLabel(c.completed) + '.</p>';
    else h += '<div class="row"><button class="btn" type="button" data-action="complete">Mark this month\'s check complete</button></div>';
    h += '</div>';
    h += '<div class="card"><h3>What to do with what you found</h3><ul>' +
      '<li>If any spot is new, changing, bleeding, not healing, or there is a new dark line in a nail, make an appointment with a doctor. Do not wait for next month.</li>' +
      '<li>Add any spot you want to watch under <a href="#spots">My spots</a>, with a note and a photo, so you can compare next month.</li>' +
      '<li>If you are not sure, ask. A doctor would rather look at a harmless spot than miss a harmful one.</li></ul></div>';
    h += signsHTML();
    h += careBoxHTML();
    h += '<div class="row"><button class="btn-outline" type="button" data-action="prev">Back</button><a class="btn-outline" href="#history">See my history</a></div>';
    area.innerHTML = h + '</div>';
    focusStep(); return Promise.resolve();
  }

  h += '<div class="step-grid">';
  if (s.map) h += '<div class="bodymap' + (s.map === 'palm' || s.map === 'sole' || s.map === 'nail' ? ' big' : '') + '">' + mapSVG(s.map, { highlight: s.regions, alt: s.regions ? 'Body map with ' + s.title.toLowerCase() + ' highlighted' : MAPS[s.map].title }) + (s.map === 'nail' ? '<p class="map-caption">Drawing: a dark line running down a nail, the kind to have checked if it is new or changing.</p>' : '') + '</div>';
  else h += '<div class="bodymap">' + mapSVG('front', { alt: 'Body map' }) + '</div>';
  h += '<div class="stack">';
  if (s.missed) h += '<p class="eyebrow">Often missed on brown and Black skin</p>';
  h += '<h3>Where to look</h3><p>' + esc(s.where) + '</p>';
  h += '<h3>How</h3><ul>' + s.how.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>';
  h += '<h3>What to look for</h3><p>' + esc(s.look) + '</p>';
  if (s.id === 'palms' || s.id === 'feet') h += '<p class="note">Among melanomas of a known type in Black patients, nearly half (46%) were the kind that grows on the palms, soles, or under the nails. Source: Culp and Lunsford, Preventing Chronic Disease, 2019.</p>';
  if (!s.info) h += signsHTML();
  h += '</div></div>';

  if (!s.info) {
    h += '<label class="check-label"><input type="checkbox" data-step="' + s.id + '"' + (c.steps[s.id] ? ' checked' : '') + '> I checked this area</label>';
    h += '<div class="card" id="photoCard"><h3>Photo of this area (optional)</h3><p class="note">The photo is saved only on this device. It is never uploaded or analyzed. Use the same spot and light each month so the pictures are easy to compare.</p><div id="photoCompare" class="photos"></div>' +
      '<div class="row"><label class="btn-outline">Take a photo<input class="vh" type="file" accept="image/*" capture="environment" data-photo-step="' + s.id + '"></label>' +
      '<label class="btn-outline">Choose from my photos<input class="vh" type="file" accept="image/*" data-photo-step="' + s.id + '"></label>' +
      '<button class="btn-outline" type="button" data-action="remove-photo" id="removePhotoBtn" hidden>Remove this month\'s photo</button></div><p class="note" id="photoNote" aria-live="polite"></p></div>';
  }
  h += '<div class="row">' + (stepIndex > 0 ? '<button class="btn-outline" type="button" data-action="prev">Back</button>' : '') +
    '<button class="btn" type="button" data-action="next">' + (s.info ? 'Begin' : 'Next area') + '</button>' +
    (s.info ? '' : '<a class="btn-outline" href="#home">Finish later</a>') + '</div>';
  area.innerHTML = h + '</div>';
  focusStep();
  if (!s.info) return renderPhotoCompare(s.id);
  return Promise.resolve();
}
function focusStep() { var t = $('#stepTitle'); if (t) t.focus({ preventScroll: false }); var top = $('#view-check'); if (top) top.scrollIntoView({ block: 'start' }); }

function renderPhotoCompare(stepId) {
  var c = currentCheck; var key = photoKeyFor(c.month, stepId);
  return Promise.all([store.get('photos', key), latestEarlierPhoto(stepId, c.month)]).then(function (r) {
    var cur = r[0], prev = r[1]; var el = $('#photoCompare'); if (!el) return;
    var h = '<figure class="frame"><figcaption>' + (prev ? 'Earlier: ' + esc(monthLabel(prev.month)) : 'Earlier photo') + '</figcaption>';
    h += prev ? '<img src="' + photoURL(prev.key, prev.blob) + '" alt="Your photo of this area from ' + esc(monthLabel(prev.month)) + '">' : '<p class="ph">No earlier photo yet. Next month you will see this month\'s photo here.</p>';
    h += '</figure><figure class="frame"><figcaption>This month: ' + esc(monthLabel(c.month)) + '</figcaption>';
    h += cur ? '<img src="' + photoURL(cur.key, cur.blob) + '" alt="Your photo of this area from ' + esc(monthLabel(c.month)) + '">' : '<p class="ph">No photo yet.</p>';
    h += '</figure>';
    el.innerHTML = h;
    var rb = $('#removePhotoBtn'); if (rb) rb.hidden = !cur;
  });
}

function saveRegionPhoto(stepId, file) {
  var note = $('#photoNote'); if (note) note.textContent = 'Saving photo on this device…';
  return processImage(file).then(function (blob) {
    var key = photoKeyFor(currentCheck.month, stepId);
    dropURL(key);
    return store.put('photos', { key: key, kind: 'region', month: currentCheck.month, region: stepId, blob: blob, type: blob.type || 'image/jpeg', taken: new Date().toISOString() });
  }).then(function () { if (note) note.textContent = 'Photo saved on this device.'; return renderPhotoCompare(stepId); })
    .catch(function () { if (note) note.textContent = 'The photo could not be saved.'; });
}

/* ---------- spots ---------- */
var spotMap = 'front', spotSide = 'left', pendingSpot = null, editingSpotId = null, updatingSpotId = null;
var SIDE_MAPS = { palm: 1, sole: 1, nail: 1 };
function spotLocationText(s) {
  var side = s.side ? (s.side === 'left' ? 'Left ' : 'Right ') : '';
  if (s.map === 'palm') return side + 'hand: ' + s.regionLabel.toLowerCase();
  if (s.map === 'sole') return side + 'foot: ' + s.regionLabel.toLowerCase();
  if (s.map === 'nail') return side + 'side, nail: ' + s.regionLabel.toLowerCase() + (s.which ? ' (' + s.which + ')' : '');
  return s.regionLabel + (s.map === 'back' ? ' (back view)' : ' (front view)');
}
function renderSpots() {
  $('#spotSideRow').hidden = !SIDE_MAPS[spotMap];
  $$('#spotMapPicker button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.map === spotMap ? 'true' : 'false'); });
  return store.all('spots').then(function (spots) {
    spots.sort(function (a, b) { return a.created < b.created ? -1 : 1; });
    var pins = [];
    spots.forEach(function (s, i) { if (s.map === spotMap && (!SIDE_MAPS[spotMap] || s.side === spotSide)) pins.push({ x: s.x, y: s.y, n: i + 1 }); });
    if (pendingSpot && pendingSpot.map === spotMap && (!SIDE_MAPS[spotMap] || pendingSpot.side === spotSide)) pins.push({ x: pendingSpot.x, y: pendingSpot.y, n: '+' });
    $('#spotMap').innerHTML = mapSVG(spotMap, { interactive: true, pins: pins });
    $('#spotMapCaption').textContent = MAPS[spotMap].title + (SIDE_MAPS[spotMap] ? ' (' + spotSide + ')' : '') + '. Tap the map, or use Tab and Enter to pick an area.';
    renderSpotForm();
    renderSpotList(spots);
  });
}
function renderSpotForm() {
  var f = $('#spotForm');
  if (!pendingSpot) { f.innerHTML = '<div class="card tint"><h3>Add a spot</h3><p>Tap the place on the map where the spot is. Then write a short note about what it looks like.</p></div>'; return; }
  var p = pendingSpot;
  f.innerHTML = '<form class="card" id="newSpotForm"><h3>New spot</h3><p><strong>Where:</strong> ' + esc(spotLocationText(p)) + '</p>' +
    (p.map === 'nail' ? '<label class="field" for="spotWhich">Which nail? (optional)<input type="text" id="spotWhich" maxlength="40" placeholder="for example: thumb, big toe"></label>' : '') +
    '<label class="field" for="spotNote">What does it look like?<textarea id="spotNote" maxlength="600" placeholder="for example: small dark brown spot, about the size of a pencil eraser, flat, not itchy"></textarea></label>' +
    '<label class="field" for="spotDate">Date<input type="date" id="spotDate" value="' + todayISO() + '"></label>' +
    '<div class="row"><label class="btn-outline">Take a photo<input class="vh" type="file" accept="image/*" capture="environment" id="spotPhotoCam"></label><label class="btn-outline">Choose from my photos<input class="vh" type="file" accept="image/*" id="spotPhotoFile"></label></div>' +
    '<p class="note" id="spotPhotoNote" aria-live="polite">No photo chosen. Photos stay on this device.</p>' +
    '<div class="row"><button class="btn" type="submit">Save this spot</button><button class="btn-outline" type="button" data-action="spot-cancel">Cancel</button></div></form>';
  $('#spotNote').focus();
}
var pendingFile = null;
function renderSpotList(spots) {
  var el = $('#spotList');
  if (!spots.length) { el.innerHTML = '<p class="note">No spots saved yet.</p>'; return; }
  el.innerHTML = spots.map(function (s, i) {
    var entries = s.entries.slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; });
    var first = entries[0], last = entries[entries.length - 1];
    var h = '<div class="spot-card" id="spot-' + s.id + '"><div class="row"><span class="num" aria-hidden="true">' + (i + 1) + '</span><h4>Spot ' + (i + 1) + ': ' + esc(spotLocationText(s)) + '</h4></div>';
    h += '<p class="note">First noted ' + dateLabel(first.date) + (entries.length > 1 ? ' · ' + entries.length + ' entries, latest ' + dateLabel(last.date) : '') + '</p>';
    if (entries.length > 1 && (first.photoKey || last.photoKey)) {
      h += '<div class="photos" data-compare="' + s.id + '"><figure class="frame"><figcaption>First: ' + dateLabel(first.date) + '</figcaption>' + (first.photoKey ? '<img data-photo="' + first.photoKey + '" alt="First photo of this spot">' : '<p class="ph">No photo</p>') + '</figure>' +
        '<figure class="frame"><figcaption>Latest: ' + dateLabel(last.date) + '</figcaption>' + (last.photoKey ? '<img data-photo="' + last.photoKey + '" alt="Latest photo of this spot">' : '<p class="ph">No photo</p>') + '</figure></div>';
    }
    h += '<div>' + entries.map(function (e) {
      return '<div class="entry"><time datetime="' + esc(e.date) + '">' + dateLabel(e.date) + '</time>' + (e.note ? '<p>' + esc(e.note) + '</p>' : '<p class="note">No note.</p>') + (e.photoKey && !(entries.length > 1 && (e === first || e === last)) ? '<img class="thumb" data-photo="' + e.photoKey + '" alt="Photo of this spot, ' + dateLabel(e.date) + '">' : (e.photoKey && entries.length === 1 ? '<img class="thumb" data-photo="' + e.photoKey + '" alt="Photo of this spot">' : '')) + '</div>';
    }).join('') + '</div>';
    if (updatingSpotId === s.id) {
      h += '<form class="card tint" data-update-form="' + s.id + '"><h4>Add an update</h4>' +
        '<label class="field" for="upNote-' + s.id + '">What does it look like now?<textarea id="upNote-' + s.id + '" maxlength="600" placeholder="for example: looks the same as last month"></textarea></label>' +
        '<label class="field" for="upDate-' + s.id + '">Date<input type="date" id="upDate-' + s.id + '" value="' + todayISO() + '"></label>' +
        '<div class="row"><label class="btn-outline">Take a photo<input class="vh" type="file" accept="image/*" capture="environment" data-up-photo="' + s.id + '"></label><label class="btn-outline">Choose from my photos<input class="vh" type="file" accept="image/*" data-up-photo="' + s.id + '"></label></div>' +
        '<p class="note" id="upPhotoNote-' + s.id + '" aria-live="polite">No photo chosen.</p>' +
        '<div class="row"><button class="btn" type="submit">Save update</button><button class="btn-outline" type="button" data-action="update-cancel">Cancel</button></div></form>';
    } else {
      h += '<div class="row"><button class="btn-outline" type="button" data-action="update-start" data-id="' + s.id + '">Add an update</button>' +
        (deletingSpotId === s.id ? '<button class="btn" type="button" data-action="spot-delete-yes" data-id="' + s.id + '">Yes, delete this spot</button><button class="btn-outline" type="button" data-action="spot-delete-no">Keep it</button>' : '<button class="btn-outline" type="button" data-action="spot-delete-ask" data-id="' + s.id + '">Delete this spot</button>') + '</div>';
    }
    return h + '</div>';
  }).join('');
  // load photos
  $$('img[data-photo]', el).forEach(function (img) {
    var key = img.dataset.photo;
    store.get('photos', key).then(function (p) { if (p) img.src = photoURL(key, p.blob); else img.alt = 'Photo missing'; });
  });
}
var deletingSpotId = null;

function addSpot(form) {
  var p = pendingSpot; if (!p) return Promise.resolve();
  var note = $('#spotNote').value.trim(), date = $('#spotDate').value || todayISO();
  var which = $('#spotWhich') ? $('#spotWhich').value.trim() : '';
  var id = uid(), entryId = uid();
  var spot = { id: id, created: new Date().toISOString(), map: p.map, side: SIDE_MAPS[p.map] ? p.side : '', x: Math.round(p.x), y: Math.round(p.y), region: p.region, regionLabel: p.regionLabel, which: which, entries: [{ id: entryId, date: date, note: note, photoKey: null }] };
  var chain = Promise.resolve();
  if (pendingFile) {
    chain = processImage(pendingFile).then(function (blob) {
      var key = 'spot:' + id + ':' + entryId;
      spot.entries[0].photoKey = key;
      return store.put('photos', { key: key, kind: 'spot', spotId: id, entryId: entryId, blob: blob, type: blob.type || 'image/jpeg', taken: new Date().toISOString() });
    });
  }
  return chain.then(function () { return store.put('spots', spot); }).then(function () { pendingSpot = null; pendingFile = null; return renderSpots(); }).then(function () { var el = $('#spot-' + id); if (el) { el.setAttribute('tabindex', '-1'); el.focus(); } }).catch(function () {});
}
var updateFile = null;
function addUpdate(spotId) {
  return store.get('spots', spotId).then(function (spot) {
    if (!spot) return;
    var note = $('#upNote-' + spotId).value.trim(), date = $('#upDate-' + spotId).value || todayISO();
    var entry = { id: uid(), date: date, note: note, photoKey: null };
    var chain = Promise.resolve();
    if (updateFile) {
      chain = processImage(updateFile).then(function (blob) {
        var key = 'spot:' + spotId + ':' + entry.id; entry.photoKey = key;
        return store.put('photos', { key: key, kind: 'spot', spotId: spotId, entryId: entry.id, blob: blob, type: blob.type || 'image/jpeg', taken: new Date().toISOString() });
      });
    }
    return chain.then(function () { spot.entries.push(entry); return store.put('spots', spot); }).then(function () { updatingSpotId = null; updateFile = null; return renderSpots(); }).then(function () { var el = $('#spot-' + spotId); if (el) { el.setAttribute('tabindex', '-1'); el.focus(); } });
  }).catch(function () {});
}
function deleteSpot(spotId) {
  return store.get('spots', spotId).then(function (spot) {
    if (!spot) return;
    return Promise.all(spot.entries.filter(function (e) { return e.photoKey; }).map(function (e) { dropURL(e.photoKey); return store.del('photos', e.photoKey); })).then(function () { return store.del('spots', spotId); });
  }).then(function () { deletingSpotId = null; return renderSpots(); }).catch(function () {});
}

/* ---------- history ---------- */
function renderHistory() {
  return store.all('checks').then(function (checks) {
    $('#historyStreak').textContent = streakSentence(checks);
    checks.sort(function (a, b) { return a.month < b.month ? 1 : -1; });
    var el = $('#historyList');
    if (!checks.length) { el.innerHTML = '<li class="note">No checks yet. Your first one will appear here.</li>'; return; }
    el.innerHTML = checks.map(function (c) {
      var n = areasDone(c);
      return '<li><strong>' + esc(monthLabel(c.month)) + '</strong><br>' + (c.completed ? 'Completed on ' + dateLabel(c.completed) + '. ' : 'Not finished. ') + n + ' of ' + AREA_COUNT + ' areas checked.' + (c.month === monthId() && !c.completed ? ' <a href="#check">Continue</a>' : '') + '</li>';
    }).join('');
  });
}

/* ---------- reminders ---------- */
function icsText(day) {
  var now = new Date();
  var start = new Date(now.getFullYear(), now.getMonth(), day);
  if (start < new Date(now.getFullYear(), now.getMonth(), now.getDate())) start = new Date(now.getFullYear(), now.getMonth() + 1, day);
  var end = new Date(start.getFullYear(), start.getMonth(), start.getDate() + 1);
  function d8(d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); }
  var stamp = now.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
  return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Every Shade//Monthly skin check//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    'BEGIN:VEVENT', 'UID:everyshade-skin-check-' + uid() + '@zainjaffar06.github.io', 'DTSTAMP:' + stamp,
    'DTSTART;VALUE=DATE:' + d8(start), 'DTEND;VALUE=DATE:' + d8(end), 'RRULE:FREQ=MONTHLY;BYMONTHDAY=' + day,
    'SUMMARY:Every Shade monthly skin check',
    'DESCRIPTION:Time for your monthly skin check. Open the guide: ' + TOOL_URL + ' \\n\\nCheck your whole body in good light\\, including palms\\, soles\\, between the toes\\, and nails. See a doctor about any spot that is new\\, changing\\, bleeding\\, or not healing\\, or a new dark line in a nail.',
    'URL:' + TOOL_URL, 'TRANSP:TRANSPARENT',
    'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:Every Shade monthly skin check', 'TRIGGER:PT9H', 'END:VALARM',
    'END:VEVENT', 'END:VCALENDAR'].join('\r\n') + '\r\n';
}
function reminderDay() { var v = parseInt($('#icsDay').value, 10); return (v >= 1 && v <= 28) ? v : 1; }
function renderSettings() {
  var sel = $('#icsDay');
  if (!sel.options.length) { for (var i = 1; i <= 28; i++) { var o = document.createElement('option'); o.value = i; o.textContent = ordinal(i); sel.appendChild(o); } }
  $('#themeSel').value = lsGet('es-theme') || 'auto';
  $('#textSel').value = lsGet('es-text') || 'normal';
  return Promise.all([getSetting('reminderDay', Math.min(new Date().getDate(), 28)), getSetting('notify', { enabled: false })]).then(function (r) {
    sel.value = r[0];
    updateNotifyUI(r[1]);
    return updateUsage();
  });
}
function ordinal(n) { var s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }
function updateNotifyUI(n) {
  var on = $('#notifyOnBtn'), off = $('#notifyOffBtn'), note = $('#notifyNote');
  if (!('Notification' in window)) { on.hidden = true; off.hidden = true; note.textContent = 'This browser does not support reminders. Use the calendar reminder instead.'; return; }
  var granted = Notification.permission === 'granted';
  on.hidden = !!(n.enabled && granted); off.hidden = !(n.enabled && granted);
  if (Notification.permission === 'denied') note.textContent = 'Reminders are blocked for this site in your browser settings. Use the calendar reminder instead.';
  else if (n.enabled && granted) note.textContent = 'On. You will see a reminder on the ' + ordinal(n.day || 1) + ' of each month, if this browser is open and this month\'s check is not done.';
  else note.textContent = 'Off.';
}
function maybeNotify() {
  if (!('Notification' in window) || Notification.permission !== 'granted') return;
  getSetting('notify', { enabled: false }).then(function (n) {
    if (!n.enabled) return;
    var m = monthId(); var today = new Date().getDate();
    if (today < (n.day || 1) || n.lastShown === m) return;
    return loadCheck(m).then(function (c) {
      if (c && c.completed) return;
      try {
        var note = new Notification('Every Shade monthly skin check', { body: 'Time for this month\'s skin check. It takes about ten minutes.', icon: 'icon.svg', tag: 'everyshade-check' });
        note.onclick = function () { window.focus(); location.hash = '#check'; };
      } catch (e) { return; }
      n.lastShown = m; return setSetting('notify', n);
    });
  }).catch(function () {});
}

/* ---------- export ---------- */
function blobToBase64(blob) { return new Promise(function (res, rej) { var r = new FileReader(); r.onload = function () { res(String(r.result).split(',')[1] || ''); }; r.onerror = function () { rej(r.error); }; r.readAsDataURL(blob); }); }
function blobToBytes(blob) { return new Promise(function (res, rej) { var r = new FileReader(); r.onload = function () { res(new Uint8Array(r.result)); }; r.onerror = function () { rej(r.error); }; r.readAsArrayBuffer(blob); }); }
function gatherData() {
  return Promise.all([store.all('checks'), store.all('spots'), store.all('photos')]).then(function (r) {
    return { app: 'Every Shade monthly skin check', version: 1, exported: new Date().toISOString(), note: 'Educational record kept by the user. Not a medical record and not a diagnosis.', checks: r[0], spots: r[1], photos: r[2] };
  });
}
function extFor(type) { return type === 'image/png' ? 'png' : type === 'image/webp' ? 'webp' : type === 'image/heic' ? 'heic' : 'jpg'; }
function exportJSON() {
  return gatherData().then(function (d) {
    return Promise.all(d.photos.map(function (p) { return blobToBase64(p.blob).then(function (b64) { return { key: p.key, kind: p.kind, month: p.month, region: p.region, spotId: p.spotId, entryId: p.entryId, taken: p.taken, type: p.type, dataBase64: b64 }; }); })).then(function (photos) {
      d.photos = photos;
      download(new Blob([JSON.stringify(d, null, 2)], { type: 'application/json' }), 'every-shade-skin-check-' + todayISO() + '.json');
    });
  });
}
var CRC_TABLE = (function () { var t = new Uint32Array(256); for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1); t[n] = c >>> 0; } return t; })();
function crc32(u8) { var c = 0xFFFFFFFF; for (var i = 0; i < u8.length; i++) c = CRC_TABLE[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
function makeZip(files) {
  var enc = new TextEncoder(), parts = [], central = [], offset = 0, now = new Date();
  var dosTime = ((now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1)) & 0xFFFF;
  var dosDate = (((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate()) & 0xFFFF;
  files.forEach(function (f) {
    var name = enc.encode(f.name), crc = crc32(f.data), n = f.data.length;
    var h = new DataView(new ArrayBuffer(30));
    h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true); h.setUint16(8, 0, true); h.setUint16(10, dosTime, true); h.setUint16(12, dosDate, true); h.setUint32(14, crc, true); h.setUint32(18, n, true); h.setUint32(22, n, true); h.setUint16(26, name.length, true); h.setUint16(28, 0, true);
    parts.push(new Uint8Array(h.buffer), name, f.data);
    var c = new DataView(new ArrayBuffer(46));
    c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true); c.setUint16(10, 0, true); c.setUint16(12, dosTime, true); c.setUint16(14, dosDate, true); c.setUint32(16, crc, true); c.setUint32(20, n, true); c.setUint32(24, n, true); c.setUint16(28, name.length, true); c.setUint16(30, 0, true); c.setUint16(32, 0, true); c.setUint16(34, 0, true); c.setUint16(36, 0, true); c.setUint32(38, 0, true); c.setUint32(42, offset, true);
    central.push(new Uint8Array(c.buffer), name);
    offset += 30 + name.length + n;
  });
  var cdSize = 0; central.forEach(function (p) { cdSize += p.length; });
  var e = new DataView(new ArrayBuffer(22));
  e.setUint32(0, 0x06054b50, true); e.setUint16(4, 0, true); e.setUint16(6, 0, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true); e.setUint32(12, cdSize, true); e.setUint32(16, offset, true); e.setUint16(20, 0, true);
  return new Blob(parts.concat(central, [new Uint8Array(e.buffer)]), { type: 'application/zip' });
}
function exportZip() {
  return gatherData().then(function (d) {
    var enc = new TextEncoder();
    return Promise.all(d.photos.map(function (p) {
      var fname = 'photos/' + p.key.replace(/[^a-z0-9_-]+/gi, '_') + '.' + extFor(p.type);
      return blobToBytes(p.blob).then(function (bytes) { return { name: fname, data: bytes, meta: { key: p.key, kind: p.kind, month: p.month, region: p.region, spotId: p.spotId, entryId: p.entryId, taken: p.taken, type: p.type, file: fname } }; });
    })).then(function (photoFiles) {
      d.photos = photoFiles.map(function (f) { return f.meta; });
      var files = [{ name: 'data.json', data: enc.encode(JSON.stringify(d, null, 2)) },
        { name: 'README.txt', data: enc.encode('Every Shade monthly skin check export\r\nExported ' + d.exported + '\r\n\r\ndata.json holds your check history, spot notes, and the list of photos.\r\nphotos/ holds the pictures. This is a personal record for you and your doctor. It is not a medical record and not a diagnosis.\r\n') }].concat(photoFiles);
      download(makeZip(files), 'every-shade-skin-check-' + todayISO() + '.zip');
    });
  });
}
function updateUsage() {
  var el = $('#usageNote'); if (!el) return;
  return Promise.all([store.all('checks'), store.all('spots'), store.all('photos')]).then(function (r) {
    var bytes = 0; r[2].forEach(function (p) { bytes += (p.blob && p.blob.size) || 0; });
    el.textContent = 'On this device: ' + r[0].length + ' month' + (r[0].length === 1 ? '' : 's') + ' of checks, ' + r[1].length + ' spot' + (r[1].length === 1 ? '' : 's') + ', ' + r[2].length + ' photo' + (r[2].length === 1 ? '' : 's') + (bytes ? ' (about ' + (bytes > 1048576 ? (bytes / 1048576).toFixed(1) + ' MB' : Math.round(bytes / 1024) + ' KB') + ')' : '') + '.' + (storageOK ? '' : ' Saving is currently not working: ' + storageMsg);
  });
}
function deleteEverything() {
  return Promise.all(['checks', 'spots', 'photos', 'settings'].map(function (s) { return store.clear(s); })).then(function () {
    Object.keys(urlCache).forEach(dropURL);
    currentCheck = null; stepIndex = 0; pendingSpot = null; pendingFile = null; updatingSpotId = null; deletingSpotId = null;
    $('#deleteConfirm').hidden = true; $('#deleteRow').hidden = false;
    $('#deleteNote').textContent = 'Everything has been deleted from this device.';
    return renderSettings();
  }).catch(function () { $('#deleteNote').textContent = 'Something could not be deleted. Please try again.'; });
}

/* ---------- events ---------- */
document.addEventListener('click', function (e) {
  var btn = e.target.closest('[data-action]'); if (!btn) return;
  var act = btn.dataset.action;
  if (act === 'print') { window.print(); }
  else if (act === 'next') { if (stepIndex < STEPS.length - 1) { stepIndex++; renderStep(); } }
  else if (act === 'prev') { if (stepIndex > 0) { stepIndex--; renderStep(); } }
  else if (act === 'complete') {
    currentCheck.completed = new Date().toISOString();
    store.put('checks', currentCheck).catch(function () {}).then(function () { renderStep(); });
  }
  else if (act === 'remove-photo') {
    var s = STEPS[stepIndex]; var key = photoKeyFor(currentCheck.month, s.id); dropURL(key);
    store.del('photos', key).then(function () { var n = $('#photoNote'); if (n) n.textContent = 'Photo removed.'; return renderPhotoCompare(s.id); }).catch(function () {});
  }
  else if (act === 'spot-cancel') { pendingSpot = null; pendingFile = null; renderSpots(); }
  else if (act === 'update-start') { updatingSpotId = btn.dataset.id; updateFile = null; deletingSpotId = null; renderSpots().then(function () { var t = $('#upNote-' + updatingSpotId); if (t) t.focus(); }); }
  else if (act === 'update-cancel') { updatingSpotId = null; updateFile = null; renderSpots(); }
  else if (act === 'spot-delete-ask') { deletingSpotId = btn.dataset.id; renderSpots().then(function () { var b = $('[data-action="spot-delete-yes"]'); if (b) b.focus(); }); }
  else if (act === 'spot-delete-no') { deletingSpotId = null; renderSpots(); }
  else if (act === 'spot-delete-yes') { deleteSpot(btn.dataset.id); }
  else if (act === 'ics') {
    var day = reminderDay();
    setSetting('reminderDay', day).catch(function () {});
    download(new Blob([icsText(day)], { type: 'text/calendar' }), 'every-shade-skin-check.ics');
    $('#icsNote').textContent = 'Downloaded. Open the file and your calendar will offer to add a repeating event on the ' + ordinal(day) + ' of each month.';
  }
  else if (act === 'notify-on') {
    if (!('Notification' in window)) return;
    var day2 = reminderDay();
    Notification.requestPermission().then(function (perm) {
      var n = { enabled: perm === 'granted', day: day2 };
      return setSetting('notify', n).catch(function () {}).then(function () { updateNotifyUI(n); if (perm === 'granted') maybeNotify(); });
    });
  }
  else if (act === 'notify-off') { var off = { enabled: false }; setSetting('notify', off).catch(function () {}).then(function () { updateNotifyUI(off); }); }
  else if (act === 'export-json') { $('#exportNote').textContent = 'Preparing your file…'; exportJSON().then(function () { $('#exportNote').textContent = 'Your JSON file has been downloaded.'; }).catch(function () { $('#exportNote').textContent = 'The export could not be made.'; }); }
  else if (act === 'export-zip') { $('#exportNote').textContent = 'Preparing your file…'; exportZip().then(function () { $('#exportNote').textContent = 'Your zip file has been downloaded.'; }).catch(function () { $('#exportNote').textContent = 'The export could not be made.'; }); }
  else if (act === 'delete-ask') { $('#deleteRow').hidden = true; $('#deleteConfirm').hidden = false; $('[data-action="delete-no"]').focus(); }
  else if (act === 'delete-no') { $('#deleteConfirm').hidden = true; $('#deleteRow').hidden = false; $('#deleteNote').textContent = 'Nothing was deleted.'; }
  else if (act === 'delete-yes') { deleteEverything(); }
});

document.addEventListener('change', function (e) {
  var t = e.target;
  if (t.matches('input[data-step]')) {
    currentCheck.steps[t.dataset.step] = t.checked;
    store.put('checks', currentCheck).catch(function () {}).then(function () {
      var done = areasDone(currentCheck); var pb = $('.progress'); if (pb) { pb.setAttribute('aria-valuenow', done); pb.setAttribute('aria-valuetext', done + ' of ' + AREA_COUNT + ' areas checked'); pb.firstElementChild.style.width = (done / AREA_COUNT * 100) + '%'; }
      var n = $('#checkArea .note'); if (n) n.textContent = done + ' of ' + AREA_COUNT + ' areas checked' + (currentCheck.completed ? ' · Completed ' + dateLabel(currentCheck.completed) : '');
    });
  }
  else if (t.matches('input[data-photo-step]')) { if (t.files && t.files[0]) saveRegionPhoto(t.dataset.photoStep, t.files[0]); t.value = ''; }
  else if (t.id === 'spotPhotoCam' || t.id === 'spotPhotoFile') { if (t.files && t.files[0]) { pendingFile = t.files[0]; $('#spotPhotoNote').textContent = 'Photo chosen (' + Math.round(pendingFile.size / 1024) + ' KB). It will be saved on this device when you save the spot.'; } }
  else if (t.matches('input[data-up-photo]')) { if (t.files && t.files[0]) { updateFile = t.files[0]; var n2 = $('#upPhotoNote-' + t.dataset.upPhoto); if (n2) n2.textContent = 'Photo chosen (' + Math.round(updateFile.size / 1024) + ' KB).'; } }
  else if (t.name === 'spotSide') { spotSide = t.value; renderSpots(); }
  else if (t.id === 'themeSel') { var v = t.value; if (v === 'auto') { document.documentElement.removeAttribute('data-theme'); lsSet('es-theme', null); } else { document.documentElement.setAttribute('data-theme', v); lsSet('es-theme', v); } }
  else if (t.id === 'textSel') { if (t.value === 'large') { document.documentElement.setAttribute('data-text', 'large'); lsSet('es-text', 'large'); } else { document.documentElement.removeAttribute('data-text'); lsSet('es-text', null); } }
  else if (t.id === 'icsDay') { setSetting('reminderDay', reminderDay()).catch(function () {}); }
});

document.addEventListener('submit', function (e) {
  if (e.target.id === 'newSpotForm') { e.preventDefault(); addSpot(e.target); }
  else if (e.target.matches('[data-update-form]')) { e.preventDefault(); addUpdate(e.target.dataset.updateForm); }
});

/* map picker */
$('#spotMapPicker').addEventListener('click', function (e) {
  var b = e.target.closest('button[data-map]'); if (!b) return;
  spotMap = b.dataset.map; pendingSpot = null; pendingFile = null; renderSpots();
});
/* tapping the map */
function placeSpot(svg, x, y, regionEl) {
  pendingSpot = { map: spotMap, side: spotSide, x: x, y: y, region: regionEl ? regionEl.dataset.region : 'other', regionLabel: regionEl ? regionEl.dataset.label : 'Somewhere on the ' + MAPS[spotMap].title.toLowerCase() };
  renderSpots();
}
$('#spotMap').addEventListener('click', function (e) {
  var svg = e.target.closest('svg'); if (!svg) return;
  var reg = e.target.closest('[data-region]');
  if (e.detail === 0 && reg) { var b = reg.getBBox(); placeSpot(svg, b.x + b.width / 2, b.y + b.height / 2, reg); return; }
  var p = svgPoint(svg, e); if (!p) return;
  placeSpot(svg, p.x, p.y, reg);
});
$('#spotMap').addEventListener('keydown', function (e) {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  var reg = e.target.closest('[data-region]'); if (!reg) return;
  e.preventDefault(); var b = reg.getBBox(); placeSpot(reg.ownerSVGElement, b.x + b.width / 2, b.y + b.height / 2, reg);
});

window.addEventListener('hashchange', route);

/* ---------- start ---------- */
openDB().then(function () {
  route();
  maybeNotify();
  setInterval(maybeNotify, 60 * 60 * 1000);
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) {
    navigator.serviceWorker.register('sw.js').catch(function () {});
  }
});
})();
