"""第 9 章 Tkinter 编程题 9.1～9.34。

每个函数都会创建并启动一个独立窗口；导入本模块不会产生 GUI 副作用。
"""

from __future__ import annotations

import datetime as dt
import math
import random
from collections.abc import Callable
from typing import Any

from .chapter05 import _loan_payment


def _window(title: str, size: str = "520x360"):
    import tkinter as tk

    root = tk.Tk(); root.title(title); root.geometry(size)
    return tk, root


def ex_9_1() -> None:
    tk, root = _window("Moving Ball")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    ball = canvas.create_oval(240, 140, 260, 160, fill="red")

    def move(dx: int, dy: int) -> None:
        x1, y1, x2, y2 = canvas.coords(ball)
        dx = max(-x1, min(dx, canvas.winfo_width() - x2))
        dy = max(-y1, min(dy, canvas.winfo_height() - y2))
        canvas.move(ball, dx, dy)

    controls = tk.Frame(root); controls.pack()
    for text, delta in (("Left", (-10, 0)), ("Right", (10, 0)), ("Up", (0, -10)), ("Down", (0, 10))):
        tk.Button(controls, text=text, command=lambda d=delta: move(*d)).pack(side="left")
    root.mainloop()


def ex_9_2() -> None:
    tk, root = _window("Investment Calculator", "380x220")
    entries = {}
    for row, label in enumerate(("Investment Amount", "Years", "Annual Interest Rate")):
        tk.Label(root, text=label).grid(row=row, column=0, sticky="e")
        entries[label] = tk.Entry(root); entries[label].grid(row=row, column=1)
    result = tk.StringVar(value="")
    tk.Label(root, text="Future Value").grid(row=3, column=0, sticky="e")
    tk.Label(root, textvariable=result).grid(row=3, column=1)

    def calculate() -> None:
        amount = float(entries["Investment Amount"].get()); years = int(entries["Years"].get()); rate = float(entries["Annual Interest Rate"].get()) / 1200
        result.set(f"{amount * (1 + rate) ** (years * 12):.2f}")

    tk.Button(root, text="Calculate", command=calculate).grid(row=4, column=1)
    root.mainloop()


def ex_9_3() -> None:
    tk, root = _window("Rectangle or Oval")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    shape, filled = tk.StringVar(value="rectangle"), tk.BooleanVar(value=False)

    def redraw(*_args: Any) -> None:
        canvas.delete("all"); options = {"fill": "red" if filled.get() else "", "outline": "black", "width": 2}
        (canvas.create_rectangle if shape.get() == "rectangle" else canvas.create_oval)(80, 50, 440, 270, **options)

    controls = tk.Frame(root); controls.pack()
    for value in ("rectangle", "oval"): tk.Radiobutton(controls, text=value.title(), variable=shape, value=value, command=redraw).pack(side="left")
    tk.Checkbutton(controls, text="Filled", variable=filled, command=redraw).pack(side="left")
    redraw(); root.mainloop()


def ex_9_4() -> None:
    tk, root = _window("Display Rectangles")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    for inset in range(0, 200, 10): canvas.create_rectangle(30 + inset, 25 + inset / 2, 490 - inset, 325 - inset / 2)
    root.mainloop()


def ex_9_5() -> None:
    tk, root = _window("Checkerboard", "420x420")
    for row in range(8):
        root.rowconfigure(row, weight=1); root.columnconfigure(row, weight=1)
        for column in range(8): tk.Canvas(root, bg=("white" if (row + column) % 2 else "black"), highlightthickness=0).grid(row=row, column=column, sticky="nsew")
    root.mainloop()


def ex_9_6() -> None:
    tk, root = _window("Tic-Tac-Toe", "330x330")
    for row in range(3):
        root.rowconfigure(row, weight=1); root.columnconfigure(row, weight=1)
        for column in range(3):
            canvas = tk.Canvas(root, bg="white"); canvas.grid(row=row, column=column, sticky="nsew")
            if random.randrange(2): canvas.create_line(20, 20, 90, 90, width=5); canvas.create_line(90, 20, 20, 90, width=5)
            else: canvas.create_oval(20, 20, 90, 90, width=5)
    root.mainloop()


def ex_9_7() -> None:
    tk, root = _window("8 x 8 Grid", "420x420")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)

    def redraw(event: Any = None) -> None:
        canvas.delete("all"); width, height = canvas.winfo_width(), canvas.winfo_height()
        for index in range(1, 8): canvas.create_line(index * width / 8, 0, index * width / 8, height, fill="red"); canvas.create_line(0, index * height / 8, width, index * height / 8, fill="blue")

    canvas.bind("<Configure>", redraw); root.mainloop()


