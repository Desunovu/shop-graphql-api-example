from api import db
from api.extras import token_required, create_result, Errors, Roles
from api.extras.resolver_utils import get_cart_total
from api.models import User, CartLine, Product


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

    cartline_and_product_list = db.session.query(CartLine, Product).\
        join(Product).join(User).filter(User.id == user_id).all()

    return create_result(cart=cartline_and_product_list, cartTotal=get_cart_total(cartline_and_product_list))
