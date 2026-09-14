"""第 8 章编程题 8.1～8.21。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering

from .chapter06 import ex_6_29


def ex_8_1(ssn: str) -> bool:
    return len(ssn) == 11 and ssn[3] == ssn[6] == "-" and (ssn[:3] + ssn[4:6] + ssn[7:]).isdigit()


def ex_8_2(substring: str, text: str) -> int:
    if substring == "":
        return 0
    for start in range(len(text) - len(substring) + 1):
        if text[start : start + len(substring)] == substring:
            return start
    return -1


def ex_8_3(password: str) -> bool:
    return len(password) >= 8 and password.isalnum() and sum(character.isdigit() for character in password) >= 2


def ex_8_4(text: str, character: str) -> int:
    if len(character) != 1:
        raise ValueError("character must contain exactly one character")
    return sum(item == character for item in text)


def ex_8_5(text: str, substring: str) -> int:
    if substring == "":
        raise ValueError("substring cannot be empty")
    occurrences = 0
    position = 0
    while position <= len(text) - len(substring):
        if text[position : position + len(substring)] == substring:
            occurrences += 1
            position += len(substring)
        else:
            position += 1
    return occurrences


def ex_8_6(text: str) -> int:
    return sum(character.isalpha() for character in text)


_PHONE_GROUPS = ("ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ")
_PHONE_MAP = {letter: str(number) for number, group in enumerate(_PHONE_GROUPS, start=2) for letter in group}


def ex_8_7(phone: str) -> str:
    return "".join(_PHONE_MAP.get(character.upper(), character) for character in phone)


def ex_8_8(binary_string: str) -> int:
    if not binary_string or any(character not in "01" for character in binary_string):
        raise ValueError("input must be a binary string")
    value = 0
    for character in binary_string:
        value = value * 2 + int(character)
    return value


def ex_8_9(binary_value: str) -> str:
    return format(ex_8_8(binary_value), "X")


def ex_8_10(value: int) -> str:
    if value < 0:
        return "-" + ex_8_10(-value)
    if value == 0:
        return "0"
    digits = []
    while value:
        value, remainder = divmod(value, 2)
        digits.append(str(remainder))
    return "".join(reversed(digits))


def ex_8_11(text: str) -> str:
    return text[::-1]


def ex_8_12(genome: str) -> tuple[str, ...]:
    sequence = genome.upper()
    genes: list[str] = []
    start = 0
    while True:
        start = sequence.find("ATG", start)
        if start < 0:
            break
        valid = True
        for end in range(start + 3, len(sequence) - 2, 3):
            codon = sequence[end : end + 3]
            if codon == "ATG":
                valid = False
                start = end
                break
            if codon in {"TAG", "TAA", "TGA"}:
                if valid:
                    genes.append(sequence[start + 3 : end])
                start = end + 3
                break
        else:
            start += 3
            continue
    return tuple(genes)


def ex_8_13(text1: str, text2: str) -> str:
    length = 0
    while length < min(len(text1), len(text2)) and text1[length] == text2[length]:
        length += 1
    return text1[:length]


def ex_8_14(number: str) -> bool:
    return ex_6_29(number)


def ex_8_15(first_nine_digits: str) -> str:
    if len(first_nine_digits) != 9 or not first_nine_digits.isdigit():
        raise ValueError("ISBN-10 prefix must contain exactly nine digits")
    checksum = sum(position * int(digit) for position, digit in enumerate(first_nine_digits, start=1)) % 11
    return first_nine_digits + ("X" if checksum == 10 else str(checksum))


def ex_8_16(first_twelve_digits: str) -> str:
    if len(first_twelve_digits) != 12 or not first_twelve_digits.isdigit():
        raise ValueError("ISBN-13 prefix must contain exactly twelve digits")
    weighted_sum = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(first_twelve_digits))
    return first_twelve_digits + str((10 - weighted_sum % 10) % 10)


@dataclass(frozen=True)
class Point:
    x: float = 0
    y: float = 0

    def getX(self) -> float: return self.x
    def getY(self) -> float: return self.y
    def distance(self, point: "Point") -> float: return math.hypot(self.x - point.x, self.y - point.y)
    def isNearBy(self, point: "Point") -> bool: return self.distance(point) < 5
    def __str__(self) -> str: return f"({self.x:g}, {self.y:g})"


def ex_8_17(x1: float, y1: float, x2: float, y2: float) -> tuple[Point, Point, float, bool]:
    first, second = Point(x1, y1), Point(x2, y2)
    return first, second, first.distance(second), first.isNearBy(second)


@total_ordering
class Circle2D:
    def __init__(self, x: float = 0, y: float = 0, radius: float = 0):
        if radius < 0: raise ValueError("radius cannot be negative")
        self.__x, self.__y, self.__radius = x, y, radius

    def getX(self) -> float: return self.__x
    def setX(self, value: float) -> None: self.__x = value
    def getY(self) -> float: return self.__y
    def setY(self, value: float) -> None: self.__y = value
    def getRadius(self) -> float: return self.__radius
    def setRadius(self, value: float) -> None:
        if value < 0: raise ValueError("radius cannot be negative")
        self.__radius = value
    def getArea(self) -> float: return math.pi * self.__radius**2
    def getPerimeter(self) -> float: return 2 * math.pi * self.__radius
    def containsPoint(self, x: float, y: float) -> bool: return math.hypot(x - self.__x, y - self.__y) <= self.__radius
    def contains(self, circle: "Circle2D") -> bool: return math.hypot(circle.__x - self.__x, circle.__y - self.__y) + circle.__radius <= self.__radius
    def overlaps(self, circle: "Circle2D") -> bool: return math.hypot(circle.__x - self.__x, circle.__y - self.__y) <= self.__radius + circle.__radius
    def __contains__(self, circle: "Circle2D") -> bool: return self.contains(circle)
    def __eq__(self, other: object) -> bool: return isinstance(other, Circle2D) and self.__radius == other.__radius
    def __lt__(self, other: "Circle2D") -> bool: return self.__radius < other.__radius


def ex_8_18(circle1: Circle2D, circle2: Circle2D) -> tuple[float, float, bool, bool, bool]:
    return circle1.getArea(), circle1.getPerimeter(), circle1.containsPoint(circle2.getX(), circle2.getY()), circle1.contains(circle2), circle1.overlaps(circle2)


@total_ordering
class Rectangle2D:
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0):
        if width < 0 or height < 0: raise ValueError("width and height cannot be negative")
        self.__x, self.__y, self.__width, self.__height = x, y, width, height

    def getX(self) -> float: return self.__x
    def setX(self, value: float) -> None: self.__x = value
    def getY(self) -> float: return self.__y
    def setY(self, value: float) -> None: self.__y = value
    def getWidth(self) -> float: return self.__width
    def setWidth(self, value: float) -> None:
        if value < 0: raise ValueError("width cannot be negative")
        self.__width = value
    def getHeight(self) -> float: return self.__height
    def setHeight(self, value: float) -> None:
        if value < 0: raise ValueError("height cannot be negative")
        self.__height = value
    def getArea(self) -> float: return self.__width * self.__height
    def getPerimeter(self) -> float: return 2 * (self.__width + self.__height)
    def containsPoint(self, x: float, y: float) -> bool: return abs(x - self.__x) <= self.__width / 2 and abs(y - self.__y) <= self.__height / 2
    def contains(self, rectangle: "Rectangle2D") -> bool: return abs(rectangle.__x - self.__x) + rectangle.__width / 2 <= self.__width / 2 and abs(rectangle.__y - self.__y) + rectangle.__height / 2 <= self.__height / 2
    def overlaps(self, rectangle: "Rectangle2D") -> bool: return abs(rectangle.__x - self.__x) <= (self.__width + rectangle.__width) / 2 and abs(rectangle.__y - self.__y) <= (self.__height + rectangle.__height) / 2
    def __contains__(self, rectangle: "Rectangle2D") -> bool: return self.contains(rectangle)
    def __eq__(self, other: object) -> bool: return isinstance(other, Rectangle2D) and self.getArea() == other.getArea()
    def __lt__(self, other: "Rectangle2D") -> bool: return self.getArea() < other.getArea()


def ex_8_19(rectangle1: Rectangle2D, rectangle2: Rectangle2D) -> tuple[float, float, bool, bool, bool]:
    return rectangle1.getArea(), rectangle1.getPerimeter(), rectangle1.containsPoint(rectangle2.getX(), rectangle2.getY()), rectangle1.contains(rectangle2), rectangle1.overlaps(rectangle2)


def ex_8_20() -> Fraction:
    return sum((Fraction(numerator, numerator + 1) for numerator in range(1, 10)), start=Fraction(0, 1))


@dataclass(frozen=True)
class Complex:
    real: float = 0
    imaginary: float = 0

    def getRealPart(self) -> float: return self.real
    def getImaginaryPart(self) -> float: return self.imaginary
    def __add__(self, other: "Complex") -> "Complex": return Complex(self.real + other.real, self.imaginary + other.imaginary)
    def __sub__(self, other: "Complex") -> "Complex": return Complex(self.real - other.real, self.imaginary - other.imaginary)
    def __mul__(self, other: "Complex") -> "Complex": return Complex(self.real * other.real - self.imaginary * other.imaginary, self.imaginary * other.real + self.real * other.imaginary)

    def __truediv__(self, other: "Complex") -> "Complex":
        denominator = other.real**2 + other.imaginary**2
        if denominator == 0: raise ZeroDivisionError("division by zero complex number")
        return Complex((self.real * other.real + self.imaginary * other.imaginary) / denominator, (self.imaginary * other.real - self.real * other.imaginary) / denominator)

    def __abs__(self) -> float: return math.hypot(self.real, self.imaginary)

    def __str__(self) -> str:
        if self.imaginary == 0: return f"{self.real:g}"
        sign = "+" if self.imaginary >= 0 else "-"
        return f"({self.real:g} {sign} {abs(self.imaginary):g}i)"


def ex_8_21(first: Complex, second: Complex) -> tuple[Complex, Complex, Complex, Complex, float]:
    return first + second, first - second, first * second, first / second, abs(first)


EXERCISES = {f"8.{number}": globals()[f"ex_8_{number}"] for number in range(1, 22)}
