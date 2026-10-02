# 第 1 讲实践：从零认识 Shell

状态：未开始。先完成 A；B、C 在理解相应概念后做，D 留到学完基础脚本后。不要一次复制整页，先预测，再逐条运行。适用于 macOS 的 Zsh 与 Linux 的 Bash；D 明确使用 Bash。

题目依据 [2026 年官方第一讲](https://missing.csail.mit.edu/2026/course-shell/)自拟，未提供完整答案。课程由 Anish Athalye、Jon Gjengset 和 Jose 团队教授，原课程材料采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)；本练习也采用该许可。

## A. 环境与命令观察：现在就能做

1. 打开终端，运行 `pwd`。记录输出，并用自己的话说明“终端”“Shell”“当前工作目录”各是什么。
2. 运行 `date`、`echo hello shell`、`ls -l /tmp`。分别指出命令名和参数；暂时只观察 `ls` 输出，不要求解释每一列。
3. 比较 `echo red blue` 与 `echo 'red blue'`：先写下分别传入几个参数，再运行。思考为什么输出可能相同；然后试试保留两个词之间的多个空格。
4. 把 `echo 'I am learning Shell'` 改成自己的学习目标，解释终端、Shell 和 `echo` 在运行它时分别做了什么。

**过关：**能够区分终端窗口与解释命令的 Shell，能指出命令名、参数，并解释空格和引号对参数边界的影响。

## B. 路径、参数与引号

先做一次只读观察：运行 `ps -p "$$" -o pid=,comm=` 查看当前 Shell 进程，再运行 `printf '%s\n' "$SHELL"` 查看登录 Shell 的配置值；两者可能不同。运行 `type cd`、`type echo`、`type date` 与 `printf '%s\n' "$PATH"`，结合笔记第 2 次学习辨认内置命令、外部程序和搜索目录。

从本组起，只在新建的临时目录里创建或修改练习文件。执行下面的准备命令；任一步报错就停下来记录，成功后确认 `pwd` 的输出是新目录：

```sh
practice_dir=$(mktemp -d) && cd "$practice_dir" && pwd
```

继续在该目录准备材料：

```sh
mkdir "My Notes" data
printf 'first note\n' > "My Notes/note.txt"
```

1. 运行 `ls -l "My Notes"`。拆出命令、选项、路径参数；说明为何带空格的路径需要引号。用 `man ls` 查询 `-l`，按 `q` 退出。
2. 比较 `printf '<%s>\n' My Notes` 与 `printf '<%s>\n' "My Notes"`。先写出两条命令分别传递了几个待打印参数，再验证。
3. 进入 `"My Notes"`，运行 `pwd`；用相对路径列出同级的 `data`。解释 `.`、`..`，然后用 `cd "$practice_dir"` 返回。另写一条用绝对路径查看 `note.txt` 的命令。
4. 自设变量 `topic=Shell`，比较 `printf '%s\n' '$topic'` 与 `printf '%s\n' "$topic"`。指出哪种引号允许变量展开；不要通过修改 `PATH` 来实验。

**过关：**不用试错就能判断相对路径指向哪里，解释引号如何影响参数边界与变量展开。

## C. 文本、管道与重定向

先 `cd "$practice_dir"`，用 `pwd` 确认位置，再准备自建数据：

```sh
printf '%s\n' pear apple pear banana apple > data/fruits.txt
```

1. 用 `cat` 查看文件，再用 `grep` 筛出含 `apple` 的行。记录筛选后行数，并说明输入来自哪里、输出去了哪里。
2. 分别观察 `uniq data/fruits.txt`、`sort data/fruits.txt` 的输出。组合 `sort` 和 `uniq -c` 统计每种水果；逐段说明数据如何流动，解释为什么顺序重要。
3. 把统计结果写入临时目录内的新文件 `data/counts.txt`。用另一份自建文件比较 `>` 与 `>>`，每次写入前先预测内容；再用 `<` 给 `wc -l` 提供输入。
4. 运行 `ls data/fruits.txt data/no-such-file`，尝试将正常输出和错误分别保存为 `data/out.txt`、`data/err.txt`。提示：流编号为 1 与 2。说明普通管道默认连接哪条流。

**过关：**能画出一条管道的输入输出，说明覆盖、追加和错误输出的区别。所有输出文件都位于本次临时目录。

## D. 基础 Bash 脚本：后续完成

1. 在临时目录内自建 `check.sh`，首行为 `#!/bin/bash`。让它接收一个文件名，使用 `if` 与 `test -f`（或 `[ -f ... ]`）输出不同提示。提示：第一个参数是 `$1`，带空格的参数要保留引号。
2. 用 `bash check.sh "My Notes/note.txt"` 和不存在的练习路径测试。再设计无参数时的提示，避免把空参数误认为正常输入。
3. 比较 `bash check.sh ...` 与 `./check.sh ...`。查看自建脚本的权限，在需要时仅对它执行 `chmod u+x check.sh`；解释执行权限与首行各解决什么问题。
4. 增加一个有限次数的 `for` 循环，打印三次自选词语；用 `bash -x check.sh ...` 观察执行过程。不得加入无限循环、后台任务或删除命令。

**过关：**脚本能处理存在、不存在、含空格的路径及无参数情况；能解释参数、条件、循环和启动方式。

## 每个任务的记录模板

```text
任务编号：
运行前预测：
实际命令：
实际输出（只保留相关部分）：
差异与原因：
现在能解释什么：
仍不明白什么：
```

本页不要求清理临时目录，也不需要 `sudo` 或额外安装工具。关闭终端后变量会丢失；重做时重新创建临时目录，不要把输出重定向到仓库文件或个人文档。完成记录后带着具体命令和疑问讨论，再继续下一组。
