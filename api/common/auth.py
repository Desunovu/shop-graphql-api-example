from functools import wraps

import jwt
from flask import request

from api import app, db
from api.models import User, Role
from api.common.common import CUSTOMER_ACCESS_LEVEL


# TODO переписать для резолверов
def token_required(access_lvl=CUSTOMER_ACCESS_LEVEL):
    def token_required_wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            token = None
            current_user = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            else:
                raise Exception

            try:
                user_data = jwt.decode(jwt=token, key=app.secret_key, algorithms='HS256')
                user = db.session.query(User).get(user_data['id'])
                user_access_level = db.session.query(Role).get(user.role).access_level
                if user_access_level >= access_lvl:
                    return func(current_user, *args, **kwargs)
                else:
                    raise Exception
            except Exception:
                raise Exception

        return decorated_view
    return token_required_wrapper
