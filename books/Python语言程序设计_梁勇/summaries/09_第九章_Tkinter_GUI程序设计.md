# 第9章：使用 Tkinter 进行 GUI 程序设计

## 本章主线

命令行程序由代码顺序推动，GUI 程序则长期等待用户和系统产生事件。Tkinter 在本书中的核心价值，是把对象、状态、布局、回调和事件驱动模型放到一个可见程序里。

## GUI 的基本结构

1. 创建应用窗口和必要的容器。
2. 创建标签、输入框、按钮、复选框、单选按钮、文本等小构件。
3. 使用几何管理器安排位置。
4. 把按钮、鼠标或键盘事件绑定到回调函数。
5. 进入事件循环，由框架在事件发生时调用相应函数。

Canvas 用于绘制线段、矩形、椭圆、多边形、圆弧和文本。菜单、弹出菜单、滚动条和标准对话框进一步组成完整交互界面。

## 三种布局思路

- `grid` 适合表单和规则的行列结构。
- `pack` 适合按方向依次排列或填充剩余空间。
- `place` 使用绝对或相对位置，控制直接，但对窗口缩放和不同显示环境更脆弱。

复杂界面应先用容器分区，再在每个区域内部布局。不要把整个窗口当成一个巨大坐标平面。

## 事件驱动的关键

回调函数应快速完成工作并返回，否则界面会失去响应。界面显示、程序状态和业务计算最好分离：输入由界面收集，计算交给普通函数，结果再由界面呈现。动画通常由定时回调逐步更新，不应使用阻塞循环长期占用事件线程。

## 版本提醒

本章的事件驱动思想仍然有效，但窗口外观、安装环境和个别 API 细节可能随 Python/Tk 版本和操作系统变化。实际开发时应以当前环境的 Tkinter 文档和运行结果为准。

## 最小练习

把第 2 章的计算器改成 GUI：输入框收集数据，按钮触发计算，标签显示结果。让计算逻辑保持为不依赖 Tkinter 的独立函数，并处理空输入和非数字输入。

## 检查点速答（9.1～9.42）

- **窗口与事件循环（9.1～9.5）**：Turtle 适合入门绘图，Tkinter 用于桌面 GUI；`window = Tk()` 创建主窗口，`window.mainloop()` 启动持续接收和分派事件的循环。创建小构件时第一个参数通常是父容器，`command=callback` 把按钮等事件绑定到回调，不能写成会立即调用的 `command=callback()`。
- **常用小构件（9.6～9.12）**：基本形式分别是 `Label(parent, text="welcome", fg="white", bg="black")`、`Button(..., text="OK", command=processOK)`、`Checkbutton(..., variable=v1, command=processApple)`、`Radiobutton(..., variable=v1, command=processSenior)`、`Entry(..., textvariable=v1)` 和 `Message(..., text="programming is fun")`。`LEFT`、`CENTER`、`RIGHT` 是 Tkinter 命名常量，可直接打印。
- **Canvas（9.13～9.20）**：线段用 `create_line(34, 50, 50, 90)`；中心为 `(70,70)`、宽高均为 100 的矩形边界是 `(20,20,120,120)`；宽 200、高 100 的椭圆边界是 `(-30,20,170,120)`。圆弧用 `create_arc(10,10,80,80,start=30,extent=45)`，多边形依次给出顶点；`width` 加粗，`arrow` 加箭头，`activefill` 设置鼠标经过时的颜色。
- **布局（9.21～9.24）**：`button.pack(LEFT)` 错在参数位置，应写 `button.pack(side=LEFT)`。`pack` 的 `fill`/`expand` 可利用剩余空间，`grid` 适合行列表单；`place` 依赖绝对坐标，对分辨率、字体和窗口缩放不稳，应尽量避免。同一父容器不要混用 `pack` 与 `grid`。
- **图像与菜单（9.25～9.29）**：本书环境的 `PhotoImage` 重点使用 GIF，构造时要写 `PhotoImage(file="image/us.gif")`；现代 Tk 支持格式取决于版本。把图像对象传给 `Button(image=image)` 并保留引用。菜单栏用 `window.config(menu=menubar)` 显示；弹出菜单通常在鼠标事件处理器中调用 `menu.post(event.x_root, event.y_root)`。
- **鼠标与键盘事件（9.30～9.36）**：`canvas.bind("<Button-1>", p)` 绑定左键单击，右键拖动是 `<B3-Motion>`，双击左键是 `<Double-Button-1>`，中键三击是 `<Triple-Button-2>`。事件对象自动传给处理器；鼠标位置是 `event.x`/`event.y`，按键字符是 `event.char`。
- **动画与滚动（9.37～9.40）**：`after(milliseconds, callback)` 安排稍后执行，`update()` 强制处理待显示事件；现代事件驱动动画应反复调度短回调，避免阻塞循环。`Text`、`Canvas`、`Listbox` 可配滚动条；例如视图设置 `yscrollcommand=scrollbar.set`，滚动条再设置 `command=view.yview`。
- **标准对话框（9.41～9.42）**：消息可用 `messagebox.showinfo("title", "Welcome to Python")`；整数、浮点数和字符串分别用 `simpledialog.askinteger`、`askfloat`、`askstring`。用户取消时可能返回 `None`，后续计算前必须判断。

## 自测

- GUI 程序为什么不是从上到下一次执行完就退出？
- 回调函数阻塞时，用户会观察到什么？
- 为什么业务逻辑不应全部写进按钮回调？
