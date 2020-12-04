from flask import Blueprint, session
from ecogame.auth import login_required
from ecogame.db import get_db
from ecogame.db_operations import (
    get_user_credits, get_user_items, add_item, subtract_credits
)


bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/user_info')
@login_required
def info():
    user_credits = get_user_credits(session['user_id'])
    user_items = get_user_items(session['user_id'])

    return {'Credits': user_credits, 'Items': user_items}


@bp.route('/')
@login_required
def items():
    db = get_db()
    user_items = dict(db.execute(
        'SELECT name, price FROM items'
    ).fetchall())
    response = {}
    items_list = []
    for item in user_items:
        items_list.append([item, user_items[item]])
    for idx in range(len(items_list)):
        response[idx+1] = items_list[idx]
    return response


@bp.route('/buy/<int:item_id>')
@login_required
def buy_item(item_id):
    db = get_db()
    try:
        price = db.execute(
            'SELECT price FROM items WHERE item_id = ?', (item_id,)
        ).fetchone()[0]
    except TypeError:
        return 'Incorrect item_id.'

    user_credits = get_user_credits(session['user_id'])

    if db.execute(
        'SELECT * FROM items WHERE item_id = ?', (item_id,)
    ).fetchall() is not None:
        if user_credits >= price:
            add_item(session['user_id'], item_id)
            subtract_credits(session['user_id'], price)
        else:
            return {'message': 'Not enough credits.'}

    return {'message': 'Item purchased.'}
