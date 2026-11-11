// Build the Every Shade senior talk deck (16:9, large type for Zoom).
// Run from the folder that has pptxgenjs installed:
//   node /Users/zainjaffar/everyshade/talk-kit/slides/build_deck.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL_DIR + "/scripts/apply_theme.js");

const OUT = path.join(__dirname, "Every-Shade-Senior-Talk-2026-11-20.pptx");

const THEME = {
  name: "Every Shade",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "2B1A12", lt1: "FFFFFF", dk2: "6B5446", lt2: "F7F1EC",
    accent1: "8E5632", accent2: "EFCBB0", accent3: "DDAA84", accent4: "C28559",
    accent5: "9C623A", accent6: "6B4127", hlink: "8E5632", folHlink: "6B4127",
  },
};
const TONES = ["EFCBB0", "DDAA84", "C28559", "9C623A", "6B4127", "3D2416"];

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Every Shade";
pres.title = "Skin cancer doesn't look the same on everyone";
const C = pres.SchemeColor;
const W = 13.333, H = 7.5, M = 0.6;

// ---------- brand helpers ----------
function logo(slide, x, y, scale, rivet) {
  // fanned swatches: five rounded bars pivoting at a common base point
  const L = 1.0 * scale, Wb = 0.28 * scale;
  const px = x, py = y + L; // pivot (base point)
  const angles = [-44, -22, 0, 22, 44];
  angles.forEach((a, i) => {
    const r = (a * Math.PI) / 180;
    const cx = px + (L / 2) * Math.sin(r), cy = py - (L / 2) * Math.cos(r);
    slide.addShape(pres.ShapeType.roundRect, {
      x: cx - Wb / 2, y: cy - L / 2, w: Wb, h: L, rotate: a, rectRadius: Wb / 2,
      fill: { color: TONES[i] }, line: { color: TONES[i], width: 0 }, objectName: `logo bar ${i + 1}`,
    });
  });
  slide.addShape(pres.ShapeType.ellipse, {
    x: px - 0.05 * scale, y: py - 0.05 * scale, w: 0.1 * scale, h: 0.1 * scale,
    fill: { color: rivet || "FFFFFF" }, line: { color: rivet || "FFFFFF", width: 0 }, objectName: "logo rivet",
  });
}
function strip(slide, y, h) {
  TONES.forEach((t, i) => slide.addShape(pres.ShapeType.rect, {
    x: (W / 6) * i, y, w: W / 6, h, fill: { color: t }, line: { color: t, width: 0 }, objectName: `tone ${i + 1}`,
  }));
}

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "DARK", background: { color: THEME.colors.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.0, w: W - 2 * M, h: 2.4, fontSize: 54, bold: true, color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "Title" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.6, w: W - 2 * M, h: 1.6, fontSize: 26, color: C.accent2, valign: "top", align: "left", margin: 0 }, text: "Body" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: THEME.colors.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: W - 2 * M, h: 1.1, fontSize: 38, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "Title" } },
    { text: { text: "every shade", options: { x: 1.05, y: 6.95, w: 3, h: 0.4, fontSize: 14, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: "footer wordmark" } } },
    { text: { text: "General health education only. Not medical advice. Our members are students, not medical professionals.", options: { x: 4.2, y: 6.95, w: W - 4.2 - M, h: 0.4, fontSize: 11, color: C.text2, align: "right", margin: 0, isTextBox: true, objectName: "footer disclaimer" } } },
  ],
  slideNumber: { x: M, y: 6.95, w: 0.4, h: 0.4, fontSize: 11, color: THEME.colors.dk2 },
});
pres.defineSlideMaster({
  title: "TINT", background: { color: THEME.colors.lt2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: W - 2 * M, h: 1.1, fontSize: 38, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "Title" } },
    { text: { text: "every shade", options: { x: 1.05, y: 6.95, w: 3, h: 0.4, fontSize: 14, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: "footer wordmark" } } },
    { text: { text: "General health education only. Not medical advice. Our members are students, not medical professionals.", options: { x: 4.2, y: 6.95, w: W - 4.2 - M, h: 0.4, fontSize: 11, color: C.text2, align: "right", margin: 0, isTextBox: true, objectName: "footer disclaimer" } } },
  ],
  slideNumber: { x: M, y: 6.95, w: 0.4, h: 0.4, fontSize: 11, color: THEME.colors.dk2 },
});

