# 第 2 讲：命令行环境

讲义：[2026 官方英文版](https://missing.csail.mit.edu/2026/command-line-environment/) · [2026 中文版](https://missing-semester-cn.github.io/2026/command-line-environment/)。

本页总结整节第二讲，包括最后的 AI 工具与终端模拟器。第一讲教我们组成命令，第二讲进一步解释：**命令怎样与其他程序通信，怎样控制正在运行的任务，以及怎样把本地和远程环境配置成方便使用的工作空间。**英文字幕用于核对术语，中文字幕辅助对照；讲义额外内容明确标为补充。

本地文件示例可在下面的临时目录中运行。SSH 地址、配置片段与需要额外工具的命令用于理解语法，使用时按实际环境替换。

```sh
cli_notes_dir=$(mktemp -d) && cd "$cli_notes_dir"
mkdir scripts
touch scripts/main.py scripts/helper.py scripts/run.sh
printf 'apple\npear\napple\n' > words.txt
```

## 1. CLI 程序的五种接口

**CLI = Command-Line Interface，命令行界面。**Shell 与 CLI 程序的协作，依赖一些广泛使用的约定，而不是所有程序必须遵守的一套固定语法。

| 接口 | 负责什么 | 例子 |
| --- | --- | --- |
| Arguments，参数 | 调用时传入字符串，指定对象、选项、模式等 | `grep 'apple' words.txt` |
| Streams，标准流 | 程序运行时读入和输出数据 | stdin、stdout、stderr |
| Environment variables，环境变量 | 随新进程继承的配置字符串 | `PATH`、`TZ` |
| Return / exit codes，退出状态 | 让调用方判断执行结果 | `0` 成功；`$?` 查看状态 |
| Signals，信号 | 通知正在运行的进程中断、暂停、继续等 | SIGINT、SIGTERM |

```text
调用时：参数 + 环境变量 → 程序
运行时：stdin → 程序 → stdout / stderr
运行中：信号 → 程序的默认行为或处理函数
结束时：退出状态 → Shell 的条件判断
```

例如，`grep` 可以同时接收一个模式参数和来自管道的文本，输出匹配行，并用退出状态说明有没有匹配。理解一条命令，要分别找出这些接口。

## 2. 参数、选项与 Shell 展开

### 选项是约定，由程序解析

`ls -l scripts/` 中，Shell 调用 `ls`，传入 `-l` 与 `scripts/` 两个参数。`-l` 是选项，但仍属于参数列表。

- 单横线常用于短选项，如 `-a`；多个不取值的短选项常能组合，如 `ls -l -a` 与 `ls -la`。
- 双横线常用于长选项，如 GNU `ls --all`；macOS 自带 `ls` 不支持所有 GNU 写法。
- 有些选项还需要一个值，如 `head -n 3`。能否合并、顺序是否重要，由具体程序决定。
- `--help`、`--version` 等是常见约定，不是 Shell 自动提供的功能；本机差异查 `man 命令`。

### `--` 与 `-` 是不同约定（`--` 为讲义练习补充）

很多程序把独立的 `--` 视为“停止解析选项”。之后的 `-myfile` 可以作为普通文件名处理，例如 `touch -- -myfile`。也可用 `./-myfile` 指定路径，避免开头的横线被当作选项。并非所有程序都支持相同约定。

独立的 `-` 则常表示 stdin 或 stdout，例如：

```sh
printf 'hello\n' | grep 'hello' -
```

这里 `grep` 把最后的 `-` 当作标准输入来源。它不是一个未写完的选项。

### glob 先展开，再交给程序

```sh
printf '<%s>\n' scripts/*.py
printf '<%s>\n' 'scripts/*.py'
```

第一条通常打印两个匹配路径，第二条打印字面文字 `scripts/*.py`。未引用的模式先由 Shell 展开，程序收到的是展开后的参数列表；它不会自动知道你原来写过星号。

| 模式 | 常见作用 |
| --- | --- |
| `*` | 匹配零个或多个字符 |
| `?` | 匹配恰好一个字符 |
| `[abc]` | 匹配字符集合中的一个 |
| `**/*.py` | Zsh 中可递归匹配 Python 文件；Bash 需要相应的 `globstar` 设置 |

默认设置下，glob 通常不包含以 `.` 开头的隐藏文件。没有匹配时，Bash 默认保留字面模式，Zsh 默认报 `no matches found`；设置可以改变这些行为。

### 花括号展开不检查文件是否存在

```sh
printf '%s\n' report.{txt,md}
touch scripts/{a,b,c}.py
```

第一条生成 `report.txt`、`report.md` 两个字符串，即使这两个文件都不存在。第二条生成三个路径，再交给 `touch` 创建文件。**花括号展开是字符串组合，glob 是查找匹配路径**；二者可组合，但机制不同。

文件名含空格时，Shell 的 glob 会保留各个匹配路径作为独立参数。不要把任意文件名列表简单保存成 `$(ls)` 后按空白拆开。更多语法见[正则表达式与通配符](regex-and-globs.md)。

## 3. 流、管道并发与缓冲

| 标准流 | 编号 | 常见用途 |
| --- | --- | --- |
| stdin | 0 | 程序读取输入 |
| stdout | 1 | 正常数据输出，默认进入下一个管道阶段 |
| stderr | 2 | 错误、警告、诊断信息 |

```sh
cat words.txt | grep 'apple' | uniq -c
```

Shell 建立管道，各阶段可以同时运行；`grep` 在读取 `cat` 产生的数据时就能处理它。这里 `uniq -c` 只统计相邻重复行，所以两条被筛出的 `apple` 会形成一组。

课堂中的 `(sleep 15 && cat numbers.txt) | grep … | sort | uniq &` 展示了一个重要区别：后面的管道阶段可以先启动，但括号中的 `cat` 必须等 `sleep` 成功结束后才运行。**管道安排数据连接，`&&` 规定条件执行。**

### 程序同时运行，不等于输出立即显示

程序可能缓冲输出，攒够数据才写出；工具也可能等待全部输入，例如完整排序的 `sort`。课堂演示 Python 逐步产生数字时，就遇到了缓冲。

Python 可用 `-u` 或 `print(..., flush=True)` 及时写出。下面是一个很短的演示：

```sh
python3 -u -c 'import time; [(print(i), time.sleep(0.2)) for i in range(3)]' | grep '[02]'
```

生产者逐步输出 0、1、2，筛选后保留 0 与 2。更多下游阶段仍可能各自缓冲；不能仅凭“屏幕没动”断定前面的程序没运行。

### 重定向再次对照

| 写法 | 作用 |
| --- | --- |
| `command > out.txt` | stdout 写入文件，默认先创建或清空 |
| `command >> out.txt` | stdout 追加到文件，不自动添加换行 |
| `command < input.txt` | stdin 从文件读取 |
| `command 2> err.txt` | stderr 写入文件 |
| `command > all.txt 2>&1` | stdout、stderr 都进入同一文件 |
| `command &> all.txt` | Bash / Zsh 的合并输出写法；不是 POSIX sh 通用语法 |
| `command 2>/dev/null` | 丢弃 stderr |

`/dev/null` 是特殊设备接口：写入的数据被丢弃，读取立即到达文件结束。丢弃诊断信息不改变程序实际的退出状态。

**`>`、`>>`、`<` 是 Shell 重定向；参数列表与标准输入是不同接口。**完整覆盖、追加和 `2>&1` 顺序示例见[第一讲的标准流部分](01-shell.md)。

### 讲义补充：`fzf` 让管道中间可以由人选择

`fzf` 是 fuzzy finder，模糊查找器：读取候选行，显示交互界面，再把选中的行输出。

```sh
printf '%s\n' apple banana pear | fzf
```

它本身不负责生成候选项；候选可以来自文件列表、历史记录或其他程序。这个例子需要已安装 `fzf`，返回的选择仍可接到后续流程中。[fzf 官方说明](https://github.com/junegunn/fzf)

## 4. Shell 变量与环境变量

```sh
topic='command line'
printf '%s\n' "$topic"
printf '%s\n' '$topic'
```

赋值的 `=` 两边没有空格。双引号保留参数边界并允许变量展开；单引号打印字面文字。普通变量通常保存字符串，但 Bash / Zsh 也有数组等功能，不能把课程中的简化解释理解成 Shell 完全没有类型或属性。

### 普通变量不会自动传给新进程

```sh
unset MS_DEMO
MS_DEMO='parent value'
bash -c 'printf "child: <%s>\n" "${MS_DEMO-unset}"'
export MS_DEMO
bash -c 'printf "child: <%s>\n" "${MS_DEMO-unset}"'
```

第一次子 Shell 看到 `unset`，第二次看到 `parent value`。`export` 给变量添加导出属性，让之后启动的子进程继承它。这里先 `unset`，避免该变量原来就有导出属性。

`bash -c '…'` 启动一个 Bash 子进程执行命令字符串；单引号让变量由子 Shell 展开。父子进程不是共享一个实时变量表：

- 子进程启动时得到环境的一份副本。
- 父 Shell 后来修改变量，不会自动改动已经启动的子进程。
- 子进程修改自己的环境，也不会自动改动父 Shell。
- 导出后再改值，之后新启动的子进程会继承新值。

### 前缀赋值：只给这一次调用使用

```sh
export MS_DEMO='normal'
MS_DEMO='temporary' bash -c 'printf "%s\n" "$MS_DEMO"'
printf '%s\n' "$MS_DEMO"
unset MS_DEMO
```

子进程输出 `temporary`，当前 Shell 仍输出 `normal`。这里用外部的 `bash` 示范；某些内置命令、特殊内置命令和 Shell 模式有额外规则。

课程用 `TZ=Asia/Tokyo date` 展示时区配置如何影响同一次程序调用。环境变量的常见名称有 `HOME`、`PATH`、`TZ`、`LANG`、`EDITOR`；它们的作用取决于程序是否读取并遵守它们。

`printenv MS_DEMO` 可查看某个导出的环境变量，`unset MS_DEMO` 删除变量。大写是常见命名惯例，不是判断变量是否导出的依据。

## 5. 命令替换与进程替换

### `$()`：捕获 stdout，形成字符串

```sh
names=$(printf 'alice\nbob\n')
printf '%s\n' "$names" | grep 'bob'
```

变量中保留内部换行，命令替换去掉末尾换行。双引号让整个变量值作为一个参数交给 `printf`，再通过 stdout 恢复为文本流。

### 讲义补充：`<()` 提供文件接口

```sh
diff <(printf 'alice\nbob\n') <(printf 'alice\ncarol\n')
```

`<(命令)` 是 **process substitution，进程替换**。Shell 执行内部命令，提供类似 `/dev/fd/…` 或命名管道的可读路径，把路径交给 `diff` 作参数；不要求一定生成一个普通临时文件。

`diff` 可以读取两份输出，而普通 stdin 只有一个入口。它返回 `1` 通常表示存在差异，并不意味着执行出错。Bash / Zsh 支持这种语法，POSIX `sh` 不保证支持。[Bash 进程替换说明](https://www.gnu.org/software/bash/manual/html_node/Process-Substitution.html)

| 写法 | 后一个程序得到什么？ |
| --- | --- |
| `A \| B` | B 的 stdin 接到 A 的 stdout |
| `B "$(A)"` | 一个包含 A 输出的字符串参数 |
| `B <(A)` | 一个可读取 A 输出的路径参数 |
| `B < file` | B 的 stdin 接到文件 |

## 6. 退出状态与控制流

退出状态是进程结束时报告的数值，Shell 用 `$?` 展示它。一般 `0` 表示成功，非零表示其他结果；非零也可能是正常的“未匹配”或“发现差异”。

```sh
false
result_code=$?
printf 'status: %s\n' "$result_code"
```

`false` 返回 `1`。立即保存状态，避免被后面的命令覆盖。脚本没有显式 `exit` 时，通常返回最后执行命令的状态，不能假定总是 `0`。

| 结构 | 根据什么行动？ |
| --- | --- |
| `A && B` | A 成功才执行 B |
| `A \|\| B` | A 失败才执行 B |
| `if A; then …; fi` | A 成功则进入分支 |
| `while A; do …; done` | A 成功则继续循环 |

```sh
grep -q 'apple' words.txt && printf 'found\n'
grep -q 'banana' words.txt || printf 'not found or grep failed\n'
```

`grep -q` 不打印匹配行，主要通过状态表达结果。`||` 不能自动区分未找到与文件读取失败；需要时检查具体状态。

`A && B || C` 中，如果 A 成功但 B 失败，C 也会执行，因此不能把它无条件当成 `if/else` 的替代。普通管道默认报告最后一段的状态；`pipefail` 的准确作用见[第一讲严格模式部分](01-shell.md#讲义补充后台任务与严格模式)。

## 7. 信号：怎样通知正在运行的程序？

信号是操作系统向进程传递事件的机制。程序可能采用默认行为，也可能注册处理函数，捕获部分信号后清理、继续运行或退出。

| 信号 | 常见来源或作用 | 关键区别 |
| --- | --- | --- |
| SIGINT | `Control + C`，请求中断 | 可以捕获或忽略 |
| SIGQUIT | `Control + \`，请求退出 | 可以捕获；默认可能终止并产生核心转储 |
| SIGTERM | `kill PID` 的默认信号 | 请求终止，程序可以先清理，也可能不退出 |
| SIGTSTP | `Control + Z`，请求暂停 | 可以捕获，与 SIGSTOP 不同 |
| SIGSTOP | 强制暂停 | 不能捕获、忽略或阻塞 |
| SIGCONT | 让暂停的进程继续 | 不等于把它切换到前台 |
| SIGHUP | 终端挂断等事件 | 常见默认行为为终止，但取决于处理方式 |
| SIGKILL | 强制终止 | 不能捕获、忽略或阻塞，程序不能靠处理它清理 |

通常由**终端驱动向前台进程组**发送快捷键对应的信号。前台作业可能是一整个管道，包含多个进程；不能简单理解为 Shell 只通知一个 PID。[终端信号规则](https://man.openbsd.org/termios.4) · [信号机制](https://man.openbsd.org/signal.3)

屏幕上的 `^C`、`^Z` 是这些按键的显示形式，不是需要输入的命令。Mac 这里用的是 Control，不是 Command。

课程中的 Python 程序注册 SIGINT 处理函数，只打印消息并继续运行，所以 `Control + C` 没有终止它。这个例子说明：快捷键发出请求，程序如何响应还取决于它自身。

### `kill` 是发送信号的工具

`kill -TERM PID` 请求终止，`kill -CONT PID` 请求继续；`kill -l` 查看本机信号名。信号编号可能因平台而异，优先使用名称。`kill` 这个名字不表示它只能“杀死程序”。

### `trap`：在退出时统一清理

下面是一个有限的 Bash 例子，保存为 `cleanup-demo.sh` 后执行 `bash cleanup-demo.sh`：

```bash
#!/bin/bash
task_temp_dir=$(mktemp -d) || exit 1

cleanup() {
    rm -f "$task_temp_dir/message.txt"
    rmdir "$task_temp_dir"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

printf 'temporary data\n' > "$task_temp_dir/message.txt"
printf 'temporary directory: %s\n' "$task_temp_dir"
sleep 1
```

正常结束时，EXIT 触发清理；INT / TERM 的处理先让脚本退出，再由 EXIT 清理一次。`EXIT` 是 Shell 退出事件，不是操作系统信号。

**仅仅 `trap cleanup INT TERM` 不会自动保证脚本退出。**也不能保证 SIGKILL 时执行清理。脚本若另外启动了后台子进程，还需要针对它们安排终止与等待；删除临时文件不会自动结束子进程。[Bash trap 说明](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)

## 8. 前台、后台与暂停的作业

| 工具或语法 | 作用 |
| --- | --- |
| `command &` | 后台运行，Shell 可继续接收命令 |
| `jobs` | 查看当前 Shell 管理的未结束作业 |
| `fg %1` | 把第 1 号作业放回前台，暂停的作业会继续 |
| `bg %1` | 让第 1 号暂停作业在后台继续 |
| `$!` | 最近一次放到后台的作业的 PID |
| `wait "$pid"` | 等待当前 Shell 的指定子进程，并取得状态 |

**前台/后台说的是与终端交互的关系，运行/暂停说的是执行状态。**后台作业可以正在运行，也可以暂停；`bg` 不是“重新启动一个新程序”。

`%1` 是当前 Shell 的作业号，不是 PID。一个管道作业可以包含多个进程；`jobs` 也不是全系统进程列表。`ps`、`pgrep` 用于查询进程信息。

### 交互演示

先执行 `sleep 30`，按 `Control + Z`。用 `jobs` 查看实际作业号；假设显示为 `[1]`，可依次用 `bg %1`、`jobs`、`fg %1`，最后按 `Control + C` 结束。已有其他作业时，使用刚创建的作业号。

一个可直接运行的短例子：

```sh
sleep 1 &
demo_pid=$!
printf 'waiting for %s\n' "$demo_pid"
wait "$demo_pid"
printf 'finished\n'
```

`wait` 不能随意等待另一个 Shell 的任意进程。讲义练习中的 `kill -0 PID` 不发送信号，可检查进程存在与权限，但不能单凭它保证某个任务仍在正常工作。

### 讲义补充：后台不等于断线后一定存活

`&` 只安排后台执行；终端关闭或 SSH 断线后，进程可能受到 SIGHUP，或失去所需的终端连接。

```sh
nohup sleep 30 > job.log 2>&1 < /dev/null &
```

`nohup` 在启动时安排忽略 SIGHUP，最后的 `&` 才让它后台运行；显式重定向处理了输入输出。`nohup` 不保证主机重启或其他终止事件后仍存活。[nohup 手册](https://man.openbsd.org/nohup.1)

`disown` 用于从当前 Shell 的作业管理中移除或标记作业，具体选项依 Shell 而异；它不会替你重新连接 stdin/stdout。需要保留远程交互工作区时，下一节的 `tmux` 更容易理解。

## 9. SSH：远程 Shell、身份与文件传输

### 连接与远程命令

```sh
ssh alice@server.example
ssh -p 2222 alice@server.example
ssh alice@server.example 'pwd'
```

`alice` 是远程用户名，`server.example` 是示例服务器地址，`-p` 指定端口。远程命令执行时，目录、工具与权限来自远程环境，不是本机的副本。

```sh
ssh alice@server.example ls | wc -l
ssh alice@server.example 'ls | wc -l'
```

第一条的 `ls` 在远程，`wc` 在本机；第二条的两者都在远程。外层单引号让字符串留给远程 Shell 解析。使用双引号时，里面的 `$变量` 可能先被本机展开。

SSH 可以传送远程命令的 stdin/stdout/stderr，因此能参加本地管道。但远程命令参数还会经过远程 Shell 解析，不要把它当作完全透明的参数列表转发。[OpenSSH ssh 手册](https://man.openbsd.org/ssh)

### 公钥、私钥、服务器身份

| 内容 | 放在哪里、用于什么 |
| --- | --- |
| 用户私钥，如 `id_ed25519` | 保留在客户端，用于证明拥有对应身份 |
| 用户公钥，如 `id_ed25519.pub` | 可复制到服务器的允许登录列表 |
| 远程账户的 `~/.ssh/authorized_keys` | 记录允许登录该账户的用户公钥 |
| 客户端的 `~/.ssh/known_hosts` | 记录已知服务器的身份密钥 |
| 私钥 passphrase，密钥口令 | 保护本地私钥，不是服务器账户密码 |

服务器应接收**公钥**，私钥不应上传。首次连接时的服务器指纹，用于确认你连到的是预期服务器；它与“服务器验证你的用户公钥”是两种不同方向的身份验证。

课程用 `ssh-keygen -a 100 -t ed25519` 生成密钥。若要在临时目录里学习文件结构，可明确指定新的练习路径：

```sh
ssh-keygen -a 100 -t ed25519 -f ./practice_ed25519
```

它会交互询问密钥口令，并生成私钥与 `.pub` 公钥；`-a` 设置口令保护所用 KDF 的轮数，`-t` 选择类型，`-f` 指定路径。练习文件不替代已有登录配置。[ssh-keygen 手册](https://man.openbsd.org/ssh-keygen)

课程还用 `ssh-copy-id` 将公钥加入远程账户的 `authorized_keys`。该工具并非每台 Mac 都默认具备；若已安装，可以指定公钥路径和目标账户。密钥口令可结合 `ssh-agent` 管理，减少重复输入。[ssh-agent 手册](https://man.openbsd.org/ssh-agent)

### `scp`：复制文件

```sh
scp notes.txt alice@server.example:~/notes.txt
scp alice@server.example:~/result.txt ./result.txt
scp -r scripts alice@server.example:~/scripts
```

远程路径用 `主机:路径`，源在前、目标在后。`-r` 递归复制目录。端口选项是大写 `scp -P 2222`，与 `ssh -p` 不同。现代 OpenSSH 的 `scp` 默认使用 SFTP 协议完成复制。[scp 手册](https://man.openbsd.org/scp)

### 讲义补充：`rsync`、SSH 配置与转发

`rsync` 可以同步目录，默认通常通过大小与修改时间判断是否需要更新；通过 SSH 工作时，两端需具备兼容的 `rsync`。假设目标目录已存在，`rsync -av src/ host:dest/` 复制源目录内容，`rsync -av src host:dest/` 则包含 `src` 目录这一层。不要把这条尾斜杠规则照搬给其他复制工具。[rsync 官方手册](https://download.samba.org/pub/rsync/rsync.1)

`~/.ssh/config` 可把常用连接参数保存为一个别名：

```sshconfig
Host study
    HostName server.example
    User alice
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```

以后用 `ssh study`；`scp` 等 SSH 工具也可使用这个别名。配置应按自己的服务器与密钥填写。

讲义练习中的 `LocalForward 9999 localhost:8888` 表示：本机 9999 端口经 SSH 通道连接到**远程视角的** localhost:8888。它不会自动启动远程 Web 服务。Mosh 则是课程提到的另一种远程交互工具，适合进一步探索网络中断与切换场景。

## 10. `tmux`：保留可重新连接的终端工作区

`tmux` 是 **terminal multiplexer，终端复用器**。一个客户端连接到 tmux server；server 管理工作区和其中的程序，因此可以分屏，也可以 detach 后再次 attach。[tmux 官方入门](https://github.com/tmux/tmux/wiki/Getting-Started)

| 层级 | 含义 |
| --- | --- |
| Session，会话 | 一组工作窗口，例如一个项目的工作区 |
| Window，窗口 | 会话中的一页，类似标签页 |
| Pane，窗格 | 窗口中的一个分屏，容纳 Shell 或其他程序 |

```sh
tmux new -s study
tmux ls
tmux attach -t study
```

这三条分别用于新建、查看和重新连接；后两条通常在从会话 detach 后的外层 Shell 中使用，按实际步骤执行。

默认前缀是 **Control + B，松开，再按下一个键**，不是把整组键一直按住：

| 前缀之后的键 | 作用 |
| --- | --- |
| `d` | detach，离开客户端显示但保留会话 |
| `c` | 新建窗口 |
| `n` / `p` | 下一个 / 上一个窗口 |
| `0`～`9` | 选择编号窗口 |
| `,` | 给窗口改名 |
| `"` | 上下分屏 |
| `%` | 左右分屏 |
| 方向键 | 移动到对应窗格 |
| `z` | 切换当前窗格的放大显示 |
| `[` | 进入回滚/复制模式 |

远程场景：先 SSH 登录服务器，再在**远程服务器**上运行 tmux 和任务；断开客户端后，远程 tmux server 与其中程序可以继续。重新 SSH 登录后，再 attach 回去。

在本机开一个 tmux 窗格并运行普通 SSH，不会自动让远程进程也获得远程 tmux 的保护。tmux 也不能让任务穿越主机重启、server 被结束或程序自身退出。

## 11. 安装工具与找到正确的命令

包管理器下载、安装、更新软件。课程按平台介绍了 macOS 的 Homebrew、Ubuntu/Debian 的 `apt`、Fedora 的 `dnf`、Arch 的 `pacman`；更完整的依赖与交付在后续课程学习。

| 工具/包 | 用途 |
| --- | --- |
| `ripgrep`，命令名 `rg` | 快速搜索文本 |
| `fd` | 更方便的文件查找接口 |
| `fzf` | 对候选列表交互筛选 |
| `tmux` | 终端复用 |
| `tldr`（讲义补充） | 提供常见用法示例，作为 `man` 的辅助 |

`command not found` 表示当前命令解析失败：可能没有安装，也可能目录未进入 `PATH`，或命令名与包名不同。`ripgrep` 和 `rg` 的区别就是课堂中的例子。

课程给出的 Homebrew 示例是 `brew install ripgrep`。先确认本机是否具备对应包管理器，再按需要安装；阅读本课不要求一次装齐工具。

安装说明中的 `curl … | bash` 表示把下载内容直接作为脚本执行。课程建议先下载、查看，再运行；`bash -c "$(curl …)"` 同样执行了下载的内容，明确了解释器也不等于审阅了脚本。

## 12. 配置文件、PATH、`source` 与别名

### 改变当前会话与持久化配置

终端里赋值或定义函数，通常只影响当前 Shell 及相应子进程。要让新 Shell 自动获得配置，需要放到它会读取的启动文件中。

| Shell / 文件 | 常见读取条件 |
| --- | --- |
| Bash `~/.bashrc` | 交互、非登录 Shell |
| Bash `~/.bash_profile`、`~/.bash_login`、`~/.profile` | 登录 Shell 按顺序读取第一个存在且可读的文件 |
| Zsh `~/.zshenv` | 通常每次启动；适合保持很少的必要设置 |
| Zsh `~/.zprofile` | 登录 Shell |
| Zsh `~/.zshrc` | 交互 Shell，常放别名、补全、提示符等 |
| Zsh `~/.zlogin` | 登录 Shell，在交互配置之后读取 |

表中是通常的用户文件路径；系统文件、启动选项及 Zsh 的 `ZDOTDIR` 等配置也会影响它们。Bash 登录 Shell 不会自动再读 `.bashrc`，很多配置会在 profile 中显式加载它。[Bash 启动文件](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html) · [Zsh 启动文件](https://zsh.sourceforge.io/Doc/Release/Files.html)

PATH 配置例如 `export PATH="$HOME/.local/bin:$PATH"`：把新目录放前面，它的同名程序优先；放到末尾则让原目录优先。重复加载这种赋值可能重复添加路径，长期配置应考虑避免重复。

### `source` 在当前 Shell 中执行文件

```sh
printf "MS_NOTE='loaded from file'\n" > demo.conf
source ./demo.conf
printf '%s\n' "$MS_NOTE"
```

`source` 或 `.` 读取文件，并在当前 Shell 执行其中内容。因此赋值、别名、函数和 `cd` 可以改变当前会话；`bash demo.conf` 在子进程中执行，不能把普通变量变化传回父 Shell。

`source` 执行的是代码，不只是被动读取设置。它也不自动把 Bash 语法转成 Zsh 语法；配置应匹配使用它的 Shell。

### 提示符与 alias（alias 为讲义补充）

提示符可用 Bash 的 `PS1` 或 Zsh 的 `PROMPT` / `PS1` 设置。两者的提示符转义语法不完全相同；改变提示符外观不改变用户权限。

```sh
alias ll='ls -lh'
alias ll
```

定义后，在交互 Shell 单独输入 `ll` 就使用这个展开；`unalias ll` 删除它。可以用 `type ll` 查实际含义，通常用 `command ls` 绕过同名别名或函数。

alias 主要适合交互快捷输入，Bash 非交互脚本默认不展开 alias。要接收并处理参数、执行多步逻辑，使用函数；转交参数写 `other_command "$@"` 保留各自边界。

## 13. 历史、dotfiles 与插件

### 历史搜索

上箭头逐条浏览历史，`Control + R` 通常进行反向搜索。安装 `fzf` 后，还需要相应 Shell 集成，才能把快捷键变成 fzf 的模糊历史搜索；仅安装程序不等于所有快捷键已经替换。

历史文件的格式、何时写入、不同会话是否共享，受 Shell 配置影响。命令历史也不等于屏幕回滚：前者记命令，后者包括终端里显示的输出。

### dotfiles 与符号链接

**dotfiles** 指名字以 `.` 开头的配置文件，如 `.zshrc`、`.gitconfig`、`.ssh/config`、`.tmux.conf`。开头的点是隐藏显示约定，不是特殊权限。

课程建议把可共享配置放进独立目录，用 Git 记录变化，再通过符号链接安装到应用期待的位置。下面只在练习目录演示这个关系：

```sh
mkdir dotfiles demo-home
printf "alias ll='ls -lh'\n" > dotfiles/zshrc
ln -s "$PWD/dotfiles/zshrc" demo-home/.zshrc
ls -l demo-home/.zshrc
```

`demo-home/.zshrc` 是指向配置文件的链接，不是另一份独立副本；修改目标内容会改变读取结果。真实部署还需保留原有配置、处理不同系统差异，并把私钥、令牌等留在共享配置之外。

### 插件按功能理解

| 课程提到的功能 | 例子 |
| --- | --- |
| 输入时语法高亮 | `zsh-syntax-highlighting` |
| 从历史推测接下来要输入的命令 | `zsh-autosuggestions` |
| 额外补全定义 | `zsh-completions` |
| 根据命令片段搜索历史 | `zsh-history-substring-search` |
| 显示目录、Git 状态等提示信息 | 提示符主题，如 `powerlevel10k` |

补全、建议、高亮、提示符是不同功能。提示符显示 Git 状态不会帮你提交；自动建议也要在接受后才成为实际输入。

课程强调按需要逐个添加功能。Oh My Zsh、Prezto 等框架可以组织配置，但启用很多插件也可能增加启动开销；Fish 等 Shell 则内置一些交互功能，语法与 Bash 不完全相同。

## 14. AI 在 Shell 中的三种用法

最后的 AI 演示仍建立在前面的接口模型上：自然语言可以帮助生成或执行操作，参数、输入流、退出状态和实际文件变化依然需要读懂。

### 生成一条命令

课程使用 Simon Willison 的 `llm` 工具，让模型根据自然语言提出 `find` 命令，例如查找近期修改的 Python 文件。

```sh
llm cmd "find all python files modified in the last day"
```

`llm cmd` 来自 `llm-cmd` 插件，需要已安装 LLM、该插件并配置可用模型；它会展示生成的命令，供使用者检查或编辑后执行。这里记录的是课堂思路，不把模型生成视为正确性保证。[llm-cmd 官方说明](https://github.com/simonw/llm-cmd)

### 把模型作为数据处理阶段

课堂有一组格式不一致的用户名记录，模型根据“每行只输出用户名”的指令解析，然后把结果交给 `sort` 等传统工具。

```sh
instructions='Extract just the username from each line, one per line, nothing else'
llm "$instructions" < users.txt | sort
```

这条命令假设已准备 `users.txt` 并配置好 `llm`：

| 部分 | 作用 |
| --- | --- |
| `"$instructions"` | 一个包含完整指令的参数 |
| `< users.txt` | 用户记录作为 stdin，而不是文件名参数 |
| `llm` 的 stdout | 模型产生的文本 |
| `\| sort` | 下游程序继续处理模型输出 |

双引号保护指令中的空格。下游会按实际收到的文本工作，所以要观察输出是否符合一行一个用户名的约定；模型可能理解错格式或添加额外文字。[LLM 官方文档](https://llm.datasette.io/)

### 代理完成多步任务

课程用 Claude Code 演示：找出最近修改的 Shell 脚本，读取信息，再提出修改 shebang 的文件编辑。与只生成一条命令相比，代理可以组织多步工具调用和文件修改。

字幕对目标 Shell 名称有歧义，这里保留演示意图，不根据转写断言具体改成了哪个解释器。**改 shebang 只改变直接执行时选择的解释器，不会自动把脚本语法翻译成另一种 Shell。**

AI 可以减少记忆选项与手工传递中间结果的负担。理解本课这些接口，则让我们能检查命令做了什么、输入来自哪里、输出是否符合预期，以及文件究竟怎样改变。

## 15. Terminal emulator：配置终端应用本身

最后一段回到 **terminal emulator，终端模拟器**。它提供显示与按键交互窗口；Shell、tmux、插件与它是不同组件。

课程讲者使用 Alacritty，并演示改变字体大小。终端设置还包括字体、颜色、快捷键、标签/分屏、回滚长度和渲染性能；这些设置不一定在 `.zshrc` 中。[Alacritty 官方配置说明](https://alacritty.org/config-alacritty.html)

| 想改变的东西 | 通常应找哪里？ |
| --- | --- |
| 字体大小、背景、窗口快捷键 | Terminal emulator 的设置 |
| 提示符、命令补全、历史行为 | Shell 的配置与插件 |
| 会话、窗格和 tmux 快捷键 | tmux 配置 |
| 远程用户名、端口、密钥选择 | SSH 配置 |
| AI 模型与提示指令 | AI CLI 工具的配置或调用参数 |

先辨认由哪个组件负责，再找到对应配置，比把所有设置写进同一个文件更容易理解。

## 16. 本讲复习检查

1. 一条 CLI 命令的参数、stdin、环境变量分别是什么？stdout 与退出状态有什么区别？
2. `--` 与 `-` 各是什么约定？glob 与花括号展开分别由谁处理？
3. 为什么管道各阶段可能同时运行，但屏幕上的结果仍迟迟不出现？
4. `export` 改变哪些进程能看到变量？已有子进程会实时得到新值吗？
5. `$()`、`<()` 与 `<` 分别产生字符串、文件接口还是输入连接？
6. `Control + C`、`Control + Z` 与 `kill -CONT` 分别改变什么？作业号与 PID 有何区别？
7. `&`、`nohup`、`disown` 与远程 `tmux` 各解决了哪一部分问题？
8. 服务器需要用户的公钥还是私钥？`authorized_keys` 与 `known_hosts` 验证谁？
9. 引号怎样影响 SSH 管道在本机还是远程执行？
10. `source` 与运行一个子 Shell 有何区别？`.zshrc` 与 `.zprofile` 何时读取？
11. AI 管道中的指令与数据分别通过什么接口传入？代理修改后怎样确认实际变化？
12. 想改字体、提示符或 SSH 端口，应分别去哪个组件的配置？

练习见[第二讲实践](../exercises/02-command-line.md)，第一讲的基础接口见[第一讲完整总结](01-shell.md)，原始字幕和术语校正见[第二讲来源记录](../source/02-command-line-source.md)。

## 来源与许可

本页依据用户提供的[第二讲英文字幕](../source/02-command-line.en.srt)、[中文字幕](../source/02-command-line.zh.srt)及 [Missing Semester 2026 官方第二讲](https://missing.csail.mit.edu/2026/command-line-environment/)重新总结，并结合上文工具官方文档与 macOS 行为核对。示例数据与有限清理演示为原创。课程由 Anish Athalye、Jon Gjengset、Jose 团队教授，本课程目录的改写内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，转载或改编须保留署名、来源和相同许可。
