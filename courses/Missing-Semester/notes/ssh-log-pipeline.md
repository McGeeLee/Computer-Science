# SSH 日志管道命令详解

截图中的命令想完成这件事：**读取远程服务器上一次启动期间的 SSH 服务日志，提取断开记录中的用户名，统计各用户名出现的次数，选出次数最多的至多十个，最后用逗号连接。**统计对象是日志记录次数，不能直接当作成功登录次数或真实用户人数。

课堂演示中，这条命令没有按老师的预期运行，这也说明：即使是非常熟练、经验丰富的使用者，使用 Shell 时依然可能遇到问题。

## 1. 先把整条命令读出来

截图中的一行命令，按管道拆开后是：

```sh
ssh tsp 'journalctl -u sshd -b-1 | grep "Disconnected from"' |
  sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' |
  sort |
  uniq -c |
  sort -nk1,1 |
  tail -n10 |
  awk '{print $2}' |
  paste -sd,
```

行末的 `|` 表示管道还没有结束，因此 Bash / Zsh 会继续读取下一行；这里分行是为了方便阅读。截图开头的 `[jon@xos:~]$` 是讲者的提示符，不属于命令，复制时不要输入。

**macOS 自带的 `paste` 需要明确给出输入文件。**在 Mac 上，末尾换成下面这一行，`-` 表示从标准输入读取：

```sh
paste -s -d ',' -
```

