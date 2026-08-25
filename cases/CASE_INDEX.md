# 案例索引

本目录只收录经过人工查看的精选静态 PNG，用来说明深蓝科技风 PPT Agent Skill 的真实输出。它不是完整生产包，也不包含原始脚本、剪辑工程或 uTools 笔记。

## 收录原则

- 只保留 Codex、WorkBuddy 和 MiniMax H3 三套代表案例。
- 每个主题优先保留第 1 张，再补充 2 张能代表截图整合、流程、卡片或技术解释的页面。
- 有现成 contact sheet 时可保留作整套 QA 证据，但 README 不铺开全部页面。
- 只记录能够从现有文件确认的页数、尺寸、来源和 SHA-256。
- 原始剪辑工程与素材保持只读，仓库只保存筛选后的静态案例。
- 不把静态图片案例解释成交互、动画、部署、PDF 或 PPTX 能力证明。

## 案例 A：Codex 从 0 到 1 保姆级教程

| 字段 | 内容 |
|---|---|
| 剪辑工程日期 | 2026-05-27 |
| 来源标识 | `2026.5.27 Codex 新手入门教学/materials/video` |
| 整套页数证据 | 图片页码显示 22 页 |
| 当前确认课件图 | 15 张 `*-terminal-studio.png` |
| 收录图片 | 3 张 |
| 尺寸 | 1920×1080 |

精选文件：

- `cover.png`：原 `01-terminal-studio.png`，第一张。
- `desktop-login.png`：原 `05-terminal-studio.png`，桌面端 App 与官方账号。
- `skill-vs-plugin.png`：原 `15-terminal-studio.png`，Skill 与插件说明。

```text
f1b6506674219ddf372d2caabd4eb7fb856de480c3c80241a32ff2fcbba2fe86  cover.png
f232f8a65d791859dd0201b0880c547b4d759ecbf9812fad4a460358bc7f6927  desktop-login.png
df32d2a3422b7b681c06d38593306dacf5754b847d72d923c308660a39262096  skill-vs-plugin.png
```

## 案例 B：WorkBuddy 新手教学

| 字段 | 内容 |
|---|---|
| 生成日期 | 2026-07-31 |
| 输出版本 | workbuddy-deepblue-v1-r1 |
| 总页数 | 36 |
| 单页尺寸 | 1920×1080 |
| 收录原因 | 长教程拆页、真实界面截图、功能说明和自动化边界 |

精选文件：

- `cover.png`：第 1 页。
- `home-overview.png`：第 9 页。
- `automation.png`：第 30 页。
- `contact-sheet.png`：36 页联系表。

```text
5df0d961b1af0ed805abc07ce030fea22414c425b9b0f6f4c4cae05500de5fa9  automation.png
ee9df3a22b9d3b1f410ac10c642cac8c9f9ad2dc738ec73e301a979f49640782  contact-sheet.png
49c402a5aa1fa17d19a0e7a3a68201c97887bea0e667f3d7f069bb17afb1cc06  cover.png
164aabc66be61f70a2a5b86f13749328fc1bc2db5ea60b4f7cec630482a2a2bb  home-overview.png
```

## 案例 C：MiniMax H3 本地部署喂饭级教程

| 字段 | 内容 |
|---|---|
| 生成日期 | 2026-08-10 |
| 输出版本 | r20260810-121700 |
| 总页数 | 32 |
| 单页尺寸 | 1920×1080 |
| 收录原因 | 本地部署环境、节点工作流、模型模块和操作结论 |

精选文件：

- `cover.png`：第 1 页。
- `workflow.png`：第 11 页。
- `h3-system.png`：第 29 页。
- `contact-sheet.png`：32 页联系表。

```text
92fc18a2ca9675ccd89f4ce8aa3a1a5c64db52db424d8c467ead86a3fffefe65  contact-sheet.png
04568a6ec111daa68567c5bf8db13876e94361527b511cef2d98f95ab308f99a  cover.png
35631a9e7a251f23bfcc6b05ed5298b6ca73bda9273004064c673f32f7e9ab4f  h3-system.png
1b740bc5bc360c9f84bcf5be0f55b8d7566aade6dec9ae151f6217e5d9879603  workflow.png
```

## 公开展示边界

这些图片可用于：

- 仓库 README 效果展示；
- 风格回归；
- 比例、安全区和标题参考；
- 新版本输出的人工对照。

维护和新增案例时必须确认：

- 图片由维护者制作，或具备公开展示所需授权；
- 页面不含账号、密钥、真实业务资料或临时链接；
- 产品名称、商标和界面截图仅用于教程说明，不暗示官方背书；
- 案例图片适用 [cases/LICENSE.md](LICENSE.md) 的保留版权条款，不跟随根目录 MIT License。

这些图片不应用于：

- 伪装成新任务生成结果；
- 替代真实源稿的事实检查；
- 证明未实际完成的交互、动画或格式能力；
- 作为第三方品牌素材包或官方模板再次分发。
