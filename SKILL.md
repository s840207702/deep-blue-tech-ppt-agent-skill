---
name: deep-blue-tech-ppt
description: "Use when creating or revising static, image-first Chinese tutorial slides from scripts or Markdown in Feige's 深蓝科技风 PPT / Terminal Studio style. Covers content splitting, source accuracy, built-in 16:9 and 1:1 profiles, static HTML rendering, PNG/contact-sheet export through the host agent, Chinese title QA, and immutable output bundles. It is not an interactive slide runtime, animation toolkit, public deployment workflow, PDF exporter, or editable PPTX workflow."
---

# 深蓝科技风 PPT

## 目标

把中文脚本、Markdown、教程提纲或已经确认的内容结构，制作成适合视频剪辑和内容发布的静态深蓝科技风演示图片。

这是 image-first Skill：

- HTML 是静态排版和浏览器渲染载体。
- PNG 是默认交付物。
- contact sheet 用于整套视觉复盘。
- 除非用户明确提出其他格式，否则不生成可编辑的 `.ppt` / `.pptx`。

本 Skill 不把键盘导航、触摸滑动、导航圆点、页面动画、在线部署或 PDF 导出作为默认能力和交付要求。

开始设计前读取：

- [references/style-spec.md](references/style-spec.md)：深蓝视觉、标题、布局和截图规范。
- [references/viewport-base.css](references/viewport-base.css)：固定画布和溢出控制。
- [references/html-template.md](references/html-template.md)：静态 HTML 渲染结构和 `?slide=N` 导出方式。

16:9 默认从 [assets/terminal-studio-16x9.html](assets/terminal-studio-16x9.html) 复制并改写内容；1:1 默认从 [assets/terminal-studio-1x1.html](assets/terminal-studio-1x1.html) 开始。不要从空白 HTML 重新发明主题。生成后依次运行源码门禁和真实浏览器门禁：

```bash
python3 scripts/validate_style.py <presentation.html>
python3 scripts/verify_rendered_style.py <presentation.html>
```

真实浏览器门禁使用 Playwright。若当前环境没有提供 Playwright，在 Skill 目录运行 `npm ci` 安装锁定的开发期 QA 依赖；若没有可用浏览器，再运行 `npx playwright install chromium` 或设置 `CHROME_PATH`。这不会让最终 HTML 或 PNG 依赖 npm。不能因为依赖缺失而静默跳过浏览器门禁。

## 默认输出

- 一个静态 HTML 渲染源。
- 按页导出的 PNG。
- 一张 contact sheet。
- 2–4 张关键页预览。
- 默认画布为 16:9、1920×1080。
- 用户指定 1:1 时，HTML、浏览器 viewport、截图区域和 PNG 统一为 1920×1920。

每次生成、修补或重导都必须使用新的 run id 和新目录，不能覆盖旧 HTML、PNG 或 contact sheet。

## 内容原则

### 一页一个教学点

- 一张图只承担一个核心观点、步骤、判断或视觉事件。
- 内容太多时拆页，不靠缩小字号硬塞。
- 完整中文口播通常需要更多页面来保留节奏；页数由内容决定，不套固定模板。

### 来源准确

- 先读取真实脚本或笔记，不凭经验补造产品入口、按钮、功能、链接或结论。
- 不主动改写用户原稿；页面文案可以压缩，但不能改变操作含义。
- 所有可见文字必须面向观众，不能出现“这页展示”“口播里提到”“观众会看到”等制作备注。
- 账号、分享链接、口令和业务信息默认脱敏，除非用户明确要求原样展示。

### 概念覆盖

- 名词解释、知识地图和分层概念稿先提取完整词表。
- 原稿中有独立段落、关键比喻、操作判断或强结论的内容，优先做成独立页面。
- 交付前对照源稿检查关键术语、操作步骤、风险提醒和结论是否遗漏。

## 视觉原则

- 深蓝黑背景，青色或蓝青色强调，少量冷蓝、紫色或告警色辅助。
- 中文标题使用统一的高字重无衬线字体，标签和页码使用等宽字体。
- 页面保持大面积呼吸空间和一个明确焦点。
- 常用布局包括封面、路线卡片、双栏说明、对比、三卡片、流程、截图页和结尾判断页。
- 截图放入深色圆角框，保留真实界面细节，不让装饰抢过内容。
- 避免廉价渐变、霓虹堆叠、通用 SaaS 模板、Bootstrap 卡片感和无关图库图。

