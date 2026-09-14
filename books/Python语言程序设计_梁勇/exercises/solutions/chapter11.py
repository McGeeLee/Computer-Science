"""第 11 章编程题 11.1～11.52：多维列表。"""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from typing import Any


Matrix = Sequence[Sequence[float]]
Point = Sequence[float]


def _rectangular(matrix: Sequence[Sequence[Any]], *, nonempty: bool = True) -> tuple[int, int]:
    rows = len(matrix)
    if nonempty and not rows:
        raise ValueError("matrix cannot be empty")
    columns = len(matrix[0]) if rows else 0
    if nonempty and not columns:
        raise ValueError("matrix rows cannot be empty")
    if any(len(row) != columns for row in matrix):
        raise ValueError("matrix must be rectangular")
    return rows, columns


def ex_11_1(matrix: Matrix, column_index: int) -> float:
    _, columns = _rectangular(matrix)
    if not 0 <= column_index < columns:
        raise IndexError("column index out of range")
    return sum(row[column_index] for row in matrix)


def ex_11_2(matrix: Matrix) -> float:
    rows, columns = _rectangular(matrix)
    if rows != columns:
        raise ValueError("matrix must be square")
    return sum(matrix[index][index] for index in range(rows))


def ex_11_3(answers: Sequence[Sequence[str]], key: Sequence[str]) -> list[tuple[int, int]]:
    if any(len(answer) != len(key) for answer in answers):
        raise ValueError("each answer row must match the key")
    scores = [(student, sum(value == expected for value, expected in zip(answer, key))) for student, answer in enumerate(answers)]
    return sorted(scores, key=lambda item: (item[1], item[0]))


def ex_11_4(hours: Matrix) -> list[tuple[int, float]]:
    return sorted(((employee, sum(row)) for employee, row in enumerate(hours)), key=lambda item: (-item[1], item[0]))


def ex_11_5(first: Matrix, second: Matrix) -> list[list[float]]:
    shape = _rectangular(first)
    if _rectangular(second) != shape:
        raise ValueError("matrices must have the same dimensions")
    return [[first[row][column] + second[row][column] for column in range(shape[1])] for row in range(shape[0])]


def ex_11_6(first: Matrix, second: Matrix) -> list[list[float]]:
    first_rows, shared = _rectangular(first); second_rows, second_columns = _rectangular(second)
    if shared != second_rows:
        raise ValueError("the first column count must equal the second row count")
    return [[sum(first[row][index] * second[index][column] for index in range(shared)) for column in range(second_columns)] for row in range(first_rows)]


def _distance(first: Point, second: Point) -> float:
    if len(first) != len(second):
        raise ValueError("points must have the same dimension")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def ex_11_7(points: Sequence[Point]) -> tuple[int, int, float]:
    pairs = ex_11_8(points)
    if not pairs:
        raise ValueError("at least two points are required")
    first, second = pairs[0]
    return first, second, _distance(points[first], points[second])


def ex_11_8(points: Sequence[Point]) -> list[tuple[int, int]]:
    if len(points) < 2:
        return []
    distances = {(first, second): _distance(points[first], points[second]) for first in range(len(points)) for second in range(first + 1, len(points))}
    minimum = min(distances.values())
    return [pair for pair, value in distances.items() if math.isclose(value, minimum)]


def _winner(board: Sequence[Sequence[str]], length: int = 3) -> str | None:
    rows, columns = _rectangular(board)
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for row in range(rows):
        for column in range(columns):
            token = board[row][column]
            if token == " ": continue
            for dr, dc in directions:
                cells = [(row + step * dr, column + step * dc) for step in range(length)]
                if all(0 <= r < rows and 0 <= c < columns and board[r][c] == token for r, c in cells):
                    return token
    return None


