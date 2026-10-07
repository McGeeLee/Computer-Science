# 第二讲 · 来源与字幕核对

对应 [2026 年官方第二讲：Command-line Environment](https://missing.csail.mit.edu/2026/command-line-environment/)。完整总结见 [第二讲笔记](../notes/02-command-line.md)。

用户提供的两份字幕按原始字节保存，未调整分段、时间、拼写或翻译：

| 保存文件 | 原始文件名 | 字节数 | 字幕段数 | 最后一段结束时间 |
| --- | --- | ---: | ---: | --- |
| [英文字幕](02-command-line.en.srt) | `[English] Lecture 2 Command-line Environment [DownSub.com].srt` | 86,836 | 1,086 | 01:06:18,774 |
| [中文字幕](02-command-line.zh.srt) | `P2 命令行环境_哔哩哔哩_bilibili_BV1CkArz1E4o_字幕.srt` | 87,524 | 1,388 | 01:06:19,000 |

中文文件名对应 [B 站视频入口](https://www.bilibili.com/video/BV1CkArz1E4o/)，其中 P2 标识第二讲。英文文件名保留用户提供的 DownSub 标识。这里的结束时间仅说明字幕覆盖范围，不代表视频总时长；两份字幕的分段和时间有细微差异。

## 核对依据

字幕提供讲解上下文，不能直接充当命令代码。整理时对照两份字幕与官方讲义，命令参数和平台差异再用本机手册或工具官方文档确认。视频与讲义的内容并不完全重合；笔记区分课堂讲解与讲义补充，不把每项讲义示例都归为视频中的演示。

| 字幕中的写法 | 核对后的理解 |
| --- | --- |
| `globin` | `globbing`：Shell 在调用程序前展开文件名模式 |
| “安全单元” | Secure Shell，工具名为 `ssh`，简称 SSH |
| `c t stop` | `SIGTSTP`，终端中 `Ctrl-Z` 通常触发的暂停信号 |
| 退出码段的 `true` | 此处应读作 `two`，讲的是课堂中某次 `ls` 失败返回 2，不保证 macOS 的失败码相同 |
| `PyPy pipe` | 此处指双竖线操作符 `\|\|`，不是 Python 实现 PyPy |
| 服务器接收 `private key` | 配置到远端 `authorized_keys` 的是公钥；私钥保留在客户端 |
| “滴漏垃圾” | `ripgrep`，命令名是 `rg` |
| `fgf`、“挑剔的查找器” | `fzf`，Fuzzy Finder，即模糊查找工具 |
| `tmax` | `tmux`，终端复用器 |
| `.basterc` | Bash 配置文件 `.bashrc` |
| `zsh RC`、“c 系列 rc 文件” | Zsh 配置文件 `.zshrc` |
| `power level 10k` | 提示符主题 `powerlevel10k` 的名称 |
| 中断处理处的 `a second`、“分段错误” | 此处指 `SIGINT`，结合 `Ctrl-C` 与官方 `trap` 示例校正，不能按“分段错误”理解 |
| `Alacrity` | 终端模拟器 `Alacritty` 的名称 |

`-a` / `--all`、信号名、变量名和配置路径都需要保留大小写及符号。macOS 的 `ls` 不提供 GNU `ls` 的全部长选项，不能把讲师 Linux 环境中的示例直接当作所有平台的用法。

原始字幕保留这些误词；修正写入学习笔记，不改附件。

来源归属：Anish Athalye、Jon Gjengset 和 Jose 团队的 MIT Missing Semester 2026 课程，以及用户提供的第二讲中英字幕。本页对资料与术语重新整理，采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，课程许可见[官方说明](https://missing.csail.mit.edu/license/)。
