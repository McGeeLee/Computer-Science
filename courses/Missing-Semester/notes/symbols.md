# 常用符号的英文名称速查

用于听懂 Missing Semester 的英文讲解、读命令和描述代码。先收齐键盘上常用的 **32 个 ASCII 半角符号**，再补充组合、空白字符和数学符号；不必一次背完，遇到时来查。

**符号名称与语法作用分开记。**例如 `$` 的名称是 **dollar sign**；它在提示符和 `$HOME` 中的作用不同。同一个符号在 Shell、正则表达式、Python 等环境中的含义也可能不同。下表优先列日常技术交流中的叫法；正式字符名称可对照 [Unicode 的 Basic Latin 字符表](https://www.unicode.org/charts/PDF/U0000.pdf)。

## 1. 标点与引号

| 符号 | 英文名称与常用叫法 | 中文与使用提醒 |
| --- | --- | --- |
| `.` | dot；period（美式）；full stop（英式） | 点、句号；读文件名和路径时常说 dot |
| `,` | comma | 逗号 |
| `:` | colon | 冒号 |
| `;` | semicolon | 分号；不要与 colon 混淆 |
| `!` | exclamation mark / exclamation point；bang | 感叹号；bang 常见于程序员口语 |
| `?` | question mark | 问号 |
| `'` | single quote；apostrophe | 单引号；英语单词中的撇号也叫 apostrophe |
| `"` | double quote；quotation mark | 双引号；泛称 quotation marks 时也可能包括单引号 |
| `` ` `` | backtick；backquote；grave accent | 反引号；与单引号 `'` 是不同字符 |

描述一对引号可以说 **single quotes** 或 **double quotes**。命令里使用直引号 `'`、`"`；排版弯引号 `‘ ’ “ ”` 是其他字符，不会被 Bash / Zsh 当作相应的引用语法。

## 2. 括号与大小于号

| 符号 | 英文名称 | 中文与使用提醒 |
| --- | --- | --- |
| `(`、`)` | parentheses；round brackets | 圆括号、小括号；单个叫 parenthesis，复数是 parentheses |
| `[`、`]` | square brackets | 方括号、中括号 |
| `{`、`}` | braces；curly braces；curly brackets | 花括号、大括号 |
| `<`、`>` | less-than sign、greater-than sign；成对时也常叫 angle brackets | 小于号、大于号；作为一对括号时叫尖括号 |

区分左右时可以用 **left / right**，描述配对的起止时也可以用 **opening / closing**：

- `(`：left parenthesis / opening parenthesis。
- `)`：right parenthesis / closing parenthesis。
- `[`：opening square bracket；`]`：closing square bracket。
- `{`：opening brace；`}`：closing brace。

单说 **brackets** 有地区和上下文差异。需要别人准确输入时，明确说 round、square 或 curly brackets。

## 3. 运算、路径与其他常用符号

| 符号 | 英文名称与常用叫法 | 中文与使用提醒 |
| --- | --- | --- |
| `+` | plus sign；plus | 加号 |
| `-` | hyphen-minus；hyphen / dash / minus | ASCII 连字符减号；选项 `-l` 中常读 dash，减法中读 minus |
| `*` | asterisk；star | 星号；asterisk 是明确的名称，star 是常见口语 |
| `/` | slash；forward slash | 斜杠、正斜杠；Unix 路径分隔符 |
| `\` | backslash | 反斜杠；Shell 中常用于转义 |
| `%` | percent sign | 百分号；具体作用取决于上下文 |
| `=` | equals sign；equal sign | 等号；读表达式时可说 equals |
| `&` | ampersand | 与号；英文单词 and 的符号形式 |
| `\|` | vertical bar；pipe | 竖线；在 Shell 管道中通常称 pipe |
| `^` | caret | 脱字符、插入符；不能默认把它理解为乘方 |
| `~` | tilde | 波浪号；`~/` 中涉及主目录展开 |
| `_` | underscore | 下划线；与 hyphen `-` 不同 |
| `#` | hash；number sign；pound sign（美式） | 井号；hashtag 通常指 `#` 加上后面的标签词 |
| `$` | dollar sign | 美元符号；提示符约定和变量展开是它的使用场景 |
| `@` | at sign；at | 艾特符号；读电子邮件地址时通常说 at |

`*`、`?` 可以用于 Shell 文件名通配；正则表达式有自己的规则。表里的名称方便认符号，具体语法按课程章节学习。

## 4. 常见组合怎么叫

这些组合有的是运算符，有的是路径或语法结构。**英文读法不总是唯一**，可直接描述字符，也可在上下文明确时说它的功能名称。以下 Shell 含义以本课程使用的 Bash / Zsh 基础语法为背景。

| 组合 | 英文读法或功能名称 | 常见含义 |
| --- | --- | --- |
| `..` | dot dot | 路径中的上一级目录 |
| `./` | dot slash | 以当前目录为起点的路径前缀，如 `./script.sh` |
| `~/` | tilde slash | 当前用户主目录下的路径前缀，如 `~/Downloads` |
| `--` | double dash | 很多命令用它引入长选项；单独出现时，很多命令用它结束选项解析，具体看命令手册 |
| `&&` | double ampersand；logical AND | Shell 中，前一个命令成功才运行后一个 |
| `\|\|` | double pipe；logical OR | Shell 中，前一个命令失败才运行后一个 |
| `>>` | double greater-than；append redirection | Shell 中追加输出；目标文件不存在时可创建 |
| `<<` | double less-than；here-document operator | Shell 中引入一段内嵌文本作为输入；不是追加输出 |
| `$(...)` | dollar sign followed by parentheses；command substitution | Shell 命令替换：将命令的标准输出用于当前命令 |
| `#!` | shebang；hashbang | 脚本首行用于指定解释器，如 `#!/bin/bash` |
| `==` | double equals；equality operator | 许多语言中的相等比较，不能直接套用到所有 Shell 判断语法 |
| `!=` | not equal；bang equals | 许多语言中的不等比较 |
| `<=`、`>=` | less than or equal to；greater than or equal to | 小于等于、大于等于；语法是否支持取决于语言与上下文 |
| `->`、`=>` | arrow；fat arrow（通常指 `=>`） | 编程中常见箭头写法，具体作用随语言而变 |
| `...` | ellipsis；three dots | 省略号或三个点；代码中的作用随语言而变 |

Shell 的条件连接与退出码见[第一讲第 4 次学习](01-shell.md#第-4-次让命令根据结果行动)。`>>`、`<<` 的语法可查 [Bash 重定向说明](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)，`$(...)` 可查 [Bash 命令替换说明](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html)。

## 5. 空白字符与相关按键

| 名称或写法 | 英文 | 含义 |
| --- | --- | --- |
| 空格 | space；space character | 一个空格字符；空格键叫 space bar |
| 制表符 | tab；tab character | 制表符；按 Tab 键在交互式 Shell 中通常触发补全，不一定插入字符 |
| 换行 | newline；line feed（LF） | 换行相关术语；字符 LF 常在支持转义的语法中写作 `\n` |
| 回车 | carriage return（CR） | 另一个控制字符，常写作 `\r`；CR 与 LF 是不同字符 |
| 回车键 | Enter key；Return key | 键名；在终端中通常用于提交当前命令 |
| 转义键 | Escape key；Esc | 键名；与反斜杠 `\` 不是同一个东西 |

**字符、字符的写法、按键要区分。**例如 `\n` 在源码或命令中是 backslash 加字母 n；支持相应转义的程序或语法会把它解释为换行，普通文本中的 `\n` 不会自动变成换行。

## 6. 常见数学符号补充

这些适合阅读课件和表达式；写代码时仍需使用相应语言支持的语法。

| 符号 | 英文名称或读法 | 中文 |
| --- | --- | --- |
| `≤` | less than or equal to | 小于等于 |
| `≥` | greater than or equal to | 大于等于 |
| `≠` | not equal to | 不等于 |
| `≈` | approximately equal to | 约等于 |
| `×` | multiplication sign；times | 乘号 |
| `÷` | division sign；divided by | 除号 |
| `±` | plus or minus；plus-minus sign | 正负号 |
| `∞` | infinity；infinity symbol | 无穷大符号 |

## 7. 看起来相近，实际不是同一个字符

| 常用于命令的字符 | 容易混淆的其他字符 | 区别 |
| --- | --- | --- |
| `~` tilde | `～` fullwidth tilde | 半角与全角；Shell 主目录展开使用前者 |
| `'` single quote、`"` double quote | `‘ ’ “ ”` curly quotes / smart quotes | 直引号与排版弯引号；Shell 引用使用前者 |
| `` ` `` backtick | `'` single quote | 反引号与单引号；不是同一个键或语法 |
| `-` hyphen-minus | `–` en dash、`—` em dash、`−` minus sign | ASCII `-` 与不同的排版横线、数学减号 |
| `/` slash | `\` backslash | 正斜杠与反斜杠 |
| `:` colon、`;` semicolon | `：`、`；` 等全角标点 | 外观相近，字符不同 |
| `#` hash / number sign | `£` pound sign / pound sterling sign、`♯` sharp sign | ASCII 井号与英镑符号、音乐升号；pound sign 一词要结合上下文 |
| `*` asterisk | `×` multiplication sign、字母 `x` | 星号、乘号与字母 x |

## 8. 用第一讲的命令练习认符号

下面用于认名称和理解作用，英文读法只是可用示例。

| 命令或片段 | 可以怎样描述 | 符号在这里的作用 |
| --- | --- | --- |
| `~/Downloads` | tilde, slash, Downloads | 从主目录进入 Downloads 子目录的路径 |
| `ls -l` | ls, dash, lowercase L | `-l` 是选项；最后是小写字母 L，不是数字 1 |
| `echo "$HOME"` | echo, double quote, dollar sign, HOME, double quote | 双引号保留变量展开的结果为一个参数 |
| `printf 'red\nblue\n' \| sort` | a pipe between printf and sort | 单引号保护参数，printf 解释 `\n`，管道把输出交给 sort |

先熟悉这十个：**tilde、dollar sign、hash、slash、backslash、pipe、single quote、double quote、backtick、hyphen / dash**。回到[第一讲笔记](01-shell.md)，每遇到一个符号，就同时回答“它叫什么”和“它在这条命令里做什么”。