class TicTacToe:
    def __init__(self):
        self.board = [[" "] * 3 for _ in range(3)]; self.turn = "X"

    @property
    def winner(self) -> str | None: return _winner(self.board)
    @property
    def full(self) -> bool: return all(cell != " " for row in self.board for cell in row)
    def play(self, row: int, column: int) -> str:
        if self.winner or self.full: raise RuntimeError("game is over")
        if not (0 <= row < 3 and 0 <= column < 3): raise IndexError("cell out of range")
        if self.board[row][column] != " ": raise ValueError("cell is occupied")
        token = self.turn; self.board[row][column] = token; self.turn = "O" if token == "X" else "X"; return token


def ex_11_9() -> TicTacToe:
    return TicTacToe()


def ex_11_10(matrix: Sequence[Sequence[int]]) -> tuple[list[int], list[int]]:
    rows, columns = _rectangular(matrix)
    row_sums = [sum(row) for row in matrix]; column_sums = [sum(matrix[row][column] for row in range(rows)) for column in range(columns)]
    return [index for index, value in enumerate(row_sums) if value == max(row_sums)], [index for index, value in enumerate(column_sums) if value == max(column_sums)]


def ex_11_11(number: int) -> list[list[str]]:
    if not 0 <= number <= 511: raise ValueError("number must be between 0 and 511")
    bits = f"{number:09b}"
    return [["T" if bits[row * 3 + column] == "1" else "H" for column in range(3)] for row in range(3)]


_TAX_RATES = (0.10, 0.15, 0.25, 0.28, 0.33, 0.35)
_TAX_BRACKETS = ((8350, 33950, 82250, 171550, 372950), (16700, 67900, 137050, 208850, 372950), (8350, 33950, 68525, 104425, 186475), (11950, 45500, 117450, 190200, 372950))


def ex_11_12(status: int, taxable_income: float) -> float:
    if status not in range(4) or taxable_income < 0: raise ValueError("invalid status or income")
    boundaries = (0,) + _TAX_BRACKETS[status] + (math.inf,)
    return sum(max(0.0, min(taxable_income, boundaries[index + 1]) - boundaries[index]) * _TAX_RATES[index] for index in range(6))


def ex_11_13(matrix: Matrix) -> list[int]:
    rows, columns = _rectangular(matrix); row, column = max(((r, c) for r in range(rows) for c in range(columns)), key=lambda item: matrix[item[0]][item[1]])
    return [row, column]


def ex_11_14(matrix_or_size: Sequence[Sequence[int]] | int, seed: int | None = None) -> tuple[list[list[int]], dict[str, list[int] | int | None]]:
    if isinstance(matrix_or_size, int):
        generator = random.Random(seed); matrix = [[generator.randrange(2) for _ in range(matrix_or_size)] for _ in range(matrix_or_size)]
    else: matrix = [list(row) for row in matrix_or_size]
    size, columns = _rectangular(matrix)
    if size != columns or any(value not in (0, 1) for row in matrix for value in row): raise ValueError("a square binary matrix is required")
    rows = [index for index, row in enumerate(matrix) if len(set(row)) == 1]
    cols = [column for column in range(size) if len({matrix[row][column] for row in range(size)}) == 1]
    major = matrix[0][0] if all(matrix[index][index] == matrix[0][0] for index in range(size)) else None
    sub = matrix[0][-1] if all(matrix[index][size - index - 1] == matrix[0][-1] for index in range(size)) else None
    return matrix, {"rows": rows, "columns": cols, "major_diagonal": major, "sub_diagonal": sub}


def ex_11_15(points: Sequence[Point], tolerance: float = 1e-9) -> bool:
    if len(points) < 3: return True
    first, second = points[0], points[1]
    return all(math.isclose((second[0]-first[0])*(point[1]-first[1]), (second[1]-first[1])*(point[0]-first[0]), abs_tol=tolerance) for point in points[2:])


def ex_11_16(points: Sequence[Point]) -> list[list[float]]:
    return sorted((list(point) for point in points), key=lambda point: (point[1], point[0]))