def ex_9_8() -> None:
    tk, root = _window("Responsive Number Triangle")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)

    def redraw(event: Any = None) -> None:
        canvas.delete("all"); rows = max(1, canvas.winfo_height() // 28)
        for row in range(1, rows + 1):
            canvas.create_text(canvas.winfo_width() / 2, row * 25, text=" ".join(map(str, range(1, row + 1))))

    canvas.bind("<Configure>", redraw); root.mainloop()


def ex_9_9() -> None:
    tk, root = _window("Bar Chart")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    data = (("Projects", 20, "red"), ("Quizzes", 10, "blue"), ("Midterm", 30, "green"), ("Final", 40, "orange"))
    for index, (label, percent, color) in enumerate(data):
        x1 = 40 + index * 115; y1 = 310 - percent * 6
        canvas.create_rectangle(x1, y1, x1 + 80, 310, fill=color); canvas.create_text(x1 + 40, y1 - 12, text=f"{label} -- {percent}%")
    root.mainloop()


def ex_9_10() -> None:
    tk, root = _window("Pie Chart")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    start = 0
    for label, percent, color in (("Projects", 20, "red"), ("Quizzes", 10, "blue"), ("Midterm", 30, "green"), ("Final", 40, "orange")):
        extent = percent * 3.6; canvas.create_arc(90, 30, 410, 350, start=start, extent=extent, fill=color); start += extent
    root.mainloop()


def ex_9_11() -> None:
    tk, root = _window("Current Time", "360x400")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)

    def update() -> None:
        canvas.delete("all"); now = dt.datetime.now(); cx, cy, radius = 180, 180, 130
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, width=2)
        for value, length, width in ((now.hour % 12 + now.minute / 60, 70, 4), (now.minute + now.second / 60, 100, 3), (now.second, 110, 1)):
            angle = math.radians(90 - value * (30 if length == 70 else 6)); canvas.create_line(cx, cy, cx + length * math.cos(angle), cy - length * math.sin(angle), width=width)
        canvas.create_text(cx, 340, text=now.strftime("%H:%M:%S"), font=("Arial", 16)); root.after(1000, update)

    update(); root.mainloop()


def ex_9_12() -> None:
    tk, root = _window("Rotating Message")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    messages = ("Programming is fun", "It is fun to program"); state = [0]

    def toggle(_event: Any = None) -> None:
        state[0] ^= 1; canvas.delete("all"); canvas.create_text(260, 170, text=messages[state[0]], font=("Arial", 22))

    canvas.bind("<Button-1>", toggle); toggle(); root.mainloop()


def ex_9_13() -> None:
    tk, root = _window("Mouse Position")
    label = tk.Label(root, text="Click or drag the mouse", font=("Arial", 18)); label.pack(expand=True)
    root.bind("<Button-1>", lambda event: label.config(text=f"Clicked: ({event.x}, {event.y})"))
    root.bind("<B1-Motion>", lambda event: label.config(text=f"Dragging: ({event.x}, {event.y})"))
    root.mainloop()


def ex_9_14() -> None:
    tk, root = _window("Arrow Keys")
    canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); point = [260, 180]

    def draw(event: Any) -> None:
        dx, dy = {"Left": (-10, 0), "Right": (10, 0), "Up": (0, -10), "Down": (0, 10)}[event.keysym]
        new = (point[0] + dx, point[1] + dy); canvas.create_line(*point, *new); point[:] = new

    for key in ("Left", "Right", "Up", "Down"): root.bind(f"<{key}>", draw)
    root.focus_set(); root.mainloop()


def _fan(canvas: Any, angle: float) -> None:
    canvas.delete("all"); canvas.create_oval(80, 40, 320, 280, width=3)
    for offset in range(0, 360, 90): canvas.create_arc(120, 80, 280, 240, start=angle + offset, extent=55, fill="gray")


def ex_9_15() -> None:
    tk, root = _window("Fan", "400x330"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); _fan(canvas, 0); root.mainloop()


def ex_9_16() -> None:
    tk, root = _window("Rotating Fan", "400x330"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); angle = [0]

    def animate() -> None: angle[0] = (angle[0] + 8) % 360; _fan(canvas, angle[0]); root.after(40, animate)
    animate(); root.mainloop()