GNU `paste` 在没有文件参数时也会读取标准输入，因此截图里的 `paste -sd,` 适用于 GNU 工具环境。本笔记的本地练习使用带 `-` 的写法，兼容两种环境。[GNU paste 文档](https://www.gnu.org/software/coreutils/manual/html_node/paste-invocation.html)；macOS 的对应规则可查本机 `man paste`。

## 2. 数据经过哪些地方？

```text
远程服务器 tsp
  journalctl：读取 SSH 服务日志
    → grep：筛选含有 Disconnected from 的行
          ↓ SSH 把输出传回本机
本机
  sed：从日志行中提取用户名
    → sort：让相同用户名相邻
    → uniq -c：统计每组的行数
    → sort -nk1,1：按次数从小到大排序
    → tail -n10：保留最后十行
    → awk：只取用户名字段
    → paste：把多行连接成一行
```

普通管道 `A | B` 把 A 的 **stdout（标准输出）**接到 B 的 **stdin（标准输入）**。传递的是数据流；stderr（标准错误）不会自动进入这条管道。

各个阶段可以同时运行，后一阶段读取前一阶段产生的数据。这里的 `sort` 要读完整个输入，才能给出完整排序结果，所以后面的统计会等待日志读取完成。管道的文字顺序表示数据流向，不表示每个程序都要等前一个程序退出后才启动。

## 3. `ssh tsp 'journalctl … | grep …'`：远程取日志

### `ssh tsp`

`ssh` 通过 SSH 连接远程机器。`tsp` 是讲者使用的连接目标，可能是主机名或 SSH 配置中的别名；它不是 Shell 的关键字，也不是你电脑上一定存在的服务器。

`ssh` 在目标后面接命令时，会请求在远程机器上执行该命令，并把输出传回来。[OpenSSH ssh 手册](https://man.openbsd.org/ssh)

### 为什么把里面的命令放在单引号中？

```sh
ssh tsp 'journalctl -u sshd -b-1 | grep "Disconnected from"'
```

本机 Shell 先解析这一行。外层单引号让下面的内容作为一个完整参数交给 `ssh`：

```text
journalctl -u sshd -b-1 | grep "Disconnected from"
```

这个字符串随后由远程 Shell 解释。因此：

| 位置 | 执行地点 |
| --- | --- |
| 单引号内的 `journalctl`、`grep` 和它们之间的 `|` | 远程服务器 |
| 单引号闭合后的 `| sed …` 及后续工具 | 本机 |

内层双引号保留在传给远程的字符串里，远程 Shell 再用它把 `Disconnected from` 作为一个参数传给 `grep`。这就是同一行里两层 Shell 分别解析各自语法的例子。

### `journalctl -u sshd -b-1`

`journalctl` 读取 systemd 的 journal 日志，通常用于采用 systemd 的 Linux 系统。这里是在远程服务器上使用它，Mac 本机不需要安装 `journalctl`。

| 部分 | 含义 |
| --- | --- |
| `journalctl` | 查询系统日志 |
| `-u sshd` | 按服务单元（unit）筛选 SSH daemon 的日志 |
| `-b-1` | 紧凑写法，相当于 `-b -1`，选择上一次启动的日志 |

`-b` 是 boot 的选项，`-1` 是相对启动编号：`0` 表示本次启动，`-1` 表示上一次。它不是“最近一天”。可查询的启动记录取决于 journal 保留了什么；SSH 服务单元在另一台服务器上也可能叫 `ssh.service` 等名称，需按该机器实际配置查询。[systemd journalctl 手册](https://www.freedesktop.org/software/systemd/man/255/journalctl.html)

### `grep "Disconnected from"`

`grep` 输出包含匹配内容的整行。这里的模式包含空格，所以用引号把它组合成一个参数；模式里没有正则特殊字符，效果就是搜索这段文字。

例如，原日志可能包含启动、认证和连接断开等多种记录，经过这一层后留下：

```text
Oct 07 09:00:01 server sshd[101]: Disconnected from invalid user admin 192.0.2.10 port 50001 [preauth]
Oct 07 09:00:02 server sshd[102]: Disconnected from authenticating user root 192.0.2.11 port 50002 [preauth]
```

到这里仍是完整日志行，用户名还没有被单独提取。

## 4. `sed -E 's/…/\1/'`：提取用户名

```sh
sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/'
```

`sed` 接收日志文本，按规则替换。`-E` 启用 **extended regular expression（扩展正则表达式，ERE）**，这里的 `(...)` 和 `+` 因而可以直接表示分组和重复。

替换表达式的结构是：

```text
s / 要匹配的正则 / 替换成的内容 /
```

这里的 `/` 是表达式分隔符；`s` 表示 substitute（替换）。没有 `-i`，所以这条命令只把处理结果写到标准输出，不修改日志文件。

### 正则逐段解释

模式是：

```regex
.*Disconnected from .* user (.*) [^ ]+ port.*
```

| 片段 | 含义 | 在例子中匹配的内容 |
| --- | --- | --- |
| 第一个 `.*` | 任意字符重复零次或多次 | 时间、主机、进程等日志前缀 |
| `Disconnected from ` | 字面文字，包含末尾空格 | `Disconnected from ` |
| `.* user ` | 若干字符，再接字面文字 ` user ` | `invalid user ` 或 `authenticating user ` |
| `(.*)` | 捕获第 1 组，目标是用户名 | `admin` |
| 分组后的空格 | 匹配一个字面空格 | 用户名和地址之间的空格 |
| `[^ ]+` | 一个或多个非空格字符 | `192.0.2.10` |
| ` port` | 字面空格与文字 `port` | ` port` |
| 最后的 `.*` | 匹配其后的字符 | ` 50001 [preauth]` |

`[^ ]` 中的 `^` 在方括号开头表示“排除”，因此整个字符类表示“一个不是普通空格的字符”。它与行首锚点 `^` 的作用不同。`+` 要求至少一个；这一段只是按字符形状匹配一个片段，并不验证它一定是合法 IP 地址。

`.*` 通常是**贪婪匹配**：在让整个表达式匹配成功的前提下，尽量吃掉更多字符。因此 `(.*)` 没有从语法上限制“只含一个用户名”；这条规则依赖截图中那类日志格式。这里用的是正则表达式，相关语法见[正则表达式与通配符](regex-and-globs.md)。

### 为什么替换成 `\1`？

括号把用户名保存为第 1 个捕获组，替换部分的 `\1` 表示“把第 1 个捕获组的内容放回来”。于是：

```text
输入：Oct 07 09:00:01 server sshd[101]: Disconnected from invalid user admin 192.0.2.10 port 50001 [preauth]
输出：admin
```

前缀、状态、地址、端口等内容都在这次匹配中被替换掉，留下捕获的用户名。外层单引号让 Shell 把反斜杠按字面交给 `sed`。`\1` 是 `sed` 的反向引用语法。[GNU sed 捕获组与反向引用说明](https://www.gnu.org/software/sed/manual/html_node/Back_002dreferences-and-Subexpressions.html)

### 原命令的一个限制：未匹配的行也会输出

`sed` 默认会输出处理后的每一行。**替换成功就输出替换结果；替换失败则输出原行。**`grep` 只检查过 `Disconnected from`，不能保证后面的完整正则一定匹配。[GNU sed 手册](https://www.gnu.org/software/sed/manual/sed.html)

例如，下面这类记录含有搜索词，却不符合截图中 `.* user ` 所要求的格式：

```text
Oct 07 09:00:07 server sshd[107]: Disconnected from user carol 192.0.2.16 port 50007
```

`Disconnected from ` 后直接是 `user`，缺少原模式在该 `user` 前要求的额外空格或内容。这一整行会原样进入后面的 `sort` 和 `uniq`；最终 `awk` 提取第二个字段时，可能拿到日志月份 `Oct`，而不是用户名。

如果希望**只输出成功提取的用户名**，并把用户名限制为一个非空格片段，可以使用：

```sh
sed -nE 's/^.*Disconnected from .* user ([^ ]+) [^ ]+ port.*$/\1/p'
```

新增的 `-n` 关闭自动输出，末尾 `p` 只在替换成功时输出；`([^ ]+)` 收紧用户名的匹配范围，`^` 和 `$` 标记整行边界。这仍是针对 `invalid user` / `authenticating user` 这类格式的规则；上面的普通 `Disconnected from user carol …` 会被跳过。若要统计其他日志格式，需要为它们另外设计提取规则。

## 5. `sort | uniq -c`：计算每个用户名的次数

假设 `sed` 得到六行：

```text
admin
root
admin
guest
root
admin
```

### 第一个 `sort`：让相同用户名相邻

```text
admin
admin
admin
guest
root
root
```

这里按文本排序，不用 `-n`，因为排序对象是用户名。

### `uniq -c`：统计相邻重复行

```text
      3 admin
      1 guest
      2 root
```

`uniq` 合并相邻的相同行，`-c`（count）在每组前面输出出现次数。输出顺序是 **次数在前、用户名在后**，前面的填充空格可能因实现而异。

`uniq` 只比较相邻行，所以前面的 `sort` 有实际作用。如果直接对原来交错的六行执行 `uniq -c`，相同用户名没有连续出现，会分成多个计数为 1 的组。

## 6. `sort -nk1,1 | tail -n10`：取频次最高的十行

### `sort -nk1,1`

这段紧凑写法可以展开成：

```sh
sort -n -k 1,1
```

| 选项 | 作用 |
| --- | --- |
| `-n` | 按数字大小比较（numeric sort） |
| `-k 1,1` | 排序键从第 1 个字段开始，在第 1 个字段结束，即只取次数这一列 |

`1,1` 中两个数字分别是起始字段、结束字段，不是“第一列和另一列”。`uniq -c` 输出前面的空格属于字段分隔，数值比较能读出后面的次数。默认从小到大排序；用数字排序才能正确比较 `2` 和 `10`。

例子变成：

```text
      1 guest
      2 root
      3 admin
```

### `tail -n10`

相当于 `tail -n 10`，保留输入的最后十行。因为次数已按升序排列，最后十行就是次数最多的十行。

需要同时记住三件事：

- 不足十个不同用户名时，全部保留；六条日志只有三个不同用户名，所以本例保留三行。
- 保留下来的行仍按次数从小到大排列，出现次数最多的名字在最后。
- 如果第十名附近有相同次数，它仍只取十行，并不会自动保留所有并列项；具体取舍受排序的后备比较和 locale（区域设置）影响。

若希望按次数从大到小展示，可以把这两步改成 `sort -nr -k1,1 | head -n10`，此时次数最多的在最前面。[GNU sort 选项说明](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)

## 7. `awk '{print $2}'`：只留下用户名

```sh
awk '{print $2}'
```

`awk` 默认按空白分隔字段，并忽略用于分隔的连续空白。对于这一行：

```text
      3 admin
```

| awk 表达式 | 对应内容 |
| --- | --- |
| `$0` | 完整输入行 |
| `$1` | 第一个字段：`3` |
| `$2` | 第二个字段：`admin` |

`{print $2}` 对每一行执行“输出第二个字段”。三个计数行处理后变成：

```text
guest
root
admin
```

这里的 `$2` 由 **awk** 解释，表示第二个字段。单引号保护它，不让 Shell 提前把它当成 Shell 的第二个位置参数展开。名字看似一样，含义取决于由哪个程序解释。

## 8. `paste -sd,`：把多行连成一行

截图中的紧凑选项是 `-s` 与 `-d ,` 的组合。使用明确的标准输入参数，可以写成：

```sh
paste -s -d ',' -
```

| 部分 | 含义 |
| --- | --- |
| `-s` | serial，依次连接一个输入源中的各行 |
| `-d ','` | delimiter，使用逗号作为连接分隔符 |
| 最后一个 `-` | 把标准输入作为输入源，接收前面管道的输出 |

所以：

```text
guest
root
admin
```

变成：

```text
guest,root,admin
```

名字之间加逗号，末尾仍有换行。次数已经在 `awk` 阶段被丢掉，因此这个最终结果只有用户名。

## 9. 在 Mac 上用小数据完整验证

下面的例子只在本机处理模拟日志，不需要讲者的服务器。`cat <<'LOG'` 使用 **here-document（此处文档）**提供多行输入；独占一行的 `LOG` 结束输入，带引号的起始标记让其中内容按字面传给 `cat`。

```sh
cat <<'LOG' |
Oct 07 09:00:00 server sshd[100]: Server listening on 0.0.0.0 port 22.
Oct 07 09:00:01 server sshd[101]: Disconnected from invalid user admin 192.0.2.10 port 50001 [preauth]
Oct 07 09:00:02 server sshd[102]: Disconnected from authenticating user root 192.0.2.11 port 50002 [preauth]
Oct 07 09:00:03 server sshd[103]: Disconnected from invalid user admin 192.0.2.12 port 50003 [preauth]
Oct 07 09:00:04 server sshd[104]: Disconnected from invalid user guest 192.0.2.13 port 50004 [preauth]
Oct 07 09:00:05 server sshd[105]: Disconnected from authenticating user root 192.0.2.14 port 50005 [preauth]
Oct 07 09:00:06 server sshd[106]: Disconnected from invalid user admin 192.0.2.15 port 50006 [preauth]
LOG
  grep "Disconnected from" |
  sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' |
  sort |
  uniq -c |
  sort -nk1,1 |
  tail -n10 |
  awk '{print $2}' |
  paste -s -d ',' -
```

预期输出：

```text
guest,root,admin
```

可以先只运行到 `grep`，观察留下哪些日志行，再逐次加上后面的阶段；每增加一段，都先预测输出。这是读懂长管道最直接的方法。

| 阶段结束后 | 数据的样子 |
| --- | --- |
| `grep` | 筛选后的完整日志行 |
| `sed` | 每行一个用户名 |
| 第一个 `sort` | 相同用户名连续出现 |
| `uniq -c` | 每行一组“次数 + 用户名” |
| 第二个 `sort` | 次数从小到大 |
| `tail` | 最多十行“次数 + 用户名” |
| `awk` | 每行一个用户名，保留排名顺序 |
| `paste` | 一行逗号分隔的用户名 |

**每一段都依赖上一段的数据形状。**例如 `awk` 的第二字段只有在上游确实产出“次数 + 单个用户名”时才是用户名；这也解释了为什么前面 `sed` 的匹配范围会影响最终结果。

## 来源与许可

命令依据用户截图，并与用户提供的[第一讲英文字幕](../source/01-shell.en.srt)核对；解释结合上文链接的工具手册与本机 macOS 行为，示例日志为原创模拟数据。本笔记属于 [Missing Semester 2026 学习资料](../README.md)，改写内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，课程来源与署名见课程目录说明。
