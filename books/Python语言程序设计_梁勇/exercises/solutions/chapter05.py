"""第 5 章编程题 5.1～5.55。"""

from __future__ import annotations

import calendar
import math
import random
import time
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any


def ex_5_1(values: Iterable[int]) -> tuple[int, int, int, float | None]:
    numbers: list[int] = []
    for value in values:
        if value == 0:
            break
        numbers.append(value)
    if not numbers:
        return 0, 0, 0, None
    total = sum(numbers)
    return sum(n > 0 for n in numbers), sum(n < 0 for n in numbers), total, total / len(numbers)


def ex_5_2(answers: Sequence[int], questions: Sequence[tuple[int, int]] | None = None) -> int:
    pairs = questions if questions is not None else tuple((random.randint(1, 15), random.randint(1, 15)) for _ in range(5))
    if len(answers) != len(pairs):
        raise ValueError("one answer is required for each question")
    return sum(answer == a + b for answer, (a, b) in zip(answers, pairs))


def ex_5_3() -> tuple[tuple[int, float], ...]:
    return tuple((kilograms, kilograms * 2.2) for kilograms in range(1, 200, 2))


def ex_5_4() -> tuple[tuple[int, float], ...]:
    return tuple((miles, miles * 1.609) for miles in range(1, 11))


def ex_5_5() -> tuple[tuple[int, float, int, float], ...]:
    return tuple((kg, kg * 2.2, pounds, pounds / 2.2) for kg, pounds in zip(range(1, 200, 2), range(20, 516, 5)))


def ex_5_6() -> tuple[tuple[int, float, int, float], ...]:
    return tuple((miles, miles * 1.609, km, km / 1.609) for miles, km in zip(range(1, 11), range(20, 66, 5)))


def ex_5_7() -> tuple[tuple[int, float, float], ...]:
    return tuple((degree, math.sin(math.radians(degree)), math.cos(math.radians(degree))) for degree in range(0, 361, 10))


def ex_5_8() -> tuple[tuple[int, float], ...]:
    return tuple((number, math.sqrt(number)) for number in range(0, 21, 2))


def ex_5_9(initial_tuition: float = 10_000, annual_growth: float = 0.05) -> tuple[float, float]:
    year_ten = initial_tuition * (1 + annual_growth) ** 10
    four_year_total = sum(year_ten * (1 + annual_growth) ** year for year in range(4))
    return year_ten, four_year_total


def ex_5_10(path: str | Path) -> float:
    values = [float(token) for token in Path(path).read_text(encoding="utf-8").split()]
    if not values:
        raise ValueError("score file is empty")
    # 若首项是后续分数的个数，则不把它当作分数。
    if values[0].is_integer() and int(values[0]) == len(values) - 1:
        values = values[1:]
    return max(values)


def ex_5_11(scores: Sequence[float]) -> tuple[float, float]:
    distinct = sorted(set(scores), reverse=True)
    if len(distinct) < 2:
        raise ValueError("at least two distinct scores are required")
    return distinct[0], distinct[1]


def ex_5_12() -> tuple[int, ...]:
    return tuple(number for number in range(100, 1001) if number % 5 == 0 and number % 6 == 0)


def ex_5_13() -> tuple[int, ...]:
    return tuple(number for number in range(100, 201) if (number % 5 == 0) != (number % 6 == 0))


def ex_5_14() -> int:
    number = 0
    while number**2 <= 12_000:
        number += 1
    return number


def ex_5_15() -> int:
    number = 0
    while (number + 1) ** 3 < 12_000:
        number += 1
    return number


def ex_5_16(number1: int, number2: int) -> int:
    for divisor in range(min(abs(number1), abs(number2)), 0, -1):
        if number1 % divisor == 0 and number2 % divisor == 0:
            return divisor
    return 0


def ex_5_17() -> tuple[str, ...]:
    return tuple(chr(code) for code in range(ord("!"), ord("~") + 1))


def ex_5_18(number: int) -> tuple[int, ...]:
    if number < 2:
        return ()
    factors: list[int] = []
    divisor = 2
    remaining = number
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def ex_5_19(lines: int) -> tuple[str, ...]:
    if not 1 <= lines <= 15:
        raise ValueError("lines must be between 1 and 15")
    rows = []
    for end in range(1, lines + 1):
        values = list(range(end, 0, -1)) + list(range(2, end + 1))
        rows.append(" ".join(map(str, values)).center(lines * 4 - 1))
    return tuple(rows)


