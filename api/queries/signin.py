import datetime

import jwt
from werkzeug.security import check_password_hash

from api import app, db
from api.common import create_result, Errors
from api.models import User


def resolve_login_user(_obj, _info, email, password):
    """
    Запрос авторизации пользователя
    Возвращает
        LoginResult!
    """
    user = db.session.query(User).filter(User.email == email).first()

    # Неверный Email или пароль
    if not (user and check_password_hash(user.password, password)):
        return create_result(status=False, errors=[Errors.WRONG_EMAIL_OR_PASSWORD])

    token = jwt.encode(payload={"id": user.id, "exp": datetime.datetime.now() + datetime.timedelta(days=7)},
                       key=app.secret_key, algorithm="HS256")
    return create_result(token=token)
