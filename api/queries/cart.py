from api import db
from api.extras import token_required, create_result, create_simple_result, Errors, Roles
from api.models import User, CartLine, Product
from flask import session


@token_required()
def resolve_get_cart(_obj, info, **kwargs):
    """
    Запрос получения корзины
        Для администратора разрешено указать id для получения корзины любого пользователя
        Для покупателя указывать id запрещено
    """
    user_id = info.context.current_user.id
    if "id" in kwargs:
        # Запрет пользователю делать запрос с аргументом
        if info.context.current_user.role != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])
        user_id = kwargs["id"]

    cartline_product_list = db.session.query(CartLine, Product).join(Product).join(User).filter(User.id == user_id).all()

    return create_result(cart=cartline_product_list)
