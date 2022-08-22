from functools import wraps

import jwt
from flask import request, session

from api import app, db
from api.models import User
from api.common.enum_types import RoleEnum


class UnauthorizedError(Exception):
    extension = {"code": 401}


def token_required(role=RoleEnum.CUSTOMER.value):
    def token_required_wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            token = None
            current_user = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            else:
                raise UnauthorizedError("Unauthorized")

            try:
                data = jwt.decode(jwt=token, key=app.secret_key, algorithms='HS256')
            except jwt.exceptions.InvalidTokenError:
                raise UnauthorizedError("Unauthorized")

            current_user = db.session.query(User).get(data['id'])
            if not current_user:
                raise UnauthorizedError("Unauthorized")

            session["current_user"] = current_user.to_dict()
            return func(*args, **kwargs)

        return decorated_view
    return token_required_wrapper
