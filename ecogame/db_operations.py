from ecogame.db import get_db
from werkzeug.security import generate_password_hash


def fetchall_to_list(fetchall):
    for idx in range(len(fetchall)):
        fetchall[idx] = fetchall[idx][0]

    return fetchall


def new_user(username, password):
    db = get_db()

    db.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()


def get_user_credits(user_id):
    db = get_db()

    user_credits = db.execute(
        'SELECT credits FROM users WHERE user_id = ?', (user_id,)
    ).fetchone()[0]
    return user_credits


def add_credits(user_id, integer):
    db = get_db()

    db.execute(
        'UPDATE users SET credits = ? WHERE user_id = ?',
        (get_user_credits(user_id) + integer, user_id)
    )
    db.commit()


def subtract_credits(user_id, integer):
    db = get_db()

    db.execute(
        'UPDATE users SET credits = ? WHERE user_id = ?',
        (get_user_credits(user_id) - integer, user_id)
    )
    db.commit()


def get_user_items(user_id):
    db = get_db()

    items_id = db.execute(
        'SELECT item_id FROM user_items WHERE user_id = ?', (user_id,)
    ).fetchall()

    items_id = fetchall_to_list(items_id)

    user_items = []
    for idx in items_id:
        user_items.append(db.execute(
            'SELECT name FROM items WHERE item_id = ?', (idx,)
        ).fetchone())

    user_items = fetchall_to_list(user_items)

    return user_items


def add_item(user_id, item_id):
    db = get_db()

    db.execute(
        'INSERT INTO user_items (user_id, item_id) VALUES (?, ?)',
        (user_id, item_id)
    )
    db.commit()


def delete_last_purchased_item(user_id, item_id):
    db = get_db()

    some_items = db.execute(
        'SELECT id FROM user_items WHERE user_id = ? AND item_id = ?',
        (user_id, item_id)
    ).fetchall()
    some_items = fetchall_to_list(some_items)

    item_to_delete = 0
    for idx in some_items:
        if item_to_delete < idx:
            item_to_delete = idx

    if item_to_delete == 0:
        return item_to_delete

    db.execute(
        'DELETE FROM user_items WHERE user_id = ? AND item_id = ? AND id = ?',
        (user_id, item_id, item_to_delete)
    )
    db.commit()
