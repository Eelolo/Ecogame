from flask import Blueprint, session
from ecogame.auth import login_required
from ecogame.db import get_db
from ecogame.db_operations import get_user_credits, get_user_items


bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/user_info')
@login_required
def info():
    kredits = get_user_credits(session['user_id'])
    user_items = get_user_items(session['user_id'])

    return {'Credits': kredits, 'Items': user_items}


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
