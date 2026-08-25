# 参与贡献

感谢你改进深蓝科技风 PPT Agent Skill。这个项目优先接受能够提升静态演示图片稳定性、内容准确性和视觉一致性的改动。

## 贡献范围

适合提交：

- 修正文档、安装说明和真实能力边界；
- 改进 16:9、1:1 母版的兼容性与可访问性；
- 加强标题、字体、图片、画布和安全区门禁；
- 补充能够复现真实问题的测试；
- 在来源与授权清晰的前提下改进案例说明。

不应把交互导航、动画、在线部署、PDF 或 PPTX 能力直接加入现有 Terminal Studio profile。确需扩展时，请先通过 Issue 说明使用场景、依赖、兼容性和验证方案，并使用新的 profile 名称。

## 本地验证

```bash
npm ci
python3 scripts/validate_style.py assets/terminal-studio-16x9.html
python3 scripts/validate_style.py assets/terminal-studio-1x1.html
python3 scripts/verify_rendered_style.py assets/terminal-studio-16x9.html
python3 scripts/verify_rendered_style.py assets/terminal-studio-1x1.html
python3 scripts/test_validate_style.py
python3 scripts/test_rendered_style.py
```

还应运行：

```bash
git diff --check
npm audit --package-lock-only
```

## Pull Request 要求

- 说明问题、修改范围和可观察结果；
- 不改变未在 PR 中声明的锁定 token；
- 新增或修改运行逻辑时同步补充回归测试；
- 不提交密钥、Cookie、账号、数据库、绝对本机路径、原始脚本、剪辑工程或缓存；
- 不提交来源或公开展示权不清晰的案例图片；
- README、`SKILL.md` 和实际实现必须保持一致；
- 保持静态 image-first 定位，不把计划中的功能写成已完成功能。

## 许可证

提交到代码、Skill、模板、脚本和文档区域的贡献将按根目录 [MIT License](LICENSE) 发布。案例 PNG 不适用 MIT，提交前必须先确认 [cases/LICENSE.md](cases/LICENSE.md) 的授权边界。
