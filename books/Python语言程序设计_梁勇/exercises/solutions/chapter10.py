"""第 10 章编程题 10.1～10.41：列表、搜索和排序。

纯计算题返回数据；Turtle/Tkinter 题只在显式调用时打开窗口。
"""

from __future__ import annotations

import ast
import math
import operator
import random
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from functools import reduce
from typing import Any


def ex_10_1(scores: Sequence[float]) -> list[str]:
    if not scores:
        return []
    best = max(scores)
    return ["A" if score >= best - 10 else "B" if score >= best - 20 else "C" if score >= best - 30 else "D" if score >= best - 40 else "F" for score in scores]


def ex_10_2(numbers: Sequence[Any]) -> list[Any]:
    return list(reversed(numbers))


def ex_10_3(numbers: Iterable[int]) -> dict[int, int]:
    counts = Counter(numbers)
    if any(number < 1 or number > 100 for number in counts):
        raise ValueError("numbers must be between 1 and 100")
    return dict(sorted(counts.items()))


def ex_10_4(scores: Sequence[float]) -> tuple[float, int, int]:
    if not scores:
        raise ValueError("scores cannot be empty")
    average = sum(scores) / len(scores)
    above = sum(score >= average for score in scores)
    return average, above, len(scores) - above


def ex_10_5(numbers: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    for number in numbers:
        if number not in result:
            result.append(number)
    return result


def _is_prime_with_known(number: int, primes: Sequence[int]) -> bool:
    return number >= 2 and all(number % prime for prime in primes if prime <= math.isqrt(number))


def ex_10_6(count: int = 50) -> list[int]:
    if count < 0:
        raise ValueError("count cannot be negative")
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if _is_prime_with_known(candidate, primes):
            primes.append(candidate)
        candidate += 1
    return primes


def ex_10_7(draws: int = 1000, seed: int | None = None) -> list[int]:
    if draws < 0:
        raise ValueError("draws cannot be negative")
    generator = random.Random(seed)
    counts = [0] * 10
    for _ in range(draws):
        counts[generator.randrange(10)] += 1
    return counts


def ex_10_8(values: Sequence[float]) -> int:
    if not values:
        raise ValueError("values cannot be empty")
    return min(range(len(values)), key=values.__getitem__)


def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("values cannot be empty")
    return sum(values) / len(values)


def deviation(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two values are required")
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values) / (len(values) - 1))


def ex_10_9(values: Sequence[float]) -> tuple[float, float]:
    return mean(values), deviation(values)


