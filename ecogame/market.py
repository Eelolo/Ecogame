from flask import Blueprint, session
from ecogame.auth import login_required
from ecogame.db_operations import get_user_credits, get_user_items


bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/user_info')
@login_required
def info():
    kredits = get_user_credits(session['user_id'])
    user_items = get_user_items(session['user_id'])

    return {'Credits': kredits, 'Items': user_items}