// ---------- content helpers ----------
function bullets(slide, items, o) {
  const arr = items.map((t, i) => ({ text: t, options: { bullet: { indent: 22 }, breakLine: i < items.length - 1, paraSpaceAfter: o.gap || 10 } }));
  slide.addText(arr, Object.assign({ fontSize: 24, color: C.text1, valign: "top", margin: 0, isTextBox: true }, o));
}
function card(slide, x, y, w, h, head, body, tone, o = {}) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.18, fill: { color: o.fill || THEME.colors.lt2 }, line: { color: o.fill || THEME.colors.lt2, width: 0 }, objectName: `card ${head}` });
  if (tone) slide.addShape(pres.ShapeType.roundRect, { x: x + 0.3, y: y + 0.3, w: 0.7, h: 0.2, rectRadius: 0.1, fill: { color: tone }, line: { color: tone, width: 0 }, objectName: `swatch ${head}` });
  slide.addText(head, { x: x + 0.3, y: y + (tone ? 0.6 : 0.3), w: w - 0.6, h: 0.95, fontSize: o.headSize || 24, bold: true, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: `card head ${head}` });
  slide.addText(body, { x: x + 0.3, y: y + (tone ? 1.6 : 1.3), w: w - 0.6, h: h - (tone ? 1.8 : 1.5), fontSize: o.bodySize || 20, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: `card body ${head}` });
}
function imageBox(slide, x, y, w, h, caption, source) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.18, fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.accent3, width: 2, dashType: "dash" }, objectName: `image placeholder ${caption}` });
  slide.addText([
    { text: "PHOTO GOES HERE", options: { bold: true, fontSize: 16, color: C.accent1, breakLine: true } },
    { text: caption, options: { fontSize: 18, color: C.text1, breakLine: true } },
    { text: source, options: { fontSize: 12, color: C.text2 } },
  ], { x: x + 0.3, y: y + 0.3, w: w - 0.6, h: h - 0.6, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `image note ${caption}` });
}
function stat(slide, x, y, w, big, label, bigSize) {
  slide.addText(big, { x, y, w, h: 1.3, fontSize: bigSize || 60, bold: true, color: C.accent1, margin: 0, isTextBox: true, valign: "bottom", objectName: `stat ${big}` });
  slide.addText(label, { x, y: y + 1.4, w, h: 1.9, fontSize: 20, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: `stat label ${big}` });
}
function numRow(slide, x, y, w, n, text, size, h) {
  slide.addShape(pres.ShapeType.ellipse, { x, y: y + 0.05, w: 0.55, h: 0.55, fill: { color: THEME.colors.dk1 }, line: { color: THEME.colors.dk1, width: 0 }, objectName: `num ${n}` });
  slide.addText(String(n), { x, y: y + 0.05, w: 0.55, h: 0.55, fontSize: 20, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `num text ${n}` });
  slide.addText(text, { x: x + 0.75, y, w: w - 0.75, h: h || 0.95, fontSize: size || 21, color: C.text1, margin: 0, isTextBox: true, valign: "top", objectName: `step ${n}` });
}
let S;

// =============== 1. Title ===============
pres.addSection({ title: "Opening" });
S = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" });
strip(S, 0, 0.18);
logo(S, 1.3, 0.7, 1.1, THEME.colors.dk1);
S.addText("every shade", { x: 2.1, y: 0.95, w: 4, h: 0.6, fontSize: 26, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: "wordmark" });
S.addText("Skin cancer doesn't look the same on everyone.", { placeholder: "title" });
S.addText("A free talk for seniors · Friday, November 20, 2026 · Every Shade, Rutgers University–New Brunswick", { placeholder: "body" });
S.addNotes("Welcome everyone as they join. Keep this slide up for 2-3 minutes while people settle in. Say: 'Thank you for joining us. My name is Zain, I am a student at Rutgers, and I'm part of a group called Every Shade. Tonight we'll talk about how to find skin cancer early, on every skin tone, and how to check your own skin at home. We'll finish with time for your questions.' Ask people to turn on captions if they want them (Zoom: 'Show captions').");

