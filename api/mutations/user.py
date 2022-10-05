from werkzeug.security import generate_password_hash
from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import create_result, Errors, Roles
from api.models import User


@convert_kwargs_to_snake_case
def resolve_update_user(obj, info, **kwargs):
    user_id = info.context.current_user.id
    # Проверка на администратра при указании id
    if kwargs.get("id"):
        if info.context.current_user.role != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])
        user_id = kwargs["id"]

    # обновить поля user из переданных аргументов
    user = db.session.query(User).get(user_id)
    user.update(**kwargs)

    # Частные случаи полей
    if kwargs.get("password"):
        user.password = generate_password_hash(kwargs["password"])

    db.session.add(user)
    db.session.commit()
    return create_result(user=user)
