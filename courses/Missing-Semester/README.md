# The Missing Semester · 2026

从零重新学习 MIT **The Missing Semester of Your CS Education**，中文常译为“计算机教育中缺失的一课”。目标是理解开发工具的工作方式，能自己完成常见任务，并能解释所用命令。

课程版本：2026。开始日期：2026-10-02。练习先使用现有的 macOS / Zsh 环境；脚本涉及 Bash 时会明确说明。

- [官方课程目录](https://missing.csail.mit.edu/2026/)
- [学习进度与问题记录](progress.md)
- [常用符号英文名称速查](notes/symbols.md)：标点、括号、路径与运算符号、常见组合和易混字符。
- [正则表达式与通配符](notes/regex-and-globs.md)：glob / regex 的区别、基础语法、引号与 grep 用法。
- [SSH 日志管道命令详解](notes/ssh-log-pipeline.md)：远程执行、正则提取、频次统计、前十名筛选与 macOS 示例。
- [第一讲视频时间索引与字幕校正](source/01-shell-video.md)
- [第一讲英文字幕](source/01-shell.en.srt)：保留原始转写，用于核对讲解；术语和命令与官方讲义一起确认。
- [第二讲来源与字幕核对](source/02-command-line-source.md)：原始中英字幕、覆盖范围及转写误词说明。

第一讲完整笔记汇总课程动机、Terminal 与 Shell、命令与路径、文本工具、管道与重定向，以及基础 Bash 脚本。符号、正则与通配符、SSH 日志管道的细节可结合上面的补充笔记查阅。

第二讲的 [完整笔记](notes/02-command-line.md)与 [实践题](exercises/02-command-line.md)接着整理命令行接口、环境传递、退出码、信号、远程环境与配置；原始字幕见 [英文](source/02-command-line.en.srt)和 [中文](source/02-command-line.zh.srt)。

## 现在从这里开始

1. 阅读正在复习的完整笔记：[第一讲](notes/01-shell.md) · [第二讲](notes/02-command-line.md)，先了解整课主线，再回看不熟悉的概念与例子。
2. 按需要选择对应练习：[第一讲](exercises/01-shell.md) · [第二讲](exercises/02-command-line.md)，先预测，再运行并解释。
3. 在当前学习 chat 中贴出命令、输出和你的解释；根据实际掌握情况更新进度。

完整笔记可作为整课复习和随时查阅的资料；练习按概念选择，不规定学习次数。材料已准备好，完成状态仍以实际练习与解释为准。

## 九讲路线

| 顺序 | 2026 官方讲义 | 学习目标 | 当前资料 |
| --- | --- | --- | --- |
| 01 | [课程概览与 Shell 入门](https://missing.csail.mit.edu/2026/course-shell/) | 理解命令、路径、程序查找、文本工具、管道与简单脚本 | [笔记](notes/01-shell.md) · [练习](exercises/01-shell.md) |
| 02 | [命令行环境](https://missing.csail.mit.edu/2026/command-line-environment/) | 理解命令行程序的输入输出、环境、退出码、信号与配置 | [笔记](notes/02-command-line.md) · [练习](exercises/02-command-line.md) |
| 03 | [开发环境与工具](https://missing.csail.mit.edu/2026/development-environment/) | 学习 Vim、语言服务、编辑器功能与 AI 辅助开发 | 学到本讲时整理 |
| 04 | [调试与性能分析](https://missing.csail.mit.edu/2026/debugging-profiling/) | 定位错误、观察运行状态、识别性能瓶颈 | 学到本讲时整理 |
| 05 | [版本控制与 Git](https://missing.csail.mit.edu/2026/version-control/) | 理解提交、分支、合并与协作 | 学到本讲时整理 |
| 06 | [代码打包与交付](https://missing.csail.mit.edu/2026/shipping-code/) | 理解依赖、运行环境、打包与交付流程 | 学到本讲时整理 |
| 07 | [Agentic Coding](https://missing.csail.mit.edu/2026/agentic-coding/) | 为编码代理组织任务、提供上下文并验证结果 | 学到本讲时整理 |
| 08 | [代码之外](https://missing.csail.mit.edu/2026/beyond-code/) | 理解软件开发中的沟通、文档与项目工作 | 学到本讲时整理 |
| 09 | [代码质量](https://missing.csail.mit.edu/2026/code-quality/) | 使用格式化、静态检查、测试等方法改进代码 | 学到本讲时整理 |

Vim 在第 3 讲中，届时单独练习其模式、移动和编辑组合。需要深入时再补充课程链接的 [2020 年 Vim 专讲](https://missing.csail.mit.edu/2020/editors/)。

## 每次怎样学

每次围绕一个小目标进行：先讲清概念，再预测命令结果，动手验证，最后用自己的话解释。卡住时保留原始输出，记录“预期是什么、实际是什么、差别在哪里”。

优先使用系统已有工具。新工具在遇到实际问题时再尝试。若命令在 macOS 和 Linux 上不同，笔记中分别说明。

## 目录

```text
Missing-Semester/
├── README.md                 # 课程入口与九讲路线
├── progress.md               # 已完成的小目标与待解决问题
├── notes/
│   ├── 01-shell.md           # 第一讲完整笔记与命令示例
│   ├── 02-command-line.md    # 第二讲完整笔记与命令示例
│   ├── symbols.md            # 常用符号的英文名称与使用提醒
│   ├── regex-and-globs.md    # 正则表达式与通配符的对照总结
│   └── ssh-log-pipeline.md   # 截图中的 SSH 日志统计管道详解
├── exercises/
│   ├── 01-shell.md           # 第一讲分步练习与结果记录模板
│   └── 02-command-line.md    # 第二讲实践与纸上拆解
└── source/
    ├── 01-shell.en.srt       # 用户提供的第一讲英文字幕
    ├── 01-shell-video.md     # 字幕来源、时间索引与术语校正
    ├── 02-command-line.en.srt # 第二讲原始英文字幕
    ├── 02-command-line.zh.srt # 第二讲原始中文字幕
    └── 02-command-line-source.md # 第二讲来源与字幕核对
```

## 来源与许可

课程由 Anish Athalye、Jon Gjengset 和 Jose 团队教授。[官方讲义、视频与练习](https://missing.csail.mit.edu/2026/)采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，详见[课程许可说明](https://missing.csail.mit.edu/license/)。本目录的课程笔记与练习在其基础上重新组织、用中文解释并加入原创例子、平台差异说明和学习记录，也采用 CC BY-NC-SA 4.0。它们是个人学习材料，不是官方讲义的逐字翻译。