// =============== 2. Who we are / plan / quiz ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Opening" });
S.addText("Tonight, in 45 minutes", { placeholder: "title" });
logo(S, 0.6, 6.85, 0.45, THEME.colors.lt1);
bullets(S, ["Why skin cancer is often found late on darker skin", "What warning signs look like on light, medium, and dark skin", "The spots people miss: palms, soles, and nails", "How to check your skin at home in 10 minutes", "When to see a doctor, and where to go without insurance", "Your questions"], { x: M, y: 1.8, w: 7.2, h: 4.9, fontSize: 22, gap: 8 });
card(S, 8.3, 1.8, 4.4, 4.6, "First, a quick quiz", "10 short questions, no names. It helps us see if the talk works. We'll ask the same questions at the end.\n\nOn Zoom: the poll will pop up on your screen now.", null, { headSize: 24, bodySize: 20 });
S.addNotes("Say: 'We are students, not doctors. Nothing tonight is medical advice, and we cannot look at a spot and tell you what it is. What we can do is help you know what to look for and where to go.' Then LAUNCH THE 'BEFORE THE TALK' ZOOM POLL. Give 3 minutes. For a watch-together room, hand out the paper quiz instead. Do not reveal answers yet.");

// =============== 3. Why we started ===============
pres.addSection({ title: "Why it matters" });
S = pres.addSlide({ masterName: "TINT", sectionTitle: "Why it matters" });
S.addText("Why we started Every Shade", { placeholder: "title" });
stat(S, M, 1.9, 3.8, "15%", "of pictures in common medical textbooks show darker skin. Doctors learn mostly from light skin.");
stat(S, 4.75, 1.9, 3.8, "66% vs 90%", "five-year survival for Black patients with melanoma compared with white patients, mostly because it is found later.", 44);
stat(S, 8.9, 1.9, 3.8, "46%", "of melanomas in Black patients were on the palms, soles, or under the nails. Few people think to look there.");
S.addText("Sources: Perlman et al., Int J Womens Dermatol, 2021. Culp and Lunsford, Preventing Chronic Disease (CDC), 2019.", { x: M, y: 6.3, w: W - 2 * M, h: 0.4, fontSize: 12, color: C.text2, margin: 0, isTextBox: true, objectName: "sources" });
S.addNotes("Keep it simple: 'Skin cancer is not rarer on darker skin because it is harmless. It is found later, because people and even doctors are not trained to look for it in the right places. Tonight we fix that for you.' The survival numbers are from a CDC journal. The textbook figure is from a 2021 study of six common medical student resources.");

// =============== 4. What is skin cancer ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Why it matters" });
S.addText("Three kinds of skin cancer", { placeholder: "title" });
card(S, M, 1.8, 3.9, 4.7, "Basal cell", "The most common. Grows slowly. A shiny bump or a sore that keeps coming back. On darker skin it is often brown or black, not pink.", TONES[1]);
card(S, 4.7, 1.8, 3.9, 4.7, "Squamous cell", "A rough, scaly patch or a sore that will not heal. On darker skin it often shows up in an old scar, burn, or long-lasting sore.", TONES[3]);
card(S, 8.8, 1.8, 3.9, 4.7, "Melanoma", "The most serious. Can spread if not caught early. A dark spot that is new or changing. On darker skin: palms, soles, under nails.", TONES[5]);
S.addNotes("Say the names once, then move on. The point is: 'There are three main kinds. Two are common and very treatable. The third, melanoma, is the one we most want to catch early, and it is the one that hides on palms, soles, and under nails.'");

