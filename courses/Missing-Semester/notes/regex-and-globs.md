# 正则表达式与通配符

**通配符（wildcards / glob patterns）**和**正则表达式（regular expressions，regex / regexp）**都是描述匹配规则的方式，但语法不同。理解一条命令时，先确定：**模式交给谁解释，匹配的对象是什么？**

本笔记以 Bash / Zsh 的基础文件名通配，以及 `grep -E` 使用的扩展正则表达式为主。

## 1. 从一条命令看两者的分工

| 对比项 | Shell 文件名通配 | 正则表达式，以 grep 为例 |
| --- | --- | --- |
| 常见用途 | 选择文件名或路径 | 搜索文本中符合规则的内容 |
| 谁解释 | Shell 在启动命令前展开 | grep 收到模式后解释 |
| 匹配范围 | 整个文件名或路径组件 | 默认寻找每行中的匹配片段 |
| 匹配结果 | 文件路径作为参数交给命令 | 默认输出包含匹配的整行 |
| 任意长度片段 | `*` | `.*` |
| 任意一个字符 | `?` | `.` |

例如，假设当前目录有 `app.log` 和 `server.log`：

```sh
grep -nE '^ERROR' *.log
```

1. Shell 将 `*.log` 展开为两个文件名，把正则字符串 `^ERROR` 原样交给 grep；引用用的单引号不会作为参数内容传入。
2. grep 按 `^ERROR` 搜索这两个文件，输出以 ERROR 开头的行；`-n` 显示行号。

此时效果类似执行 `grep -nE '^ERROR' app.log server.log`。`*.log` 和 `^ERROR` 分别由不同的程序解释。

这个分工描述的是上述用法。glob 规则也能由 `find -name` 等工具解释；正则也能用于匹配文件名字符串，不必把两者的用途固定成“只能处理文件名”或“只能处理文件内容”。

## 2. 基础通配符：glob

| 写法 | 含义 | 示例 |
| --- | --- | --- |
| `*` | 匹配零个或多个字符 | `*.txt` 匹配 `note.txt`、`report.txt` |
| `?` | 匹配恰好一个字符 | `report?.txt` 匹配 `report1.txt`，不匹配 `report12.txt` |
| `[abc]` | 匹配集合中的一个字符 | `file[ab].txt` 匹配 `filea.txt`、`fileb.txt` |
| `[0-9]` | 匹配范围内的一个字符，此例用于数字 | `file[0-9].txt` 匹配 `file3.txt`，不匹配 `file12.txt` |
| `[!abc]` | 匹配不在集合中的一个字符；Bash / Zsh 也支持 `[^abc]` | `file[^ab].txt` 可匹配 `filec.txt` |
| `.` | 普通的点 | `*.txt` 中的点就是文件名中的点 |

`[abc]` 只占一个字符的位置，不表示字符串 `abc`。范围的解释可能受 locale（区域设置）影响；上面的例子使用普通 ASCII 名称。[Bash 模式匹配说明](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)