def ex_9_17() -> None:
    tk, root = _window("Racing Car", "650x220"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); x, speed = [0], [4]

    def draw_car() -> None:
        canvas.delete("car"); base = x[0]; canvas.create_rectangle(base, 120, base + 70, 145, fill="blue", tags="car"); canvas.create_polygon(base + 15, 120, base + 30, 95, base + 55, 95, base + 65, 120, fill="red", tags="car"); canvas.create_oval(base + 10, 135, base + 28, 153, fill="black", tags="car"); canvas.create_oval(base + 50, 135, base + 68, 153, fill="black", tags="car")
    def animate() -> None: x[0] = (x[0] + speed[0]) % max(1, canvas.winfo_width()); draw_car(); root.after(30, animate)
    root.bind("<Up>", lambda _e: speed.__setitem__(0, min(20, speed[0] + 1))); root.bind("<Down>", lambda _e: speed.__setitem__(0, max(1, speed[0] - 1)))
    animate(); root.mainloop()


def ex_9_18() -> None:
    tk, root = _window("Flashing Text"); label = tk.Label(root, text="Welcome", font=("Arial", 28)); label.pack(expand=True); visible = [True]
    def flash() -> None: visible[0] = not visible[0]; label.config(text="Welcome" if visible[0] else ""); root.after(500, flash)
    flash(); root.mainloop()


def ex_9_19() -> None:
    tk, root = _window("Moving Circle"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); circle = canvas.create_oval(240, 150, 280, 190, fill="red")
    def move(event: Any) -> None:
        dx, dy = {"Left": (-10, 0), "Right": (10, 0), "Up": (0, -10), "Down": (0, 10)}[event.keysym]; canvas.move(circle, dx, dy)
    for key in ("Left", "Right", "Up", "Down"): root.bind(f"<{key}>", move)
    root.mainloop()


def ex_9_20() -> None:
    tk, root = _window("Inside the Circle?"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); canvas.create_oval(50, 10, 150, 110)
    message = canvas.create_text(260, 180, text="Move while holding the left button")
    canvas.bind("<B1-Motion>", lambda e: canvas.itemconfig(message, text="Mouse pointer is inside the circle" if math.hypot(e.x - 100, e.y - 60) <= 50 else "Mouse pointer is outside the circle")); root.mainloop()


def ex_9_21() -> None:
    tk, root = _window("Inside the Rectangle?"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); canvas.create_rectangle(50, 40, 150, 80)
    message = canvas.create_text(260, 180, text="Move while holding the left button")
    canvas.bind("<B1-Motion>", lambda e: canvas.itemconfig(message, text="Mouse pointer is inside the rectangle" if abs(e.x - 100) <= 50 and abs(e.y - 60) <= 20 else "Mouse pointer is outside the rectangle")); root.mainloop()


def ex_9_22() -> None:
    tk, root = _window("Pendulum"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); angle, delta, delay, running = [0.0], [0.04], [30], [True]
    def animate() -> None:
        if running[0]:
            angle[0] += delta[0]
            if abs(angle[0]) > 0.8: delta[0] *= -1
            canvas.delete("all"); x, y = 260 + 180 * math.sin(angle[0]), 40 + 180 * math.cos(angle[0]); canvas.create_line(260, 40, x, y, width=2); canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="red")
        root.after(delay[0], animate)
    root.bind("<Up>", lambda _e: delay.__setitem__(0, max(5, delay[0] - 5))); root.bind("<Down>", lambda _e: delay.__setitem__(0, min(200, delay[0] + 5))); root.bind("<s>", lambda _e: running.__setitem__(0, False)); root.bind("<r>", lambda _e: running.__setitem__(0, True)); animate(); root.mainloop()


def ex_9_23() -> None:
    tk, root = _window("Radio Buttons and Buttons"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); text = canvas.create_text(260, 180, text="Welcome", font=("Arial", 22)); color = tk.StringVar(value="white")
    controls = tk.Frame(root); controls.pack()
    for name in ("red", "yellow", "white", "gray", "green"): tk.Radiobutton(controls, text=name.title(), variable=color, value=name, command=lambda: canvas.config(bg=color.get())).pack(side="left")
    tk.Button(controls, text="<=", command=lambda: canvas.move(text, -10, 0)).pack(side="left"); tk.Button(controls, text="=>", command=lambda: canvas.move(text, 10, 0)).pack(side="left"); root.mainloop()