def ex_11_17(balances: Sequence[float], loans: Matrix, limit: float) -> list[int]:
    rows, columns = _rectangular(loans)
    if rows != columns or len(balances) != rows: raise ValueError("one square loan matrix and one balance per bank are required")
    current = [list(row) for row in loans]; unsafe: list[int] = []
    while True:
        new = next((bank for bank in range(rows) if bank not in unsafe and balances[bank] + sum(current[bank]) < limit), None)
        if new is None: break
        unsafe.append(new)
        for lender in range(rows): current[lender][new] = 0
    return unsafe


def ex_11_18(matrix: list[list[Any]], seed: int | None = None) -> list[list[Any]]:
    random.Random(seed).shuffle(matrix); return matrix


def consecutive_four_cells(values: Sequence[Sequence[Any]]) -> list[tuple[int, int]]:
    rows, columns = _rectangular(values); directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for row in range(rows):
        for column in range(columns):
            for dr, dc in directions:
                cells = [(row + step*dr, column + step*dc) for step in range(4)]
                if all(0 <= r < rows and 0 <= c < columns for r, c in cells) and len({values[r][c] for r, c in cells}) == 1: return cells
    return []


def ex_11_19(values: Sequence[Sequence[Any]]) -> bool:
    return bool(consecutive_four_cells(values))


class ConnectFour:
    def __init__(self): self.board = [[" "] * 7 for _ in range(6)]; self.turn = "R"
    @property
    def winner(self) -> str | None: return _winner(self.board, 4)
    @property
    def full(self) -> bool: return all(self.board[0][column] != " " for column in range(7))
    def drop(self, column: int) -> tuple[int, int]:
        if self.winner or self.full: raise RuntimeError("game is over")
        if not 0 <= column < 7: raise IndexError("column out of range")
        row = next((r for r in range(5, -1, -1) if self.board[r][column] == " "), None)
        if row is None: raise ValueError("column is full")
        self.board[row][column] = self.turn; self.turn = "Y" if self.turn == "R" else "R"; return row, column


def ex_11_20() -> ConnectFour:
    return ConnectFour()


