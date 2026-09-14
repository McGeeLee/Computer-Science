"""第 7 章编程题 7.1～7.10。"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Rectangle:
    width: float = 1
    height: float = 2

    def getArea(self) -> float:
        return self.width * self.height

    def getPerimeter(self) -> float:
        return 2 * (self.width + self.height)


def ex_7_1(width: float = 1, height: float = 2) -> Rectangle:
    return Rectangle(width, height)


class Stock:
    def __init__(self, symbol: str, name: str, previous_closing_price: float, current_price: float):
        self.__symbol = symbol
        self.__name = name
        self.__previousClosingPrice = previous_closing_price
        self.__currentPrice = current_price

    def getSymbol(self) -> str: return self.__symbol
    def getName(self) -> str: return self.__name
    def getPreviousClosingPrice(self) -> float: return self.__previousClosingPrice
    def setPreviousClosingPrice(self, value: float) -> None: self.__previousClosingPrice = value
    def getCurrentPrice(self) -> float: return self.__currentPrice
    def setCurrentPrice(self, value: float) -> None: self.__currentPrice = value

    def getChangePercent(self) -> float:
        if self.__previousClosingPrice == 0:
            raise ZeroDivisionError("previous closing price cannot be zero")
        return (self.__currentPrice - self.__previousClosingPrice) / self.__previousClosingPrice * 100


def ex_7_2() -> Stock:
    return Stock("INTC", "Intel Corporation", 20.5, 20.35)


class Account:
    def __init__(self, account_id: int = 0, balance: float = 100, annual_interest_rate: float = 0):
        self.__id = account_id
        self.__balance = balance
        self.__annualInterestRate = annual_interest_rate

    def getId(self) -> int: return self.__id
    def setId(self, value: int) -> None: self.__id = value
    def getBalance(self) -> float: return self.__balance
    def setBalance(self, value: float) -> None: self.__balance = value
    def getAnnualInterestRate(self) -> float: return self.__annualInterestRate
    def setAnnualInterestRate(self, value: float) -> None: self.__annualInterestRate = value
    def getMonthlyInterestRate(self) -> float: return self.__annualInterestRate / 1200
    def getMonthlyInterest(self) -> float: return self.__balance * self.getMonthlyInterestRate()

    def withdraw(self, amount: float) -> None:
        if amount < 0 or amount > self.__balance:
            raise ValueError("invalid withdrawal")
        self.__balance -= amount

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("deposit cannot be negative")
        self.__balance += amount


def ex_7_3() -> Account:
    account = Account(1122, 20_000, 4.5)
    account.withdraw(2500)
    account.deposit(3000)
    return account


class Fan:
    SLOW, MEDIUM, FAST = 1, 2, 3

    def __init__(self, speed: int = SLOW, radius: float = 5, color: str = "blue", on: bool = False):
        self.__speed, self.__radius, self.__color, self.__on = speed, radius, color, on

    def getSpeed(self) -> int: return self.__speed
    def setSpeed(self, value: int) -> None: self.__speed = value
    def getRadius(self) -> float: return self.__radius
    def setRadius(self, value: float) -> None: self.__radius = value
    def getColor(self) -> str: return self.__color
    def setColor(self, value: str) -> None: self.__color = value
    def isOn(self) -> bool: return self.__on
    def setOn(self, value: bool) -> None: self.__on = value


def ex_7_4() -> tuple[Fan, Fan]:
    return Fan(Fan.FAST, 10, "yellow", True), Fan(Fan.MEDIUM, 5, "blue", False)


class RegularPolygon:
    def __init__(self, n: int = 3, side: float = 1, x: float = 0, y: float = 0):
        if n < 3 or side <= 0:
            raise ValueError("a regular polygon needs at least three positive-length sides")
        self.__n, self.__side, self.__x, self.__y = n, side, x, y

    def getN(self) -> int: return self.__n
    def setN(self, value: int) -> None:
        if value < 3: raise ValueError("n must be at least 3")
        self.__n = value
    def getSide(self) -> float: return self.__side
    def setSide(self, value: float) -> None:
        if value <= 0: raise ValueError("side must be positive")
        self.__side = value
    def getX(self) -> float: return self.__x
    def setX(self, value: float) -> None: self.__x = value
    def getY(self) -> float: return self.__y
    def setY(self, value: float) -> None: self.__y = value
    def getPerimeter(self) -> float: return self.__n * self.__side
    def getArea(self) -> float: return self.__n * self.__side**2 / (4 * math.tan(math.pi / self.__n))


def ex_7_5() -> tuple[RegularPolygon, RegularPolygon, RegularPolygon]:
    return RegularPolygon(), RegularPolygon(6, 4), RegularPolygon(10, 4, 5.6, 7.8)


class QuadraticEquation:
    def __init__(self, a: float, b: float, c: float): self.__a, self.__b, self.__c = a, b, c
    def getA(self) -> float: return self.__a
    def getB(self) -> float: return self.__b
    def getC(self) -> float: return self.__c
    def getDiscriminant(self) -> float: return self.__b**2 - 4 * self.__a * self.__c

    def getRoot1(self) -> float:
        if self.__a == 0 or self.getDiscriminant() < 0: return 0
        return (-self.__b + math.sqrt(self.getDiscriminant())) / (2 * self.__a)

    def getRoot2(self) -> float:
        if self.__a == 0 or self.getDiscriminant() < 0: return 0
        return (-self.__b - math.sqrt(self.getDiscriminant())) / (2 * self.__a)


def ex_7_6(a: float, b: float, c: float) -> QuadraticEquation:
    return QuadraticEquation(a, b, c)


class LinearEquation:
    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float):
        self.__a, self.__b, self.__c, self.__d, self.__e, self.__f = a, b, c, d, e, f

    def getA(self) -> float: return self.__a
    def getB(self) -> float: return self.__b
    def getC(self) -> float: return self.__c
    def getD(self) -> float: return self.__d
    def getE(self) -> float: return self.__e
    def getF(self) -> float: return self.__f
    def isSolvable(self) -> bool: return not math.isclose(self.__a * self.__d - self.__b * self.__c, 0.0)

    def getX(self) -> float:
        if not self.isSolvable(): raise ValueError("equation has no unique solution")
        return (self.__e * self.__d - self.__b * self.__f) / (self.__a * self.__d - self.__b * self.__c)

    def getY(self) -> float:
        if not self.isSolvable(): raise ValueError("equation has no unique solution")
        return (self.__a * self.__f - self.__e * self.__c) / (self.__a * self.__d - self.__b * self.__c)


def ex_7_7(a: float, b: float, c: float, d: float, e: float, f: float) -> LinearEquation:
    return LinearEquation(a, b, c, d, e, f)


class StopWatch:
    def __init__(self): self.__startTime, self.__endTime = time.perf_counter(), None
    def getStartTime(self) -> float: return self.__startTime
    def getEndTime(self) -> Optional[float]: return self.__endTime
    def start(self) -> None: self.__startTime, self.__endTime = time.perf_counter(), None
    def stop(self) -> None: self.__endTime = time.perf_counter()

    def getElapsedTime(self) -> float:
        end = time.perf_counter() if self.__endTime is None else self.__endTime
        return (end - self.__startTime) * 1000


def ex_7_8(iterations: int = 1_000_000) -> float:
    watch = StopWatch(); watch.start()
    value = 0
    for _ in range(iterations): value += 1
    watch.stop()
    return watch.getElapsedTime()


def ex_7_9(points: tuple[float, float, float, float, float, float, float, float]) -> tuple[float, float] | None:
    x1, y1, x2, y2, x3, y3, x4, y4 = points
    equation = LinearEquation(y1 - y2, x2 - x1, y3 - y4, x4 - x3, (y1 - y2) * x1 + (x2 - x1) * y1, (y3 - y4) * x3 + (x4 - x3) * y3)
    return (equation.getX(), equation.getY()) if equation.isSolvable() else None


class Time:
    def __init__(self, elapsed_time: float | None = None):
        self.setTime(time.time() if elapsed_time is None else elapsed_time)

    def getHour(self) -> int: return self.__hour
    def getMinute(self) -> int: return self.__minute
    def getSecond(self) -> int: return self.__second

    def setTime(self, elapsed_time: float) -> None:
        total_seconds = int(elapsed_time) % (24 * 3600)
        self.__hour, remainder = divmod(total_seconds, 3600)
        self.__minute, self.__second = divmod(remainder, 60)


def ex_7_10(elapsed_time: float | None = None) -> Time:
    return Time(elapsed_time)


EXERCISES = {f"7.{number}": globals()[f"ex_7_{number}"] for number in range(1, 11)}
