from datetime import datetime
import os
import shutil
import uuid
from fastapi import FastAPI, HTTPException, Depends, UploadFile
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import basic_auth

app = FastAPI()
MAX_FILE_SIZE_MB = 5
UPLOAD_DIR = "files"

@app.get("/film", response_model=List[pyd.FilmSchema])
def get_all_film(db:Session=Depends(get_db)):
    films = db.query(m.Film).all()
    return films

@app.get("/film/{film_id}", response_model=pyd.FilmSchema)
def get_film(film_id:int, db:Session=Depends(get_db)):
    film = db.query(m.Film).filter(
        m.Film.id == film_id
    ).first()
    if not film:
        raise HTTPException(404, 'Игра не найдена')
    return film


@app.post("/film", response_model=pyd.BaseFilm)
def create_film(
    film: pyd.CreateFilm,
    user: m.User = Depends(basic_auth),
    db: Session = Depends(get_db)
):
    film_db = db.query(m.Film).filter(m.Film.name == film.name).first()
    if film_db:
        raise HTTPException(400, "Такой фильм уже есть")
    
    film_db = m.Film(
        name=film.name,
        year=film.year,
        duration=film.duration,
        rating=film.rating,
        description=film.description,
        date_added=datetime.now()
    )
    
    if not film.genre:
        raise HTTPException(status_code=400, detail="Добавьте хотя бы один жанр")
    
    for genre_id in film.genre:
        genre = db.query(m.Genre).filter(m.Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(status_code=404, detail=f"Жанр с id {genre_id} не найден")
        film_db.genres.append(genre) 
    
    db.add(film_db)
    db.commit()
    db.refresh(film_db)
    return film_db

@app.put("/film/img/{film_id}", response_model=pyd.BaseFilm)
def add_film_img(film_id: int, img: UploadFile, user: m.User = Depends(basic_auth), db:Session=Depends(get_db)):
    film = db.query(m.Film).filter(
        m.Film.id == film_id
    ).first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    if img.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Неверный формат")
    with open(f"files/{img.filename}", "wb") as f:
        shutil.copyfileobj(img.file, f)
    film.img = f"files/{img.filename}"
    img.file.seek(0, os.SEEK_END)
    size_mb = img.file.tell() / (1024 * 1024)
    img.file.seek(0)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Размер файла превышает {MAX_FILE_SIZE_MB} МБ")
    ext = img.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(img.file, f)
    film.img = filepath
    db.commit()
    db.refresh(film)
    return film

@app.put("/film/{film_id}", response_model=pyd.BaseFilm)
def update_film_info(film_id: int, film_data: pyd.CreateFilm, user: m.User = Depends(basic_auth), db:Session=Depends(get_db)):
    film = db.query(m.Film).filter(
        m.Film.id == film_id
    ).first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    film.name = film_data.name
    film.year = film_data.year
    film.duration = film_data.duration
    film.rating = film_data.rating
    film.description = film_data.description
    film.date_added = datetime.now()
    genres = db.query(m.Genre).filter(m.Genre.id.in_(film_data.genre)).all()
    if len(genres) != len(film_data.genre):
        raise HTTPException(status_code=400, detail="Некоторые жанры не найдены")
    film.genres = genres
    db.commit()
    db.refresh(film)
    return film

@app.delete("/film/{film_id}")
def del_film(film_id:int, user: m.User = Depends(basic_auth), db:Session=Depends(get_db)):
    film = db.query(m.Film).filter(
        m.Film.id == film_id
    ).first()
    if not film:
        raise HTTPException(404, 'Товар не найден')
    db.delete(film)
    db.commit()
    return "Фильм удален"

@app.get("/genre", response_model=List[pyd.GenreSchema])
def get_all_genre(db:Session=Depends(get_db)):
    genre = db.query(m.Genre).all()
    return genre

@app.post("/genre", response_model=pyd.BaseGenre)
def create_genre(genre:pyd.CreateGenre, user: m.User = Depends(basic_auth), db:Session=Depends(get_db)):
    genre_db = db.query(m.Genre).filter(m.Genre.name == genre.name).first()
    if genre_db:
        raise HTTPException(400, "Такой жанр уже есть")
    genre_db = m.Genre()
    genre_db.name = genre.name
    genre_db.description = genre.description
    db.add(genre_db)
    db.commit()
    return genre_db
