from api import db
from api.common import token_required, create_result, create_simple_result, Errors
from api.models import CartLine, Product
from flask import session


@token_required()
def resolve_remove_product_from_cart(_obj, _info, **kwargs):
    product = db.session.query(Product).get([kwargs["id"]])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    cart_line = db.session.query(CartLine).get((session["current_user"]["id"], kwargs["id"]))
    if not cart_line:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # Изменить количество заказа позиции
    if kwargs.get("all"):
        cart_line.amount = 0
    else:
        cart_line.amount -= 1

    # Удалить запись если не осталось элементов
    if cart_line.amount <= 0:
        db.session.delete(cart_line)

    db.session.commit()
    return create_result(cartline=create_simple_result(
        product=product.to_dict(),
        amount=cart_line.amount))
