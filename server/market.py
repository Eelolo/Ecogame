from flask import Blueprint, session
from .auth import login_required
from .db import get_db
from .db_operations import (
    get_user_credits, get_user_items, add_item, subtract_credits, add_credits, delete_last_purchased_item
)

bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/user_info')
@login_required
def info():
    user_credits = get_user_credits(session['user_id'])
    user_items = get_user_items(session['user_id'])

    return {
            'data': {
                'code': 200,
                'message': 'user_info',
                'Credits': user_credits,
                'Items': user_items
                }
            }


@bp.route('/')
@login_required
def items():
    db = get_db()
    user_items = dict(db.execute(
        'SELECT name, price FROM items'
    ).fetchall())
    items_info = {}
    items_list = []
    for item in user_items:
        items_list.append([item, user_items[item]])
    for idx in range(len(items_list)):
        items_info[idx+1] = items_list[idx]

    return {
            'data': {
                'code': 200,
                'message': 'items info',
                'items info': items_info
                }
            }


@bp.route('/buy/<int:item_id>')
@login_required
def buy_item(item_id):
    db = get_db()
    try:
        price = db.execute(
            'SELECT price FROM items WHERE item_id = ?', (item_id,)
        ).fetchone()[0]
    except TypeError:
        return {
                'error': {
                    'code': 400,
                    'error_message': 'Incorrect item_id.'
                    }
                }

    user_credits = get_user_credits(session['user_id'])

    if db.execute(
        'SELECT * FROM items WHERE item_id = ?', (item_id,)
    ).fetchall() is not None:
        if user_credits >= price:
            add_item(session['user_id'], item_id)
            subtract_credits(session['user_id'], price)
        else:
            return {
                    'error': {
                        'code': 403,
                        'error_message': 'Not enough credits.'
                        }
                    }

    return {
            'data': {
                'code': 200,
                'message': 'Item purchased.'
                }
            }


@bp.route('/sell/<int:item_id>')
@login_required
def sell_item(item_id):
    db = get_db()

    try:
        price = db.execute(
            'SELECT price FROM items WHERE item_id = ?', (item_id,)
        ).fetchone()[0]
    except TypeError:
        return {'error': {
                    'code': 400,
                    'error_message': 'Incorrect item_id.'
                    }
                }
    add_credits(session['user_id'], price)

    if delete_last_purchased_item(session['user_id'], item_id) == 0:
        return {
                'error': {
                    'code': 403,
                    'error_message': 'There is no such item.'
                    }
                }

    return {
            'data': {
                'code': 200,
                'message': 'Item sold.'
                }
            }