def _sudoku_candidates(grid: Sequence[Sequence[int]], row: int, column: int) -> set[int]:
    used = set(grid[row]) | {grid[r][column] for r in range(9)} | {grid[r][c] for r in range(row//3*3, row//3*3+3) for c in range(column//3*3, column//3*3+3)}
    return set(range(1, 10)) - used


def sudoku_solutions(grid: Sequence[Sequence[int]], limit: int | None = None) -> list[list[list[int]]]:
    if _rectangular(grid) != (9, 9) or any(type(value) is not int or not 0 <= value <= 9 for row in grid for value in row): raise ValueError("grid must be 9 x 9 with digits 0..9")
    work = [list(row) for row in grid]; answers: list[list[list[int]]] = []
    def solve() -> None:
        if limit is not None and len(answers) >= limit: return
        blanks = [(len(candidates := _sudoku_candidates(work, r, c)), r, c, candidates) for r in range(9) for c in range(9) if work[r][c] == 0]
        if not blanks: answers.append([row[:] for row in work]); return
        _, row, column, candidates = min(blanks, key=lambda item: item[0])
        for value in sorted(candidates): work[row][column] = value; solve(); work[row][column] = 0
    if all(len([value for value in row if value]) == len(set(value for value in row if value)) for row in work): solve()
    return answers


def ex_11_21(grid: Sequence[Sequence[int]]) -> tuple[int, list[list[list[int]]]]:
    answers = sudoku_solutions(grid); return len(answers), answers[:2]


def ex_11_22(matrix: Sequence[Sequence[int]]) -> bool:
    rows, columns = _rectangular(matrix)
    return all(sum(row) % 2 == 0 for row in matrix) and all(sum(matrix[row][column] for row in range(rows)) % 2 == 0 for column in range(columns))


def ex_11_23(matrix: Sequence[Sequence[int]]) -> tuple[int, int] | None:
    rows, columns = _rectangular(matrix); odd_rows = [row for row in range(rows) if sum(matrix[row]) % 2]; odd_columns = [column for column in range(columns) if sum(matrix[row][column] for row in range(rows)) % 2]
    return (odd_rows[0], odd_columns[0]) if len(odd_rows) == len(odd_columns) == 1 else None


def ex_11_24(grid: Sequence[Sequence[int]]) -> bool:
    try: rows, columns = _rectangular(grid)
    except ValueError: return False
    target = set(range(1, 10))
    return rows == columns == 9 and all(set(row) == target for row in grid) and all({grid[row][column] for row in range(9)} == target for column in range(9)) and all({grid[row+dr][column+dc] for dr in range(3) for dc in range(3)} == target for row in range(0, 9, 3) for column in range(0, 9, 3))


def ex_11_25(matrix: Matrix, tolerance: float = 1e-9) -> bool:
    try: rows, columns = _rectangular(matrix)
    except ValueError: return False
    return rows == columns and all(value > 0 for row in matrix for value in row) and all(math.isclose(sum(matrix[row][column] for row in range(rows)), 1.0, abs_tol=tolerance) for column in range(columns))


def ex_11_26(matrix: Matrix) -> list[list[float]]:
    _rectangular(matrix); return [sorted(row) for row in matrix]


def ex_11_27(matrix: Matrix) -> list[list[float]]:
    rows, columns = _rectangular(matrix); sorted_columns = [sorted(matrix[row][column] for row in range(rows)) for column in range(columns)]
    return [[sorted_columns[column][row] for column in range(columns)] for row in range(rows)]


def ex_11_28(first: Sequence[Sequence[Any]], second: Sequence[Sequence[Any]]) -> bool:
    return first == second


def ex_11_29(first: Sequence[Sequence[Any]], second: Sequence[Sequence[Any]]) -> bool:
    return Counter(value for row in first for value in row) == Counter(value for row in second for value in row)


def ex_11_30(coefficients: Matrix, constants: Sequence[float]) -> list[float] | None:
    if _rectangular(coefficients) != (2, 2) or len(constants) != 2: raise ValueError("a 2 x 2 system is required")
    a00, a01 = coefficients[0]; a10, a11 = coefficients[1]; determinant = a00*a11-a01*a10
    if math.isclose(determinant, 0): return None
    return [(constants[0]*a11-a01*constants[1])/determinant, (a00*constants[1]-constants[0]*a10)/determinant]


def ex_11_31(points: Sequence[Point]) -> list[float] | None:
    if len(points) != 4 or any(len(point) != 2 for point in points): raise ValueError("four 2D points are required")
    (x1,y1),(x2,y2),(x3,y3),(x4,y4)=points
    return ex_11_30([[y1-y2, x2-x1], [y3-y4, x4-x3]], [x2*y1-x1*y2, x4*y3-x3*y4])


def ex_11_32(points: Sequence[Point]) -> float | None:
    if len(points) != 3 or any(len(point) != 2 for point in points): raise ValueError("three 2D points are required")
    (x1,y1),(x2,y2),(x3,y3)=points; area = abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))/2
    return None if math.isclose(area, 0) else area


def ex_11_33(points: Sequence[Point]) -> list[float]:
    if len(points) != 4: raise ValueError("four points are required")
    return sorted(ex_11_32([points[i] for i in range(4) if i != omitted]) or 0.0 for omitted in range(4))


def ex_11_34(points: Sequence[Point]) -> list[float]:
    if not points: raise ValueError("points cannot be empty")
    return list(min(points, key=lambda point: (point[1], -point[0])))


def ex_11_35(points: Sequence[Point]) -> tuple[list[float], float]:
    if not points: raise ValueError("points cannot be empty")
    index = min(range(len(points)), key=lambda candidate: sum(_distance(points[candidate], other) for other in points))
    total = sum(_distance(points[index], other) for other in points)
    return list(points[index]), total


def self_avoiding_walk(size: int, seed: int | None = None) -> tuple[list[tuple[int, int]], bool]:
    if size < 2: raise ValueError("size must be at least 2")
    generator = random.Random(seed); current = (size // 2, size // 2); path = [current]; visited = {current}
    while 0 < current[0] < size-1 and 0 < current[1] < size-1:
        neighbors = [(current[0]+dr, current[1]+dc) for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)) if (current[0]+dr,current[1]+dc) not in visited]
        if not neighbors: return path, True
        current = generator.choice(neighbors); visited.add(current); path.append(current)
    return path, False