def ex_10_10(values: list[Any]) -> list[Any]:
    for index in range(len(values) // 2):
        opposite = len(values) - 1 - index
        values[index], values[opposite] = values[opposite], values[index]
    return values


def ex_10_11(values: list[Any], seed: int | None = None) -> list[Any]:
    generator = random.Random(seed)
    for index in range(len(values) - 1, 0, -1):
        other = generator.randrange(index + 1)
        values[index], values[other] = values[other], values[index]
    return values


def ex_10_12(numbers: Sequence[int]) -> int:
    if not numbers:
        raise ValueError("numbers cannot be empty")
    return reduce(math.gcd, numbers)


def ex_10_13(values: Iterable[Any]) -> list[Any]:
    return ex_10_5(values)


def ex_10_14(values: list[float]) -> list[float]:
    for end in range(len(values) - 1, 0, -1):
        largest = max(range(end + 1), key=values.__getitem__)
        values[largest], values[end] = values[end], values[largest]
    return values


def ex_10_15(values: Sequence[float]) -> bool:
    return all(values[index] <= values[index + 1] for index in range(len(values) - 1))


def ex_10_16(values: list[float]) -> list[float]:
    for end in range(len(values) - 1, 0, -1):
        changed = False
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                changed = True
        if not changed:
            break
    return values


def ex_10_17(first: str, second: str) -> bool:
    return sorted(first) == sorted(second)


def _queen_solutions(size: int = 8) -> list[tuple[int, ...]]:
    solutions: list[tuple[int, ...]] = []

    def place(columns: tuple[int, ...]) -> None:
        row = len(columns)
        if row == size:
            solutions.append(columns)
            return
        for column in range(size):
            if column not in columns and all(abs(column - old) != row - old_row for old_row, old in enumerate(columns)):
                place(columns + (column,))

    place(())
    return solutions


def ex_10_18() -> tuple[int, ...]:
    return _queen_solutions()[0]


def ex_10_19(number_of_balls: int, slots: int, seed: int | None = None) -> tuple[list[str], list[int]]:
    if number_of_balls < 0 or slots < 2:
        raise ValueError("number_of_balls must be nonnegative and slots at least 2")
    generator = random.Random(seed)
    bins = [0] * slots
    paths: list[str] = []
    for _ in range(number_of_balls):
        path = "".join(generator.choice("LR") for _ in range(slots - 1))
        paths.append(path)
        bins[path.count("R")] += 1
    return paths, bins


def ex_10_20() -> list[tuple[int, ...]]:
    return _queen_solutions()


def ex_10_21(number_of_lockers: int = 100) -> list[int]:
    if number_of_lockers < 0:
        raise ValueError("number_of_lockers cannot be negative")
    opened = [False] * number_of_lockers
    for student in range(1, number_of_lockers + 1):
        for locker in range(student - 1, number_of_lockers, student):
            opened[locker] = not opened[locker]
    return [index + 1 for index, value in enumerate(opened) if value]


_SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
_RANKS = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")


def _card_name(card: int) -> str:
    return f"{_RANKS[card % 13]} of {_SUITS[card // 13]}"


def ex_10_22(seed: int | None = None) -> tuple[list[str], int]:
    generator = random.Random(seed)
    chosen: dict[int, int] = {}
    picks = 0
    while len(chosen) < 4:
        card = generator.randrange(52)
        picks += 1
        chosen.setdefault(card // 13, card)
    return [_card_name(chosen[suit]) for suit in range(4)], picks


def ex_10_23(equation: Sequence[float]) -> list[float]:
    if len(equation) != 3:
        raise ValueError("equation must contain a, b and c")
    a, b, c = equation
    if a == 0:
        raise ValueError("a cannot be zero")
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return []
    roots = {(-b + sign * math.sqrt(discriminant)) / (2 * a) for sign in (-1, 1)}
    return sorted(root for root in roots if root >= 0)


def ex_10_24(numbers: Sequence[int]) -> list[tuple[int, int]]:
    return [(numbers[first], numbers[second]) for first in range(len(numbers)) for second in range(first + 1, len(numbers))]


def ex_10_25(seed: int | None = None, max_attempts: int = 100_000) -> tuple[list[str], int]:
    generator = random.Random(seed)
    deck = list(range(52))
    for _ in range(max_attempts):
        cards = generator.sample(deck, 4)
        value = sum(card % 13 + 1 for card in cards)
        if value == 24:
            return [_card_name(card) for card in cards], value
    raise RuntimeError("no hand found within max_attempts")


def ex_10_26(first: Sequence[float], second: Sequence[float]) -> list[float]:
    merged: list[float] = []
    left = right = 0
    while left < len(first) and right < len(second):
        if first[left] <= second[right]:
            merged.append(first[left]); left += 1
        else:
            merged.append(second[right]); right += 1
    merged.extend(first[left:]); merged.extend(second[right:])
    return merged


def ex_10_27(values: Sequence[Any]) -> bool:
    return any(values[index] == values[index + 1] == values[index + 2] == values[index + 3] for index in range(len(values) - 3))


def ex_10_28(values: list[float]) -> int:
    if not values:
        raise ValueError("values cannot be empty")
    pivot = values[0]
    low = 1
    for index in range(1, len(values)):
        if values[index] <= pivot:
            values[low], values[index] = values[index], values[low]
            low += 1
    pivot_index = low - 1
    values[0], values[pivot_index] = values[pivot_index], values[0]
    return pivot_index


@dataclass
class HangmanRound:
    word: str
    guessed: set[str] = field(default_factory=set)
    misses: int = 0

    @property
    def display(self) -> str:
        return "".join(character if character in self.guessed else "*" for character in self.word)

    @property
    def complete(self) -> bool:
        return all(character in self.guessed for character in self.word)

    def guess(self, character: str) -> str:
        if len(character) != 1 or not character.isalpha():
            raise ValueError("guess must be one letter")
        character = character.lower()
        if character in self.guessed:
            return "already guessed"
        self.guessed.add(character)
        if character not in self.word:
            self.misses += 1
            return "miss"
        return "hit"


def ex_10_29(word: str = "program") -> HangmanRound:
    return HangmanRound(word.lower())


_ZODIAC = ("monkey", "rooster", "dog", "pig", "rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep")


def ex_10_30(year: int) -> str:
    return _ZODIAC[year % 12]


def ex_10_31(text: str) -> list[int]:
    counts = [0] * 10
    for character in text:
        if character.isascii() and character.isdigit():
            counts[int(character)] += 1
    return counts


def ex_10_32(point1: Sequence[float], point2: Sequence[float]) -> None:
    import turtle

    pen = turtle.Turtle(); pen.hideturtle(); pen.penup(); pen.goto(point1); pen.pendown(); pen.goto(point2)
    turtle.done()


def _letter_counts(size: int = 1000, seed: int | None = None) -> list[int]:
    generator = random.Random(seed)
    result = [0] * 26
    for _ in range(size):
        result[generator.randrange(26)] += 1
    return result


def _bar_canvas(canvas: Any, values: Sequence[float], labels: Sequence[str], active: set[int] | None = None) -> None:
    canvas.delete("all")
    width, height = max(canvas.winfo_width(), 400), max(canvas.winfo_height(), 220)
    maximum = max(values, default=1)
    bar_width = width / max(len(values), 1)
    active = active or set()
    for index, value in enumerate(values):
        x1, x2 = index * bar_width + 2, (index + 1) * bar_width - 2
        y1 = height - 25 - value / maximum * (height - 55)
        canvas.create_rectangle(x1, y1, x2, height - 25, fill="red" if index in active else "lightblue")
        canvas.create_text((x1 + x2) / 2, height - 10, text=labels[index])


def ex_10_33(seed: int | None = None) -> None:
    import tkinter as tk

    root = tk.Tk(); root.title("Count of Each Letter"); canvas = tk.Canvas(root, width=780, height=360, bg="white"); canvas.pack()
    counts = _letter_counts(seed=seed); root.after_idle(lambda: _bar_canvas(canvas, counts, list("abcdefghijklmnopqrstuvwxyz")))
    root.mainloop()


def ex_10_34(seed: int | None = None) -> None:
    import turtle

    counts = _letter_counts(seed=seed); screen = turtle.Screen(); screen.title("Count of Each Letter")
    pen = turtle.Turtle(); pen.hideturtle(); pen.speed(0); maximum = max(counts)
    for index, count in enumerate(counts):
        x = -390 + index * 30; height = count / maximum * 220
        pen.penup(); pen.goto(x, -130); pen.pendown(); pen.goto(x, -130 + height); pen.goto(x + 20, -130 + height); pen.goto(x + 20, -130); pen.penup(); pen.goto(x + 6, -150); pen.write(chr(97 + index))
    turtle.done()


def ex_10_35() -> None:
    import tkinter as tk

    root = tk.Tk(); root.title("Bouncing Ball"); canvas = tk.Canvas(root, width=600, height=320, bg="white"); canvas.pack(); ball = canvas.create_oval(20, 140, 50, 170, fill="red")
    velocity, running = [4, 3], [True]

    def animate() -> None:
        if running[0]:
            x1, y1, x2, y2 = canvas.coords(ball)
            if x1 <= 0 or x2 >= canvas.winfo_width(): velocity[0] *= -1
            if y1 <= 0 or y2 >= canvas.winfo_height(): velocity[1] *= -1
            canvas.move(ball, *velocity)
        root.after(25, animate)

    controls = tk.Frame(root); controls.pack()
    for label, command in (("Stop/Resume", lambda: running.__setitem__(0, not running[0])), ("Faster", lambda: velocity.__setitem__(slice(None), [v * 1.25 for v in velocity])), ("Slower", lambda: velocity.__setitem__(slice(None), [v / 1.25 for v in velocity]))):
        tk.Button(controls, text=label, command=command).pack(side="left")
    animate(); root.mainloop()


def _search_window(binary: bool) -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk(); root.title("Binary Search Animation" if binary else "Linear Search Animation")
    canvas = tk.Canvas(root, width=700, height=350, bg="white"); canvas.pack(); entry = tk.Entry(root); entry.pack(side="left")
    values = list(range(1, 21))
    if not binary: random.shuffle(values)
    state = {"index": 0, "low": 0, "high": len(values) - 1, "done": False}

    def draw(active: set[int] | None = None) -> None: _bar_canvas(canvas, values, list(map(str, values)), active)
    def reset() -> None:
        if not binary: random.shuffle(values)
        state.update(index=0, low=0, high=len(values)-1, done=False); draw()
    def step() -> None:
        if state["done"]: return
        try: key = int(entry.get())
        except ValueError: messagebox.showerror("Input", "Enter an integer"); return
        index = (state["low"] + state["high"]) // 2 if binary else state["index"]
        draw({index})
        if values[index] == key: state["done"] = True; messagebox.showinfo("Result", f"Found at index {index}")
        elif binary:
            if values[index] < key: state["low"] = index + 1
            else: state["high"] = index - 1
            if state["low"] > state["high"]: state["done"] = True; messagebox.showinfo("Result", "Not found")
        else:
            state["index"] += 1
            if state["index"] == len(values): state["done"] = True; messagebox.showinfo("Result", "Not found")
    tk.Button(root, text="Step", command=step).pack(side="left"); tk.Button(root, text="Reset", command=reset).pack(side="left"); reset(); root.mainloop()


def ex_10_36() -> None:
    _search_window(False)


def ex_10_37() -> None:
    _search_window(True)


def _sort_window(insertion: bool) -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk(); root.title("Insertion Sort Animation" if insertion else "Selection Sort Animation")
    canvas = tk.Canvas(root, width=700, height=350, bg="white"); canvas.pack(); values = list(range(1, 21)); index = [1 if insertion else len(values) - 1]
    def reset() -> None: random.shuffle(values); index[0] = 1 if insertion else len(values) - 1; _bar_canvas(canvas, values, list(map(str, values)))
    def step() -> None:
        if (insertion and index[0] >= len(values)) or (not insertion and index[0] <= 0): messagebox.showinfo("Done", "The list is sorted"); return
        if insertion:
            value, position = values[index[0]], index[0]
            while position and values[position - 1] > value: values[position] = values[position - 1]; position -= 1
            values[position] = value; active = set(range(index[0] + 1)); index[0] += 1
        else:
            largest = max(range(index[0] + 1), key=values.__getitem__); values[largest], values[index[0]] = values[index[0]], values[largest]; active = set(range(index[0], len(values))); index[0] -= 1
        _bar_canvas(canvas, values, list(map(str, values)), active)
    tk.Button(root, text="Step", command=step).pack(side="left"); tk.Button(root, text="Reset", command=reset).pack(side="left"); reset(); root.mainloop()


def ex_10_38() -> None:
    _sort_window(False)


_BINARY_OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _safe_arithmetic(expression: str) -> tuple[float, list[int]]:
    tree = ast.parse(expression, mode="eval")
    numbers: list[int] = []
    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression): return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            numbers.append(node.value); return float(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand); return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS: return _BINARY_OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        raise ValueError("only integers, parentheses and + - * / are allowed")
    return evaluate(tree), numbers


def verify_24_expression(cards: Sequence[int], expression: str) -> tuple[bool, str]:
    try: value, numbers = _safe_arithmetic(expression)
    except (SyntaxError, ValueError, ZeroDivisionError) as error: return False, str(error)
    if sorted(numbers) != sorted(cards): return False, "the expression must use each card exactly once"
    return (math.isclose(value, 24), "correct" if math.isclose(value, 24) else f"value is {value:g}, not 24")


def ex_10_39() -> None:
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk(); root.title("24-Point Game"); cards = [1, 1, 1, 1]; label = tk.Label(root, font=("Arial", 25)); label.pack(); entry = tk.Entry(root, width=35); entry.pack()
    def refresh() -> None: cards[:] = [random.randint(1, 13) for _ in range(4)]; label.config(text="  ".join(map(str, cards)))
    def verify() -> None: ok, message = verify_24_expression(cards, entry.get()); (messagebox.showinfo if ok else messagebox.showerror)("Result", message)
    tk.Button(root, text="Verify", command=verify).pack(side="left"); tk.Button(root, text="Refresh", command=refresh).pack(side="left"); refresh(); root.mainloop()


def ex_10_40() -> None:
    _sort_window(True)


def ex_10_41() -> None:
    import tkinter as tk

    root = tk.Tk(); root.title("Olympic Symbol"); canvas = tk.Canvas(root, width=620, height=300, bg="white"); canvas.pack(); centers = [[130 + index * 90, 110 + (index % 2) * 70] for index in range(5)]; colors = ("blue", "black", "red", "yellow", "green"); selected = [-1]
    def draw() -> None:
        canvas.delete("all")
        for center, color in zip(centers, colors): canvas.create_oval(center[0]-48, center[1]-48, center[0]+48, center[1]+48, outline=color, width=7)
    def press(event: Any) -> None:
        candidates = [index for index, point in enumerate(centers) if math.hypot(event.x-point[0], event.y-point[1]) <= 52]
        selected[0] = candidates[-1] if candidates else -1
    def drag(event: Any) -> None:
        if selected[0] >= 0: centers[selected[0]][:] = [event.x, event.y]; draw()
    canvas.bind("<Button-1>", press); canvas.bind("<B1-Motion>", drag); draw(); root.mainloop()


EXERCISES: dict[str, Callable[..., Any]] = {f"10.{number}": globals()[f"ex_10_{number}"] for number in range(1, 42)}
