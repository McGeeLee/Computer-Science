# 第 1 讲：课程概览与 Shell 入门

讲义：[2026 官方英文版](https://missing.csail.mit.edu/2026/course-shell/) · [2026 中文版](https://missing-semester-cn.github.io/2026/course-shell/)。

本页总结整节第一讲的主要内容，重点理解：**谁解释命令、参数怎样传入、数据怎样在程序和文件之间流动，以及怎样把命令组织成自动化脚本。**示例按 macOS 的 Bash / Zsh 环境核对；涉及 Bash 脚本时明确标注。官方讲义的进一步展开会单独标为补充。

文件读写示例使用下面的自建材料。先在一个终端中准备临时目录，后续示例在该目录运行；脚本也保存到这里：

```sh
shell_notes_dir=$(mktemp -d) && cd "$shell_notes_dir"
printf '%s\n' pear apple pear > words.txt
printf 'example\n' > existing.txt
mkdir "My Notes"
printf 'note\n' > "My Notes/note.txt"
```

## 1. 课程目标、Terminal 与 Shell

Missing Semester 教的是开发工具与工作方式：把重复操作交给工具，把简单工具组合成能解决实际问题的流程。Shell 提供交互命令和编程语言；学习目标是读懂、检查和修改这些流程，而不只是记住命令名。2026 课程有九讲，每讲配有实践与探索练习。

**IAP = Independent Activities Period，自主活动期。**MIT 在秋季和春季学期之间的一月安排约四周，供师生参加短课、独立研究和其他活动。视频中的 IAP 2026 表示本课程在这一活动期中开设。[MIT 对 IAP 的说明](https://elo.mit.edu/iap/)

| 角色 | 负责什么 | 例子 |
| --- | --- | --- |
| Terminal，终端应用 | 接收按键、显示文字，提供交互窗口 | macOS Terminal |
| Shell，命令解释器 | 解释命令、处理变量和重定向、执行内置功能或启动程序 | Bash、Zsh、PowerShell |
| 被调用的程序 | 根据参数或输入完成任务 | `ls`、`sort`、`python3` |

```text
键盘输入 → Terminal → Shell 解析 → 内置命令或外部程序执行
程序输出 → Terminal 显示，或者经管道/重定向送往别处
```

Shell 是类别，**Bash、Zsh、PowerShell 是并列的具体实现**。Terminal 可以容纳不同的 Shell，它们都运行在操作系统上。

- **Bash = Bourne-Again SHell**：名称承接 Stephen Bourne 编写的 Bourne Shell；Bourne 与 born 同音，因此也有“重生”的双关。[GNU 的名称解释](https://www.gnu.org/software/bash/manual/html_node/What-is-Bash_003f.html)
- **Zsh = Z Shell**：提供交互补全、历史记录等功能；macOS 默认使用 Zsh。它与 Bash 有许多相似用法，但默认展开规则等行为可能不同。[Apple 的默认 Shell 说明](https://support.apple.com/guide/terminal/change-the-default-shell-trml113/mac)
- **PowerShell**：也是 Shell，管道常传递结构化对象。本课主要使用 Unix 风格工具，其普通管道传递字节流，常用于文本。[PowerShell 概览](https://learn.microsoft.com/en-us/powershell/scripting/overview)

### 提示符、补全与历史

以 `mei@laptop:~$` 为例：`mei` 是用户名，`laptop` 是主机名，`~` 表示主目录。`$` 常表示普通用户，`#` 常表示 root；Zsh 常用 `%` 表示普通用户。提示符可自定义，判断身份可用 `id -u`，其中 `0` 表示 root。

复制命令时不要复制提示符。主目录使用半角 `~`，不是全角 `～`；`$HOME` 中的 `$` 则属于取变量值的语法。root 用户与根目录 `/` 是不同概念。

输入路径的一部分后按 Tab 可补全或显示候选项。上箭头通常浏览 Shell 的命令历史；历史的保存方式受 Shell 配置影响，例如 Zsh 的 `HISTFILE`。

**Mac 上也是 `Control + C` 中断前台命令或取消当前输入；`Control + Z` 通常暂停前台作业，程序仍存在。**暂停后可用 `jobs` 查看、`fg` 恢复；`Command + C` 通常用于复制。程序对信号的处理可能不同，具体作业控制在下一讲继续学习。[Bash 作业控制说明](https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html)

## 2. 命令与参数：Shell 怎样拆开你输入的文字？

```sh
ls -l "My Notes"
```

Shell 解析后，命令名是 `ls`，传给它两个参数：`-l` 和 `My Notes`。`-l` 是改变行为的选项，后一个是路径；选项也是参数，含义由程序决定。

**参数（argument）是调用时传入的一个个字符串。**Shell 用空格等分隔词，引号和转义保护参数边界；引号通常不会作为内容传给程序。

```sh
printf '<%s>\n' My Notes
printf '<%s>\n' "My Notes"
printf '<%s>\n' My\ Notes
```

第一条传入格式字符串和两个待打印参数，输出 `<My>`、`<Notes>` 两行。后两条各传入一个待打印参数，输出 `<My Notes>` 一行。`printf` 会重复使用格式以处理剩余参数；因此它适合观察参数边界。

| 写法 | 关键作用 |
| --- | --- |
| `'单引号'` | 内容按字面保留，不进行变量与命令替换 |
| `"双引号"` | 保留参数边界，仍允许 `$变量`、`$(命令)` 等展开 |
| `\` | 保护下一个字符，例如用 `\ ` 保留一个空格 |

```sh
topic=Shell
printf '%s\n' '$topic'
printf '%s\n' "$topic"
```

分别输出字面文字 `$topic` 和变量值 `Shell`。赋值的 `=` 两边没有空格；使用变量作参数时，通常写 `"$topic"` 来保留完整值。

### 参数与输入数据是两种接口

```text
参数：启动命令时交给它的字符串，例如文件名、选项、搜索模式
stdin：程序运行时读取的数据流，例如文件内容或另一个程序的输出
```

```sh
wc -l words.txt
wc -l < words.txt
cat words.txt | wc -l
```

| 写法 | 谁打开文件？ | `wc` 收到哪些参数？ | 数据从哪里读？ |
| --- | --- | --- | --- |
| `wc -l words.txt` | `wc` | `-l`、`words.txt` | `wc` 自己读取指定文件 |
| `wc -l < words.txt` | Shell | `-l` | `wc` 的标准输入，接到文件 |
| `cat words.txt \| wc -l` | `cat` | `-l` | `wc` 的标准输入，接到 `cat` 输出 |

这里假设 `words.txt` 已存在。第一种输出通常带文件名，后两种通常只有计数；三者都能统计相同的换行数量。**文件名作为参数，与文件内容作为标准输入，要分别理解。**

## 3. 路径、目录与程序查找

`pwd` 显示当前工作目录，`cd` 改变它，`ls` 查看目录内容。当前目录是 Shell 的状态；相对路径从它出发。

| 写法 | 含义 |
| --- | --- |
| `/Users/mei/notes` | 绝对路径，从根目录 `/` 出发 |
| `notes/file.txt` | 相对路径，从当前目录出发 |
| `.` / `..` | 当前目录 / 上一级目录 |
| `~` / `~/Downloads` | 当前用户主目录 / 主目录下的 Downloads |
| `./check.sh` | 明确指定当前目录中的脚本路径 |

`cd ~` 回到主目录；`cd '~'` 则把 `~` 当作普通目录名。路径含空格时使用引号，例如 `cd "$HOME/My Notes"`，前提是目录存在。

常用文件操作：`mkdir` 创建目录，`touch` 创建空文件或更新时间，`cp` 复制，`mv` 移动或改名，`rm` 删除。查看参数可用 `man 命令`，在手册中按 `q` 退出；macOS 工具不一定支持 GNU 风格的 `--help`。

### `PATH` 与内置命令

```sh
printf '%s\n' "$PATH"
type cd
type echo
command -v python3
```

`PATH` 是以冒号分隔的搜索目录列表，Shell 查找外部命令时通常按顺序选择第一个可执行的匹配。直接写 `/完整路径/python3` 或 `./check.sh`，则明确指定路径。

命令也可能是内置功能、别名或函数。`type` 可以辨别，`command -v` 查看当前解析结果；结果不一定是外部程序路径。`cd` 必须改变当前 Shell 的目录，通常作为内置命令执行。

多个 Python 安装可以同时存在：`which -a python3` 可列出该名字在搜索路径中的多个匹配，但别名、函数等还应结合 `type` 判断；应用也可能配置自己的解释器。要确认一次 Python 运行实际用了谁，可运行 `python3 -c 'import sys; print(sys.executable)'`。

`bin` 来自 binaries，通常是存放可执行程序的目录名称，也可能包含脚本。目录叫 `bin` 不表示其中程序跨平台；编译好的可执行文件仍受操作系统与 CPU 架构限制。

## 4. 标准流、`>`、`>>` 与管道

这是理解 Shell 组合命令的核心。

| 流 | 编号 | 通常负责 |
| --- | --- | --- |
| stdin，标准输入 | 0 | 程序读取输入 |
| stdout，标准输出 | 1 | 程序输出正常结果 |
| stderr，标准错误 | 2 | 程序输出错误或诊断 |

默认情况下，输入常来自终端，正常结果与错误都显示在终端。它们是不同的流，可以分别改变去向。

### `>`：写入文件，已有内容会被截断

```sh
printf 'first\n' > result.txt
printf 'second\n' > result.txt
cat result.txt
```

最后只有一行 `second`。默认情况下，Shell 在运行命令**之前**打开输出文件：不存在就创建，存在就清空，然后让命令的 stdout 写入它。`>` 与 `1>` 表示同一条流。

这解释了为什么 `cat file.txt > file.txt` 不能用来“读取后写回”：Shell 先截断文件，`cat` 再读取时原内容已经丢失。某些 Shell 配置可禁止覆盖；这里讲的是默认行为。[Bash 输出重定向说明](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)

### `>>`：追加到已有内容后面

```sh
printf 'first\n' > result.txt
printf 'second\n' >> result.txt
cat result.txt
```

现在文件依次包含 `first`、`second` 两行。`>>` 与 `1>>` 等价，文件不存在时也会创建。**追加不等于自动换行**：这些例子有换行，是因为 `printf` 中写了 `\n`。

`>` 适合保存这一次的结果；`>>` 适合累积多次记录。输出目标写成 `"$log_file"`，可以保留带空格的路径。

### 重定向由 Shell 处理，不是传给程序的参数

```sh
printf '%s\n' hello > result.txt
```

```text
Shell 交给 printf 的参数：'%s\n' 和 'hello'，引号已移除
Shell 另外处理的事：打开 result.txt，把 stdout 接到该文件
```

这里的 `>` 和 `result.txt` 都不进入 `printf` 的参数列表。若写成 `printf '%s\n' '>'`，引号保护的 `>` 就变成普通参数，程序会把它打印出来。

### `<`：从文件读取标准输入

```sh
sort < words.txt
```

Shell 打开 `words.txt`，把内容作为 `sort` 的 stdin；`sort` 没有收到文件名参数。这是前面“参数与输入数据”区别的另一种例子。

### `|`：前一个 stdout 接到后一个 stdin

```sh
printf '%s\n' pear apple pear | sort | uniq -c
```

```text
printf 产生三行文本
  → sort 将它们排序
  → uniq -c 统计相邻相同行
```

管道传递的是数据流。后一个程序不会自动把这些数据当作它的参数；例如 `sort` 排的是输入文本，不是它的参数列表。

管道各阶段可以同时运行，一边输出、一边读取；`sort` 等工具要收到完整输入才能给出完整结果。Shell 可以在一行中组合多个命令，也可以把一个复合命令写在多行。

### stderr：为什么错误没有写进结果文件？

```sh
ls existing.txt missing.txt > out.txt 2> err.txt
```

假设 `existing.txt` 存在，`missing.txt` 不存在：正常结果进 `out.txt`，错误信息进 `err.txt`。普通 `>` 和 `|` 都默认只处理 stdout。

把两条输出合并到一个文件：

```sh
ls existing.txt missing.txt > all.txt 2>&1
```

`2>&1` 表示让 fd 2 指向 **fd 1 此刻指向的地方**，不是写到名叫 `1` 的文件；这里 stdout 已经指向 `all.txt`，所以 stderr 也进入同一文件。

重定向从左到右处理，顺序有意义：`> all.txt 2>&1` 合并两条流到文件；`2>&1 > all.txt` 则先把 stderr 接到原 stdout，随后只改变 stdout，stderr 仍去原来的位置，常见情况是终端。[Bash 重定向顺序说明](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)

### 讲义补充：`tee` 同时显示与保存

```sh
printf 'first\n' | tee output.txt
printf 'second\n' | tee -a output.txt
```

`tee` 读取 stdin，同时写 stdout 和文件。第一条默认覆盖文件，第二条 `-a` 追加；文件内容也会继续出现在终端或下游管道里。

### 一张表区分数据的传递方式

| 写法 | 发生什么？ |
| --- | --- |
| `tool argument` | 给程序传入参数 |
| `tool < file` | 把文件作为程序的标准输入 |
| `A \| B` | 把 A 的标准输出接到 B 的标准输入 |
| `tool > file` | 把标准输出写入文件，默认覆盖 |
| `tool >> file` | 把标准输出追加到文件 |
| `tool 2> file` | 把标准错误写入文件 |
| `tool > file 2>&1` | 把标准输出与标准错误都写入文件 |
| `tool "$(other)"` | 先运行 other，再把其 stdout 作为一个参数传给 tool |

## 5. 文本工具、正则与文件查找

| 工具 | 作用与常见用法 |
| --- | --- |
| `cat` | 输出文件内容，或读取 stdin |
| `head` / `tail` | 取前 / 后若干行，如 `tail -n 10` |
| `sort` | 按行排序；`-n` 按数值，`-r` 反向 |
| `uniq` | 合并相邻重复行；`-c` 计数 |
| `grep` | 筛选匹配模式的行；`-F` 固定字符串，`-E` 扩展正则，`-r` 递归搜索 |
| `wc -l` | 统计换行符数量 |
| `sed` | 按规则替换等文本编辑 |
| `awk` | 按字段提取、筛选与计算 |
| `find` | 递归查找符合条件的文件或目录 |

### `sort` 与 `uniq` 的顺序

`uniq` 只合并相邻行，不会记住所有出现过的内容。因此 `sort | uniq -c` 才能把交错出现的相同行一起计数。`sort -n -k1,1` 表示只按第一个字段数值排序。

### `grep`、`sed` 与模式

```sh
printf '%s\n' apple pear pineapple | grep 'apple'
printf 'draft draft\n' | sed 's/draft/ready/g'
```

第一个例子保留包含 `apple` 的行，包括 `pineapple`。第二个输出 `ready ready`：`s/模式/替换/g` 中的 `s` 是替换，末尾 `g` 表示每行所有匹配，不是命令行选项 `-g`。

`sed -E` 使用扩展正则；括号可以捕获内容，替换部分的 `\1` 引用第一个捕获组。`sed` 默认输出每一行，未匹配的行仍会原样输出；只想输出匹配的替换结果时可用 `sed -nE 's/模式/替换/p'`。

**glob 与 regex 分工不同。**`ls *.txt` 中的 `*.txt` 通常由 Shell 展开为匹配的文件名；`grep 'a.*b'` 中的模式交给 `grep` 解释，匹配文本。regex 的 `*` 重复前一个元素，glob 的 `*` 匹配一段文件名；不能混用同一含义。详见[正则表达式与通配符](regex-and-globs.md)。

macOS 的 BSD `sed` 和 GNU `sed` 的 `-i` 参数形式不同；这里用标准输出示例，不原地修改文件。

### `find`：条件与 `-exec`

```sh
find . -type f -name '*.txt'
find "$HOME/Downloads" -type f -name '*.zip' -mtime +30
find . -type f -name '*.py' -exec grep -l 'TODO' {} \;
```

| 部分 | 含义 |
| --- | --- |
| `.` 或其他路径 | 从哪里开始递归查找 |
| `-type f` | 只找普通文件 |
| `-name '*.py'` | 文件名符合 glob；引号让模式留给 `find` 解释 |
| `-mtime +30` | 按修改时间筛选较旧的文件，以 24 小时为单位，取整规则见下文 |
| `-size +100M` | 可用于按大小筛选；单位与取整规则查本机 `man find` |
| `-maxdepth 2` | 限制递归深度，以起始路径为深度 0 |
| `-exec 命令 … \;` | 对每个匹配路径执行指定命令 |
| `{}` | 由 `find` 替换成当前匹配的路径 |
| `\;` | 将分号交给 `find`，作为 `-exec` 参数结束标记 |

第三条查找 `.py` 文件，并让 `grep -l` 输出其中包含 `TODO` 的文件名。Shell 去掉 `\;` 的反斜杠后，`find` 接收到字面分号；若不保护分号，Shell 会先把它当成命令分隔符。`-exec` 直接把路径作为命令参数传入，路径里的空格不会被重新当成 Shell 分词。[GNU find 时间条件](https://www.gnu.org/software/findutils/manual/html_node/find_html/Age-Ranges.html)

时间边界有平台差异：GNU `find` 的无单位 `-mtime` 按完整 24 小时向下取整，macOS 的 BSD `find` 按 24 小时向上取整，再与数值比较。因此 `-mtime +30` 在两者中的精确边界不同，也不是按日历日期判断；需要精确筛选时查本机 `man find`。

### `awk`：字段、分隔符与筛选

```sh
printf 'alice 100\nbob 200\n' | awk '{print $2}'
printf 'alice,100\nbob,200\n' | awk -F, '{print $1}'
printf 'alice 100\nbob 200\n' | awk '$2 > 100 {print $1}'
```

依次输出第二字段、逗号分隔的第一字段、第二字段大于 100 的行中的名字。`$0` 是整行，`$1`、`$2` 是字段；默认按空白分隔，`-F,` 把分隔符改成逗号。

单引号保护 awk 程序中的 `$2`，让 awk 自己解释它。这里的简单逗号分隔处理不能解析带引号、字段内逗号或换行的完整 CSV。

### 整体案例：SSH 日志统计

第一讲用 `ssh → 日志筛选 → 用户名提取 → 计数 → 排序 → 前十名 → 逗号连接` 展示工具组合。完整命令、每阶段输出、正则限制与 Mac 兼容写法见 [SSH 日志管道命令详解](ssh-log-pipeline.md)。

课堂演示没有按老师的预期运行，这也说明：即使是非常熟练、经验丰富的使用者，使用 Shell 时依然可能遇到问题。

## 6. 命令组合、退出码与条件判断

Shell 有变量、条件、循环和函数。一次输入可以是一条简单命令，也可以是一段复合程序。

| 组合 | 含义 |
| --- | --- |
| `A; B` | A 结束后执行 B，通常不检查 A 是否成功 |
| `A && B` | A 返回成功时执行 B |
| `A \|\| B` | A 返回失败时执行 B |
| `A \| B` | 连接数据流，各阶段可以同时运行 |

**退出码**通常 `0` 表示成功，非零表示其他结果。它不是程序打印的文本。`grep` 的常见状态为：`0` 找到匹配，`1` 未找到匹配，`2` 出错。

```sh
grep 'apple' words.txt
printf 'exit status: %s\n' "$?"
```

`$?` 保存上一条前台命令或管道的退出状态，要紧接着查看；之后会被新命令更新。普通 Bash 管道默认取最后一个命令的状态，不能由此保证每一段都成功。

### `if` 判断的是命令是否成功

```bash
if grep -q 'apple' words.txt; then
    printf 'found\n'
else
    printf 'not found or grep failed\n'
fi
```

`-q` 只用退出状态表达是否匹配，不打印匹配行。这里的 `else` 同时包含未找到与出错；需要区分时应分别检查状态。

### `test`、`[` 与 `[[`

```bash
file='My Notes/note.txt'
if [ -f "$file" ]; then
    printf 'regular file exists\n'
fi
```

`test -f "$file"` 与 `[ -f "$file" ]` 都判断该路径是否存在且为普通文件；`-e` 判断路径是否存在，`-d` 判断目录，`-n` 判断字符串非空。比较字符串可用 `[ "$topic" = 'Shell' ]`，比较整数可用 `[ "$count" -gt 3 ]`。

`[` 是命令名，末尾 `]` 是它要求的参数；两侧的空格不可省略。Bash 中通常有内置的 `test` / `[`，系统也可能有外部版本。`if`、`then`、`fi` 则是 Shell 语法关键字。

`[[ ... ]]` 是 Bash / Zsh 提供的条件语法，在内部避免普通的拆词和文件名展开，因此处理变量更方便；它不是标准 POSIX `sh` 的语法。`[[ "$topic" == S* ]]` 中未引用的右侧是模式，引用右侧则按字面比较。[Bash 条件语法](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html)

## 7. 循环与命令替换 `$()`

### `while`：条件成功就继续

```bash
count=1
while [ "$count" -le 3 ]; do
    printf 'run %s\n' "$count"
    count=$((count + 1))
done
```

这段有限循环打印三次。`while` 每轮执行条件命令，状态为 `0` 才进入循环体。`$((...))` 是算术展开，计算整数表达式。

课堂中还用 `sleep 10` 让循环每次暂停十秒，避免持续快速重复；`sleep` 本身是等待指定时长的命令。

### `for`：依次取列表中的值

```bash
for tool in shell git; do
    printf 'Learning %s\n' "$tool"
done
```

变量 `tool` 依次成为 `shell`、`git`。数字列表可通过 `seq` 产生：

```bash
for i in $(seq 1 3); do
    printf '%s\n' "$i"
done
```

`seq 1 3` 输出 1、2、3；Bash 将这里未引用的命令替换结果按空白拆成列表。该例明确使用 Bash，不据此假设 Zsh 的所有未引用展开也按相同规则拆词。

### `$()`：输出进入变量或参数

```sh
today=$(date +%Y-%m-%d)
printf 'Today is %s\n' "$today"
printf '<%s>\n' "$(printf 'My Notes')"
```

`$(命令)` 先运行内部命令，捕获 stdout，并去掉末尾换行，再把结果放回当前位置。最后一条中，外层双引号让 `My Notes` 作为一个参数传给 `printf`。[Bash 命令替换说明](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html)

| 对比 | 输出进入哪里？ |
| --- | --- |
| `A \| B` | B 的 stdin |
| `B "$(A)"` | B 的一个参数 |
| `value=$(A)` | 变量 value |

例如 `sort "$(cat words.txt)"` 会把整段文本当作一个文件名参数，通常无法完成文本排序。**管道和命令替换不能随意互换，先看后一个工具要参数还是输入流。**

`$()` 可以嵌套，阅读通常比旧式反引号更清晰。包含任意文件名的列表应保留边界，不套用上面的数字列表拆词方法。

## 8. 脚本、shebang 与参数转交

长命令可以保存成 `.sh` 文件，便于重复运行和修改。把下面内容保存为 `check.sh`：

```bash
#!/bin/bash
if [ "$#" -ne 1 ]; then
    printf 'Usage: %s FILE\n' "$0" >&2
    exit 2
fi

if [ -f "$1" ]; then
    printf 'exists: %s\n' "$1"
else
    printf 'missing or not a regular file: %s\n' "$1"
    exit 1
fi
```

| 表达式 | 在脚本中的含义 |
| --- | --- |
| `$0` | 脚本名称或调用路径 |
| `$1`、`$2` | 第一个、第二个位置参数 |
| `$#` | 参数个数 |
| `"$@"` | 全部位置参数，分别保留为独立参数 |
| `$?` | 上一条前台命令或管道的退出状态 |

```sh
bash check.sh "My Notes/note.txt"
chmod u+x check.sh
./check.sh "My Notes/note.txt"
```

`bash check.sh` 明确让 Bash 读取脚本，不要求脚本有执行位。`./check.sh` 直接执行脚本，需要执行权限；首行 **shebang `#!/bin/bash`** 指定解释器。它不是 stdin 重定向，也不能把 `/bin/sh` 一概当作 Bash。

`chmod u+x` 给所有者添加执行权限。`ls -l` 开头如 `-rwxr-xr--`：第一个字符表示类型，随后三组 `rwx` 分别属于所有者、组、其他用户，`-` 表示缺少对应权限。目录的 `x` 表示可进入/遍历，与普通文件执行含义不同。

### 转交全部参数时，用 `"$@"`

函数也可以接收位置参数，适合复用一段命令：

```bash
show_args() {
    printf 'count: %s\n' "$#"
    for arg_item in "$@"; do
        printf '<%s>\n' "$arg_item"
    done
}
show_args "My Notes/note.txt" '*.txt'
```

输出参数个数 `2`，随后分别打印 `<My Notes/note.txt>`、`<*.txt>`。`"$@"` 相当于逐个保留 `"$1"`、`"$2"` 等参数；不能用 `"$*"` 代替，后者通常把它们连接成一个字符串。[Bash 特殊参数说明](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)

包装其他命令时同样使用 `other_command "$@"`，让带空格的路径和每个原始参数边界继续保留。观察脚本执行过程可用 `bash -x check.sh ...`。

## 9. 最后的自动化案例：重复测试直到失败

老师最后展示的思路是：后台制造 CPU 压力，反复运行测试，把每次输出保存到日志；测试一旦失败，退出循环，停止压力程序，显示失败那次的日志。

这个案例把本讲的几个概念连起来：**退出码控制循环，参数指定测试，重定向保存输出，脚本组织整个流程。**

下面是无需额外安装工具的有限模拟。保存为 `repeat-test.sh`，用 `bash repeat-test.sh` 运行；模拟测试前两次成功，第三次失败：

```bash
#!/bin/bash
set -euo pipefail

run=1
log_file='test-run.log'

demo_test() {
    printf 'test run %s\n' "$1"
    if [ "$1" -ge 3 ]; then
        printf 'simulated failure\n' >&2
        return 1
    fi
    return 0
}

while demo_test "$run" > "$log_file" 2>&1; do
    printf 'run %s passed\n' "$run"
    run=$((run + 1))
done

printf 'run %s failed\n' "$run"
cat "$log_file"
```

终端先显示前两次通过，再显示第三次失败及失败日志。每轮的 `>` 都覆盖上一轮日志，最后文件只保留第三次；如果换成 `>>`，文件会累积全部轮次。`2>&1` 让错误信息也保存在日志中。

`demo_test` 是函数，成功轮次返回 `0`，失败轮次明确 `return 1`。失败发生在 `while` 的条件位置，因此退出循环，继续执行后面的报告；不会因为 `set -e` 直接跳过报告。

### 讲义补充：后台任务与严格模式

| 写法 | 作用 |
| --- | --- |
| `command &` | 把命令放到后台，Shell 可继续执行后续命令 |
| `$!` | 最近一次放到后台的作业的进程 ID |
| `kill "$pid"` | 向指定进程发送信号，默认请求终止 |
| `wait "$pid"` | 等待指定子进程结束，并取得其退出状态 |

官方脚本用 `stress --cpu 8 &`、`STRESS_PID=$!` 与 `kill "$STRESS_PID"` 控制压力程序。它依赖额外工具和真实测试环境，这里的模拟用固定三轮展示数据流与条件，不要求安装这些工具。实际脚本还需要考虑执行前提与提前退出时的清理。

`set -euo pipefail` 中：

- `-e`：在适用位置，命令失败时提前退出；`if` / `while` 条件等位置有例外。
- `-u`：展开未设置变量时报告错误，非交互脚本通常退出。
- `-o pipefail`：管道中有失败时，以最右侧失败命令的非零状态作为管道状态，避免只看到末尾命令成功；是否退出还取决于上下文与 `-e`。

这些选项帮助发现问题，但不能代替检查参数和程序逻辑。示例使用 `run=$((run + 1))` 递增，避免把算术命令自身的退出状态与测试状态混在一起。[Bash set 选项说明](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)

## 10. 本讲复习时要能回答的问题

1. Terminal、Shell、外部程序分别做什么？哪些字符由 Shell 解释？
2. 命令收到哪些参数？含空格的路径怎样保持一个参数？
3. 文件名参数、`<`、管道提供的输入有什么区别？
4. `>` 什么时候清空文件？`>>` 是否自动添加换行？
5. stdout、stderr 怎样分别保存？为什么 `2>&1` 的顺序会改变结果？
6. `uniq` 为什么常放在 `sort` 后面？`find -exec` 中 `{}` 与 `\;` 分别做什么？
7. `if`、`while` 看的是输出文字还是退出状态？管道默认报告哪一段的状态？
8. `$()` 与 `|` 把结果送到哪里？`"$@"` 怎样保留参数边界？
9. shebang、执行权限、`./` 与 `bash script.sh` 分别解决什么问题？
10. 最后的测试循环为什么能在失败后保留日志并继续报告？

实际操作见[第一讲练习](../exercises/01-shell.md)，符号读法见[常用符号英文名称](symbols.md)。官方讲义还推荐了 `rg`、`fd` 等工具，并提供 `xargs`、`curl`、`jq` 等课后探索；它们属于继续练习的方向，不要求把本讲所有工具一次装齐。

## 来源与许可

本页依据用户提供的[第一讲英文字幕](../source/01-shell.en.srt)与 [Missing Semester 2026 第一讲讲义](https://missing.csail.mit.edu/2026/course-shell/)重新总结，结合工具官方手册及 macOS 实测补充参数与重定向解释。模拟日志与有限测试例子为原创；字幕转写校正见[来源记录](../source/01-shell-video.md)。课程由 Anish Athalye、Jon Gjengset、Jose 团队教授，本课程目录中的改写内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，转载或改编须保留署名、来源与相同许可。