// =============== 5. Myth vs fact ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "Why it matters" });
S.addText("Everyone can get skin cancer", { placeholder: "title" });
card(S, M, 1.8, 5.9, 4.7, "Myth", "\"Dark skin doesn't get skin cancer.\"\n\n\"If it doesn't hurt, it's nothing.\"\n\n\"It only happens where the sun hits.\"", null, { fill: "FFFFFF", bodySize: 22 });
card(S, 6.85, 1.8, 5.9, 4.7, "Fact", "Melanin gives some protection, but every skin tone can get skin cancer.\n\nMost skin cancers do not hurt at first.\n\nOn darker skin, melanoma often appears where the sun never reaches.", null, { fill: "FFFFFF", bodySize: 20 });
S.addNotes("Ask the room: 'Who has heard that darker skin cannot get skin cancer?' Let people answer. Then: 'Melanin does help against the sun, but not against every kind. And the kind that hides on palms and soles has nothing to do with sun.'");

// =============== 6. Risk ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Why it matters" });
S.addText("What raises your risk", { placeholder: "title" });
bullets(S, ["Sunburns in the past, or many years outdoors or in tanning beds", "Age over 50", "A parent, brother, sister, or child who had melanoma", "Many moles, or a spot that has already been treated", "A weak immune system (for example after a transplant)", "An old scar, burn, or sore that has lasted a long time"], { x: M, y: 1.8, w: 7.6, h: 4.9, fontSize: 22, gap: 8 });
card(S, 8.7, 1.8, 4.0, 4.7, "Even with no risk factors", "Check your skin once a month. Most melanomas on darker skin are found on people with none of these.", TONES[4], { headSize: 22, bodySize: 20 });
S.addNotes("Go through the list quickly. Emphasize age: 'Just being over 50 is a reason to look once a month.' Emphasize the scar point for darker skin: squamous cell cancers on darker skin often start in a scar or a sore that never healed.");

// =============== 7. Melanoma: lighter skin ===============
pres.addSection({ title: "What to look for" });
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What to look for" });
S.addText("Melanoma on lighter skin: the ABCDEs", { placeholder: "title" });
imageBox(S, M, 1.8, 5.6, 4.7, "Melanoma on lighter skin: an uneven brown/black spot", "Use a licensed image: AAD public gallery, Skin Cancer Foundation, or the Full Spectrum of Dermatology atlas");
bullets(S, ["A: Asymmetry. One half does not match the other", "B: Border. Edges are ragged or blurred", "C: Color. More than one color, or changing", "D: Diameter. Bigger than a pencil eraser", "E: Evolving. Changing in size, shape, color, or feel"], { x: 6.6, y: 1.8, w: 6.1, h: 4.8, fontSize: 22, gap: 10 });
S.addNotes("Explain ABCDE slowly. Then say: 'E, evolving, is the most important letter. A spot that is changing is a spot to show a doctor, whatever it looks like.' IMAGE: replace the placeholder with a licensed photo before the talk.");

// =============== 8. Melanoma: darker skin ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "What to look for" });
S.addText("Melanoma on darker skin looks different", { placeholder: "title" });
imageBox(S, M, 1.8, 5.6, 4.7, "Melanoma on a palm or sole (acral melanoma) on brown or Black skin", "Use a licensed image: Full Spectrum of Dermatology atlas (jddonline.com/project-atlas) or AAD skin-of-color gallery");
bullets(S, ["Often very dark brown or black, but can be purple, gray, or even pink", "Most often on the palms, the soles, between the toes, or under a nail", "Can look like a bruise or a stain that does not fade", "Usually does not hurt", "Any new dark spot in these places is worth a doctor visit"], { x: 6.6, y: 1.8, w: 6.1, h: 4.8, fontSize: 22, gap: 10 });
S.addNotes("This is the heart of the talk. Say: 'If you remember one thing tonight, remember this: on darker skin, melanoma likes the palms, the soles, and the nails. A dark spot there that you did not have before, or a bruise that never fades, should be looked at.' IMAGE: replace placeholder with a licensed photo.");

