from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import token_required, create_result, Errors, Roles
from api.extras.resolver_utils import query_sort, query_pagination
from api.models import Order, User


@token_required()
@convert_kwargs_to_snake_case
def resolve_get_orders(_obj, info, **kwargs):
    user_id = info.context.current_user.id

    # Если администратор указал userId
    if kwargs.get("userId"):
        if info.context.current_user.role != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])
        user_id = kwargs["userId"]
        if not db.session.query(User).get(user_id):
            return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    query = db.session.query(Order).filter(Order.user_id == user_id)
    query = query_sort(query=query, resolver_args=kwargs)
    query = query_pagination(query=query, resolver_args=kwargs)
    orders = query.all()

    return create_result(orders=orders)
