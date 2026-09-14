"""第 15 章编程题 15.1～15.36：递归。"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

from .chapter10 import ex_10_20


def ex_15_1(number: int) -> int:
    number=abs(number)
    return number if number<10 else number%10+ex_15_1(number//10)


def ex_15_2(number: int) -> int:
    if number<0: raise ValueError("number cannot be negative")
    if number<2: return number
    previous,current=0,1
    for _ in range(2,number+1): previous,current=current,previous+current
    return current


def ex_15_3(first: int,second: int) -> int:
    first,second=abs(first),abs(second)
    if second==0: return first
    return ex_15_3(second,first%second)


def ex_15_4(index: int) -> float:
    if index<1: raise ValueError("index must be positive")
    return 1.0 if index==1 else ex_15_4(index-1)+1/index


def ex_15_5(index: int) -> float:
    if index<1: raise ValueError("index must be positive")
    return 1/3 if index==1 else ex_15_5(index-1)+index/(2*index+1)


def ex_15_6(index: int) -> float:
    if index<1: raise ValueError("index must be positive")
    return 1/2 if index==1 else ex_15_6(index-1)+index/(index+1)


def ex_15_7(number: int) -> tuple[int,int]:
    if number<0: raise ValueError("number cannot be negative")
    calls=[0]
    def fib(n: int) -> int:
        calls[0]+=1
        return n if n<2 else fib(n-1)+fib(n-2)
    return fib(number),calls[0]


def ex_15_8(value: int) -> str:
    sign="-" if value<0 else ""; number=abs(value)
    def reverse(n: int) -> str: return str(n) if n<10 else str(n%10)+reverse(n//10)
    return sign+reverse(number)


def ex_15_9(value: str) -> str:
    return value if len(value)<2 else value[-1]+ex_15_9(value[:-1])


def ex_15_10(text: str,character: str) -> int:
    if len(character)!=1: raise ValueError("character must have length one")
    return 0 if not text else (text[0]==character)+ex_15_10(text[1:],character)


def reverseDisplayHelper(text: str,high: int) -> str:
    return "" if high<0 else text[high]+reverseDisplayHelper(text,high-1)


def ex_15_11(text: str) -> str:
    return reverseDisplayHelper(text,len(text)-1)


def ex_15_12(values: Sequence[float]) -> float:
    if not values: raise ValueError("values cannot be empty")
    def maximum(high: int) -> float: return values[0] if high==0 else max(values[high],maximum(high-1))
    return maximum(len(values)-1)


def countUppercaseHelper(text: str,high: int) -> int:
    return 0 if high<0 else text[high].isupper()+countUppercaseHelper(text,high-1)


def ex_15_13(text: str) -> int:
    return countUppercaseHelper(text,len(text)-1)


def countHelper(text: str,character: str,high: int) -> int:
    return 0 if high<0 else (text[high]==character)+countHelper(text,character,high-1)


def ex_15_14(text: str,character: str) -> int:
    if len(character)!=1: raise ValueError("character must have length one")
    return countHelper(text,character,len(text)-1)


def _uppercase_list_helper(characters: Sequence[str],high: int) -> int:
    return 0 if high<0 else characters[high].isupper()+_uppercase_list_helper(characters,high-1)


def ex_15_15(characters: Sequence[str]) -> int:
    return _uppercase_list_helper(characters,len(characters)-1)


def _list_count_helper(characters: Sequence[str],character: str,high: int) -> int:
    return 0 if high<0 else (characters[high]==character)+_list_count_helper(characters,character,high-1)


def ex_15_16(characters: Sequence[str],character: str) -> int:
    return _list_count_helper(characters,character,len(characters)-1)


def sierpinski_triangles(order: int,points: tuple[tuple[float,float],tuple[float,float],tuple[float,float]]) -> list[tuple[tuple[float,float],tuple[float,float],tuple[float,float]]]:
    if order<0: raise ValueError("order cannot be negative")
    if order==0: return [points]
    a,b,c=points; ab=((a[0]+b[0])/2,(a[1]+b[1])/2); ac=((a[0]+c[0])/2,(a[1]+c[1])/2); bc=((b[0]+c[0])/2,(b[1]+c[1])/2)
    return sierpinski_triangles(order-1,(a,ab,ac))+sierpinski_triangles(order-1,(ab,b,bc))+sierpinski_triangles(order-1,(ac,bc,c))


def _sierpinski_window(interactive: bool,filled: bool,initial: int=0) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Sierpinski Triangle"); canvas=tk.Canvas(root,width=600,height=500,bg="white"); canvas.pack(); order=[initial]
    def draw() -> None:
        canvas.delete("all")
        for triangle in sierpinski_triangles(order[0],((300,30),(40,460),(560,460))): canvas.create_polygon(*[v for p in triangle for v in p],fill="blue" if filled else "",outline="black")
        canvas.create_text(50,20,text=f"order {order[0]}")
    if interactive:
        def change(delta: int) -> None: order[0]=max(0,order[0]+delta); draw()
        canvas.bind("<Button-1>",lambda _e:change(1)); canvas.bind("<Button-3>",lambda _e:change(-1))
    draw(); root.mainloop()


def ex_15_17(initial_order: int=0) -> None: _sierpinski_window(True,False,initial_order)


def ex_15_18(disks: int) -> int:
    if disks<0: raise ValueError("disks cannot be negative")
    return 0 if disks==0 else 2*ex_15_18(disks-1)+1


def ex_15_19(value: int) -> str:
    if value<0: return "-"+ex_15_19(-value)
    return str(value) if value<2 else ex_15_19(value//2)+str(value%2)


_HEX="0123456789ABCDEF"
def ex_15_20(value: int) -> str:
    if value<0: return "-"+ex_15_20(-value)
    return _HEX[value] if value<16 else ex_15_20(value//16)+_HEX[value%16]


def ex_15_21(binary_string: str) -> int:
    if not binary_string or any(character not in "01" for character in binary_string): raise ValueError("invalid binary string")
    return int(binary_string) if len(binary_string)==1 else 2*ex_15_21(binary_string[:-1])+int(binary_string[-1])


def ex_15_22(hex_string: str) -> int:
    text=hex_string.upper()
    if not text or any(character not in _HEX for character in text): raise ValueError("invalid hexadecimal string")
    return _HEX.index(text) if len(text)==1 else 16*ex_15_22(text[:-1])+_HEX.index(text[-1])


def ex_15_23(text: str) -> list[str]:
    result=[]
    def permute(prefix: str,remainder: str) -> None:
        if not remainder: result.append(prefix); return
        for index,character in enumerate(remainder): permute(prefix+character,remainder[:index]+remainder[index+1:])
    permute("",text); return result


def ex_15_24(directory: str | Path) -> int:
    path=Path(directory)
    if not path.is_dir(): raise NotADirectoryError(path)
    def count(current: Path) -> int:
        total=0
        for child in current.iterdir(): total+=count(child) if child.is_dir() else child.is_file()
        return total
    return count(path)


def koch_points(order: int,start: complex,end: complex) -> list[complex]:
    if order<0: raise ValueError("order cannot be negative")
    if order==0: return [start,end]
    vector=(end-start)/3; first=start+vector; second=end-vector; peak=first+vector*complex(.5,-math.sqrt(3)/2)
    sections=((start,first),(first,peak),(peak,second),(second,end)); result=[]
    for a,b in sections: result.extend(koch_points(order-1,a,b)[:-1])
    result.append(end); return result


def _koch_snowflake(order: int) -> list[complex]:
    vertices=(complex(300,40),complex(50,450),complex(550,450)); points=[]
    for start,end in zip(vertices,vertices[1:]+vertices[:1]): points.extend(koch_points(order,start,end)[:-1])
    points.append(vertices[0]); return points


def ex_15_25(order: int=2) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Koch Snowflake"); canvas=tk.Canvas(root,width=600,height=500,bg="white"); canvas.pack(); points=_koch_snowflake(order); canvas.create_line(*[coordinate for point in points for coordinate in (point.real,point.imag)]); root.mainloop()


def ex_15_26(order: int=2) -> None:
    import turtle
    points=_koch_snowflake(order); pen=turtle.Turtle(); pen.hideturtle(); pen.speed(0); pen.penup(); pen.goto(points[0].real-300,250-points[0].imag); pen.pendown()
    for point in points[1:]: pen.goto(point.real-300,250-point.imag)
    turtle.done()


def ex_15_27() -> list[tuple[int,...]]:
    return ex_10_20()


def ex_15_28(directory: str | Path,word: str) -> int:
    path=Path(directory)
    if not path.is_dir(): raise NotADirectoryError(path)
    def count(current: Path) -> int:
        total=0
        for child in current.iterdir():
            if child.is_dir(): total+=count(child)
            elif child.is_file():
                try: total+=child.read_text(encoding="utf-8").count(word)
                except (UnicodeDecodeError,OSError): pass
        return total
    return count(path)


def h_tree_lines(order: int,x: float,y: float,size: float) -> list[tuple[float,float,float,float]]:
    if order<0: raise ValueError("order cannot be negative")
    half=size/2; lines=[(x-half,y-half,x-half,y+half),(x+half,y-half,x+half,y+half),(x-half,y,x+half,y)]
    if order:
        for cx in (x-half,x+half):
            for cy in (y-half,y+half): lines.extend(h_tree_lines(order-1,cx,cy,size/2))
    return lines


def ex_15_29(order: int=2) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("H-Tree Fractal"); canvas=tk.Canvas(root,width=600,height=600,bg="white"); canvas.pack()
    for line in h_tree_lines(order,300,300,280): canvas.create_line(*line)
    root.mainloop()


def ex_15_30(order: int=2) -> None:
    import turtle
    pen=turtle.Turtle(); pen.hideturtle(); pen.speed(0)
    for x1,y1,x2,y2 in h_tree_lines(order,0,0,280): pen.penup(); pen.goto(x1,y1); pen.pendown(); pen.goto(x2,y2)
    turtle.done()


def recursive_tree_lines(depth: int,x: float,y: float,length: float,angle: float=90) -> list[tuple[float,float,float,float]]:
    if depth<0: raise ValueError("depth cannot be negative")
    end=(x+length*math.cos(math.radians(angle)),y-length*math.sin(math.radians(angle))); line=(x,y,end[0],end[1])
    return [line] if depth==0 else [line]+recursive_tree_lines(depth-1,*end,length*.72,angle+35)+recursive_tree_lines(depth-1,*end,length*.72,angle-35)


def ex_15_31(depth: int=8) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Recursive Tree"); canvas=tk.Canvas(root,width=700,height=600,bg="white"); canvas.pack()
    for line in recursive_tree_lines(depth,350,580,130): canvas.create_line(*line)
    root.mainloop()


def ex_15_32(depth: int=8) -> None:
    import turtle
    pen=turtle.Turtle(); pen.hideturtle(); pen.speed(0)
    for x1,y1,x2,y2 in recursive_tree_lines(depth,0,-280,130): pen.penup(); pen.goto(x1,y1); pen.pendown(); pen.goto(x2,y2)
    turtle.done()


def hilbert_points(order: int,step: float=10) -> list[tuple[float,float]]:
    if order<1: raise ValueError("order must be positive")
    position=[0.0,0.0]; angle=[0]; points=[tuple(position)]
    def move() -> None:
        radians=math.radians(angle[0]); position[0]+=step*math.cos(radians); position[1]+=step*math.sin(radians); points.append(tuple(position))
    def hilbert(level: int,turn: int) -> None:
        if level==0: return
        angle[0]+=turn*90; hilbert(level-1,-turn); move(); angle[0]-=turn*90; hilbert(level-1,turn); move(); hilbert(level-1,turn); angle[0]-=turn*90; move(); hilbert(level-1,-turn); angle[0]+=turn*90
    hilbert(order,1); return points


def ex_15_33(order: int=4) -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Hilbert Curve"); canvas=tk.Canvas(root,width=600,height=600,bg="white"); canvas.pack(); scale=520/(2**order-1); points=hilbert_points(order,scale); xs=[p[0] for p in points]; ys=[p[1] for p in points]; canvas.create_line(*[value for x,y in points for value in (40+x-min(xs),40+y-min(ys))]); root.mainloop()


def ex_15_34(order: int=4) -> None:
    import turtle
    points=hilbert_points(order,500/(2**order-1)); xs=[p[0] for p in points]; ys=[p[1] for p in points]; pen=turtle.Turtle(); pen.hideturtle(); pen.speed(0); pen.penup(); pen.goto(points[0][0]-(min(xs)+max(xs))/2,points[0][1]-(min(ys)+max(ys))/2); pen.pendown()
    for x,y in points[1:]: pen.goto(x-(min(xs)+max(xs))/2,y-(min(ys)+max(ys))/2)
    turtle.done()


def ex_15_35(order: int=4) -> None: _sierpinski_window(False,True,order)


def ex_15_36(order: int=4) -> None:
    import turtle
    pen=turtle.Turtle(); pen.hideturtle(); pen.speed(0)
    for triangle in sierpinski_triangles(order,((0,250),(-280,-230),(280,-230))):
        pen.penup(); pen.goto(triangle[0]); pen.pendown(); pen.goto(triangle[1]); pen.goto(triangle[2]); pen.goto(triangle[0])
    turtle.done()


EXERCISES: dict[str,Callable[...,Any]]={f"15.{number}":globals()[f"ex_15_{number}"] for number in range(1,37)}