// =============== 9. The spots people miss ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What to look for" });
S.addText("The spots people miss", { placeholder: "title" });
const miss = [["Palms", "Both hands, and between the fingers"], ["Soles", "The bottom of each foot and the heels"], ["Between the toes", "Spread them apart in good light"], ["Under the nails", "Fingernails and toenails, with polish off"]];
miss.forEach((m, i) => card(S, M + i * 3.1, 1.8, 2.9, 3.2, m[0], m[1], TONES[i + 1], { headSize: 24, bodySize: 19 }));
S.addText("Also: scalp, ears, inside the mouth, and anywhere a helper has to look for you.", { x: M, y: 5.3, w: W - 2 * M, h: 1.0, fontSize: 22, color: C.text1, margin: 0, isTextBox: true, valign: "middle", objectName: "also" });
S.addNotes("Have everyone look at their palms right now. Say: 'Go ahead, look at your palms. Now you have done part of a skin check.' It gets a laugh and it builds the habit.");

// =============== 10. Nails ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "What to look for" });
S.addText("A dark line in a nail", { placeholder: "title" });
imageBox(S, M, 1.8, 5.6, 4.7, "A dark band running the length of a fingernail or toenail", "Use a licensed image; many people with darker skin have harmless nail bands, so choose one showing a worrying band (wide, uneven, nail-fold darkening)");
bullets(S, ["Many people with darker skin have harmless thin lines in their nails", "See a doctor if a line is new, getting wider, darker, or uneven", "Or if the skin next to the nail turns dark", "Or if the nail splits, lifts, or bleeds near the line", "A new line in only one nail, after age 50, deserves a look"], { x: 6.6, y: 1.8, w: 6.1, h: 4.8, fontSize: 22, gap: 10 });
S.addNotes("Balance this carefully: many people in the room will have harmless nail bands and may worry. Say: 'Thin, even lines that have been there for years are usually fine. What we care about is a NEW line, a WIDENING line, or dark color spreading onto the skin around the nail.' IMAGE: replace placeholder.");

// =============== 11. Other skin cancers on every tone ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "What to look for" });
S.addText("The other skin cancers, on every tone", { placeholder: "title" });
card(S, M, 1.8, 3.9, 4.7, "Lighter skin", "A pink, pearly, or shiny bump. A rough, scaly patch. A sore that bleeds, scabs, and comes back.", TONES[0]);
card(S, 4.7, 1.8, 3.9, 4.7, "Medium skin", "A brown, tan, or shiny bump. A scaly patch that is darker than the skin around it.", TONES[2]);
card(S, 8.8, 1.8, 3.9, 4.7, "Darker skin", "A dark, shiny bump that looks like a mole. A sore inside an old scar or burn that will not heal.", TONES[4]);
S.addNotes("Say: 'These two kinds are common and very treatable. The thing to catch is a sore that will not heal after three or four weeks, or a shiny bump that keeps growing.'");

// =============== 12. Ugly duckling ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "What to look for" });
S.addText("Look for the ugly duckling", { placeholder: "title" });
const dots = [[1.2, 2.6, 0.5, TONES[3]], [2.4, 3.6, 0.45, TONES[3]], [3.6, 2.4, 0.5, TONES[3]], [1.6, 4.5, 0.45, TONES[3]], [3.4, 4.4, 0.95, "3D2416"], [4.6, 3.3, 0.5, TONES[3]]];
S.addShape(pres.ShapeType.roundRect, { x: M, y: 1.8, w: 5.2, h: 4.7, rectRadius: 0.18, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 }, objectName: "duckling card" });
dots.forEach((d, i) => S.addShape(pres.ShapeType.ellipse, { x: d[0], y: d[1], w: d[2], h: d[2], fill: { color: d[3] }, line: { color: d[3], width: 0 }, objectName: `dot ${i + 1}` }));
S.addText("One of these is not like the others.", { x: M + 0.3, y: 5.6, w: 4.6, h: 0.7, fontSize: 18, italic: true, color: C.text2, margin: 0, isTextBox: true, objectName: "duckling caption" });
bullets(S, ["Most of your moles look like each other. A spot that stands out from the rest is the one to show a doctor.", "Skin cancer usually does not hurt, itch, or bleed at first.", "Do not wait for pain. Wait for change."], { x: 6.2, y: 1.8, w: 6.5, h: 4.8, fontSize: 24, gap: 16 });
S.addNotes("The ugly duckling idea is easier than ABCDE for many people. Say: 'You do not need to memorize letters. Look for the one spot that is different from all the rest.'");

