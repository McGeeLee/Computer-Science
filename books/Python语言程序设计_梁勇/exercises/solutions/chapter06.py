"""第 6 章编程题 6.1～6.48。"""

from __future__ import annotations

import datetime as dt
import math
import random
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Literal

from . import chapter03, chapter04, chapter05


def ex_6_1(n: int) -> int:
    return n * (3 * n - 1) // 2


def ex_6_2(n: int) -> int:
    return sum(int(digit) for digit in str(abs(n)))


def ex_6_3(number: int) -> bool:
    return str(abs(number)) == str(abs(number))[::-1]


def ex_6_4(number: int) -> int:
    sign = -1 if number < 0 else 1
    return sign * int(str(abs(number))[::-1])


def ex_6_5(number1: float, number2: float, number3: float) -> tuple[float, float, float]:
    return tuple(sorted((number1, number2, number3)))


def ex_6_6(n: int) -> tuple[str, ...]:
    return tuple(" ".join(map(str, range(row, 0, -1))).rjust(n * 2 - 1) for row in range(1, n + 1))


def ex_6_7(investment_amount: float, monthly_interest_rate: float, years: int) -> float:
    return investment_amount * (1 + monthly_interest_rate) ** (years * 12)


def celsius_to_fahrenheit(celsius: float) -> float:
    return 9 / 5 * celsius + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return 5 / 9 * (fahrenheit - 32)


def ex_6_8() -> tuple[tuple[float, float, float, float], ...]:
    return tuple((c, celsius_to_fahrenheit(c), f, fahrenheit_to_celsius(f)) for c, f in zip(range(40, 30, -1), range(120, 20, -10)))


def foot_to_meter(foot: float) -> float:
    return 0.305 * foot


def meter_to_foot(meter: float) -> float:
    return meter / 0.305


def ex_6_9() -> tuple[tuple[float, float, float, float], ...]:
    return tuple((foot, foot_to_meter(foot), meter, meter_to_foot(meter)) for foot, meter in zip(range(1, 11), range(20, 66, 5)))


def ex_6_10(limit: int = 10_000) -> int:
    return sum(chapter05._is_prime(number) for number in range(2, limit))


def ex_6_11(sales_amount: float) -> float:
    return chapter05._commission(sales_amount)


def ex_6_12(ch1: str, ch2: str, number_per_line: int) -> tuple[str, ...]:
    if len(ch1) != 1 or len(ch2) != 1 or number_per_line <= 0:
        raise ValueError("provide two characters and a positive line width")
    characters = [chr(code) for code in range(ord(ch1), ord(ch2) + 1)]
    return tuple(" ".join(characters[start : start + number_per_line]) for start in range(0, len(characters), number_per_line))


def ex_6_13(i: int) -> float:
    return sum(number / (number + 1) for number in range(1, i + 1))


def ex_6_14(i: int) -> float:
    return 4 * sum((-1) ** (number + 1) / (2 * number - 1) for number in range(1, i + 1))


def ex_6_15(status: int, taxable_income: float) -> float:
    return chapter04.ex_4_13(status, taxable_income)


def ex_6_16(year: int) -> int:
    import calendar

    return 366 if calendar.isleap(year) else 365


def ex_6_17(side1: float, side2: float, side3: float) -> float | None:
    if chapter04.ex_4_19(side1, side2, side3) is None:
        return None
    s = (side1 + side2 + side3) / 2
    return math.sqrt(s * (s - side1) * (s - side2) * (s - side3))


def ex_6_18(n: int, rng: random.Random | None = None) -> tuple[tuple[int, ...], ...]:
    if n < 0:
        raise ValueError("n cannot be negative")
    generator = random if rng is None else rng
    return tuple(tuple(generator.randrange(2) for _ in range(n)) for _ in range(n))


Point = tuple[float, float]


def ex_6_19(p0: Point, p1: Point, p2: Point) -> tuple[Literal["left", "right", "same line"], bool]:
    return chapter04.ex_4_31(p0, p1, p2), chapter04.ex_4_32(p0, p1, p2)


def ex_6_20(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)


def ex_6_21(number: float, tolerance: float = 0.0001) -> float:
    if number < 0:
        raise ValueError("square root is undefined for negative real numbers")
    if number == 0:
        return 0.0
    last_guess = 1.0
    while True:
        next_guess = (last_guess + number / last_guess) / 2
        if abs(next_guess - last_guess) < tolerance:
            return next_guess
        last_guess = next_guess


def ex_6_22(timestamp: float | None = None) -> dt.datetime:
    return dt.datetime.now().astimezone() if timestamp is None else dt.datetime.fromtimestamp(timestamp).astimezone()


def ex_6_23(milliseconds: int) -> str:
    if milliseconds < 0:
        raise ValueError("milliseconds cannot be negative")
    total_seconds = milliseconds // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes}:{seconds}"


