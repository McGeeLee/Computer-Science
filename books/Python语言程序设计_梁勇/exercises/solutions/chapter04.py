"""第 4 章编程题；中文版未印出 4.37。"""

from __future__ import annotations

import calendar
import math
import random
import time
from collections.abc import Callable
from typing import Any, Literal


def ex_4_1(a: float, b: float, c: float) -> tuple[float, ...]:
    if a == 0:
        raise ValueError("a must be nonzero for a quadratic equation")
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return ()
    if discriminant == 0:
        return (-b / (2 * a),)
    root = math.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


def ex_4_2(answer: int, numbers: tuple[int, int, int] | None = None) -> tuple[tuple[int, int, int], bool]:
    values = numbers if numbers is not None else tuple(random.randint(0, 9) for _ in range(3))
    return values, answer == sum(values)


def ex_4_3(a: float, b: float, c: float, d: float, e: float, f: float) -> tuple[float, float] | None:
    determinant = a * d - b * c
    if math.isclose(determinant, 0.0):
        return None
    return (e * d - b * f) / determinant, (a * f - e * c) / determinant


def ex_4_4(answer: int, numbers: tuple[int, int] | None = None) -> tuple[tuple[int, int], bool]:
    values = numbers if numbers is not None else (random.randrange(100), random.randrange(100))
    return values, answer == sum(values)


def ex_4_5(today: int, elapsed_days: int) -> tuple[str, str]:
    names = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    if not 0 <= today <= 6:
        raise ValueError("today must be from 0 (Sunday) to 6 (Saturday)")
    return names[today], names[(today + elapsed_days) % 7]


def _bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def ex_4_6(weight_pounds: float, feet: int, inches: float) -> tuple[float, str]:
    total_inches = feet * 12 + inches
    if total_inches <= 0:
        raise ValueError("height must be positive")
    bmi = weight_pounds * 0.45359237 / (total_inches * 0.0254) ** 2
    return bmi, _bmi_category(bmi)


def ex_4_7(amount_in_cents: int) -> tuple[str, ...]:
    if amount_in_cents < 0:
        raise ValueError("amount cannot be negative")
    units = (("dollar", 100), ("quarter", 25), ("dime", 10), ("nickel", 5), ("penny", 1))
    result: list[str] = []
    remaining = amount_in_cents
    for name, value in units:
        count, remaining = divmod(remaining, value)
        if count:
            plural = "pennies" if name == "penny" and count != 1 else name + ("s" if count != 1 else "")
            result.append(f"{count} {plural}")
    return tuple(result)


def ex_4_8(a: int, b: int, c: int) -> tuple[int, int, int]:
    return tuple(sorted((a, b, c)))


def ex_4_9(weight1: float, price1: float, weight2: float, price2: float) -> Literal[1, 2, 0]:
    if weight1 <= 0 or weight2 <= 0:
        raise ValueError("package weights must be positive")
    unit1, unit2 = price1 / weight1, price2 / weight2
    return 0 if math.isclose(unit1, unit2) else (1 if unit1 < unit2 else 2)


def ex_4_10(answer: int, numbers: tuple[int, int] | None = None) -> tuple[tuple[int, int], bool]:
    values = numbers if numbers is not None else (random.randrange(100), random.randrange(100))
    return values, answer == values[0] * values[1]


