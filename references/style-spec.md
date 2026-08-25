# Terminal Studio Style Spec

## Visual Identity

This style is for polished Chinese software tutorial videos. It should feel like a premium developer tool tutorial, not a generic PPT template.

Core feeling:

- deep blue-black terminal studio
- calm technical confidence
- elegant and restrained
- useful as a video insert frame
- consistent across software tutorials and local AI deployment guides

## Palette

Use this palette unless the user explicitly asks for another brand color:

```css
:root {
  --bg-primary: #0b0f17;
  --bg-secondary: #151b25;
  --bg-card: rgba(246, 241, 231, 0.075);
  --bg-card-strong: rgba(246, 241, 231, 0.13);
  --text-primary: #f7f2ea;
  --text-secondary: #b9c2ce;
  --text-muted: #7f8a99;
  --accent: #77d7ff;
  --accent-2: #f4c76b;
  --accent-3: #78f0b7;
  --danger: #ff6b6b;
  --line: rgba(246, 241, 231, 0.16);
  --line-strong: rgba(119, 215, 255, 0.42);
  --shadow: 0 30px 120px rgba(0, 0, 0, 0.42);
}
```

Avoid:

- neon green as the dominant accent
- purple-blue gradient hero pages
- beige paper/card notebook designs
- flat black backgrounds with no depth
- bright SaaS gradients

## Typography

Use:

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Noto+Sans+SC:wght@400;500;700;800;900&display=swap" rel="stylesheet" />
```

Rules:

- The default profile is `terminal-studio-16x9-v1`; use `assets/terminal-studio-16x9.html`. For a square deck, use `terminal-studio-1x1-v1` and `assets/terminal-studio-1x1.html`. Do not recreate either visual foundation from memory.
- Main headings: `Noto Sans SC`, weight `900`, letter spacing `-0.045em`, line height `1.08`.
- Use the following locked title tokens exactly unless the user explicitly requests a different visual profile:

```css
:root {
  --font-sans: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-mono: "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, monospace;
  --main-title-family: var(--font-sans);
  --main-title-weight: 900;
  --main-title-letter-spacing: -0.045em;
  --main-title-line-height: 1.08;
  --title-size: clamp(3.7rem, 6vw, 6.4rem);
  --h2-size: clamp(3rem, 5vw, 5.3rem);
  --h3-size: clamp(1.2rem, 1.7vw, 1.8rem);
  --body-size: clamp(1rem, 1.45vw, 1.5rem);
  --small-size: clamp(0.72rem, 0.9vw, 0.95rem);
  --slide-padding: clamp(3rem, 5.2vw, 6rem);
  --content-gap: clamp(1rem, 2vw, 2.2rem);
}

.title,
.cover-title {
  font-family: var(--main-title-family);
  font-weight: var(--main-title-weight);
  letter-spacing: var(--main-title-letter-spacing);
  line-height: var(--main-title-line-height);
  text-wrap: balance;
}