在交互式 Zsh 中，`[!abc]` 的 `!` 可能先触发历史展开，报 `event not found`；直接试文件名通配时，可以使用 `[^abc]`。给整个模式加引号会阻止 Shell 文件名展开，不能用它来实现同一个效果；交给 `find -name` 的模式则可以加引号。[Zsh 历史展开规则](https://zsh.sourceforge.io/Doc/Release/Expansion.html#History-Expansion)

Shell 文件名展开还要注意：

- 普通 `*` 不跨越路径分隔符 `/`；`*.txt` 不会自动搜索整个目录树。`src/*.py` 选择 src 目录下匹配的名字。
- 默认情况下，`*` 不包含名称以 `.` 开头的隐藏项，如 `.git`；相关 Shell 设置可以改变这一点。
- 文件名中的空格不会让一个展开结果拆成多个参数。
- 无匹配时，Bash 默认把模式原样留下；Zsh 默认通常报 `no matches found`，此时目标命令还没有执行。设置可以改变这些行为。
- `**` 的递归含义随 Shell 和设置而变，不能把它当成所有环境通用的基础规则。

这些是文件名展开规则，而非正则语法。[Bash 文件名展开](https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html)、[Zsh 文件名展开](https://zsh.sourceforge.io/Doc/Release/Expansion.html#Filename-Generation)

## 3. 正则表达式基础：以 ERE 为主

下面的写法用于 `grep -E '模式'`。**量词作用于紧挨着它的前一个匹配项**：可以是一个字符、字符集合或括号分组。

| 写法 | 含义 | 示例 |
| --- | --- | --- |
| `abc` | 连续的普通字符 | 可在 `xxabcxx` 中找到 `abc` |
| `.` | 当前行中任意一个字符 | `a.c` 可匹配 `abc`、`a-c` |
| `*` | 前一项重复零次或多次 | `ab*c` 可匹配 `ac`、`abc`、`abbc` |
| `+` | 前一项重复一次或多次 | `ab+c` 匹配 `abc`、`abbc`，不匹配 `ac` |
| `?` | 前一项出现零次或一次 | `colou?r` 匹配 `color`、`colour` |
| `{n}` | 前一项恰好出现 n 次 | `a{3}` 匹配 `aaa` |
| `{n,m}` | 前一项出现 n 到 m 次 | `a{2,4}` 匹配长度为 2～4 的 a 片段 |
| `{n,}` | 前一项至少出现 n 次 | `a{2,}` 匹配至少两个连续的 a |
| `[abc]` | 集合中的一个字符 | `[ab]c` 匹配 `ac` 或 `bc` |
| `[^abc]` | 不在集合中的一个字符 | `[^0-9]` 匹配一个非数字字符 |
| `[0-9]` | 数字范围中的一个字符 | `[0-9]+` 匹配连续数字片段 |
| `^` | 行首位置，不消耗字符 | `^ERROR` 匹配行首的 ERROR |
| `$` | 行尾位置，不消耗字符 | `\.txt$` 匹配行尾的 `.txt` |
| `(ab)` | 将内容组成一个匹配项 | `(ab)+` 匹配 `ab`、`abab` 等片段 |
| `a\|b` | 选择左边或右边 | `cat\|dog` 匹配 cat 或 dog |
| `\.` | 匹配普通的点 | `a\.c` 匹配 `a.c` |

这里 `*`、`+`、`?`、`{...}` 称为 **量词（quantifiers）**，`^`、`$` 称为 **锚点（anchors）**。[正则的组合与重复规则](https://www.gnu.org/software/grep/manual/html_node/Fundamental-Structure.html)、[锚点说明](https://www.gnu.org/software/grep/manual/html_node/Anchoring.html)

常用 POSIX 字符类包括 `[[:digit:]]`（数字）、`[[:alpha:]]`（字母）、`[[:alnum:]]`（字母或数字）、`[[:space:]]`（空白字符）。注意是两层方括号；成员范围与 locale 有关。[字符类说明](https://www.gnu.org/software/grep/manual/html_node/Character-Classes-and-Bracket-Expressions.html)

## 4. 同一个符号，两套规则

| 符号或目的 | 基础 glob | ERE 正则 |
| --- | --- | --- |
| `*` | 任意长度的名字片段 | 重复前一项零次或多次 |
| `?` | 恰好一个字符 | 前一项可有可无 |
| `.` | 普通的点 | 任意一个字符；普通点写 `\.` |
| `[abc]` | 集合中的一个字符 | 集合中的一个字符 |
| 排除字符集合 | `[!abc]`；Bash / Zsh 也支持 `[^abc]` | `[^abc]` |
| 匹配整个名字 / 整行 | glob 本身匹配整个名字 | 用 `^...$` 或 `grep -x` |
| 以 `.txt` 结尾 | 文件名模式 `*.txt` | 文本模式 `\.txt$`；整行模式 `^.*\.txt$` |

尤其注意 `a*`：

- glob 中，它选择以 a 开头、后面可以有其他字符的名字，如 `apple`。
- ERE 中，它描述零个或多个 a；它也能匹配空串，所以 `grep -E 'a*'` 会选中所有输入行，包括不含 a 的行。

如果要搜索“字母 a 后面跟任意内容”，正则写 `a.*`。如果要验证整行都由 a 组成且至少有一个 a，写 `^a+$`。

## 5. 搜索片段与匹配整行

`grep -E 'cat'` 会选中 `cat`、`catfish` 和 `a cat sleeps` 所在的行。找到匹配片段后，grep 默认输出整行。

```sh
printf '%s\n' 'cat' 'catfish' 'a cat sleeps' | grep -Ex 'cat'
```

结果只有 `cat`。`-x` 要求模式匹配整行；也可以使用 `grep -E '^cat$'`。若只想输出匹配到的片段，可以加 `-o`；若忽略大小写，可以加 `-i`。[grep 匹配范围](https://www.gnu.org/software/grep/manual/html_node/Matching-Control.html)、[输出控制](https://www.gnu.org/software/grep/manual/html_node/General-Output-Control.html)

多选分支与锚点组合时，要把整体括起来：

| 模式 | 含义 |
| --- | --- |
| `^cat\|dog$` | 行首是 cat，或者行尾是 dog；两边是不同分支 |
| `^(cat\|dog)$` | 整行恰好是 cat 或 dog |

## 6. 引号、转义与固定字符串

```sh
grep -E 'a.*b' notes.txt
grep -F 'a.*b' notes.txt
```

第一行把 `a.*b` 作为正则，搜索 a 与 b 之间可以有任意内容的片段。第二行按字面搜索字符序列 `a.*b`。

**单引号保护的是 Shell 这一层；grep 收到参数后，仍按所选模式解释。**想搜索普通文本，用 `grep -F`；想在正则里匹配普通的点，用 `\.`。例如 `grep -E '\.txt$' names.txt` 搜索以 `.txt` 结尾的文本行。

两层规则也解释了下面的写法：

```sh
printf '%s\n' *.txt
printf '%s\n' '*.txt'
find . -type f -name '*.txt'
```

- 第一行让 Shell 展开匹配的文件名，前提是存在匹配项。
- 第二行只输出字面文字 `*.txt`。
- 第三行用引号保留模式，让 **find** 自己按 glob 规则筛选文件名，并递归搜索当前目录；`-type f` 限制为普通文件。

因此是否加引号，要看这段模式准备交给 Shell 展开，还是交给后面的工具解释。[find 的模式与引号说明](https://www.gnu.org/software/findutils/manual/html_node/find_html/Shell-Pattern-Matching.html)

## 7. 正则有不同的语法版本

| 用法 | 模式类型 | 本笔记中的用法 |
| --- | --- | --- |
| `grep '模式'` | BRE：基本正则表达式 | 可以使用点、星号、方括号和锚点；部分符号的写法与 ERE 不同 |
| `grep -E '模式'` | ERE：扩展正则表达式 | 本笔记的正则表以它为准，如 `+`、`?`、`(...)`、`a\|b` |
| `grep -F '文字'` | fixed strings：固定字符串 | 按字面搜索，不解释正则元字符 |

BRE 与 ERE 的区别不只是“功能强弱”，还包括特殊符号的写法。某些实现支持额外扩展，不能把一处能用的写法默认套到所有工具。[grep 模式类型](https://www.gnu.org/software/grep/manual/html_node/grep-Programs.html)、[BRE 与 ERE 的区别](https://www.gnu.org/software/grep/manual/html_node/Basic-vs-Extended.html)

Python 的 `re`、编辑器的搜索框和 PCRE 又有各自的规则。不能假定 `grep -E` 支持 `\d`、`\s`、懒惰量词或前后查找；在这里用 `[[:digit:]]`、`[[:space:]]` 等对应写法。`grep -P` 的支持情况取决于实现，本笔记的示例不依赖它。

## 8. 可直接运行的小例子

下面只处理临时生成的文本，不需要创建文件。

```sh
printf '%s\n' 'A12' '007' 'abc' | grep -E '[0-9]+'

printf '%s\n' 'A12' '007' 'abc' | grep -Ex '[0-9]+'

printf '%s\n' 'note.txt' 'noteXtxt' 'note.txt.bak' | grep -E '\.txt$'

printf '%s\n' 'a.*b' 'axxb' 'ab' | grep -F 'a.*b'
```

| 上面第几条命令 | 筛选条件 | 预期输出 |
| --- | --- | --- |
| 1 | 含至少一个数字 | `A12` 和 `007` 两行 |
| 2 | 整行只有数字 | `007` |
| 3 | 行尾是普通的 `.txt` | `note.txt`，不包含 `noteXtxt` 或 `note.txt.bak` |
| 4 | 字面包含 `a.*b` | `a.*b` |

| 需求 | 可用写法 |
| --- | --- |
| 选择当前目录里的 `.py` 文件名 | Shell 模式 `*.py` |
| 递归查找 `.py` 普通文件 | `find . -type f -name '*.py'` |
| 搜索以 ERROR 开头的日志行 | `grep -E '^ERROR' app.log` |
| 搜索整行都是数字的行 | `grep -Ex '[0-9]+' data.txt` |
| 搜索字面文本 `a+b` | `grep -F 'a+b' notes.txt` |

回看命令与参数的基础解释：[第一讲笔记](01-shell.md)；查询符号的英文名称：[符号速查](symbols.md)。
