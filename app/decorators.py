from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import User

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        is_admin = User.query.filter_by(is_admin=True).first()
        if not current_user.is_admin :
            abort(403)
        else:
            return f(*args, **kwargs)
    return wrapper