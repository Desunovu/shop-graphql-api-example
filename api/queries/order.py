from api import db
from api.models import CartLine, OrderLine, Order, User, Product
from api.extras import token_required, create_result, create_error, Errors, Roles, NotEnoughProduct


@token_required()
def resolve_get_orders(_obj, info, **kwargs):
    user_id = info.context.current_user.id

    # Если администратор указал userId
    if kwargs.get("userId"):
        if info.context.current_user.role != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])
        user_id = kwargs["userId"]
        if not db.session.query(User).get(user_id):
            return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    orders = db.session.query(Order).filter(Order.user_id == user_id).all()

    return create_result(orders=orders)
