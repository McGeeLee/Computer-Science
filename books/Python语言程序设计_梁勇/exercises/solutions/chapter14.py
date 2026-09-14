"""第 14 章编程题 14.1～14.11：元组、集合和字典。"""

from __future__ import annotations

import io
import keyword
import random
import re
import tokenize
import urllib.request
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any

from .chapter11 import _STATE_CAPITALS


def keyword_counts(source: str) -> dict[str,int]:
    counts=Counter()
    try:
        tokens=tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type==tokenize.NAME and keyword.iskeyword(token.string): counts[token.string]+=1
    except (tokenize.TokenError,IndentationError):
        raise ValueError("invalid or incomplete Python source")
    return dict(sorted(counts.items()))


def ex_14_1(path: str | Path) -> list[str]:
    return list(keyword_counts(Path(path).read_text(encoding="utf-8")))


def ex_14_2(numbers: Iterable[int]) -> list[int]:
    counts=Counter(numbers)
    if not counts: return []
    maximum=max(counts.values()); return sorted(number for number,count in counts.items() if count==maximum)


def ex_14_3(path: str | Path) -> dict[str,int]:
    return keyword_counts(Path(path).read_text(encoding="utf-8"))


def letter_counts(text: str) -> dict[str,int]:
    counts=Counter(character.lower() for character in text if character.isascii() and character.isalpha())
    return {character:counts[character] for character in "abcdefghijklmnopqrstuvwxyz"}


def _url_text(url: str) -> str:
    with urllib.request.urlopen(url,timeout=15) as response: return response.read().decode(response.headers.get_content_charset() or "utf-8")


def _letter_gui(from_url: bool,histogram: bool) -> None:
    import tkinter as tk
    from tkinter import filedialog,messagebox
    root=tk.Tk(); root.title("Occurrence of Letters"); top=tk.Frame(root); top.pack(fill="x"); entry=tk.Entry(top,width=65); entry.pack(side="left",fill="x",expand=True)
    if not from_url: tk.Button(top,text="Browse",command=lambda:(entry.delete(0,"end"),entry.insert(0,filedialog.askopenfilename()))).pack(side="left")
    canvas=tk.Canvas(root,width=780,height=380,bg="white"); text=tk.Text(root,width=55,height=25)
    (canvas if histogram else text).pack(fill="both",expand=True)
    def show() -> None:
        try: content=_url_text(entry.get()) if from_url else Path(entry.get()).read_text(encoding="utf-8"); counts=letter_counts(content)
        except Exception as error: messagebox.showerror("Read error",str(error)); return
        if histogram:
            canvas.delete("all"); maximum=max(counts.values()) or 1
            for index,(letter,count) in enumerate(counts.items()): x=index*30+5; y=340-count/maximum*300; canvas.create_rectangle(x,y,x+22,340,fill="lightblue"); canvas.create_text(x+11,355,text=letter)
        else:
            text.delete("1.0","end"); text.insert("end","\n".join(f"{letter} appears {count} times" for letter,count in counts.items()))
    tk.Button(top,text="Show Result",command=show).pack(side="left"); root.mainloop()


def ex_14_4() -> None: _letter_gui(False,False)
def ex_14_5() -> None: _letter_gui(False,True)
def ex_14_6() -> None: _letter_gui(True,False)
def ex_14_7() -> None: _letter_gui(True,True)


def ex_14_8(path: str | Path) -> list[str]:
    words=re.findall(r"[^\W_]+(?:['-][^\W_]+)*",Path(path).read_text(encoding="utf-8").casefold(),flags=re.UNICODE)
    return sorted(set(words))


def ex_14_9(words: Iterable[str] = ("python","program","recursive","computer"),seed: int | None=None) -> None:
    import tkinter as tk
    choices=[word.lower() for word in words]
    if not choices: raise ValueError("at least one word is required")
    generator=random.Random(seed); root=tk.Tk(); root.title("Hangman"); canvas=tk.Canvas(root,width=500,height=340,bg="white"); canvas.pack(); entry=tk.Entry(root); entry.pack(); word=[generator.choice(choices)]; guessed:set[str]=set(); misses=[]; status=tk.StringVar(); tk.Label(root,textvariable=status,font=("Arial",18)).pack()
    def draw() -> None:
        canvas.delete("all"); canvas.create_line(80,300,230,300); canvas.create_line(130,300,130,40); canvas.create_line(130,40,300,40); canvas.create_line(300,40,300,75)
        parts=(lambda:canvas.create_oval(275,75,325,125),lambda:canvas.create_line(300,125,300,210),lambda:canvas.create_line(300,145,260,180),lambda:canvas.create_line(300,145,340,180),lambda:canvas.create_line(300,210,265,270),lambda:canvas.create_line(300,210,335,270),lambda:canvas.create_text(300,100,text="x  x"))
        for part in parts[:len(misses)]: part()
        display="".join(character if character in guessed else "*" for character in word[0]); status.set(f"Guess a word: {display}    Missed letters: {''.join(misses)}")
        if all(character in guessed for character in word[0]) or len(misses)>=7: status.set(f"The word is: {word[0]}  (press Enter for a new word)")
    def submit(_event: Any=None) -> None:
        character=entry.get().lower()[:1]; entry.delete(0,"end")
        if all(ch in guessed for ch in word[0]) or len(misses)>=7: word[0]=generator.choice(choices); guessed.clear(); misses.clear(); draw(); return
        if character and character not in guessed: guessed.add(character); misses.append(character) if character not in word[0] else None
        draw()
    entry.bind("<Return>",submit); draw(); root.mainloop()


class CapitalQuiz:
    def __init__(self,capitals: Mapping[str,str]=_STATE_CAPITALS,seed: int | None=None): self.capitals=dict(capitals); self.states=list(self.capitals); random.Random(seed).shuffle(self.states); self.index=0; self.correct=0
    @property
    def current(self) -> str | None: return self.states[self.index] if self.index<len(self.states) else None
    def answer(self,value: str) -> bool:
        if self.current is None: raise StopIteration("quiz is complete")
        correct=value.strip().casefold()==self.capitals[self.current].casefold(); self.correct+=correct; self.index+=1; return correct


def ex_14_10(seed: int | None=None) -> CapitalQuiz:
    return CapitalQuiz(seed=seed)


def ex_14_11(path: str | Path) -> tuple[int,int]:
    text=Path(path).read_text(encoding="utf-8"); vowels=set("aeiouAEIOU"); letters=[character for character in text if character.isascii() and character.isalpha()]; vowel_count=sum(character in vowels for character in letters); return vowel_count,len(letters)-vowel_count


EXERCISES: dict[str,Callable[...,Any]]={f"14.{number}":globals()[f"ex_14_{number}"] for number in range(1,12)}
