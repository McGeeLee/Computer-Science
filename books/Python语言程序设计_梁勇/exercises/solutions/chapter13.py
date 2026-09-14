"""第 13 章编程题 13.1～13.17：文件和异常处理。"""

from __future__ import annotations

import pickle
import random
import re
import urllib.request
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Union

from .chapter10 import HangmanRound
from .chapter12 import Triangle


PathLike = Union[str, Path]


def _read_text(path: PathLike) -> str:
    return Path(path).read_text(encoding="utf-8")


def _write_text(path: PathLike, text: str) -> None:
    Path(path).write_text(text,encoding="utf-8")


def ex_13_1(path: PathLike, target: str) -> int:
    text=_read_text(path); count=text.count(target); _write_text(path,text.replace(target,"")); return count


def ex_13_2(path: PathLike) -> tuple[int,int,int]:
    text=_read_text(path); return len(text),len(text.split()),len(text.splitlines())


def ex_13_3(path: PathLike) -> tuple[int,float,float]:
    scores=[float(token) for token in _read_text(path).split()]
    if not scores: raise ValueError("the file contains no scores")
    total=sum(scores); return len(scores),total,total/len(scores)


def ex_13_4(path: PathLike, count: int=100, seed: int | None=None) -> list[int]:
    target=Path(path)
    if target.exists(): raise FileExistsError(target)
    generator=random.Random(seed); numbers=[generator.randrange(1000) for _ in range(count)]; _write_text(target," ".join(map(str,numbers))); return sorted(map(int,_read_text(target).split()))


def ex_13_5(path: PathLike, old: str, new: str) -> int:
    text=_read_text(path); count=text.count(old); _write_text(path,text.replace(old,new)); return count


def _url_text(url: str, timeout: float=15) -> str:
    with urllib.request.urlopen(url,timeout=timeout) as response: return response.read().decode(response.headers.get_content_charset() or "utf-8")


def ex_13_6(url: str="https://liveexample.pearsoncmg.com/data/Lincoln.txt") -> int:
    return len(_url_text(url).split())


def ex_13_7(path: PathLike, seed: int | None=None) -> HangmanRound:
    words=_read_text(path).split()
    if not words: raise ValueError("word file is empty")
    return HangmanRound(random.Random(seed).choice(words).lower())


def ex_13_8(input_path: PathLike, output_path: PathLike) -> int:
    data=Path(input_path).read_bytes(); encrypted=bytes((byte+5)%256 for byte in data); Path(output_path).write_bytes(encrypted); return len(encrypted)


def ex_13_9(input_path: PathLike, output_path: PathLike) -> int:
    data=Path(input_path).read_bytes(); decrypted=bytes((byte-5)%256 for byte in data); Path(output_path).write_bytes(decrypted); return len(decrypted)


class Rational(Fraction):
    def __new__(cls,numerator: int=0,denominator: int=1):
        if denominator==0: raise RuntimeError("denominator cannot be zero")
        return super().__new__(cls,numerator,denominator)


def ex_13_10(numerator: int=0, denominator: int=1) -> Rational:
    return Rational(numerator,denominator)


def _valid_triangle(side1: float,side2: float,side3: float) -> bool:
    return min(side1,side2,side3)>0 and side1+side2>side3 and side1+side3>side2 and side2+side3>side1


class ValidatedTriangle(Triangle):
    def __init__(self,side1: float=1,side2: float=1,side3: float=1,**kwargs: Any):
        if not _valid_triangle(side1,side2,side3): raise RuntimeError("the sides cannot form a triangle")
        super().__init__(side1,side2,side3,**kwargs)


def ex_13_11(side1: float=1,side2: float=1,side3: float=1) -> ValidatedTriangle:
    return ValidatedTriangle(side1,side2,side3)


class TriangleError(RuntimeError):
    def __init__(self,side1: float,side2: float,side3: float):
        self.__side1=side1; self.__side2=side2; self.__side3=side3; super().__init__(f"invalid triangle sides: {side1}, {side2}, {side3}")
    def getSide1(self) -> float: return self.__side1
    def getSide2(self) -> float: return self.__side2
    def getSide3(self) -> float: return self.__side3


class StrictTriangle(Triangle):
    def __init__(self,side1: float=1,side2: float=1,side3: float=1,**kwargs: Any):
        if not _valid_triangle(side1,side2,side3): raise TriangleError(side1,side2,side3)
        super().__init__(side1,side2,side3,**kwargs)


def ex_13_12(side1: float=1,side2: float=1,side3: float=1) -> StrictTriangle:
    return StrictTriangle(side1,side2,side3)


@dataclass(frozen=True)
class GraphData:
    points: dict[int,tuple[float,float]]
    edges: set[tuple[int,int]]


def parse_graph(text: str) -> GraphData:
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    if not lines: raise ValueError("empty graph")
    count=int(lines[0]); points={}; edges=set()
    if len(lines)-1<count: raise ValueError("not enough vertex rows")
    for line in lines[1:count+1]:
        parts=line.split(); vertex=int(parts[0]); points[vertex]=(float(parts[1]),float(parts[2]))
        for neighbor in map(int,parts[3:]): edges.add(tuple(sorted((vertex,neighbor))))
    if set(points)!=set(range(count)): raise ValueError("vertices must be numbered 0 through n-1")
    if any(first not in points or second not in points for first,second in edges): raise ValueError("edge references an unknown vertex")
    return GraphData(points,edges)


def read_graph(path: PathLike) -> GraphData:
    return parse_graph(_read_text(path))


