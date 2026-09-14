"""第 12 章编程题 12.1～12.22：继承和多态。"""

from __future__ import annotations

import datetime as dt
import math
import random
import tkinter as tk
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .chapter07 import Account
from .chapter08 import Circle2D, Rectangle2D
from .chapter11 import ConnectFour, TicTacToe


class GeometricObject:
    def __init__(self, color: str = "green", filled: bool = True):
        self.__color = color; self.__filled = filled; self.__date_created = dt.datetime.now()
    def getColor(self) -> str: return self.__color
    def setColor(self, color: str) -> None: self.__color = color
    def isFilled(self) -> bool: return self.__filled
    def setFilled(self, filled: bool) -> None: self.__filled = bool(filled)
    def getDateCreated(self) -> dt.datetime: return self.__date_created
    def __str__(self) -> str: return f"created on {self.__date_created.isoformat()}, color: {self.__color}, filled: {self.__filled}"


class Triangle(GeometricObject):
    def __init__(self, side1: float = 1.0, side2: float = 1.0, side3: float = 1.0, color: str = "green", filled: bool = True):
        if min(side1,side2,side3) <= 0: raise ValueError("sides must be positive")
        super().__init__(color,filled); self.__side1=side1; self.__side2=side2; self.__side3=side3
    def getSide1(self) -> float: return self.__side1
    def getSide2(self) -> float: return self.__side2
    def getSide3(self) -> float: return self.__side3
    def getPerimeter(self) -> float: return self.__side1+self.__side2+self.__side3
    def getArea(self) -> float:
        s=self.getPerimeter()/2; return math.sqrt(max(0,s*(s-self.__side1)*(s-self.__side2)*(s-self.__side3)))
    def __str__(self) -> str: return f"Triangle: side1 = {self.__side1:g} side2 = {self.__side2:g} side3 = {self.__side3:g}"


def ex_12_1(side1: float = 1, side2: float = 1, side3: float = 1, color: str = "green", filled: bool = True) -> Triangle:
    return Triangle(side1,side2,side3,color,filled)


@dataclass(frozen=True)
class Location:
    row: int
    column: int
    maxValue: float


def ex_12_2(matrix: Sequence[Sequence[float]]) -> Location:
    if not matrix or not matrix[0] or any(len(row)!=len(matrix[0]) for row in matrix): raise ValueError("a nonempty rectangular matrix is required")
    row,column=max(((r,c) for r in range(len(matrix)) for c in range(len(matrix[0]))),key=lambda item:matrix[item[0]][item[1]])
    return Location(row,column,matrix[row][column])


class ATM:
    def __init__(self, count: int = 10, initial_balance: float = 100):
        self.accounts=[Account(identifier,initial_balance) for identifier in range(count)]
    def account(self, identifier: int) -> Account:
        if not 0 <= identifier < len(self.accounts): raise ValueError("invalid account id")
        return self.accounts[identifier]
    def transact(self, identifier: int, action: str, amount: float = 0) -> float:
        account=self.account(identifier)
        if action=="balance": return account.getBalance()
        if action=="withdraw": account.withdraw(amount)
        elif action=="deposit": account.deposit(amount)
        else: raise ValueError("action must be balance, withdraw or deposit")
        return account.getBalance()


def ex_12_3() -> ATM:
    return ATM()