### 默认风格配置不可漂移

默认配置为 `terminal-studio-16x9-v1`；方形配置为 `terminal-studio-1x1-v1`。两个配置共享以下锁定标题基线。除非用户明确要求换风格，否则不能按页面或主题自由改写：

- `Noto Sans SC`，字重 `900`；
- 封面字号 `clamp(3.7rem, 6vw, 6.4rem)`；
- 内容页主标题字号 `clamp(3rem, 5vw, 5.3rem)`；
- 主标题字距 `-0.045em`；
- 主标题行高 `1.08`；
- 封面最大宽度 `min(82vw, 1500px)`；
- 内容页主标题最大宽度 `min(86vw, 1550px)`。

允许变化的是页面内容、语义断行、卡片数量、截图和布局组合；不允许为了“更科技”擅自换成正字距、小标题、紫色渐变、霓虹看板或另一套字体。确需偏离时，先向用户说明偏离项，并使用新的 profile 名称，不能继续标记为 `terminal-studio-16x9-v1`。

## 中文标题门禁

- 主标题按语义手动断行，不能完全依赖浏览器自动换行。
- 不留下单个汉字、标点或很短的语义尾巴。
- 先缩短标题，再决定是否插入 `<br>`。
- 封面可以只强调一个关键词或一行核心承诺。
- cover、chapter、quote、closing 和普通内容页必须共享同一套标题字体、字重、行高与字距。

## 静态 HTML 约定

- 默认使用单个 HTML 文件，CSS 内联；本地图片使用相对路径。
- 每个 `.slide` 固定为目标 viewport，必须 `overflow: hidden`。
- HTML 的目的，是让浏览器稳定渲染指定页面，不要求做成可交互网站。
- 支持 `?slide=N` 只用于导出指定页面。
- 页面不得依赖 npm、Vite 或运行中的开发服务器才能完成默认导出。
- 字体与图片加载完成后再截图。

## 工作流

1. 读取源稿和用户指定的比例、用途及输出位置。
2. 列出页面计划：页码、标题、核心信息和页面类型。
3. 完成来源准确性检查和关键内容覆盖表。
4. 为所有中文主标题确定语义断行。
5. 创建唯一的新输出目录和 run id。
6. 16:9 从 `assets/terminal-studio-16x9.html` 创建，1:1 从 `assets/terminal-studio-1x1.html` 创建；保留锁定 token 和运行时门禁，只替换内容和增加必要布局，不覆盖任何旧输出。
7. 运行 `python3 scripts/validate_style.py <presentation.html>` 检查源码约束；失败时不得导出。
8. 运行 `python3 scripts/verify_rendered_style.py <presentation.html>`，逐页检查浏览器计算后的标题样式和实际已加载 FontFace；失败时不得导出。
9. 等待字体和图片完成加载；字体或计算样式门禁失败时停止，不能静默使用系统字体或覆盖后的 CSS 截图。
10. 使用目标 viewport 逐页导出 PNG。
11. 生成 contact sheet，检查整套节奏和重复布局。
12. 逐张检查封面、截图页、卡片页、流程页、多行标题页和结尾页。
13. 检查全部文件名、尺寸、run id 和计算后标题样式后交付。

## 导出与验收

浏览器导出必须验证真实 PNG，不能只检查 HTML 源码。

最低抽查范围：

- 封面；
- 一张截图或图片页；
- 一张卡片或流程页；
- 所有特殊标题页面；
- 所有多行中文主标题；
- 结尾页。

交付前确认：

- 每张 PNG 尺寸与目标画布一致。
- 没有标题孤字、溢出、遮挡或底部安全区冲突。
- 截图和正文在视频画面中仍可读。
- 页面风格、主标题系统和页码体系一致。
- HTML 同时通过 `scripts/validate_style.py` 与 `scripts/verify_rendered_style.py`，并确认实际渲染使用已加载的 `Noto Sans SC` 与 `JetBrains Mono`。
- source coverage 没有遗漏关键内容。
- 输出路径没有复用旧目录或旧文件名。

## 典型调用

```text
使用 $deep-blue-tech-ppt，把这篇中文教程脚本制作成 16:9 静态演示图片。
每页一个教学点，输出 HTML、1920×1080 PNG 和 contact sheet。
```

```text
使用 $deep-blue-tech-ppt，把这篇 Markdown 制作成 1:1 演示图片。
所有标题按中文语义断行，输出新的不可变版本，不覆盖旧素材。
```