def ex_11_36(size: int = 16, seed: int | None = None) -> None:
    import turtle
    path, dead_end = self_avoiding_walk(size, seed); screen = turtle.Screen(); screen.title("Self-Avoiding Random Walk")
    pen = turtle.Turtle(); pen.hideturtle(); pen.speed(0); scale = 360/(size-1); pen.penup()
    for index,(row,column) in enumerate(path):
        pen.goto((column-(size-1)/2)*scale, (row-(size-1)/2)*scale)
        if index == 0: pen.pendown()
    pen.write("  dead end" if dead_end else "  boundary"); turtle.done()


def ex_11_37(sizes: Iterable[int] = range(10, 81), trials: int = 10_000, seed: int | None = None) -> dict[int, float]:
    if trials <= 0: raise ValueError("trials must be positive")
    generator = random.Random(seed); result = {}
    for size in sizes: result[size] = sum(self_avoiding_walk(size, generator.randrange(2**32))[1] for _ in range(trials)) / trials
    return result


def _turtle_poly(points: Sequence[Point], close: bool, fill: bool) -> None:
    import turtle
    if not points: return
    pen = turtle.Turtle(); pen.hideturtle(); pen.penup(); pen.goto(points[0]); pen.pendown()
    if fill: pen.begin_fill()
    for point in points[1:]: pen.goto(point)
    if close: pen.goto(points[0])
    if fill: pen.end_fill()
    turtle.done()


def drawPolyline(points: Sequence[Point]) -> None: _turtle_poly(points, False, False)
def drawPolygon(points: Sequence[Point]) -> None: _turtle_poly(points, True, False)
def fillPolygon(points: Sequence[Point]) -> None: _turtle_poly(points, True, True)


def ex_11_38(points: Sequence[Point], mode: str = "polyline") -> None:
    {"polyline": drawPolyline, "polygon": drawPolygon, "fill": fillPolygon}[mode](points)


def ex_11_39() -> None:
    import tkinter as tk
    from tkinter import messagebox
    root=tk.Tk(); root.title("Consecutive Four"); entries=[[tk.Entry(root,width=4,justify="center") for _ in range(7)] for _ in range(6)]
    for row in range(6):
        for column in range(7): entries[row][column].grid(row=row,column=column,padx=2,pady=2)
    def solve() -> None:
        try: matrix=[[int(entry.get()) for entry in row] for row in entries]
        except ValueError: messagebox.showerror("Input","Enter integers in every cell"); return
        cells=set(consecutive_four_cells(matrix))
        for r,row in enumerate(entries):
            for c,entry in enumerate(row): entry.config(bg="yellow" if (r,c) in cells else "white")
        if not cells: messagebox.showinfo("Result","No consecutive four")
    tk.Button(root,text="Solve",command=solve).grid(row=6,column=0,columnspan=7); root.mainloop()


_STATE_CAPITALS = {
    "Alabama":"Montgomery","Alaska":"Juneau","Arizona":"Phoenix","Arkansas":"Little Rock","California":"Sacramento","Colorado":"Denver","Connecticut":"Hartford","Delaware":"Dover","Florida":"Tallahassee","Georgia":"Atlanta","Hawaii":"Honolulu","Idaho":"Boise","Illinois":"Springfield","Indiana":"Indianapolis","Iowa":"Des Moines","Kansas":"Topeka","Kentucky":"Frankfort","Louisiana":"Baton Rouge","Maine":"Augusta","Maryland":"Annapolis","Massachusetts":"Boston","Michigan":"Lansing","Minnesota":"Saint Paul","Mississippi":"Jackson","Missouri":"Jefferson City","Montana":"Helena","Nebraska":"Lincoln","Nevada":"Carson City","New Hampshire":"Concord","New Jersey":"Trenton","New Mexico":"Santa Fe","New York":"Albany","North Carolina":"Raleigh","North Dakota":"Bismarck","Ohio":"Columbus","Oklahoma":"Oklahoma City","Oregon":"Salem","Pennsylvania":"Harrisburg","Rhode Island":"Providence","South Carolina":"Columbia","South Dakota":"Pierre","Tennessee":"Nashville","Texas":"Austin","Utah":"Salt Lake City","Vermont":"Montpelier","Virginia":"Richmond","Washington":"Olympia","West Virginia":"Charleston","Wisconsin":"Madison","Wyoming":"Cheyenne"
}