def ex_5_20(size: int = 6) -> tuple[tuple[str, ...], ...]:
    pattern_a = tuple(" ".join(map(str, range(1, row + 1))) for row in range(1, size + 1))
    pattern_b = tuple(" ".join(map(str, range(1, size - row + 1))) for row in range(size))
    pattern_c = tuple(("  " * (size - row) + " ".join(map(str, range(row, 0, -1)))).rstrip() for row in range(1, size + 1))
    pattern_d = tuple(("  " * row + " ".join(map(str, range(1, size - row + 1)))).rstrip() for row in range(size))
    return pattern_a, pattern_b, pattern_c, pattern_d


def ex_5_21(lines: int = 8) -> tuple[str, ...]:
    rows = []
    for row in range(lines):
        values = [2**power for power in range(row + 1)] + [2**power for power in range(row - 1, -1, -1)]
        rows.append(" ".join(f"{value:3d}" for value in values).center(lines * 8))
    return tuple(rows)


def _is_prime(number: int) -> bool:
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    return all(number % divisor for divisor in range(3, math.isqrt(number) + 1, 2))


def ex_5_22() -> tuple[int, ...]:
    return tuple(number for number in range(2, 1001) if _is_prime(number))


def _loan_payment(amount: float, years: int, annual_rate_percent: float) -> float:
    monthly_rate = annual_rate_percent / 1200
    months = years * 12
    if monthly_rate == 0:
        return amount / months
    return amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)


def ex_5_23(amount: float, years: int) -> tuple[tuple[float, float, float], ...]:
    rows = []
    for eighths in range(40, 65):
        rate = eighths / 8
        monthly = _loan_payment(amount, years, rate)
        rows.append((rate, monthly, monthly * years * 12))
    return tuple(rows)


def ex_5_24(amount: float, years: int, annual_rate_percent: float) -> tuple[float, tuple[tuple[int, float, float, float], ...]]:
    payment = _loan_payment(amount, years, annual_rate_percent)
    balance = amount
    rows = []
    monthly_rate = annual_rate_percent / 1200
    for number in range(1, years * 12 + 1):
        interest = balance * monthly_rate
        principal = payment - interest
        balance -= principal
        if abs(balance) < 1e-8:
            balance = 0.0
        rows.append((number, interest, principal, balance))
    return payment, tuple(rows)


def ex_5_25(n: int = 50_000) -> tuple[float, float]:
    left_to_right = sum(1 / number for number in range(1, n + 1))
    right_to_left = sum(1 / number for number in range(n, 0, -1))
    return left_to_right, right_to_left


def ex_5_26() -> float:
    return sum(number / (number + 2) for number in range(1, 98, 2))


def ex_5_27(stops: Iterable[int] = range(10_000, 100_001, 10_000)) -> tuple[tuple[int, float], ...]:
    requested = set(stops)
    if not requested:
        return ()
    total = 0.0
    results = []
    for index in range(1, max(requested) + 1):
        total += (-1) ** (index + 1) / (2 * index - 1)
        if index in requested:
            results.append((index, 4 * total))
    return tuple(results)


def ex_5_28(stops: Iterable[int] = range(10_000, 100_001, 10_000)) -> tuple[tuple[int, float], ...]:
    requested = set(stops)
    if not requested:
        return ()
    value = 1.0
    term = 1.0
    results = []
    for index in range(1, max(requested) + 1):
        term /= index
        value += term
        if index in requested:
            results.append((index, value))
    return tuple(results)


def ex_5_29() -> tuple[int, ...]:
    return tuple(year for year in range(2001, 2101) if calendar.isleap(year))


def ex_5_30(year: int, january_first: int) -> tuple[tuple[str, str], ...]:
    if january_first not in range(7):
        raise ValueError("weekday must be 0 (Sunday) through 6 (Saturday)")
    names = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    weekday = january_first
    rows = []
    for month in range(1, 13):
        rows.append((calendar.month_name[month], names[weekday]))
        weekday = (weekday + calendar.monthrange(year, month)[1]) % 7
    return tuple(rows)


