from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import create_result, token_required, Errors, Roles
from api.extras.resolver_utils import query_sort, query_pagination
from api.models import User


@token_required()
def resolve_get_user(_obj, _info, **kwargs):
    # Для администратора
    if "id" in kwargs:
        # Запрет пользователю делать запрос с аргументом
        if _info.context.current_user.role != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])

        user = db.session.query(User).get(kwargs["id"])
        if not user:
            return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])
        return create_result(user=user)

    # Если аргумент не передан
    return create_result(user=_info.context.current_user)


@token_required(allowed_roles=[Roles.ADMIN])
@convert_kwargs_to_snake_case
def resolve_get_users(_obj, _info, **kwargs):
    query = db.session.query(User)
    query = query_sort(query=query, resolver_args=kwargs)
    query = query_pagination(query=query, resolver_args=kwargs)
    users = query.all()

    return create_result(users=[user for user in users])
