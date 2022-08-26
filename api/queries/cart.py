from api import db
from api.common import token_required, create_result, create_simple_result, Errors, Roles
from api.models import User, CartLine, Product
from flask import session


@token_required()
def resolve_get_cart(_obj, _info, **kwargs):
    """
    Запрос получения корзины
        Для администратора разрешено указать id для получения корзины любого пользователя
        Для покупателя указывать id запрещено
    Возвращает
        LoginResult!
    """
    user_id = session["current_user"]["id"]
    if "id" in kwargs:
        # Запрет пользователю делать запрос с аргументом
        if session["current_user"]["role"] != Roles.ADMIN:
            return create_result(status=False, errors=[Errors.ACCESS_DENIED])
        user_id = kwargs["id"]

    # (Product, ammount)
    # TODO переписать лаконичнее
    cart_lines = db.session.query(Product, CartLine.amount).join(CartLine).join(User).filter(User.id == user_id).all()

    return create_result(
        cart=[create_simple_result(
            product=cart_line[0].to_dict(),
            amount=cart_line[1])
            for cart_line in cart_lines])
