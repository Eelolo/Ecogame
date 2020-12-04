from flask import Blueprint, request
from ecogame.db import get_db
from ecogame.db_operations import new_user

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
            return {'Registration': 'Succes'}

        return {'Error': error}