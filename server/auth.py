import functools
from flask import (Blueprint, g, request, session)
from werkzeug.security import check_password_hash
from .db import get_db
from random import randint
from .db_operations import (
    new_user, add_credits, get_user_credits, get_user_items
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT user_id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            new_user(username, password)
            return {'Registration': 'Success'}

        return {'Error': error}


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if g.user is not None:
            return {'Message': 'Already logged in.'}

        username = request.json['username']
        password = request.json['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']

            bonuses = [450, 1350, 3100, 4800, 6300]
            bonus = bonuses[randint(0, 4)]

            add_credits(session['user_id'], bonus)

            user_items = ', '.join(get_user_items(session['user_id']))

            return {
                "Bonus": "Received {} credits".format(bonus),
                "Credits": get_user_credits(session['user_id']),
                "Items": user_items
            }

        return {'Error': error}


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    user_id = session.get('user_id')

    if user_id is None:
        return {'Error': 'You are not logged in.'}
    else:
        session.clear()
        return {'Message': 'Good Bye.'}


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {'Error': 'Please log in.'}

        return view(**kwargs)

    return wrapped_view
