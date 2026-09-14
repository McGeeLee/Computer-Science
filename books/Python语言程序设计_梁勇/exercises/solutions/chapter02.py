"""第 2 章编程题 2.1～2.26。"""

from __future__ import annotations

import math
import sys
import time
from collections.abc import Callable
from typing import Any


def ex_2_1(celsius: float) -> float:
    return 9 / 5 * celsius + 32


def ex_2_2(radius: float, length: float) -> tuple[float, float]:
    area = radius**2 * math.pi
    return area, area * length


def ex_2_3(feet: float) -> float:
    return feet * 0.305


def ex_2_4(pounds: float) -> float:
    return pounds * 0.454


def ex_2_5(subtotal: float, gratuity_rate: float) -> tuple[float, float]:
    gratuity = subtotal * gratuity_rate / 100
    return gratuity, subtotal + gratuity


def ex_2_6(number: int) -> int:
    if not 0 <= number <= 1000:
        raise ValueError("number must be between 0 and 1000")
    return sum(int(digit) for digit in str(number))


def ex_2_7(minutes: int) -> tuple[int, int]:
    if minutes < 0:
        raise ValueError("minutes cannot be negative")
    days = minutes // (24 * 60)
    return days // 365, days % 365


def ex_2_8(
    water_kg: float,
    initial_temperature: float,
    final_temperature: float,
) -> float:
    return water_kg * (final_temperature - initial_temperature) * 4184


def ex_2_9(temperature_f: float, wind_speed_mph: float) -> float:
    if not -58 <= temperature_f <= 41:
        raise ValueError("temperature must be between -58°F and 41°F")
    if wind_speed_mph < 2:
        raise ValueError("wind speed must be at least 2 mph")
    speed_power = wind_speed_mph**0.16
    return 35.74 + 0.6215 * temperature_f - 35.75 * speed_power + 0.4275 * temperature_f * speed_power


def ex_2_10(speed: float, acceleration: float) -> float:
    if acceleration <= 0:
        raise ValueError("acceleration must be positive")
    return speed**2 / (2 * acceleration)


def ex_2_11(final_value: float, annual_rate_percent: float, years: float) -> float:
    monthly_rate = annual_rate_percent / 1200
    return final_value / (1 + monthly_rate) ** (years * 12)


def ex_2_12() -> tuple[tuple[int, int, int], ...]:
    return tuple((a, a + 1, a ** (a + 1)) for a in range(1, 6))


def ex_2_13(number: int) -> tuple[int, int, int, int]:
    if not 1000 <= number <= 9999:
        raise ValueError("number must contain exactly four digits")
    return tuple(map(int, reversed(str(number))))  # type: ignore[return-value]


def ex_2_14(points: tuple[float, float, float, float, float, float]) -> float:
    x1, y1, x2, y2, x3, y3 = points
    side1 = math.hypot(x2 - x1, y2 - y1)
    side2 = math.hypot(x3 - x2, y3 - y2)
    side3 = math.hypot(x1 - x3, y1 - y3)
    semiperimeter = (side1 + side2 + side3) / 2
    radicand = semiperimeter * (semiperimeter - side1) * (semiperimeter - side2) * (semiperimeter - side3)
    return math.sqrt(max(0.0, radicand))


def ex_2_15(side: float) -> float:
    return 3 * math.sqrt(3) / 2 * side**2


def ex_2_16(initial_velocity: float, final_velocity: float, seconds: float) -> float:
    if seconds == 0:
        raise ValueError("time cannot be zero")
    return (final_velocity - initial_velocity) / seconds


def ex_2_17(weight_pounds: float, height_inches: float) -> float:
    if height_inches <= 0:
        raise ValueError("height must be positive")
    kilograms = weight_pounds * 0.45359237
    meters = height_inches * 0.0254
    return kilograms / meters**2


def ex_2_18(gmt_offset_hours: int, timestamp: float | None = None) -> tuple[int, int, int]:
    now = time.time() if timestamp is None else timestamp
    seconds = (int(now) + gmt_offset_hours * 3600) % (24 * 3600)
    return seconds // 3600, seconds % 3600 // 60, seconds % 60


def ex_2_19(investment: float, annual_rate_percent: float, years: float) -> float:
    monthly_rate = annual_rate_percent / 1200
    return investment * (1 + monthly_rate) ** (years * 12)


def ex_2_20(balance: float, annual_rate_percent: float) -> float:
    return balance * annual_rate_percent / 1200


def ex_2_21(monthly_saving: float, annual_rate_percent: float = 5, months: int = 6) -> float:
    monthly_rate = annual_rate_percent / 1200
    balance = 0.0
    for _ in range(months):
        balance = (balance + monthly_saving) * (1 + monthly_rate)
    return balance


def ex_2_22(years: int, initial_population: int = 312_032_486) -> int:
    seconds_per_year = 365 * 24 * 60 * 60
    change = seconds_per_year * (1 / 7 - 1 / 13 + 1 / 45)
    return round(initial_population + years * change)


def _turtle_screen(title: str):
    import turtle

    screen = turtle.Screen()
    screen.title(title)
    pen = turtle.Turtle()
    pen.speed(0)
    return screen, pen


def _finish(screen: Any, pen: Any) -> None:
    pen.hideturtle()
    screen.mainloop()


def ex_2_23(radius: float) -> None:
    screen, pen = _turtle_screen("Exercise 2.23 - Four circles")
    for x, y in ((-radius, 0), (radius, 0), (-radius, -2 * radius), (radius, -2 * radius)):
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.circle(radius)
    _finish(screen, pen)


def ex_2_24(side: float = 60) -> None:
    screen, pen = _turtle_screen("Exercise 2.24 - Four hexagons")

    def hexagon(x: float, y: float) -> None:
        pen.penup()
        pen.goto(x, y)
        pen.setheading(0)
        pen.pendown()
        for _ in range(6):
            pen.forward(side)
            pen.left(60)

    height = math.sqrt(3) * side
    for x, y in ((-side, 0), (0, 0), (-side / 2, height / 2), (-side / 2, -height / 2)):
        hexagon(x, y)
    _finish(screen, pen)


def ex_2_25(center_x: float, center_y: float, width: float, height: float) -> None:
    screen, pen = _turtle_screen("Exercise 2.25 - Rectangle")
    pen.penup()
    pen.goto(center_x - width / 2, center_y - height / 2)
    pen.pendown()
    for distance in (width, height, width, height):
        pen.forward(distance)
        pen.left(90)
    _finish(screen, pen)


def ex_2_26(center_x: float, center_y: float, radius: float) -> None:
    screen, pen = _turtle_screen("Exercise 2.26 - Circle and area")
    pen.penup()
    pen.goto(center_x, center_y - radius)
    pen.pendown()
    pen.circle(radius)
    pen.penup()
    pen.goto(center_x, center_y)
    pen.write(f"Area = {math.pi * radius**2:.2f}", align="center")
    _finish(screen, pen)


EXERCISES: dict[str, Callable[..., Any]] = {
    f"2.{number}": globals()[f"ex_2_{number}"] for number in range(1, 27)
}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args or args[0] not in EXERCISES:
        print("Import this module and call ex_2_N with the parameters stated in the book.")
        return 2
    print("Exercises 2.1～2.26 are exposed as testable functions; import the module to pass typed arguments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
