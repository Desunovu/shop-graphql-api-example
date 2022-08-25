from api import db
from api.common import token_required, create_result, create_simple_result, Errors
from api.models import CartLine, Product
from flask import session


@token_required()
def resolve_add_product_to_cart(_obj, _info, **kwargs):
    product = db.session.query(Product).get([kwargs["id"]])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    cart_line = db.session.query(CartLine).get((session["current_user"]["id"], kwargs["id"]))

    # Создать новую строку в корзине
    if not cart_line:
        cart_line = CartLine(user_id=session["current_user"]["id"], product_id=kwargs["id"], amount=1)
        db.session.add(cart_line)
        db.session.commit()
        return create_result(cartline=create_simple_result(
            product=product.to_dict(),
            amount=cart_line.amount))

    # увеличить количество товара в корзине если строка уже есть
    if product.amount > cart_line.amount:
        cart_line.amount += 1
        db.session.commit()
        return create_result(cartline=create_simple_result(
            product=product.to_dict(),
            amount=cart_line.amount))

    return create_result(status=False, errors=[Errors.CANT_ADD_MORE_PRODUCTS])