def ex_11_40(answers: dict[str, str]) -> tuple[int, dict[str, bool]]:
    results = {state: answers.get(state, "").strip().casefold() == capital.casefold() for state,capital in _STATE_CAPITALS.items()}
    return sum(results.values()), results


def ex_11_41() -> None:
    import tkinter as tk
    from tkinter import messagebox
    root=tk.Tk(); root.title("Sudoku"); entries=[[tk.Entry(root,width=2,justify="center",font=("Arial",18)) for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9): entries[r][c].grid(row=r,column=c,padx=(2 if c%3==0 else 0),pady=(2 if r%3==0 else 0))
    def solve() -> None:
        try: grid=[[int(entry.get() or "0") for entry in row] for row in entries]; answer=sudoku_solutions(grid,1)[0]
        except (ValueError,IndexError): messagebox.showerror("Sudoku","No solution"); return
        for r in range(9):
            for c in range(9): entries[r][c].delete(0,"end"); entries[r][c].insert(0,str(answer[r][c]))
    def clear() -> None:
        for row in entries:
            for entry in row: entry.delete(0,"end")
    tk.Button(root,text="Solve",command=solve).grid(row=9,column=2,columnspan=2); tk.Button(root,text="Clear",command=clear).grid(row=9,column=5,columnspan=2); root.mainloop()


def _plot_window(title: str, curves: Sequence[tuple[str, Callable[[float],float]]]) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title(title); canvas=tk.Canvas(root,width=500,height=350,bg="white"); canvas.pack(); canvas.create_line(20,175,480,175,arrow="last"); canvas.create_line(250,330,250,20,arrow="last")
    for color,function in curves:
        points=[]
        for pixel in range(20,481):
            x=(pixel-250)/70; points.extend((pixel,175-90*function(x)))
        canvas.create_line(*points,fill=color,width=2)
    root.mainloop()


def ex_11_42() -> None: _plot_window("Sine Function", (("blue",math.sin),))
def ex_11_43() -> None: _plot_window("Sine and Cosine Functions", (("blue",math.sin),("red",math.cos)))


def ex_11_44(points: Sequence[Point] | None = None) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Polygon"); canvas=tk.Canvas(root,width=520,height=360,bg="white"); canvas.pack(); data=points or ((80,280),(160,70),(280,40),(440,120),(400,300),(210,260)); canvas.create_polygon(*[value for point in data for value in point],fill="lightblue",outline="black"); root.mainloop()


def ex_11_45() -> None: _plot_window("Square Function", (("blue",lambda x: x*x/8),))


def ex_11_46() -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Stop Sign"); canvas=tk.Canvas(root,width=360,height=360,bg="white"); canvas.pack(); points=[]
    for index in range(8): angle=math.radians(22.5+index*45); points.extend((180+130*math.cos(angle),180+130*math.sin(angle)))
    canvas.create_polygon(*points,fill="red",outline="black",width=3); canvas.create_text(180,180,text="STOP",fill="white",font=("Arial",55,"bold")); root.mainloop()


def largest_square_block(matrix: Sequence[Sequence[int]]) -> tuple[int,int,int]:
    rows,columns=_rectangular(matrix); sizes=[[0]*columns for _ in range(rows)]; best=(0,0,0)
    for r in range(rows):
        for c in range(columns):
            if matrix[r][c]==1:
                sizes[r][c]=1 if r==0 or c==0 else 1+min(sizes[r-1][c],sizes[r][c-1],sizes[r-1][c-1])
                if sizes[r][c]>best[2]: best=(r-sizes[r][c]+1,c-sizes[r][c]+1,sizes[r][c])
    return best


def ex_11_47() -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Find Largest Block"); entries=[[tk.Entry(root,width=2,justify="center") for _ in range(10)] for _ in range(10)]
    for r in range(10):
        for c in range(10): entries[r][c].grid(row=r,column=c)
    def refresh() -> None:
        for row in entries:
            for entry in row: entry.delete(0,"end"); entry.insert(0,str(random.randrange(2))); entry.config(bg="white")
    def find() -> None:
        matrix=[[int(entry.get()) for entry in row] for row in entries]; top,left,size=largest_square_block(matrix)
        for r,row in enumerate(entries):
            for c,entry in enumerate(row): entry.config(bg="yellow" if top<=r<top+size and left<=c<left+size else "white")
    tk.Button(root,text="Refresh",command=refresh).grid(row=10,column=1,columnspan=3); tk.Button(root,text="Find Largest Block",command=find).grid(row=10,column=5,columnspan=4); refresh(); root.mainloop()


def ex_11_48() -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Bounding Rectangle"); canvas=tk.Canvas(root,width=600,height=420,bg="white"); canvas.pack(); points=[]
    def draw() -> None:
        canvas.delete("all")
        for x,y in points: canvas.create_oval(x-10,y-10,x+10,y+10,fill="blue")
        if points:
            xs=[p[0] for p in points]; ys=[p[1] for p in points]; canvas.create_rectangle(min(xs)-10,min(ys)-10,max(xs)+10,max(ys)+10,outline="red",width=2)
    def add(event: Any) -> None: points.append((event.x,event.y)); draw()
    def remove(event: Any) -> None:
        if points:
            index=min(range(len(points)),key=lambda i:math.hypot(points[i][0]-event.x,points[i][1]-event.y))
            if math.hypot(points[index][0]-event.x,points[index][1]-event.y)<=12: points.pop(index); draw()
    canvas.bind("<Button-1>",add); canvas.bind("<Button-2>",remove); canvas.bind("<Button-3>",remove); root.mainloop()


def ex_11_49() -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Tic-Tac-Toe"); labels=[[tk.Label(root,font=("Arial",50),width=2,height=1,relief="solid") for _ in range(3)] for _ in range(3)]
    def refresh() -> None:
        for row in labels:
            for label in row: label.config(text=random.choice("XO"))
    for r,row in enumerate(labels):
        for c,label in enumerate(row): label.grid(row=r,column=c)
    tk.Button(root,text="Refresh",command=refresh).grid(row=3,column=0,columnspan=3); refresh(); root.mainloop()


class NearestPointTracker:
    def __init__(self): self.points: list[tuple[float,float]]=[]; self.closest: tuple[tuple[float,float],tuple[float,float],float] | None=None
    def add(self, point: tuple[float,float]) -> None:
        for old in self.points:
            distance=math.dist(point,old)
            if self.closest is None or distance<self.closest[2]: self.closest=(old,point,distance)
        self.points.append(point)


def ex_11_50(points: Iterable[tuple[float,float]] = ()) -> NearestPointTracker:
    tracker=NearestPointTracker()
    for point in points: tracker.add(point)
    return tracker


def ex_11_51(students: Sequence[tuple[str,float]]) -> list[tuple[str,float]]:
    return sorted(students,key=lambda student:(student[1],student[0]))


def ex_11_52(square: Sequence[Sequence[str]]) -> bool:
    try: rows,columns=_rectangular(square)
    except ValueError: return False
    allowed={chr(ord("A")+index) for index in range(rows)}
    return rows==columns and all(set(row)==allowed for row in square) and all({square[row][column] for row in range(rows)}==allowed for column in range(columns))


EXERCISES: dict[str, Callable[..., Any]] = {f"11.{number}": globals()[f"ex_11_{number}"] for number in range(1, 53)}