def ex_12_4(points: Sequence[Sequence[float]]) -> Rectangle2D:
    if not points or any(len(point)!=2 for point in points): raise ValueError("2D points are required")
    xs=[point[0] for point in points]; ys=[point[1] for point in points]
    return Rectangle2D((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,max(xs)-min(xs),max(ys)-min(ys))


def ex_12_5() -> None:
    root=tk.Tk(); root.title("Tic-Tac-Toe"); game=TicTacToe(); status=tk.StringVar(value="X's turn")
    class Cell(tk.Label):
        def __init__(self,parent: Any,row: int,column: int):
            super().__init__(parent,text="",font=("Arial",55),width=2,height=1,relief="solid"); self.row=row; self.column=column; self.bind("<Button-1>",self.click)
        def click(self,_event: Any) -> None:
            try: token=game.play(self.row,self.column)
            except (ValueError,RuntimeError): return
            self.config(text=token)
            status.set(f"{game.winner} won! The game is over" if game.winner else "Draw! The game is over" if game.full else f"{game.turn}'s turn")
    for row in range(3):
        for column in range(3): Cell(root,row,column).grid(row=row,column=column)
    tk.Label(root,textvariable=status).grid(row=3,column=0,columnspan=3); root.mainloop()


def _draggable_shapes(kind: str, editable: bool) -> None:
    root=tk.Tk(); root.title("Two Circles" if kind=="circle" else "Two Rectangles"); canvas=tk.Canvas(root,width=600,height=320,bg="white"); canvas.pack(); centers=[[180,150],[390,170]]; sizes=[[60,60],[70,70]] if kind=="circle" else [[130,80],[100,100]]; selected=[-1]; status=tk.StringVar(); tk.Label(root,textvariable=status).pack()
    entries=[]
    if editable:
        form=tk.Frame(root); form.pack()
        labels=("Center x","Center y","Radius") if kind=="circle" else ("Center x","Center y","Width","Height")
        for shape in range(2):
            row=[]
            for index,label in enumerate(labels): tk.Label(form,text=f"{shape+1} {label}").grid(row=index,column=shape*2); entry=tk.Entry(form,width=8); entry.grid(row=index,column=shape*2+1); row.append(entry)
            entries.append(row)
    def intersects() -> bool:
        if kind=="circle": return math.dist(centers[0],centers[1]) <= sizes[0][0]+sizes[1][0]
        return abs(centers[0][0]-centers[1][0]) <= (sizes[0][0]+sizes[1][0])/2 and abs(centers[0][1]-centers[1][1]) <= (sizes[0][1]+sizes[1][1])/2
    def draw() -> None:
        canvas.delete("all")
        for index,((x,y),(width,height)) in enumerate(zip(centers,sizes)):
            if kind=="circle": box=(x-width,y-width,x+width,y+width)
            else: box=(x-width/2,y-height/2,x+width/2,y+height/2)
            (canvas.create_oval if kind=="circle" else canvas.create_rectangle)(*box,outline=("blue","red")[index],width=3); canvas.create_text(x,y,text=f"{kind[0].upper()}{index+1}")
            if editable:
                values=(x,y,width) if kind=="circle" else (x,y,width,height)
                for entry,value in zip(entries[index],values): entry.delete(0,"end"); entry.insert(0,f"{value:g}")
        status.set(f"Two {kind}s {'intersect' if intersects() else 'do not intersect'}")
    def press(event: Any) -> None:
        selected[0]=next((index for index,((x,y),(w,h)) in enumerate(zip(centers,sizes)) if (math.hypot(event.x-x,event.y-y)<=w if kind=="circle" else abs(event.x-x)<=w/2 and abs(event.y-y)<=h/2)),-1)
    def drag(event: Any) -> None:
        if selected[0]>=0: centers[selected[0]][:]=[event.x,event.y]; draw()
    def redraw() -> None:
        try:
            for index,row in enumerate(entries):
                values=list(map(float,(entry.get() for entry in row))); centers[index][:]=values[:2]; sizes[index][:]=([values[2],values[2]] if kind=="circle" else values[2:])
            draw()
        except ValueError: status.set("Enter valid numbers")
    canvas.bind("<Button-1>",press); canvas.bind("<B1-Motion>",drag)
    if editable: tk.Button(root,text=f"Redraw {kind.title()}s",command=redraw).pack()
    draw(); root.mainloop()


def ex_12_6() -> None: _draggable_shapes("circle",False)
def ex_12_7() -> None: _draggable_shapes("rectangle",False)
def ex_12_8() -> None: _draggable_shapes("circle",True)
def ex_12_9() -> None: _draggable_shapes("rectangle",True)


def ex_12_10() -> None:
    root=tk.Tk(); root.title("Racing Cars"); canvas=tk.Canvas(root,width=750,height=330,bg="white"); canvas.pack(); positions=[0.0]*4; speeds=[random.uniform(2,7) for _ in range(4)]
    def animate() -> None:
        canvas.delete("all")
        for lane in range(4):
            y=45+lane*70; canvas.create_line(0,y+28,750,y+28); x=positions[lane]; canvas.create_rectangle(x,y,x+58,y+25,fill=("red","blue","green","orange")[lane]); canvas.create_oval(x+7,y+19,x+22,y+34,fill="black"); canvas.create_oval(x+40,y+19,x+55,y+34,fill="black"); positions[lane]=(x+speeds[lane])%750
        root.after(30,animate)
    animate(); root.mainloop()


def ex_12_11() -> None:
    from tkinter import messagebox
    root=tk.Tk(); root.title("Guess Birthday"); variables=[tk.BooleanVar() for _ in range(5)]; sets=[]
    for bit in range(5): sets.append([day for day in range(1,32) if day & (1<<bit)])
    for column,(variable,days) in enumerate(zip(variables,sets)): tk.Checkbutton(root,text="\n".join(" ".join(map(str,days[row:row+4])) for row in range(0,len(days),4)),variable=variable).grid(row=0,column=column)
    tk.Button(root,text="Guess Birthday",command=lambda:messagebox.showinfo("Birthday",f"Your birthday is {sum((1<<bit) for bit,var in enumerate(variables) if var.get())}")).grid(row=1,column=0,columnspan=5); root.mainloop()


def _draw_clock(canvas: tk.Canvas, hour: int, minute: int, second: int) -> None:
    cx=cy=100; radius=75; canvas.create_oval(cx-radius,cy-radius,cx+radius,cy+radius)
    for value,period,length,width in ((hour%12+minute/60,12,45,4),(minute+second/60,60,62,3),(second,60,67,1)):
        angle=math.radians(90-value/period*360); canvas.create_line(cx,cy,cx+length*math.cos(angle),cy-length*math.sin(angle),width=width)
    canvas.create_text(cx,190,text=f"{hour:02d}:{minute:02d}:{second:02d}")


def ex_12_12() -> None:
    root=tk.Tk(); root.title("Display Clocks"); now=dt.datetime.now()
    for index in range(4): canvas=tk.Canvas(root,width=200,height=210,bg="white"); canvas.grid(row=0,column=index); _draw_clock(canvas,(now.hour+index*3)%24,now.minute,now.second)
    root.mainloop()


def ex_12_13() -> None:
    from tkinter import messagebox
    root=tk.Tk(); root.title("Connect Four"); game=[ConnectFour()]; canvas=tk.Canvas(root,width=490,height=420,bg="navy"); canvas.pack()
    def draw() -> None:
        canvas.delete("all")
        for r in range(6):
            for c in range(7): canvas.create_oval(c*70+8,r*70+8,c*70+62,r*70+62,fill={" ":"white","R":"red","Y":"yellow"}[game[0].board[r][c]])
    def click(event: Any) -> None:
        try: game[0].drop(event.x//70)
        except (ValueError,RuntimeError,IndexError): return
        draw()
        if game[0].winner: messagebox.showinfo("Game",f"{game[0].winner} won")
        elif game[0].full: messagebox.showinfo("Game","Draw")
    def reset() -> None: game[0]=ConnectFour(); draw()
    canvas.bind("<Button-1>",click); tk.Button(root,text="Start Over",command=reset).pack(); draw(); root.mainloop()


COUNT_LIMIT=60
def mandelbrot_iterations(c: complex, limit: int = COUNT_LIMIT, z: complex = 0j) -> int:
    for iteration in range(limit):
        z=z*z+c
        if abs(z)>2: return iteration
    return limit


def _fractal_window(julia: bool) -> None:
    root=tk.Tk(); root.title("Julia Set" if julia else "Mandelbrot Fractal"); canvas=tk.Canvas(root,width=400,height=400,bg="black"); canvas.pack()
    for px in range(0,400,2):
        for py in range(0,400,2):
            point=complex(px/100-2,py/100-2); count=mandelbrot_iterations(complex(-.3,.6),z=point) if julia else mandelbrot_iterations(point); color="red" if count==COUNT_LIMIT else f"#{count*4:02x}{(60-count)*3:02x}80"; canvas.create_rectangle(px,py,px+2,py+2,outline=color,fill=color)
    root.mainloop()


def ex_12_14(c: complex | None = None) -> int | None:
    if c is not None: return mandelbrot_iterations(c)
    _fractal_window(False); return None


def ex_12_15(z: complex | None = None, c: complex = complex(-.3,.6)) -> int | None:
    if z is not None: return mandelbrot_iterations(c,z=z)
    _fractal_window(True); return None


class Stack(list):
    def push(self,value: Any) -> None: self.append(value)
    def peek(self) -> Any:
        if not self: raise IndexError("peek from empty stack")
        return self[-1]
    def isEmpty(self) -> bool: return not self
    def getSize(self) -> int: return len(self)


def ex_12_16(values: Iterable[Any] = ()) -> Stack:
    stack=Stack(); stack.extend(values); return stack


def solve_24(cards: Sequence[int]) -> str | None:
    if len(cards)!=4 or any(type(card)is not int or not 1<=card<=13 for card in cards): raise ValueError("four integer card values from 1 to 13 are required")
    def search(items: list[tuple[Fraction,str]]) -> str | None:
        if len(items)==1: return items[0][1] if items[0][0]==24 else None
        for first in range(len(items)):
            for second in range(first+1,len(items)):
                a,sa=items[first]; b,sb=items[second]; remaining=[item for index,item in enumerate(items) if index not in (first,second)]
                candidates=[(a+b,f"({sa}+{sb})"),(a-b,f"({sa}-{sb})"),(b-a,f"({sb}-{sa})"),(a*b,f"({sa}*{sb})")]
                if b: candidates.append((a/b,f"({sa}/{sb})"))
                if a: candidates.append((b/a,f"({sb}/{sa})"))
                for value,expression in candidates:
                    result=search(remaining+[(value,expression)])
                    if result: return result
        return None
    return search([(Fraction(card),str(card)) for card in cards])


def ex_12_17() -> None:
    root=tk.Tk(); root.title("24-Point Game"); cards=[1]*4; shown=tk.StringVar(); answer=tk.StringVar()
    tk.Label(root,textvariable=shown,font=("Arial",30)).pack(); tk.Label(root,textvariable=answer,font=("Arial",18)).pack()
    def refresh() -> None: cards[:]=[random.randint(1,13) for _ in range(4)]; shown.set("  ".join(map(str,cards))); answer.set(solve_24(cards) or "No solution")
    tk.Button(root,text="Refresh / Solve",command=refresh).pack(); refresh(); root.mainloop()


class BarChart(tk.Canvas):
    def __init__(self,parent: Any,data: Sequence[Sequence[Any]],width: int=400,height: int=300): super().__init__(parent,width=width,height=height,bg="white"); self.data=data; self.bind("<Configure>",self._draw); self.after_idle(self._draw)
    def _draw(self,_event: Any=None) -> None:
        self.delete("all"); width=max(self.winfo_width(),1); height=max(self.winfo_height(),1); maximum=max((row[0] for row in self.data),default=1); bar=width/max(len(self.data),1)
        for index,(value,label,color) in enumerate(self.data): x1=index*bar+10; x2=(index+1)*bar-10; y1=height-35-value/maximum*(height-60); self.create_rectangle(x1,y1,x2,height-35,fill=color); self.create_text((x1+x2)/2,height-15,text=label)


def ex_12_18() -> None:
    root=tk.Tk(); root.title("BarChart Reusable Class"); BarChart(root,((40,"CS","red"),(30,"IS","blue"),(50,"IT","yellow"))).pack(side="left"); BarChart(root,((140,"Freshman","red"),(130,"Sophomore","blue"),(150,"Junior","yellow"),(80,"Senior","green"))).pack(side="left"); root.mainloop()


class PieChart(tk.Canvas):
    def __init__(self,parent: Any,data: Sequence[Sequence[Any]],width: int=400,height: int=300): super().__init__(parent,width=width,height=height,bg="white"); self.data=data; self.bind("<Configure>",self._draw); self.after_idle(self._draw)
    def _draw(self,_event: Any=None) -> None:
        self.delete("all"); total=sum(row[0] for row in self.data) or 1; start=0; size=min(self.winfo_width(),self.winfo_height())-60
        for value,label,color in self.data: extent=value/total*360; self.create_arc(20,20,20+size,20+size,start=start,extent=extent,fill=color); self.create_text(30+size,(start/360*size)%max(size,1)+20,text=label,anchor="w"); start+=extent


def ex_12_19() -> None:
    root=tk.Tk(); root.title("Pie Chart"); PieChart(root,((40,"CS","red"),(30,"IS","blue"),(50,"IT","yellow"))).pack(side="left"); PieChart(root,((140,"Freshman","red"),(130,"Sophomore","blue"),(150,"Junior","yellow"),(80,"Senior","green"))).pack(side="left"); root.mainloop()


class RegularPolygonCanvas(tk.Canvas):
    def __init__(self,parent: Any,numberOfSides: int=5,**kwargs: Any): super().__init__(parent,**kwargs); self.numberOfSides=max(3,numberOfSides); self.bind("<Configure>",self.draw); self.after_idle(self.draw)
    def setNumberOfSides(self,value: int) -> None: self.numberOfSides=max(3,value); self.draw()
    def draw(self,_event: Any=None) -> None:
        self.delete("all"); cx,cy=self.winfo_width()/2,self.winfo_height()/2; radius=.4*min(self.winfo_width(),self.winfo_height()); points=[]
        for index in range(self.numberOfSides): angle=math.radians(-90+index*360/self.numberOfSides); points.extend((cx+radius*math.cos(angle),cy+radius*math.sin(angle)))
        self.create_polygon(*points,fill="",outline="black",width=2)


def ex_12_20() -> None:
    root=tk.Tk(); root.title("Regular Polygons")
    for index,sides in enumerate(range(5,11)): RegularPolygonCanvas(root,sides,width=180,height=180,bg="white").grid(row=index//3,column=index%3)
    root.mainloop()


def ex_12_21() -> None:
    root=tk.Tk(); root.title("n-sided Polygon"); canvas=RegularPolygonCanvas(root,5,width=480,height=360,bg="white"); canvas.pack()
    def change(delta: int) -> None: canvas.setNumberOfSides(canvas.numberOfSides+delta)
    tk.Button(root,text="+1",command=lambda:change(1)).pack(side="left"); tk.Button(root,text="-1",command=lambda:change(-1)).pack(side="left"); root.bind("<Up>",lambda _e:change(1)); root.bind("<Down>",lambda _e:change(-1)); canvas.bind("<Button-1>",lambda _e:change(1)); canvas.bind("<Button-3>",lambda _e:change(-1)); root.mainloop()


class CoinCell(tk.Label):
    def __init__(self,parent: Any): super().__init__(parent,text="H",font=("Arial",35),width=2,height=1,relief="solid"); self.bind("<Button-1>",self.flip)
    def flip(self,_event: Any=None) -> None: self.config(text="T" if self.cget("text")=="H" else "H")


def ex_12_22() -> None:
    root=tk.Tk(); root.title("Flip Coin")
    for row in range(3):
        for column in range(3): CoinCell(root).grid(row=row,column=column)
    root.mainloop()


EXERCISES: dict[str, Callable[..., Any]]={f"12.{number}":globals()[f"ex_12_{number}"] for number in range(1,23)}
