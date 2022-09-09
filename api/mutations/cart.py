from api import db
from api.common import token_required, create_result, create_simple_result, Errors
from api.models import CartLine, Product
from flask import session


@token_required()
def resolve_add_product_to_cart(_obj, info, **kwargs):
    """Запрос для добавления товара в корзину"""

    product = db.session.query(Product).get([kwargs["id"]])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    cartline = db.session.query(CartLine).get((info.context.current_user.id, kwargs["id"]))

    # Создать новую строку в корзине если ее нет
    if not cartline:
        cartline = CartLine(user_id=info.context.current_user.id, product_id=kwargs["id"], amount=1)
        db.session.add(cartline)
        db.session.commit()
        return create_result(cartline=[cartline, product])  # для cartline resolver

    # увеличить количество товара в корзине если строка уже есть
    if product.amount > cartline.amount:
        cartline.amount += 1
        db.session.commit()
        return create_result(cartline=[cartline, product])

    return create_result(status=False, errors=[Errors.CANT_ADD_MORE_PRODUCTS])


@token_required()
def resolve_remove_product_from_cart(_obj, info, **kwargs):
    product = db.session.query(Product).get([kwargs["id"]])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    cartline = db.session.query(CartLine).get((info.context.current_user.id, kwargs["id"]))
    if not cartline:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # Изменить количество заказа позиции
    if kwargs.get("all"):
        cartline.amount = 0
    else:
        cartline.amount -= 1

    # Удалить запись если не осталось элементов
    if cartline.amount <= 0:
        db.session.delete(cartline)

    db.session.commit()
    return create_result(cartline=[cartline, product])
