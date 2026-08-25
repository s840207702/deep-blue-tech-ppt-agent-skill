# Static HTML Render Template

Use this reference when the deliverable is a static PNG slide bundle. For 16:9, copy [../assets/terminal-studio-16x9.html](../assets/terminal-studio-16x9.html). For 1:1, copy [../assets/terminal-studio-1x1.html](../assets/terminal-studio-1x1.html). Replace sample content instead of rebuilding the theme from scratch.

The HTML is a rendering carrier, not an interactive presentation website. It only needs to render one requested slide reliably at the target viewport.

## Content skeleton

This excerpt only shows slide semantics. It is not a standalone template. Keep the selected canonical asset's `<head>`, locked CSS tokens, visible failure gate, slide selector, loaded-FontFace checks, computed-style checks, and `window.__SLIDES_READY__` logic unchanged.

```html
<section class="slide">
  <main class="slide-content">
    <p class="kicker">01 / INTRO</p>
    <h1 class="cover-title">教程标题</h1>
    <p class="subtitle">一句话说明本页内容</p>
  </main>
  <span class="big-number">01</span>
  <footer><span>页面摘要</span><span>01 / 16</span></footer>
</section>

<section class="slide" hidden>
  <main class="slide-content">
    <p class="kicker">02 / TOPIC</p>
    <h2 class="title">内容页标题</h2>
  </main>
</section>
```

## Requirements

- Keep CSS in the HTML unless local project constraints require a separate stylesheet.
- Preserve the exact selected profile and its title tokens. Change content and layout composition, not the identity contract.
- Use relative paths for local screenshots and images.
- Fix every slide to the target viewport and hide overflow.
- Use `?slide=N` only to select the page for browser capture.
- Do not add keyboard controls, touch gestures, navigation dots, progress animation, inline editing or local storage unless the user explicitly requests a separate interactive deliverable.
- Keep the canonical runtime gate and wait for `window.__SLIDES_READY__ === true` before taking the screenshot.
- Require `data-fonts-ready`, `data-style-ready`, and `data-render-ready` to all equal `true`; abort instead of exporting a fallback-font or CSS-overridden render.
- Keep the visible `REQUIRED STYLE, FONTS, OR IMAGES NOT READY — DO NOT EXPORT` gate. It prevents a premature or invalid screenshot from looking deliverable.
- Run `python3 scripts/validate_style.py <presentation.html>` before export.
- Run `python3 scripts/verify_rendered_style.py <presentation.html>` before export.
- Export every page at the exact requested pixel dimensions.
- Inspect the rendered PNG and contact sheet; source-code review alone is insufficient.

## Export cleanup

The captured page must not show:

- browser controls;
- edit controls;
- hover or focus state;
- debug outlines;
- loading placeholders;
- production notes;
- cursor or selection state.
