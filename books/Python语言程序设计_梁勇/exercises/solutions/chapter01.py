"""第 1 章编程题 1.1～1.21。

1.1～1.11 返回可测试的数据；1.12～1.21 是 Turtle 绘图函数。直接运行本模块并传入
题号（例如 ``python3 -m solutions.chapter01 1.18``）可以显示结果或打开绘图窗口。
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from typing import Any


def ex_1_1() -> tuple[str, str, str]:
    """显示三条欢迎消息。"""
    return (
        "Welcome to Python",
        "Welcome to Computer Science",
        "Programming is fun",
    )


def ex_1_2() -> tuple[str, ...]:
    """显示五次欢迎消息。"""
    return ("Welcome to Python",) * 5


def ex_1_3() -> str:
    """显示由 F、U、N 组成的字符图案。"""
    return "\n".join(
        (
            "FFFFFFF   U     U   NN    NN",
            "FF        U     U   NNN   NN",
            "FFFFFFF   U     U   NN N  NN",
            "FF         U   U    NN  NNNN",
            "FF          UUU     NN   NNN",
        )
    )


def ex_1_4() -> tuple[tuple[int, int, int], ...]:
    """生成 a、a²、a³ 表格中的数据行。"""
    return tuple((a, a**2, a**3) for a in range(1, 5))


def ex_1_5() -> float:
    """计算书中给定表达式。"""
    return (9.5 * 4.5 - 2.5 * 3) / (45.5 - 3.5)


def ex_1_6() -> int:
    """计算 1+2+...+9。"""
    return sum(range(1, 10))


def ex_1_7() -> tuple[float, float]:
    """分别用四项和八项莱布尼茨级数近似 π。"""

    def approximation(term_count: int) -> float:
        return 4 * sum((-1) ** k / (2 * k + 1) for k in range(term_count))

    return approximation(4), approximation(8)


def ex_1_8(radius: float = 5.5) -> tuple[float, float]:
    """返回圆的面积和周长。"""
    return radius * radius * math.pi, 2 * radius * math.pi


def ex_1_9(width: float = 4.5, height: float = 7.9) -> tuple[float, float]:
    """返回矩形的面积和周长。"""
    return width * height, 2 * (width + height)


def ex_1_10(
    distance_km: float = 14,
    minutes: int = 45,
    seconds: int = 30,
    kilometers_per_mile: float = 1.6,
) -> float:
    """返回以英里/小时表示的平均速度。"""
    hours = (minutes * 60 + seconds) / 3600
    return distance_km / kilometers_per_mile / hours


def ex_1_11(
    years: int = 5,
    initial_population: int = 312_032_486,
) -> tuple[int, ...]:
    """返回未来每年末的预测人口。

    书中按一年 365 天，并对出生、死亡和移民人数分别使用整数除法。
    """
    seconds_per_year = 365 * 24 * 60 * 60
    annual_change = (
        seconds_per_year // 7
        - seconds_per_year // 13
        + seconds_per_year // 45
    )
    return tuple(initial_population + annual_change * year for year in range(1, years + 1))


def _turtle_screen(title: str):
    import turtle

    screen = turtle.Screen()
    screen.title(title)
    pen = turtle.Turtle()
    pen.speed(0)
    return screen, pen


def _finish_turtle(screen: Any, pen: Any) -> None:
    pen.hideturtle()
    screen.mainloop()


def ex_1_12() -> None:
    """Turtle：绘制正方形。"""
    screen, pen = _turtle_screen("Exercise 1.12 - Square")
    for _ in range(4):
        pen.forward(120)
        pen.right(90)
    _finish_turtle(screen, pen)


def ex_1_13() -> None:
    """Turtle：绘制十字。"""
    screen, pen = _turtle_screen("Exercise 1.13 - Cross")
    for heading in (0, 180, 90, 270):
        pen.setheading(heading)
        pen.forward(80)
        pen.backward(80)
    _finish_turtle(screen, pen)


def ex_1_14() -> None:
    """Turtle：绘制等边三角形。"""
    screen, pen = _turtle_screen("Exercise 1.14 - Triangle")
    for _ in range(3):
        pen.forward(140)
        pen.left(120)
    _finish_turtle(screen, pen)


def ex_1_15() -> None:
    """Turtle：绘制两个首尾相接的三角形。"""
    screen, pen = _turtle_screen("Exercise 1.15 - Two triangles")
    for heading in (0, 180):
        pen.setheading(heading)
        for _ in range(3):
            pen.forward(120)
            pen.left(120)
    _finish_turtle(screen, pen)


def ex_1_16() -> None:
    """Turtle：绘制四个相切的圆。"""
    screen, pen = _turtle_screen("Exercise 1.16 - Four circles")
    radius = 50
    for x, y in ((-radius, 0), (radius, 0), (-radius, -2 * radius), (radius, -2 * radius)):
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.circle(radius)
    _finish_turtle(screen, pen)


def ex_1_17() -> None:
    """Turtle：连接 (-39, 48) 与 (50, -50)，并标注坐标。"""
    screen, pen = _turtle_screen("Exercise 1.17 - Line")
    pen.color("red")
    pen.penup()
    pen.goto(-39, 48)
    pen.write("(-39, 48)")
    pen.pendown()
    pen.goto(50, -50)
    pen.write("(50, -50)")
    _finish_turtle(screen, pen)


def ex_1_18() -> None:
    """Turtle：绘制五角星。"""
    screen, pen = _turtle_screen("Exercise 1.18 - Star")
    for _ in range(5):
        pen.forward(160)
        pen.right(144)
    _finish_turtle(screen, pen)


def ex_1_19() -> None:
    """Turtle：按 PDF 中六个顶点绘制多边形。"""
    screen, pen = _turtle_screen("Exercise 1.19 - Polygon")
    points = ((40, -69.28), (-40, -69.28), (-80, -9.8), (-40, 69), (40, 69), (80, 0))
    pen.penup()
    pen.goto(points[0])
    pen.pendown()
    for point in points[1:] + points[:1]:
        pen.goto(point)
    _finish_turtle(screen, pen)


def ex_1_20() -> None:
    """Turtle：以两个偏移正方形及连接边显示立方体。"""
    screen, pen = _turtle_screen("Exercise 1.20 - Cube")
    front = ((-70, -50), (50, -50), (50, 50), (-70, 50))
    back = tuple((x + 35, y + 35) for x, y in front)

    def polygon(points: tuple[tuple[int, int], ...]) -> None:
        pen.penup()
        pen.goto(points[0])
        pen.pendown()
        for point in points[1:] + points[:1]:
            pen.goto(point)

    polygon(front)
    polygon(back)
    for start, end in zip(front, back):
        pen.penup()
        pen.goto(start)
        pen.pendown()
        pen.goto(end)
    _finish_turtle(screen, pen)


def ex_1_21() -> None:
    """Turtle：显示指向 9:15:00 的模拟时钟。"""
    screen, pen = _turtle_screen("Exercise 1.21 - Clock")
    radius = 120
    pen.penup()
    pen.goto(0, -radius)
    pen.setheading(0)
    pen.pendown()
    pen.circle(radius)

    for label, angle in (("12", 90), ("3", 0), ("6", 270), ("9", 180)):
        x = math.cos(math.radians(angle)) * (radius - 15)
        y = math.sin(math.radians(angle)) * (radius - 15)
        pen.penup()
        pen.goto(x, y - 6)
        pen.write(label, align="center")

    pen.goto(0, 0)
    pen.setheading(90)
    pen.pendown()
    pen.forward(72)  # 秒针：00 秒，指向 12。
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(0)
    pen.pendown()
    pen.forward(88)
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(172.5)  # 时针：9 点 15 分，位于 9 与 10 之间。
    pen.pendown()
    pen.forward(58)
    pen.penup()
    pen.goto(0, -radius - 28)
    pen.write("9:15:00", align="center")
    _finish_turtle(screen, pen)


EXERCISES: dict[str, Callable[[], Any]] = {
    f"1.{number}": globals()[f"ex_1_{number}"] for number in range(1, 22)
}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] not in EXERCISES:
        print("Usage: python3 -m solutions.chapter01 <1.1 ... 1.21>")
        return 2
    result = EXERCISES[args[0]]()
    if result is None:
        return 0
    if isinstance(result, tuple):
        for item in result:
            print(*item) if isinstance(item, tuple) else print(item)
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
