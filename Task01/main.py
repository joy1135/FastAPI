from typing import Union
from fastapi import FastAPI
import random
from pydantic import BaseModel
import math

app = FastAPI()

class Triangle(BaseModel):
    a: int
    b: int
    c: int

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/about")
def read_about():
    return {
        "name" : "Oleg",
        "surname" : "Sokolov",
        "lastname" : "Alexandrovich",
        "group" : "T-323901"
    }

@app.get("/rnd")
def reade_rnd():
    rnd = random.randint(1,10)
    return {
        "Число" : rnd
    }

@app.post("/t_square")
def p_t_square(tr : Triangle):
    if tr.a <= 0 or tr.b <= 0 or tr.c <= 0:
        return {
            "Ошибка": "Сторона должна быть больше 0"
        }
    per = tr.a + tr.b + tr.c
    p = per/2
    s = math.sqrt(p*(p-tr.a)*(p-tr.b)*(p-tr.c))
    return {
        "Периметр" : per,
        "Площадь" : s
    }
