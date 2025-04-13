from pydantic import BaseModel, Field
from typing import Optional, Union
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

items = [
    {"id": 1, "name": "Айфон 30", "price": 100000, "description": "Топовый смартфон"},
    {"id": 2, "name": "Телевизор 444", "price": 15000, "description": "Топовый ТВ"},
    {"id": 3, "name": "Батон", "price": 45, "description": "Нежный, вкусный"},
    {"id": 4, "name": "LEGO Star Wars", "price": 300000, "description": "Набор для детей"},
    {"id": 5, "name": "Пакет WB", "price": 1, "description": "Вместительный"},
]

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)


@app.get("/items")
def get_all_items(
    name: str | None = Query(None, min_lenght = 2),
    min_price: float | None = Query(None, gt = 0),
    max_price: float | None = Query(None, gt = 0),
    limit: int = Query(10, lt = 100),
):
    if max_price:
        if max_price < min_price:
            raise HTTPException(400, "Максимальная цена не может быть меньше минимальной")
    res = []
    for i in items:
        if name:
            if name != i["name"]:
                continue
        if min_price:
            if min_price > i["price"]:
                continue
        if max_price:
            if max_price < i["price"]:
                continue
        if limit == len(res):
            return res
        res.append(i)
    return res 

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(gt = 0)
):
    for i in items:
        if item_id == i["id"]:
            return i
    return HTTPException(400, "Товар не найден")

@app.post("/items/")
def create_item(item: ItemCreate):
    new_id = max(i["id"] for i in items) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "description": item.description
    }
    items.append(new_item)
    return new_item