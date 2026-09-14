"""第 3 章编程题 3.1～3.19。"""

from __future__ import annotations

import math
import time
from collections.abc import Callable
from typing import Any


EARTH_RADIUS_KM = 6371.01


def ex_3_1(radius: float) -> float:
    side = 2 * radius * math.sin(math.pi / 5)
    return 5 * side**2 / (4 * math.tan(math.pi / 5))


def ex_3_2(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    lat1, lon1, lat2, lon2 = map(
        math.radians,
        (latitude1, longitude1, latitude2, longitude2),
    )
    cosine = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
    return EARTH_RADIUS_KM * math.acos(max(-1.0, min(1.0, cosine)))


def _triangle_area_from_sides(a: float, b: float, c: float) -> float:
    s = (a + b + c) / 2
    return math.sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)))


def ex_3_3() -> float:
    """估算 Atlanta、Charlotte、Savannah、Orlando 围成的面积（km²）。"""
    atlanta = (33.7489954, -84.3879824)
    orlando = (28.5383355, -81.3792365)
    savannah = (32.0835407, -81.0998342)
    charlotte = (35.2270869, -80.8431267)

    def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
        return ex_3_2(*p1, *p2)

    first = _triangle_area_from_sides(
        distance(atlanta, charlotte),
        distance(charlotte, savannah),
        distance(savannah, atlanta),
    )
    second = _triangle_area_from_sides(
        distance(atlanta, savannah),
        distance(savannah, orlando),
        distance(orlando, atlanta),
    )
    return first + second


def ex_3_4(side: float) -> float:
    return math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side**2 / 4


def ex_3_5(number_of_sides: int, side: float) -> float:
    if number_of_sides < 3:
        raise ValueError("a polygon needs at least three sides")
    return number_of_sides * side**2 / (4 * math.tan(math.pi / number_of_sides))


def ex_3_6(ascii_code: int) -> str:
    if not 0 <= ascii_code <= 127:
        raise ValueError("ASCII code must be between 0 and 127")
    return chr(ascii_code)


def ex_3_7(timestamp: float | None = None) -> str:
    milliseconds = int((time.time() if timestamp is None else timestamp) * 1000)
    return chr(ord("A") + milliseconds % 26)


def ex_3_8(amount_in_cents: int) -> dict[str, int]:
    if amount_in_cents < 0:
        raise ValueError("amount cannot be negative")
    remaining = amount_in_cents
    result: dict[str, int] = {}
    for name, value in (("dollars", 100), ("quarters", 25), ("dimes", 10), ("nickels", 5), ("pennies", 1)):
        result[name], remaining = divmod(remaining, value)
    return result


def ex_3_9(
    employee_name: str,
    hours: float,
    hourly_rate: float,
    federal_rate: float,
    state_rate: float,
) -> dict[str, float | str]:
    gross = hours * hourly_rate
    federal = gross * federal_rate
    state = gross * state_rate
    deductions = federal + state
    return {
        "employee": employee_name,
        "hours": hours,
        "hourly_rate": hourly_rate,
        "gross_pay": gross,
        "federal_withholding": federal,
        "state_withholding": state,
        "total_deduction": deductions,
        "net_pay": gross - deductions,
    }


def ex_3_10() -> str:
    return "αβγδεζηθ"


def ex_3_11(number: int) -> int:
    if not 1000 <= number <= 9999:
        raise ValueError("number must contain exactly four digits")
    return int(str(number)[::-1])


def _screen(title: str):
    import turtle

    screen = turtle.Screen()
    screen.title(title)
    pen = turtle.Turtle()
    pen.speed(0)
    return screen, pen


def _finish(screen: Any, pen: Any) -> None:
    pen.hideturtle()
    screen.mainloop()


def ex_3_12(side: float) -> None:
    screen, pen = _screen("Exercise 3.12 - Star")
    for _ in range(5):
        pen.forward(side)
        pen.right(144)
    _finish(screen, pen)


