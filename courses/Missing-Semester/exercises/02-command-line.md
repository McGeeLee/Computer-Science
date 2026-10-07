# 第 2 讲实践：命令行程序怎样协作

状态：未开始，尚无实际练习结果。结合 [完整笔记](../notes/02-command-line.md)按需选做，每题先预测，再运行并解释。题目依据 [2026 年官方第二讲](https://missing.csail.mit.edu/2026/command-line-environment/)自拟，不提供完整答案。

本地练习使用 macOS / Zsh 或 Linux / Bash 的已有工具。先准备一个新临时目录与自建材料：

```sh
lesson2_dir=$(mktemp -d) && cd "$lesson2_dir" && pwd
touch a.py b.py "two words.py" note.txt .hidden ./-notes.txt
printf 'error one\nok two\nerror three\n' > sample.log
```

文件练习沿用这份材料。若关闭了终端或变量丢失，重新准备即可。

## A. 参数、glob 与标准流

1. 比较 `printf '<%s>\n' *.py` 与 `printf '<%s>\n' '*.py'`：程序分别收到哪些参数？带空格的文件名会不会被拆开？再观察 `printf '<%s>\n' {a,b}.py`，解释花括号展开与文件名匹配的区别。用 `ls -- -notes.txt` 和 `ls ./-notes.txt` 查看自建文件，说明为何两种写法都能避免把文件名当成选项；用本机 `man ls` 核对。
2. 比较 `grep error sample.log`、`grep error < sample.log` 与 `cat sample.log | grep error`：指出参数和 stdin 分别是什么、谁打开文件。再将 `ls sample.log no-such-file` 的 stdout 与 stderr 分别写入临时目录内的 `out.txt`、`err.txt`，解释普通管道默认连接哪条流。

**过关：**能区分 Shell 展开、程序参数解析和标准输入；能追踪结果及错误输出。

## B. 环境传递与退出码

1. 自设练习变量 `MS_LESSON2_TAG`，通过 `bash -c 'printf "<%s>\n" "${MS_LESSON2_TAG-unset}"'` 观察子进程。分别尝试普通赋值、单条命令前的赋值、`export` 后启动子进程；解释结果为何不同，单条命令赋值是否改变父 Shell。完成后用 `unset MS_LESSON2_TAG` 清除自建变量。
2. 对 `sample.log` 分别用 `grep -q` 查找存在与不存在的字符串，再尝试读取不存在的练习文件。每次紧接着查看 `$?`，区分“无匹配”和“读取出错”。自拟两条使用 `&&`、`||` 的命令，预测后续提示何时出现；说明没有文本输出为什么仍有结果。

**过关：**能说明子进程继承哪些变量；能根据退出码判断执行结果，而非只看文字输出。

## C. 信号与作业控制

只针对本题自己启动的短作业观察，不按进程名称批量结束其他程序。

1. 在交互式终端运行 `sleep 30`，按 `Ctrl-Z` 暂停，用 `jobs -l` 找到这项作业。用 `bg %N` 恢复后台运行，再用 `fg %N` 回到前台，最后按 `Ctrl-C`。`N` 换成本次 `sleep` 对应的作业号。记录状态变化，说明暂停与终止有什么区别；如果它已自然结束，重新启动一项短作业观察。
2. 运行 `sleep 30 &`，紧接着用 `lesson2_pid=$!` 保存 PID。通过 `jobs -l` 核对它仍是本次作业，然后只对这个 PID 发送 `kill -TERM "$lesson2_pid"`，用 `wait "$lesson2_pid"` 等待并观察退出状态。若已结束，就不再发送信号。解释 PID、作业号、`$!` 与 `wait` 的关系。

**过关：**能辨认自建作业，解释前台、后台、暂停及信号；知道 `wait` 等待当前 Shell 的子进程。

## D. SSH、tmux 与配置：纸上拆解

1. 不实际连接，拆解 `ssh student@example.invalid hostname | wc -c` 与 `ssh student@example.invalid 'hostname | wc -c'`。分别标出本地与远端运行的程序、流向和引号由哪端解析；说明公钥、私钥和远端 `authorized_keys` 各自的用途。若以后使用自己的已有服务器，可另行验证。
2. 画出 tmux 的 session / window / pane 层级，写出 detach、reattach 与退出 Shell 的区别。再在临时目录的 `config-draft.txt` 草拟 SSH 的 `Host`、`HostName`、`User`、`Port` 配置及一个 Shell alias，说明各自属于哪种配置文件。此题只写草稿，无需安装 tmux、生成密钥或修改真实 dotfiles。

**过关：**能解释远程命令的执行位置，区分会话管理与 Shell 配置，并能读懂配置草稿。

## 记录模板

```text
题号：
预测：
命令或纸上拆解：
实际输出与退出码：
我的解释：
仍不明白的概念：
```

课程由 Anish Athalye、Jon Gjengset 和 Jose 团队教授。原材料与本练习采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，转载或改编时保留署名与来源。