def ex_9_24() -> None:
    tk, root = _window("Dynamic Circles"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); circles: list[int] = []
    canvas.bind("<Button-1>", lambda e: circles.append(canvas.create_oval(e.x - 20, e.y - 20, e.x + 20, e.y + 20)))
    def remove(_event: Any) -> None:
        if circles: canvas.delete(circles.pop())
    canvas.bind("<Button-2>", remove); canvas.bind("<Button-3>", remove); root.mainloop()


def ex_9_25() -> None:
    tk, root = _window("Traffic Lights", "260x430"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); choice = tk.StringVar(value="")
    def redraw() -> None:
        canvas.delete("all"); canvas.create_rectangle(80, 20, 180, 300, width=3)
        for y, color in ((70, "red"), (160, "yellow"), (250, "green")): canvas.create_oval(105, y - 25, 155, y + 25, fill=color if choice.get() == color else "white")
    controls = tk.Frame(root); controls.pack()
    for color in ("red", "yellow", "green"): tk.Radiobutton(controls, text=color.title(), variable=choice, value=color, command=redraw).pack(side="left")
    redraw(); root.mainloop()


def ex_9_26() -> None:
    tk, root = _window("Random Balls"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    def display() -> None:
        canvas.delete("all")
        for _ in range(10):
            x, y, r = random.randrange(30, 490), random.randrange(30, 300), random.randrange(8, 25); canvas.create_oval(x - r, y - r, x + r, y + r, fill=f"#{random.randrange(0x1000000):06x}")
    tk.Button(root, text="Display", command=display).pack(); display(); root.mainloop()


def ex_9_27() -> None:
    tk, root = _window("Compare Interest Rates", "540x500"); top = tk.Frame(root); top.pack(); amount, years = tk.Entry(top), tk.Entry(top); tk.Label(top, text="Loan Amount").grid(row=0, column=0); amount.grid(row=0, column=1); tk.Label(top, text="Years").grid(row=0, column=2); years.grid(row=0, column=3)
    text = tk.Text(root, width=62, height=24); text.pack()
    def calculate() -> None:
        text.delete("1.0", "end"); text.insert("end", "Interest Rate  Monthly Payment  Total Payment\n")
        for eighths in range(40, 65):
            rate = eighths / 8; monthly = _loan_payment(float(amount.get()), int(years.get()), rate); text.insert("end", f"{rate:>7.3f}% {monthly:>17.2f} {monthly * int(years.get()) * 12:>14.2f}\n")
    tk.Button(top, text="Calculate", command=calculate).grid(row=0, column=4); root.mainloop()


def _draggable_points(canvas: Any, points: list[list[float]], redraw: Callable[[], None]) -> None:
    selected = [-1]
    def press(event: Any) -> None:
        distances = [math.hypot(event.x - p[0], event.y - p[1]) for p in points]; selected[0] = min(range(len(points)), key=distances.__getitem__) if min(distances) < 18 else -1
    def drag(event: Any) -> None:
        if selected[0] >= 0: points[selected[0]][:] = [event.x, event.y]; redraw()
    canvas.bind("<Button-1>", press); canvas.bind("<B1-Motion>", drag); canvas.bind("<ButtonRelease-1>", lambda _e: selected.__setitem__(0, -1))


def ex_9_28() -> None:
    tk, root = _window("Triangle Angles"); canvas = tk.Canvas(root, bg="white", cursor="crosshair"); canvas.pack(fill="both", expand=True); points = [[120, 280], [260, 70], [420, 280]]
    def redraw() -> None:
        canvas.delete("all"); flat = [coordinate for point in points for coordinate in point]; canvas.create_polygon(*flat, fill="", outline="black")
        sides = [math.dist(points[1], points[2]), math.dist(points[0], points[2]), math.dist(points[0], points[1])]
        for index, (point, a, b, c) in enumerate(zip(points, sides, sides[1:] + sides[:1], sides[2:] + sides[:2])):
            angle = math.degrees(math.acos(max(-1, min(1, (b*b + c*c - a*a) / (2*b*c))))); canvas.create_oval(point[0]-6, point[1]-6, point[0]+6, point[1]+6, fill="red"); canvas.create_text(point[0]+18, point[1]-12, text=f"{angle:.1f}°")
    _draggable_points(canvas, points, redraw); redraw(); root.mainloop()


def ex_9_29() -> None:
    from .chapter04 import ex_4_25
    tk, root = _window("Intersecting Lines"); canvas = tk.Canvas(root, bg="white", cursor="crosshair"); canvas.pack(fill="both", expand=True); points = [[20, 20], [56, 130], [100, 20], [16, 130]]
    def redraw() -> None:
        canvas.delete("all"); canvas.create_line(*points[0], *points[1], width=2); canvas.create_line(*points[2], *points[3], width=2)
        for point in points: canvas.create_oval(point[0]-5, point[1]-5, point[0]+5, point[1]+5, fill="blue")
        intersection = ex_4_25(tuple(coordinate for point in points for coordinate in point))
        if intersection: canvas.create_oval(intersection[0]-6, intersection[1]-6, intersection[0]+6, intersection[1]+6, fill="red")
    _draggable_points(canvas, points, redraw); redraw(); root.mainloop()


def ex_9_30() -> None:
    tk, root = _window("Rectanguloid"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); front = ((140, 120), (360, 120), (360, 270), (140, 270)); back = tuple((x + 50, y - 50) for x, y in front)
    for polygon in (front, back): canvas.create_polygon(*[c for p in polygon for c in p], fill="", outline="black")
    for a, b in zip(front, back): canvas.create_line(*a, *b)
    root.mainloop()


def ex_9_31() -> None:
    tk, root = _window("Drag the Blue Circle"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); circles = [canvas.create_oval(40+i*85, 130, 100+i*85, 190, fill=("blue" if i == 0 else "red")) for i in range(5)]; last = [0, 0]
    canvas.tag_bind(circles[0], "<Button-1>", lambda e: last.__setitem__(slice(None), [e.x, e.y]))
    def drag(event: Any) -> None: canvas.move(circles[0], event.x-last[0], event.y-last[1]); last[:] = [event.x, event.y]
    canvas.tag_bind(circles[0], "<B1-Motion>", drag); root.mainloop()


def ex_9_32() -> None:
    tk, root = _window("Two Circles"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True); points = [[80, 160], [360, 200]]
    def redraw() -> None:
        canvas.delete("all"); distance = math.dist(points[0], points[1]); canvas.create_line(*points[0], *points[1]); canvas.create_text((points[0][0]+points[1][0])/2, (points[0][1]+points[1][1])/2-12, text=f"{distance:.2f}")
        for point in points: canvas.create_oval(point[0]-20, point[1]-20, point[0]+20, point[1]+20, fill="lightblue")
    selected = [-1]
    def press(event: Any) -> None: selected[0] = min(range(2), key=lambda i: math.hypot(event.x-points[i][0], event.y-points[i][1]))
    def drag(event: Any) -> None:
        other = points[1-selected[0]]
        if math.hypot(event.x-other[0], event.y-other[1]) >= 70: points[selected[0]][:] = [event.x, event.y]; redraw()
    canvas.bind("<Button-1>", press); canvas.bind("<B1-Motion>", drag); redraw(); root.mainloop()


def ex_9_33() -> None:
    tk, root = _window("Random Arrow Line"); canvas = tk.Canvas(root, bg="white"); canvas.pack(fill="both", expand=True)
    def draw() -> None: canvas.delete("all"); canvas.create_line(random.randrange(500), random.randrange(300), random.randrange(500), random.randrange(300), arrow="last", width=3)
    tk.Button(root, text="Draw a Random Arrow Line", command=draw).pack(); draw(); root.mainloop()


def ex_9_34() -> None:
    tk, root = _window("Address Book", "620x260"); fields = {}; labels = ("Name", "Street", "City", "State", "ZIP")
    for row, label in enumerate(labels): tk.Label(root, text=label).grid(row=row, column=0, sticky="e"); fields[label] = tk.Entry(root, width=55); fields[label].grid(row=row, column=1, columnspan=5, sticky="ew")
    addresses: list[dict[str, str]] = []; current = [0]
    def show(index: int) -> None:
        if not addresses: return
        current[0] = index % len(addresses)
        for label in labels: fields[label].delete(0, "end"); fields[label].insert(0, addresses[current[0]][label])
    def add() -> None: addresses.append({label: fields[label].get() for label in labels}); show(len(addresses)-1)
    actions = (("Add", add), ("First", lambda: show(0)), ("Next", lambda: show(current[0]+1)), ("Previous", lambda: show(current[0]-1)), ("Last", lambda: show(len(addresses)-1)))
    for column, (label, command) in enumerate(actions): tk.Button(root, text=label, command=command).grid(row=5, column=column+1)
    root.mainloop()


EXERCISES: dict[str, Callable[[], None]] = {f"9.{number}": globals()[f"ex_9_{number}"] for number in range(1, 35)}