def ex_3_13() -> None:
    screen, pen = _screen("Exercise 3.13 - STOP")
    side = 65
    pen.penup()
    pen.goto(-side / 2, -side * 1.2)
    pen.setheading(22.5)
    pen.pendown()
    pen.color("red")
    pen.begin_fill()
    for _ in range(8):
        pen.forward(side)
        pen.left(45)
    pen.end_fill()
    pen.penup()
    pen.goto(0, -18)
    pen.color("white")
    pen.write("STOP", align="center", font=("Arial", 34, "bold"))
    _finish(screen, pen)


def ex_3_14(radius: float) -> None:
    screen, pen = _screen("Exercise 3.14 - Olympic rings")
    positions = ((-2.2 * radius, 0), (0, 0), (2.2 * radius, 0), (-1.1 * radius, -radius), (1.1 * radius, -radius))
    for color, (x, y) in zip(("blue", "black", "red", "yellow", "green"), positions):
        pen.color(color)
        pen.penup()
        pen.goto(x, y - radius)
        pen.pendown()
        pen.circle(radius)
    _finish(screen, pen)


def ex_3_15() -> None:
    screen, pen = _screen("Exercise 3.15 - Smiley")
    pen.penup()
    pen.goto(0, -100)
    pen.pendown()
    pen.circle(100)
    for x in (-35, 35):
        pen.penup()
        pen.goto(x, 30)
        pen.dot(16)
    pen.penup()
    pen.goto(-48, -25)
    pen.setheading(-60)
    pen.pendown()
    pen.circle(55, 120)
    _finish(screen, pen)


def ex_3_16(side: float = 50) -> None:
    screen, pen = _screen("Exercise 3.16 - Colorful shapes")
    shapes = ((3, "red"), (4, "orange"), (5, "green"), (6, "blue"), (8, "purple"))
    x = -260
    for sides, color in shapes:
        pen.penup()
        pen.goto(x, -40)
        pen.setheading(0 if sides % 2 == 0 else 90 - 180 / sides)
        pen.pendown()
        pen.color(color)
        pen.begin_fill()
        for _ in range(sides):
            pen.forward(side)
            pen.left(360 / sides)
        pen.end_fill()
        x += 115
    _finish(screen, pen)


def ex_3_17(points: tuple[float, float, float, float, float, float]) -> None:
    screen, pen = _screen("Exercise 3.17 - Triangle area")
    vertices = tuple(zip(points[::2], points[1::2]))
    pen.penup()
    pen.goto(vertices[0])
    pen.pendown()
    for vertex in vertices[1:] + vertices[:1]:
        pen.goto(vertex)
    area = _coordinate_triangle_area(points)
    bottom = min(y for _, y in vertices)
    pen.penup()
    pen.goto(sum(x for x, _ in vertices) / 3, bottom - 30)
    pen.write(f"The area is {area:.2f}", align="center")
    _finish(screen, pen)


def _coordinate_triangle_area(points: tuple[float, float, float, float, float, float]) -> float:
    x1, y1, x2, y2, x3, y3 = points
    return abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2


def ex_3_18(points: tuple[float, float, float, float, float, float]) -> None:
    screen, pen = _screen("Exercise 3.18 - Triangle angles")
    vertices = tuple(zip(points[::2], points[1::2]))
    sides = (
        math.dist(vertices[1], vertices[2]),
        math.dist(vertices[0], vertices[2]),
        math.dist(vertices[0], vertices[1]),
    )
    a, b, c = sides
    angles = (
        math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c))),
        math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c))),
        math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b))),
    )
    pen.penup()
    pen.goto(vertices[0])
    pen.pendown()
    for vertex in vertices[1:] + vertices[:1]:
        pen.goto(vertex)
    for (x, y), angle in zip(vertices, angles):
        pen.penup()
        pen.goto(x, y)
        pen.write(f"{angle:.2f}°")
    _finish(screen, pen)


def ex_3_19(x1: float, y1: float, x2: float, y2: float) -> None:
    screen, pen = _screen("Exercise 3.19 - Line")
    pen.penup()
    pen.goto(x1, y1)
    pen.write(f"({x1:g}, {y1:g})")
    pen.pendown()
    pen.goto(x2, y2)
    pen.write(f"({x2:g}, {y2:g})")
    _finish(screen, pen)


EXERCISES: dict[str, Callable[..., Any]] = {
    f"3.{number}": globals()[f"ex_3_{number}"] for number in range(1, 20)
}
