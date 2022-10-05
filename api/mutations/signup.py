from werkzeug.security import generate_password_hash
from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import create_result, Errors, Roles
from api.models import User


@convert_kwargs_to_snake_case
def resolve_create_user(obj, info, **kwargs):
    user = db.session.query(User).filter(User.email == kwargs["email"]).first()
    if user:
        return create_result(status=False, errors=[Errors.USER_ALREADY_EXISTS])

    # Задать поля присутствующие в модели из аргументов, в поле пароля поместить его хэш
    user = User(**kwargs, role=Roles.CUSTOMER)
    user.password = generate_password_hash(kwargs["password"])
    db.session.add(user)
    db.session.commit()
    return create_result(user=user)