def ex_6_24(count: int = 100) -> tuple[int, ...]:
    values = []
    number = 2
    while len(values) < count:
        if chapter05._is_prime(number) and str(number) == str(number)[::-1]:
            values.append(number)
        number += 1
    return tuple(values)


def ex_6_25(count: int = 100) -> tuple[int, ...]:
    values = []
    number = 2
    while len(values) < count:
        reversed_number = int(str(number)[::-1])
        if number != reversed_number and chapter05._is_prime(number) and chapter05._is_prime(reversed_number):
            values.append(number)
        number += 1
    return tuple(values)


def ex_6_26(maximum_p: int = 31) -> tuple[tuple[int, int], ...]:
    return tuple((p, 2**p - 1) for p in range(2, maximum_p + 1) if chapter05._is_prime(2**p - 1))


def ex_6_27(limit: int = 1000) -> tuple[tuple[int, int], ...]:
    return tuple((number, number + 2) for number in range(2, limit - 2) if chapter05._is_prime(number) and chapter05._is_prime(number + 2))


Roll = tuple[int, int]


def ex_6_28(rolls: Iterable[Roll] | None = None, rng: random.Random | None = None) -> tuple[bool, tuple[Roll, ...]]:
    generator = random if rng is None else rng
    supplied = iter(rolls) if rolls is not None else None
    history: list[Roll] = []

    def roll() -> Roll:
        value = next(supplied) if supplied is not None else (generator.randint(1, 6), generator.randint(1, 6))
        history.append(value)
        return value

    first = sum(roll())
    if first in (7, 11):
        return True, tuple(history)
    if first in (2, 3, 12):
        return False, tuple(history)
    point = first
    while True:
        total = sum(roll())
        if total == point:
            return True, tuple(history)
        if total == 7:
            return False, tuple(history)


def _get_size(number: int) -> int:
    return len(str(abs(number)))


def _get_prefix(number: int, k: int) -> int:
    digits = str(abs(number))
    return int(digits[:k]) if len(digits) > k else abs(number)


def _luhn_digit(number: int) -> int:
    return number if number < 10 else number // 10 + number % 10


def ex_6_29(number: int | str) -> bool:
    digits = str(number)
    if not digits.isdigit() or not 13 <= len(digits) <= 16 or not digits.startswith(("4", "5", "6", "37")):
        return False
    total = 0
    parity = len(digits) % 2
    for index, character in enumerate(digits):
        digit = int(character)
        total += _luhn_digit(digit * 2) if index % 2 == parity else digit
    return total % 10 == 0


def ex_6_30(games: int = 10_000, rng: random.Random | None = None) -> int:
    generator = random.Random() if rng is None else rng
    return sum(ex_6_28(rng=generator)[0] for _ in range(games))


def ex_6_31(timestamp: float | None = None) -> str:
    return ex_6_22(timestamp).strftime("%B %-d, %Y %H:%M:%S")


def ex_6_32(year: int, month: int) -> str:
    import calendar

    # calendar.month 的星期计算与 Zeller 公式结果一致，且避免复制排版逻辑。
    return calendar.TextCalendar(calendar.SUNDAY).formatmonth(year, month)


def ex_6_33(side: float) -> float:
    return chapter03.ex_3_4(side)


def ex_6_34(number_of_sides: int, side: float) -> float:
    return chapter03.ex_3_5(number_of_sides, side)


def _random_uppercase(generator: random.Random) -> str:
    return chr(ord("A") + generator.randrange(26))


def ex_6_35(count: int = 10_000, rng: random.Random | None = None) -> int:
    generator = random.Random() if rng is None else rng
    return sum(_random_uppercase(generator) == "A" for _ in range(count))


def ex_6_36(count: int = 100, rng: random.Random | None = None) -> tuple[str, ...]:
    generator = random.Random() if rng is None else rng
    return tuple(_random_uppercase(generator) for _ in range(count))


def _screen(title: str):
    import turtle

    screen = turtle.Screen(); screen.title(title)
    pen = turtle.Turtle(); pen.speed(0)
    return screen, pen


def _finish(screen: Any, pen: Any) -> None:
    pen.hideturtle(); screen.mainloop()


