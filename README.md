# saki-pptx

将当次用户提供的技术路线图、流程图或架构图重建为可编辑 PowerPoint，并执行图片比例、对象越界、内容清单和渲染预览检查。

仓库名称：`saki-pptx-skill` · Skill 名称：`saki-pptx` · 当前发布版本：`v0.1.0`。

本 Skill 已由作者在 ChatGPT 中实际使用验证。`v0.1.0` 保留已验证的操作流程、参考规范和脚本逻辑，仅统一命名并补充发布说明。使用平台为 ChatGPT，未指定具体底层模型版本；其他模型或平台的使用效果尚未验证。

## 文件结构
- `SKILL.md`：主工作流程、质量门禁及数据保护约束
- `references/`：通用输入、截图、排版和验收规范
- `examples/`：完全虚构的占位示例，不含真实项目数据
- `scripts/`：本地检测脚本（Python，依赖 `python-pptx`、`Pillow`）
- `requirements.txt`：辅助脚本依赖清单
- `CHANGELOG.md`：发布版本记录

## 使用环境
- ChatGPT 需具备读取上传图片/PPT、执行代码及生成文件的能力；实际可用能力以当前环境为准。
- 辅助脚本需要 Python；本地运行时可使用 `python -m pip install -r requirements.txt` 安装依赖。
- 实际 PPT 渲染仍需要环境提供相应工具，Python 依赖不包含 PowerPoint 或 LibreOffice。

## 数据保护
- 本仓库只包含通用规则、代码和占位示例，**不包含**原始用户提示词、项目图片、PPT、内容清单、日志、实际裁剪图、质量报告、私人绝对路径或用户资料。
- 运行时可以读取当前任务的图片或 PPT，但除非用户明确要求，不要把输入文件、裁剪图、manifest、检测报告和渲染图写回本 Skill 的目录或下一次分享的 ZIP。
- 如果需要分享已生成的 PPT、示例或测试文件，须由用户单独批准并自行审核具体内容。
- 安装本地 Skill 的实际步骤以当前 ChatGPT 的界面及账户权限为准。

## 使用示例
“使用 saki-pptx，按这次上传的图片制作可编辑 PPTX，并提供 PNG 预览与检查结果。”

## 使用限制
自动检查可以检测图片拉伸、边界越界等，但无法自动保证每一个裁剪图块在语义上完整；需要人工目视核查。

## 后续打包与更新
- 发布包可按版本命名为 `saki-pptx-v0.1.0.zip`，用于直接上传到 ChatGPT 安装。
- ZIP 根目录直接包含 `SKILL.md`、`LICENSE`、`requirements.txt` 及资源目录，不添加外层 `saki-pptx/` 文件夹。手动安装到目录时，目录名统一为 `saki-pptx`。
- 精简安装包保留 `SKILL.md`、`references/`、`scripts/`、`examples/`、`requirements.txt` 和 `LICENSE`。示例被参考文档引用，应随包保留。
- `README.md`、`CHANGELOG.md` 用于仓库展示和版本维护，默认不放入精简安装包。
- 任务输入、生成的 PPT、预览、裁剪图、报告、日志和缓存不放入安装包。
- 后续版本继续使用相同 Skill 名称，通过发布版本号及 `CHANGELOG.md` 记录变化。升级前保留旧版，任务产物存放在 Skill 目录之外。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。分发时请保留版权声明和许可文本。