.cover-title { font-size: var(--title-size); max-width: min(82vw, 1500px); }
.title { font-size: var(--h2-size); max-width: min(86vw, 1550px); }
```

- These values are a visual identity contract, not suggestions. Do not replace negative tracking with positive tracking, shrink the title scale, or define a second title system for a special page.
- Cover slides may accent one semantic title segment with cyan/blue, for example `.title-accent { color: var(--accent); text-shadow: 0 0 24px rgba(119, 215, 255, 0.28); }`. The accent must inherit the same title font, weight, line-height, and spacing; use it for the opening promise, not as a general multicolor-title habit.
- Quote, closing, chapter, and other special slides must inherit the same main-title contract and locked size as ordinary content slides. They may add a quote mark or accent line, but changing the H1/H2 size requires an explicitly named new profile and must not be labeled as either locked v1 profile.
- Avoid isolated title classes such as `.quote-text` unless they explicitly inherit the same title tokens. If a special title looks thinner, wider, system-font-like, or visually disconnected from the deck, treat it as a delivery-blocking bug.
- Labels, slide numbers, terminal snippets: `JetBrains Mono`.
- Use `clamp()` for all major sizes.
- Do not use viewport-width-only font scaling.
- Chinese H1/H2 line breaks are manually designed. Do not rely on arbitrary browser wrapping for large headings.
- Avoid single-character or suffix-only title lines. Bad: `为什么要给书起别` / `名？`; bad: `项目本质：小说平台` / `推荐`; bad: `回填：视频发完后的` / `打卡留痕`.
- Prefer semantic chunks with enough visual weight on both lines. Good: `为什么要给书` / `起别名？`; good: `项目本质` / `小说平台推荐`; good: `视频发完后` / `记得回填留痕`.
- Do not split 2-3 character words or labels into their own H1/H2 line, such as `回填`, `推荐`, `留痕`, unless the slide is intentionally a centered keyword card.
- For long headings, either shorten the copy or insert explicit `<br>` at a phrase boundary that leaves both lines substantial. CSS `text-wrap: balance` may help, but it does not replace manual breaking.
- H1/H2 blocks default to visual centering: `text-align: center`, centered max-width, and balanced line lengths. Use left-aligned titles only for an intentional two-column explainer where the opposite side carries a screenshot, terminal block, or panel.

### Font loading gate

- Include the Google Fonts link above or equivalent local `@font-face` declarations for both font families.
- Wait for `document.fonts.ready` and all images before export.
- Do not rely on `document.fonts.check()` alone: browsers may return `true` because a fallback can render the text.
- Inspect `[...document.fonts]` and require loaded `FontFace` entries for `Noto Sans SC` weight 900 and `JetBrains Mono` weight 700.
- The canonical asset also checks browser-computed title family, weight, size, tracking, line-height, max-width, alignment, root font size, and `.title-accent` inheritance on every visible page.
- Run both `scripts/validate_style.py` and `scripts/verify_rendered_style.py`. If either fails, stop the export and report the failure. Do not silently accept `PingFang SC`, Microsoft YaHei, Arial, a late CSS override, or another fallback as the final render.

## Background

Use layered backgrounds:

```css
.slide {
  background:
    radial-gradient(circle at 82% 16%, rgba(119, 215, 255, 0.14), transparent 28%),
    radial-gradient(circle at 17% 82%, rgba(244, 199, 107, 0.08), transparent 26%),
    linear-gradient(135deg, #080b11 0%, #111722 48%, #0b0f17 100%);
}

.slide::before {
  background-image:
    linear-gradient(rgba(176, 255, 198, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(119, 215, 255, 0.035) 1px, transparent 1px);
  background-size: clamp(28px, 3.5vw, 56px) clamp(28px, 3.5vw, 56px);
}
```

Add a subtle rounded border inset around each slide.

## Signature Elements

Every slide should usually include:

- top or center `kicker` pill: `02 / 主题`
- large low-opacity number in bottom-right: `01`, `02`, etc.
- bottom-left micro summary
- bottom-right slide count: `01 / 16`
- one clear focal point

Kicker style:

```css
.kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgba(216, 255, 224, 0.06);
  color: var(--accent);
  font-family: var(--font-mono);
  font-weight: 700;
}
```

## Layout Patterns

Use a small set of repeatable patterns:

- **Cover centered**: centered kicker, big title, one short subtitle, 2-3 chips. Use one restrained cyan/blue `.title-accent` segment when it strengthens the opening hook.
- **Route timeline**: 4 cards across, each with step label, title, one-line explanation.
- **Two-column explainer**: title/copy on one side, terminal block or screenshot on the other. Left alignment is allowed here, but the whole composition should still feel centered and intentional.
- **Comparison**: 2 cards, one for old way, one for new way.
- **Three-card grid**: 3 equal cards for tools, concepts, or choices.
- **Checklist**: 2x2 risk/control points.
- **Closing quote**: centered strong quote with one accent line.

Avoid more than 4 cards unless the slide is specifically a timeline. Do not nest cards inside cards.

## Screenshot Treatment

Screenshots should not fill the entire slide. Put them in a dark frame:

```css
.screenshot {
  border: 1px solid var(--line);
  border-radius: 1.2rem;
  background: rgba(5, 8, 13, 0.78);
  box-shadow: var(--shadow);
  padding: 0.7rem;
}
```

Add a small mono caption under the image.

## Content Rules

- One slide = one teaching point.
- Prefer 8-18 Chinese characters for main headings when possible.
- Body text should be short enough to read in video editing.
- Avoid visible instructional text like "这里展示..." unless it is part of the slide's real teaching content.
- Use direct, practical wording.
- Keep operational examples faithful to the source. If the user provides a real platform share口令, do not convert it into made-up placeholders like `video_id / share_code / short_key` unless that is truly how the platform works.
- For short-video回填 examples, say the user should keep only the platform-required effective short link, usually the `https`-starting link segment inside the copied share text. Do not display the exact user-provided URL in the slide unless asked.
- Contrast it against the wrong action: copying the full share口令, title, hashtags, "复制此链接" instructions, or unrelated extra text.
- Before export, scan every H1/H2 visually at 1920x1080 and fix awkward Chinese breaks. A slide is not deliverable if a title leaves a lonely character, punctuation mark, or broken semantic phrase on a separate line.
- A slide is also not deliverable if manual `<br>` creates an ugly 2-3 character title line that could be solved by shorter copy, centered layout, or a more balanced phrase split.
- For glossary,名词解释, concept-map, or knowledge-map source material, extract the complete core term list before designing. Every term must appear in the exported slides with at least a short audience-facing explanation, not only as a name in an overview or final recap.

## Quality Checklist

Before delivery:

- `python3 scripts/validate_style.py <presentation.html>` and `python3 scripts/verify_rendered_style.py <presentation.html>` both pass for the selected profile.
- No page is an error screenshot.
- Text does not overlap with the large background number.
- All slides fit in 1920x1080.
- Contact sheet shows consistent style across the whole set.
- Cover, screenshot slide, card slide, and closing slide have been inspected.
- Every multi-line Chinese title has been inspected for semantic line breaks.
- Every special title treatment, including quote, chapter, and closing slides, has been checked against the normal content-slide title style.
- Browser-computed title styles match the locked profile: `Noto Sans SC`, `900`, `-0.045em`, and `1.08`.
- If the source has an explicit term list, all terms have been counted and verified against visible slide copy.