def ex_4_11(month: int, year: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    return calendar.monthrange(year, month)[1]


def ex_4_12(number: int) -> tuple[bool, bool, bool]:
    by5, by6 = number % 5 == 0, number % 6 == 0
    return by5 and by6, by5 or by6, by5 != by6


def ex_4_13(status: int, taxable_income: float) -> float:
    if taxable_income < 0:
        raise ValueError("taxable income cannot be negative")
    brackets = (
        (8350, 33950, 82250, 171550, 372950),
        (16700, 67900, 137050, 208850, 372950),
        (8350, 33950, 68525, 104425, 186475),
        (11950, 45500, 117450, 190200, 372950),
    )
    rates = (0.10, 0.15, 0.25, 0.28, 0.33, 0.35)
    if not 0 <= status < len(brackets):
        raise ValueError("status must be 0, 1, 2, or 3")
    cutoffs = brackets[status]
    tax = 0.0
    lower = 0.0
    for upper, rate in zip(cutoffs, rates):
        if taxable_income <= lower:
            break
        tax += (min(taxable_income, upper) - lower) * rate
        lower = upper
    if taxable_income > cutoffs[-1]:
        tax += (taxable_income - cutoffs[-1]) * rates[-1]
    return tax


def ex_4_14(guess: int, coin: int | None = None) -> tuple[int, bool]:
    if guess not in (0, 1):
        raise ValueError("guess must be 0 or 1")
    result = random.randint(0, 1) if coin is None else coin
    return result, guess == result


def ex_4_15(guess: int, lottery: int | None = None) -> tuple[int, int]:
    if not 0 <= guess <= 999:
        raise ValueError("guess must be between 000 and 999")
    winning = random.randrange(1000) if lottery is None else lottery
    guessed_digits = f"{guess:03d}"
    winning_digits = f"{winning:03d}"
    if guessed_digits == winning_digits:
        prize = 10_000
    elif sorted(guessed_digits) == sorted(winning_digits):
        prize = 3_000
    elif set(guessed_digits) & set(winning_digits):
        prize = 1_000
    else:
        prize = 0
    return winning, prize


def ex_4_16(value: int | None = None) -> str:
    index = random.randrange(26) if value is None else value
    if not 0 <= index < 26:
        raise ValueError("value must be between 0 and 25")
    return chr(ord("A") + index)


def ex_4_17(user_choice: int, computer_choice: int | None = None) -> tuple[str, str, str]:
    choices = ("scissor", "rock", "paper")
    if user_choice not in range(3):
        raise ValueError("choice must be 0, 1, or 2")
    computer = random.randrange(3) if computer_choice is None else computer_choice
    outcome = "draw" if user_choice == computer else ("win" if (user_choice - computer) % 3 == 1 else "lose")
    return choices[computer], choices[user_choice], outcome


def ex_4_18(rate_dollars_to_rmb: float, direction: int, amount: float) -> float:
    if rate_dollars_to_rmb <= 0:
        raise ValueError("exchange rate must be positive")
    if direction == 0:
        return amount * rate_dollars_to_rmb
    if direction == 1:
        return amount / rate_dollars_to_rmb
    raise ValueError("direction must be 0 or 1")


def ex_4_19(a: float, b: float, c: float) -> float | None:
    if min(a, b, c) <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return None
    return a + b + c


def ex_4_20(temperature_f: float, wind_speed_mph: float) -> float:
    from .chapter02 import ex_2_9

    return ex_2_9(temperature_f, wind_speed_mph)


def ex_4_21(year: int, month: int, day: int) -> str:
    if month in (1, 2):
        month += 12
        year -= 1
    century, year_of_century = divmod(year, 100)
    h = (day + 26 * (month + 1) // 10 + year_of_century + year_of_century // 4 + century // 4 + 5 * century) % 7
    return ("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")[h]


def ex_4_22(x: float, y: float) -> bool:
    return math.hypot(x, y) <= 10


def ex_4_23(x: float, y: float) -> bool:
    return abs(x) <= 5 and abs(y) <= 2.5


def ex_4_24(card_number: int | None = None) -> tuple[str, str]:
    card = random.randrange(52) if card_number is None else card_number
    if not 0 <= card < 52:
        raise ValueError("card number must be between 0 and 51")
    ranks = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")
    suits = ("Clubs", "Diamonds", "Hearts", "Spades")
    return ranks[card % 13], suits[card // 13]


def ex_4_25(points: tuple[float, float, float, float, float, float, float, float]) -> tuple[float, float] | None:
    x1, y1, x2, y2, x3, y3, x4, y4 = points
    a, b, e = y1 - y2, x2 - x1, (y1 - y2) * x1 + (x2 - x1) * y1
    c, d, f = y3 - y4, x4 - x3, (y3 - y4) * x3 + (x4 - x3) * y3
    return ex_4_3(a, b, c, d, e, f)


def ex_4_26(number: int) -> bool:
    return 100 <= number <= 999 and str(number) == str(number)[::-1]


def ex_4_27(x: float, y: float) -> bool:
    return x >= 0 and y >= 0 and x / 200 + y / 100 <= 1


Rectangle = tuple[float, float, float, float]
Circle = tuple[float, float, float]


def ex_4_28(rectangle1: Rectangle, rectangle2: Rectangle) -> Literal["inside", "overlap", "disjoint"]:
    x1, y1, w1, h1 = rectangle1
    x2, y2, w2, h2 = rectangle2
    if min(w1, h1, w2, h2) < 0:
        raise ValueError("width and height cannot be negative")
    if abs(x2 - x1) + w2 / 2 <= w1 / 2 and abs(y2 - y1) + h2 / 2 <= h1 / 2:
        return "inside"
    if abs(x2 - x1) <= (w1 + w2) / 2 and abs(y2 - y1) <= (h1 + h2) / 2:
        return "overlap"
    return "disjoint"


def ex_4_29(circle1: Circle, circle2: Circle) -> Literal["inside", "overlap", "disjoint"]:
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    if min(r1, r2) < 0:
        raise ValueError("radius cannot be negative")
    distance = math.hypot(x2 - x1, y2 - y1)
    if distance + r2 <= r1:
        return "inside"
    if distance <= r1 + r2:
        return "overlap"
    return "disjoint"


def ex_4_30(gmt_offset_hours: int, timestamp: float | None = None) -> tuple[int, int, int, str]:
    now = time.time() if timestamp is None else timestamp
    seconds = (int(now) + gmt_offset_hours * 3600) % (24 * 3600)
    hour24, remainder = divmod(seconds, 3600)
    minute, second = divmod(remainder, 60)
    return (12 if hour24 % 12 == 0 else hour24 % 12), minute, second, ("AM" if hour24 < 12 else "PM")


Point = tuple[float, float]


def _cross(p0: Point, p1: Point, p2: Point) -> float:
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def ex_4_31(p0: Point, p1: Point, p2: Point) -> Literal["left", "right", "same line"]:
    value = _cross(p0, p1, p2)
    if math.isclose(value, 0.0):
        return "same line"
    return "left" if value > 0 else "right"


def ex_4_32(p0: Point, p1: Point, p2: Point) -> bool:
    return math.isclose(_cross(p0, p1, p2), 0.0) and min(p0[0], p1[0]) <= p2[0] <= max(p0[0], p1[0]) and min(p0[1], p1[1]) <= p2[1] <= max(p0[1], p1[1])


def ex_4_33(decimal_value: int) -> str:
    if not 0 <= decimal_value <= 15:
        raise ValueError("decimal value must be between 0 and 15")
    return format(decimal_value, "X")


def ex_4_34(hex_character: str) -> int:
    if len(hex_character) != 1 or hex_character.upper() not in "0123456789ABCDEF":
        raise ValueError("input must be one hexadecimal character")
    return int(hex_character, 16)


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


def ex_4_35(p0: Point, p1: Point, p2: Point) -> None:
    screen, pen = _screen("Exercise 4.35 - Point position")
    pen.penup(); pen.goto(p0); pen.pendown(); pen.goto(p1)
    for label, point in (("p0", p0), ("p1", p1), ("p2", p2)):
        pen.penup(); pen.goto(point); pen.dot(7); pen.write(f"{label}{point}")
    pen.goto(0, min(p0[1], p1[1], p2[1]) - 35)
    pen.write(f"p2 is on the {ex_4_31(p0, p1, p2)} of the line", align="center")
    _finish(screen, pen)


def _draw_rectangle(pen: Any, rectangle: Rectangle) -> None:
    x, y, width, height = rectangle
    pen.penup(); pen.goto(x - width / 2, y - height / 2); pen.setheading(0); pen.pendown()
    for distance in (width, height, width, height):
        pen.forward(distance); pen.left(90)


def ex_4_36(x: float, y: float) -> None:
    screen, pen = _screen("Exercise 4.36 - Point in rectangle")
    _draw_rectangle(pen, (0, 0, 100, 50))
    pen.penup(); pen.goto(x, y); pen.dot(7)
    pen.goto(0, -55); pen.write("The point is inside the rectangle" if ex_4_23(x / 10, y / 10) else "The point is not inside the rectangle", align="center")
    _finish(screen, pen)


def ex_4_38(rectangle1: Rectangle, rectangle2: Rectangle) -> None:
    screen, pen = _screen("Exercise 4.38 - Two rectangles")
    _draw_rectangle(pen, rectangle1); _draw_rectangle(pen, rectangle2)
    pen.penup(); pen.goto(0, min(rectangle1[1], rectangle2[1]) - max(rectangle1[3], rectangle2[3]) / 2 - 30)
    pen.write(f"r2 is {ex_4_28(rectangle1, rectangle2)} relative to r1", align="center")
    _finish(screen, pen)


def _draw_circle(pen: Any, circle: Circle) -> None:
    x, y, radius = circle
    pen.penup(); pen.goto(x, y - radius); pen.setheading(0); pen.pendown(); pen.circle(radius)


def ex_4_39(circle1: Circle, circle2: Circle) -> None:
    screen, pen = _screen("Exercise 4.39 - Two circles")
    _draw_circle(pen, circle1); _draw_circle(pen, circle2)
    pen.penup(); pen.goto(0, min(circle1[1] - circle1[2], circle2[1] - circle2[2]) - 30)
    pen.write(f"circle2 is {ex_4_29(circle1, circle2)} relative to circle1", align="center")
    _finish(screen, pen)


_PRINTED_NUMBERS = tuple(range(1, 37)) + (38, 39)
EXERCISES: dict[str, Callable[..., Any]] = {
    f"4.{number}": globals()[f"ex_4_{number}"] for number in _PRINTED_NUMBERS
}