// =============== 13. How to check at home ===============
pres.addSection({ title: "Check your skin" });
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Check your skin" });
S.addText("The 10-minute skin check, once a month", { placeholder: "title" });
const steps = ["Good light, a full-length mirror, a hand mirror, and a helper if you can", "Face, ears, lips, inside the mouth. Part your hair and check the scalp", "Neck, chest, belly. Lift the breasts and check underneath", "Arms, underarms, both sides of the hands. Palms and between the fingers", "Fingernails and toenails: look for a new dark line", "Back, buttocks, backs of the legs, with the hand mirror or a helper", "Front of the legs, then the feet: soles, heels, between the toes", "Write down anything new. Take a phone photo to compare next month"];
steps.forEach((t, i) => numRow(S, i < 4 ? M : 6.85, 1.8 + (i % 4) * 1.18, 5.9, i + 1, t, 19));
S.addNotes("Walk through it in order. Say: 'This is on the handout we sent your center, so you do not have to memorize it. Same day every month, for example the first of the month. Ten minutes.'");

// =============== 14. Tools & reminders ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "Check your skin" });
S.addText("Make it easy to remember", { placeholder: "title" });
card(S, M, 1.8, 3.9, 4.7, "Pick a day", "The first of the month, or the day your pension or Social Security comes. Put it on the calendar.", TONES[1]);
card(S, 4.7, 1.8, 3.9, 4.7, "Use your phone", "Take a photo of any spot you are watching. Next month, compare. Change is what matters.", TONES[3]);
card(S, 8.8, 1.8, 3.9, 4.7, "Free guide online", "Our step-by-step self-check with monthly reminders. Photos stay on your phone.\n\nzainjaffar06.github.io/everyshade/check", TONES[5], { bodySize: 18 });
S.addNotes("Mention the free online guide once, without pressure: 'If you like using your phone, we built a free guide that walks you through the check and reminds you every month. Nothing you put in it leaves your phone. The address is on your handout.'");

// =============== 15. When to see a doctor ===============
pres.addSection({ title: "Getting care" });
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Getting care" });
S.addText("See a doctor about a spot that is", { placeholder: "title" });
const signs = [["New", "You have not seen it before"], ["Changing", "Size, shape, color, or feel"], ["Bleeding", "Or itching, crusting, or tender"], ["Not healing", "After 3 to 4 weeks"], ["A dark nail line", "New, widening, or spreading to the skin"], ["Different", "The ugly duckling"]];
signs.forEach((s, i) => card(S, M + (i % 3) * 4.1, 1.8 + Math.floor(i / 3) * 2.45, 3.9, 2.25, s[0], s[1], null, { headSize: 26, bodySize: 19 }));
S.addNotes("Read the six words out loud: new, changing, bleeding, not healing, a dark nail line, different. Say: 'You do not have to decide what it is. That is the doctor's job. Your job is to notice and to go.'");

// =============== 16. What happens at the visit ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "Getting care" });
S.addText("What happens at the doctor's office", { placeholder: "title" });
numRow(S, M, 1.9, 12, 1, "The doctor looks at the spot, often with a small magnifying light called a dermatoscope. It does not hurt.", 22);
numRow(S, M, 3.1, 12, 2, "Most spots turn out to be harmless, and you go home reassured.", 22);
numRow(S, M, 4.3, 12, 3, "If the doctor is not sure, they numb the skin and take a tiny sample (a biopsy). It takes a few minutes and heals in about a week.", 22);
numRow(S, M, 5.5, 12, 4, "Found early, most skin cancers are removed in the office and cured.", 22);
S.addNotes("Many seniors avoid the visit because they fear what happens there. Take the fear out: 'It is a look, maybe a tiny sample, done in the office. Found early, it is usually cured right there.' Do not promise outcomes for any individual.");

