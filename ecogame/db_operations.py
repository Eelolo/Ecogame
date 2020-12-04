from ecogame.db import get_db
from werkzeug.security import generate_password_hash


def new_user(username, password):
    db = get_db()

    db.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()