def ex_6_37(seed: int | None = None) -> None:
    screen, pen = _screen("Exercise 6.37 - Random lowercase letters")
    generator = random.Random(seed)
    letters = [chr(ord("a") + generator.randrange(26)) for _ in range(100)]
    for row in range(0, 100, 15):
        pen.penup(); pen.goto(-220, 140 - row // 15 * 35); pen.write(" ".join(letters[row : row + 15]), font=("Courier", 14, "normal"))
    _finish(screen, pen)


def _draw_line(pen: Any, x1: float, y1: float, x2: float, y2: float, color: str = "black", size: int = 1) -> None:
    pen.color(color); pen.pensize(size); pen.penup(); pen.goto(x1, y1); pen.pendown(); pen.goto(x2, y2)


def ex_6_38(x1: float, y1: float, x2: float, y2: float, color: str = "black", size: int = 1) -> None:
    screen, pen = _screen("Exercise 6.38 - Line")
    _draw_line(pen, x1, y1, x2, y2, color, size)
    _finish(screen, pen)


def ex_6_39() -> None:
    screen, pen = _screen("Exercise 6.39 - Star")
    points = [(math.cos(math.radians(90 - i * 72)) * 120, math.sin(math.radians(90 - i * 72)) * 120) for i in range(5)]
    for index in range(5):
        _draw_line(pen, *points[index], *points[(index + 2) % 5])
    _finish(screen, pen)


def _fill_rectangle(pen: Any, color: str, x: float, y: float, width: float, height: float) -> None:
    pen.color(color); pen.penup(); pen.goto(x - width / 2, y - height / 2); pen.setheading(0); pen.pendown(); pen.begin_fill()
    for distance in (width, height, width, height): pen.forward(distance); pen.left(90)
    pen.end_fill()


def _fill_circle(pen: Any, color: str, x: float, y: float, radius: float) -> None:
    pen.color(color); pen.penup(); pen.goto(x, y - radius); pen.setheading(0); pen.pendown(); pen.begin_fill(); pen.circle(radius); pen.end_fill()


def ex_6_40() -> None:
    screen, pen = _screen("Exercise 6.40 - Filled shapes")
    _fill_rectangle(pen, "black", -60, 0, 80, 50); _fill_circle(pen, "blue", 70, 0, 40)
    _finish(screen, pen)


def ex_6_41(seed: int | None = None) -> None:
    screen, pen = _screen("Exercise 6.41 - Points in shapes")
    generator = random.Random(seed)
    pen.penup(); pen.goto(-125, -50); pen.setheading(0); pen.pendown()
    for distance in (100, 100, 100, 100): pen.forward(distance); pen.left(90)
    pen.penup(); pen.goto(50, -50); pen.pendown(); pen.circle(50)
    for _ in range(10):
        pen.penup(); pen.goto(generator.uniform(-125, -25), generator.uniform(-50, 50)); pen.dot(6)
        angle, radius = generator.random() * 2 * math.pi, math.sqrt(generator.random()) * 50
        pen.goto(50 + radius * math.cos(angle), radius * math.sin(angle)); pen.dot(6)
    _finish(screen, pen)


def ex_6_42() -> None:
    chapter05.ex_5_52()


def ex_6_43() -> None:
    chapter05.ex_5_53()


def ex_6_44() -> None:
    chapter05.ex_5_54()


def _polygon_points(x: float, y: float, radius: float, sides: int) -> tuple[Point, ...]:
    return tuple((x + radius * math.cos(math.radians(90 + index * 360 / sides)), y + radius * math.sin(math.radians(90 + index * 360 / sides))) for index in range(sides))


def _draw_polygon(pen: Any, points: Sequence[Point]) -> None:
    pen.penup(); pen.goto(points[0]); pen.pendown()
    for point in tuple(points[1:]) + (points[0],): pen.goto(point)


def ex_6_45() -> None:
    screen, pen = _screen("Exercise 6.45 - Regular polygons")
    for sides, x in zip(range(3, 9), range(-250, 251, 100)):
        _draw_polygon(pen, _polygon_points(x, 0, 42, sides))
    _finish(screen, pen)


def ex_6_46() -> None:
    screen, pen = _screen("Exercise 6.46 - Complete hexagon")
    points = _polygon_points(0, 0, 130, 6)
    for first in range(6):
        for second in range(first + 1, 6):
            _draw_line(pen, *points[first], *points[second])
    _finish(screen, pen)


def _draw_chessboard(pen: Any, start_x: float, end_x: float, start_y: float, end_y: float) -> None:
    width, height = (end_x - start_x) / 8, (end_y - start_y) / 8
    for row in range(8):
        for column in range(8):
            color = "black" if (row + column) % 2 == 0 else "white"
            _fill_rectangle(pen, color, start_x + (column + 0.5) * width, start_y + (row + 0.5) * height, width, height)


def ex_6_47() -> None:
    screen, pen = _screen("Exercise 6.47 - Two chessboards")
    _draw_chessboard(pen, -280, -20, -130, 130); _draw_chessboard(pen, 20, 280, -130, 130)
    _finish(screen, pen)


def ex_6_48(number: int, width: int) -> str:
    text = str(number)
    return text if len(text) >= width else "0" * (width - len(text)) + text


EXERCISES: dict[str, Callable[..., Any]] = {
    f"6.{number}": globals()[f"ex_6_{number}"] for number in range(1, 49)
}