// =============== 17. Where to go ===============
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Getting care" });
S.addText("Where to go in New Jersey", { placeholder: "title" });
card(S, M, 1.8, 3.9, 4.7, "Have Medicare or insurance", "Call your regular doctor or a dermatologist. A visit for a spot that worries you is covered when it is medically needed.", TONES[1], { bodySize: 19 });
card(S, 4.7, 1.8, 3.9, 4.7, "No insurance", "Community health centers see everyone and charge by what you can pay.\n\nfindahealthcenter.hrsa.gov\nor call 1-877-464-4772", TONES[3], { bodySize: 19 });
card(S, 8.8, 1.8, 3.9, 4.7, "Free skin checks", "The American Academy of Dermatology lists free screening events.\n\naad.org/spotme\n\nOr email us and we will help you find one.", TONES[5], { bodySize: 19 });
S.addNotes("Say the HRSA phone number slowly, twice. The address and number are on the handout. Offer: 'If you are not sure where to go, email or call us and we will find the closest place for you.' (Every Shade: everyshadescreening@gmail.com, 915-400-7072.)");

// =============== 18. Sun protection ===============
S = pres.addSlide({ masterName: "TINT", sectionTitle: "Getting care" });
S.addText("Protecting your skin, at every tone", { placeholder: "title" });
bullets(S, ["Shade between 10 am and 4 pm, especially in summer", "A hat with a brim, and sunglasses", "Sunscreen SPF 30 or higher on skin the sun reaches, every tone included", "Skip tanning beds", "Protect scars and healed sores from the sun"], { x: M, y: 1.8, w: 7.4, h: 4.8, fontSize: 24, gap: 12 });
card(S, 8.5, 1.8, 4.2, 4.7, "Remember", "Sun protection helps, but it does not reach your palms, soles, or nails. Only looking does.", TONES[4], { headSize: 24, bodySize: 21 });
S.addNotes("Keep this short. The main message of the night is checking, not sunscreen. Note for darker skin: SPF still matters, and tinted sunscreens avoid the white cast.");

// =============== 19. Recap ===============
pres.addSection({ title: "Closing" });
S = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Closing" });
S.addText("Three things to take home", { placeholder: "title" });
numRow(S, M, 1.9, 12, 1, "Skin cancer happens on every skin tone. On darker skin it hides on the palms, soles, and under the nails.", 26, 1.4);
numRow(S, M, 3.45, 12, 2, "Check your skin once a month, head to toe, in good light. Ten minutes.", 26, 1.4);
numRow(S, M, 5.0, 12, 3, "A spot that is new, changing, bleeding, not healing, or a new dark nail line: see a doctor. It does not have to hurt.", 26, 1.5);
S.addNotes("Read the three points slowly. Then: 'Now the same ten quiz questions as before, so we can see if we did our job.' LAUNCH THE 'AFTER THE TALK' ZOOM POLL. Give 3 minutes. Paper version for watch-together rooms.");

// =============== 20. Thank you / Q&A ===============
S = pres.addSlide({ masterName: "DARK", sectionTitle: "Closing" });
strip(S, H - 0.18, 0.18);
logo(S, 1.3, 0.7, 1.1, THEME.colors.dk1);
S.addText("every shade", { x: 2.1, y: 0.95, w: 4, h: 0.6, fontSize: 26, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: "wordmark" });
S.addText("Your questions", { placeholder: "title" });
S.addText("everyshadescreening@gmail.com · (915) 400-7072\nWe can help you find a free or low-cost place to get a spot looked at.", { placeholder: "body" });
S.addNotes("Q&A rules: never say what a spot is, even if someone holds it up to the camera. Say: 'I can't tell you what that is, and I would not want to guess wrong. It is exactly the kind of spot to show a doctor, and we will help you find one.' If someone describes bleeding, rapid growth, or a sore that has not healed for months, encourage a visit this month. Thank the center. Ask them to tell friends. Mention we will send the handout and the free guide link.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