def ex_5_31(year: int, january_first: int) -> str:
    if january_first not in range(7):
        raise ValueError("weekday must be 0 (Sunday) through 6 (Saturday)")
    weekday = january_first
    blocks: list[str] = []
    for month in range(1, 13):
        lines = [f"{calendar.month_name[month]} {year}".center(28), "Sun Mon Tue Wed Thu Fri Sat"]
        days = calendar.monthrange(year, month)[1]
        cells = ["    "] * weekday + [f"{day:>3} " for day in range(1, days + 1)]
        lines.extend("".join(cells[start : start + 7]).rstrip() for start in range(0, len(cells), 7))
        blocks.append("\n".join(lines))
        weekday = (weekday + days) % 7
    return "\n\n".join(blocks)


def ex_5_32(monthly_saving: float, annual_rate_percent: float, months: int) -> float:
    from .chapter02 import ex_2_21

    return ex_2_21(monthly_saving, annual_rate_percent, months)


def ex_5_33(initial_deposit: float, annual_yield_percent: float, months: int) -> tuple[float, ...]:
    value = initial_deposit
    values = []
    for _ in range(months):
        value *= 1 + annual_yield_percent / 1200
        values.append(value)
    return tuple(values)


def ex_5_34(rng: random.Random | None = None) -> int:
    generator = random if rng is None else rng
    first = generator.randrange(10)
    second = generator.randrange(10)
    while second == first:
        second = generator.randrange(10)
    return first * 10 + second