def _display_graph(graph: GraphData,title: str="Display a Graph") -> None:
    import tkinter as tk
    root=tk.Tk(); root.title(title); canvas=tk.Canvas(root,width=600,height=450,bg="white"); canvas.pack(); xs=[p[0] for p in graph.points.values()]; ys=[p[1] for p in graph.points.values()]; sx=500/(max(xs)-min(xs) or 1); sy=350/(max(ys)-min(ys) or 1)
    mapped={vertex:(50+(point[0]-min(xs))*sx,50+(point[1]-min(ys))*sy) for vertex,point in graph.points.items()}
    for first,second in graph.edges: canvas.create_line(*mapped[first],*mapped[second])
    for vertex,(x,y) in mapped.items(): canvas.create_oval(x-12,y-12,x+12,y+12,fill="white"); canvas.create_text(x,y,text=str(vertex))
    root.mainloop()


def ex_13_13(path: PathLike,display: bool=True) -> GraphData:
    graph=read_graph(path)
    if display: _display_graph(graph)
    return graph


def ex_13_14(url: str,display: bool=True) -> GraphData:
    graph=parse_graph(_url_text(url))
    if display: _display_graph(graph)
    return graph


@dataclass
class Address:
    name: str
    street: str
    city: str
    state: str
    zipcode: str


class AddressBookStore:
    def __init__(self,path: PathLike): self.path=Path(path); self.addresses: list[Address]=[]; self.index=0; self.load()
    def load(self) -> None:
        if self.path.exists():
            with self.path.open("rb") as source: self.addresses=pickle.load(source)
        self.index=min(self.index,max(0,len(self.addresses)-1))
    def save(self) -> None:
        with self.path.open("wb") as target: pickle.dump(self.addresses,target)
    def add(self,address: Address) -> None: self.addresses.append(address); self.index=len(self.addresses)-1; self.save()
    def update(self,address: Address) -> None:
        if not self.addresses: raise IndexError("address book is empty")
        self.addresses[self.index]=address; self.save()
    def current(self) -> Address | None: return self.addresses[self.index] if self.addresses else None
    def first(self) -> Address | None: self.index=0; return self.current()
    def last(self) -> Address | None: self.index=max(0,len(self.addresses)-1); return self.current()
    def next(self) -> Address | None:
        if self.addresses: self.index=min(len(self.addresses)-1,self.index+1)
        return self.current()
    def previous(self) -> Address | None:
        if self.addresses: self.index=max(0,self.index-1)
        return self.current()


def ex_13_15(path: PathLike="addresses.dat") -> None:
    import tkinter as tk
    root=tk.Tk(); root.title("Address Book"); store=AddressBookStore(path); labels=("name","street","city","state","zipcode"); entries={}
    for row,label in enumerate(labels): tk.Label(root,text=label.title()).grid(row=row,column=0); entries[label]=tk.Entry(root,width=50); entries[label].grid(row=row,column=1,columnspan=6)
    status=tk.StringVar(); tk.Label(root,textvariable=status).grid(row=6,column=0,columnspan=7)
    def get_address() -> Address: return Address(*(entries[label].get() for label in labels))
    def show(address: Address | None) -> None:
        if address:
            for label,value in zip(labels,(address.name,address.street,address.city,address.state,address.zipcode)): entries[label].delete(0,"end"); entries[label].insert(0,value)
        status.set(f"current address index: {store.index if store.addresses else '-'} / number of addresses: {len(store.addresses)}")
    actions=(("Add",lambda:(store.add(get_address()),show(store.current()))),("First",lambda:show(store.first())),("Next",lambda:show(store.next())),("Previous",lambda:show(store.previous())),("Last",lambda:show(store.last())),("Update",lambda:(store.update(get_address()),show(store.current()))))
    for column,(label,command) in enumerate(actions): tk.Button(root,text=label,command=command).grid(row=5,column=column+1)
    show(store.current()); root.mainloop()


_SALARY_RANGES={"assistant":(50_000,80_000),"associate":(60_000,110_000),"full":(75_000,130_000)}


def ex_13_16(path: PathLike="Salary.txt",count: int=1000,seed: int | None=None) -> None:
    target=Path(path)
    if target.exists(): raise FileExistsError(target)
    generator=random.Random(seed); lines=[]
    for index in range(1,count+1):
        rank=generator.choice(tuple(_SALARY_RANGES)); low,high=_SALARY_RANGES[rank]; lines.append(f"FirstName{index} LastName{index} {rank} {generator.uniform(low,high):.2f}")
    _write_text(target,"\n".join(lines)+"\n")


def _salary_report(text: str) -> dict[str,tuple[int,float,float]]:
    salaries={rank:[] for rank in _SALARY_RANGES}
    for line in text.splitlines():
        if not line.strip(): continue
        first,last,rank,salary=line.split()
        if rank not in salaries: raise ValueError(f"unknown rank: {rank}")
        salaries[rank].append(float(salary))
    all_values=[salary for values in salaries.values() for salary in values]; result={}
    for rank,values in list(salaries.items())+[("all",all_values)]: result[rank]=(len(values),sum(values),sum(values)/len(values) if values else 0.0)
    return result


def ex_13_17(source: PathLike | str) -> dict[str,tuple[int,float,float]]:
    text=_url_text(str(source)) if re.match(r"https?://",str(source)) else _read_text(source)
    return _salary_report(text)


EXERCISES: dict[str,Callable[...,Any]]={f"13.{number}":globals()[f"ex_13_{number}"] for number in range(1,18)}
