from sqlalchemy import Date, Float, Numeric, Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


# Многие ко многим
film_genre = Table('film_genre', Base.metadata,
                         Column('film_id', ForeignKey('films.id'), primary_key=True),
                         Column('genre_id', ForeignKey('genres.id'), primary_key=True)
                         )

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key = True)
    name = Column(String(255), unique = True)
    year = Column(Integer)
    duration = Column(Float)
    rating = Column(Integer)
    description = Column(String(255), nullable=True)
    img = Column(String(255), nullable=True)
    date_added = Column(Date)

    genres = relationship("Genre", secondary="film_genre", backref="films")