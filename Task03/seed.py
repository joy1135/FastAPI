from datetime import datetime
from sqlalchemy.orm import Session
from database import engine
import models as m

m.Base.metadata.drop_all(bind = engine)
m.Base.metadata.create_all(bind = engine)

with Session(bind = engine) as session:
    g1 = m.Genre(name = "Фантастика")
    g2 = m.Genre(name = "Экшн")
    f1 = m.Film(
        name = "Star Wars 1", 
        year = 1999, duration = 120, 
        rating = 10, 
        genres=[g1, g2],
        date_added = datetime.now()
        )
    f2 = m.Film(
        name = "Star Wars 2", 
        year = 2001, duration = 120, 
        rating = 9, 
        genres=[g1, g2],
        date_added = datetime.now()
        )
    u1 = m.User(
        username = "J5",
        passwrod =  "qwerty",
        email = "dasdasd",
        created_at = datetime.now()
    )

    session.add_all([g1, f1, g2, f2, u1])
    session.commit()