def ex_5_35(limit: int = 10_000) -> tuple[int, ...]:
    perfect = []
    for number in range(2, limit):
        factor_sum = 1 + sum(divisor + (number // divisor if divisor * divisor != number else 0) for divisor in range(2, math.isqrt(number) + 1) if number % divisor == 0)
        if factor_sum == number:
            perfect.append(number)
    return tuple(perfect)


def ex_5_36(user_choices: Sequence[int], computer_choices: Sequence[int]) -> tuple[int, int, int]:
    from .chapter04 import ex_4_17

    user_wins = computer_wins = rounds = 0
    for user, computer in zip(user_choices, computer_choices):
        outcome = ex_4_17(user, computer)[-1]
        rounds += 1
        user_wins += outcome == "win"
        computer_wins += outcome == "lose"
        if abs(user_wins - computer_wins) > 2:
            break
    return user_wins, computer_wins, rounds


def ex_5_37() -> float:
    return sum(1 / (math.sqrt(number) + math.sqrt(number + 1)) for number in range(1, 625))


def ex_5_38(seconds: int) -> tuple[str, ...]:
    if seconds < 0:
        raise ValueError("seconds cannot be negative")
    return tuple(f"{remaining} second{'s' if remaining != 1 else ''} remaining" for remaining in range(seconds - 1, 0, -1)) + ("Stopped",)


def _commission(sales: float) -> float:
    return min(sales, 5000) * 0.08 + min(max(sales - 5000, 0), 5000) * 0.10 + max(sales - 10_000, 0) * 0.12


def ex_5_39(target_income: float = 30_000, base_salary: float = 5_000) -> float:
    required = target_income - base_salary
    if required <= 0:
        return 0.0
    first = 5000 * 0.08
    second = 5000 * 0.10
    if required <= first:
        return required / 0.08
    if required <= first + second:
        return 5000 + (required - first) / 0.10
    return 10_000 + (required - first - second) / 0.12


def ex_5_40(trials: int = 1_000_000, rng: random.Random | None = None) -> tuple[int, int]:
    generator = random if rng is None else rng
    heads = sum(generator.randrange(2) for _ in range(trials))
    return heads, trials - heads


def ex_5_41(values: Iterable[int]) -> tuple[int, int]:
    numbers = []
    for value in values:
        if value == 0:
            break
        numbers.append(value)
    if not numbers:
        raise ValueError("at least one nonzero number is required")
    maximum = max(numbers)
    return maximum, numbers.count(maximum)


def ex_5_42(trials: int = 1_000_000, rng: random.Random | None = None) -> float:
    generator = random if rng is None else rng
    odd = 0
    for _ in range(trials):
        x, y = generator.uniform(-1, 1), generator.uniform(-1, 1)
        odd += x < 0 or (x >= 0 and y >= 0 and y <= 1 - x)
    return odd / trials


def ex_5_43() -> tuple[tuple[int, int], ...]:
    return tuple((first, second) for first in range(1, 8) for second in range(first + 1, 8))


def ex_5_44(number: int) -> str:
    if number < 0:
        return "-" + format(-number, "b")
    return format(number, "b")


def ex_5_45(number: int) -> str:
    if number < 0:
        return "-" + format(-number, "X")
    return format(number, "X")


def ex_5_46(values: Sequence[float]) -> tuple[float, float]:
    if len(values) < 2:
        raise ValueError("at least two values are required")
    mean = sum(values) / len(values)
    deviation = math.sqrt((sum(value**2 for value in values) - sum(values) ** 2 / len(values)) / (len(values) - 1))
    return mean, deviation


def _screen(title: str):
    import turtle

    screen = turtle.Screen(); screen.title(title)
    pen = turtle.Turtle(); pen.speed(0)
    return screen, pen


def _finish(screen: Any, pen: Any) -> None:
    pen.hideturtle(); screen.mainloop()


def ex_5_47(seed: int | None = None) -> None:
    screen, pen = _screen("Exercise 5.47 - Random balls")
    generator = random.Random(seed)
    for _ in range(10):
        pen.penup(); pen.goto(generator.uniform(-60, 60), generator.uniform(-50, 50)); pen.dot(10)
    pen.goto(-60, -50); pen.pendown()
    for distance in (120, 100, 120, 100): pen.forward(distance); pen.left(90)
    _finish(screen, pen)


def ex_5_48() -> None:
    screen, pen = _screen("Exercise 5.48 - Concentric circles")
    for radius in range(10, 101, 10):
        pen.penup(); pen.goto(0, -radius); pen.pendown(); pen.circle(radius)
    _finish(screen, pen)


def ex_5_49() -> None:
    screen, pen = _screen("Exercise 5.49 - Multiplication table")
    for row in range(1, 10):
        for column in range(1, 10):
            pen.penup(); pen.goto(-180 + column * 38, 170 - row * 34); pen.write(str(row * column), align="right")
    _finish(screen, pen)


def ex_5_50() -> None:
    screen, pen = _screen("Exercise 5.50 - Number triangle")
    for row in range(1, 11):
        pen.penup(); pen.goto(-170, 170 - row * 32)
        for number in range(1, row + 1):
            pen.write(str(number)); pen.forward(30)
    _finish(screen, pen)


def ex_5_51(size: int = 18, cell: int = 15) -> None:
    screen, pen = _screen("Exercise 5.51 - Grid")
    extent = size * cell
    for index in range(size + 1):
        offset = -extent / 2 + index * cell
        for start, end in (((-extent / 2, offset), (extent / 2, offset)), ((offset, -extent / 2), (offset, extent / 2))):
            pen.penup(); pen.goto(start); pen.pendown(); pen.goto(end)
    _finish(screen, pen)


def _axes(pen: Any) -> None:
    for start, end in (((-190, 0), (190, 0)), ((0, -100), (0, 100))):
        pen.penup(); pen.goto(start); pen.pendown(); pen.goto(end)


def _plot(pen: Any, function: Callable[[float], float], color: str) -> None:
    pen.color(color); pen.penup()
    for x in range(-175, 176):
        y = function(x)
        if x == -175: pen.goto(x, y); pen.pendown()
        else: pen.goto(x, y)


def ex_5_52() -> None:
    screen, pen = _screen("Exercise 5.52 - Sine")
    _axes(pen); _plot(pen, lambda x: 50 * math.sin(x / 100 * 2 * math.pi), "blue")
    _finish(screen, pen)


def ex_5_53() -> None:
    screen, pen = _screen("Exercise 5.53 - Sine and cosine")
    _axes(pen)
    _plot(pen, lambda x: 50 * math.sin(x / 100 * 2 * math.pi), "blue")
    _plot(pen, lambda x: 50 * math.cos(x / 100 * 2 * math.pi), "red")
    _finish(screen, pen)


def ex_5_54() -> None:
    screen, pen = _screen("Exercise 5.54 - Square function")
    _axes(pen); _plot(pen, lambda x: 0.01 * x**2, "black")
    _finish(screen, pen)


def ex_5_55(size: int = 8, cell: int = 35) -> None:
    screen, pen = _screen("Exercise 5.55 - Chessboard")
    origin = -size * cell / 2
    for row in range(size):
        for column in range(size):
            pen.penup(); pen.goto(origin + column * cell, origin + row * cell); pen.setheading(0); pen.pendown()
            if (row + column) % 2 == 0: pen.begin_fill()
            for _ in range(4): pen.forward(cell); pen.left(90)
            if (row + column) % 2 == 0: pen.end_fill()
    _finish(screen, pen)


EXERCISES: dict[str, Callable[..., Any]] = {
    f"5.{number}": globals()[f"ex_5_{number}"] for number in range(1, 56)
}
