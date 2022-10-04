import datetime
from sqlalchemy import update

from api import db
from api.models import CartLine, OrderLine, Order, User, Product
from api.extras import token_required, create_result, create_error, Errors, Roles, NotEnoughProduct


@token_required()
def resolve_create_order(_obj, info, **kwargs):
    # Получить недоступные к заказу строки и разрешенное количество, чтобы исправить их и вернуть ошибку
    update_stmt = update(CartLine.__table__)\
        .values(amount=Product.__table__.c.amount)\
        .where(CartLine.__table__.c.user_id == info.context.current_user.id)\
        .where(CartLine.__table__.c.product_id == Product.__table__.c.id)\
        .where(CartLine.__table__.c.amount > Product.__table__.c.amount)
    update_result = db.session.execute(update_stmt)
    db.session.commit()
    if update_result.rowcount:
        return create_result(status=False, errors=[Errors.NOT_ENOUGH_PRODUCT])

    # Запрос строк корзины, если нет возврат ошибки
    cartlines = db.session.query(CartLine).filter(CartLine.user_id == info.context.current_user.id)
    if not cartlines:
        return create_result(status=False, errors=[Errors.NO_PRODUCTS_IN_CART])

    # запись в таблице orders
    new_order = Order(
        user_id=info.context.current_user.id,
        date=datetime.date.today(),
        delivery_address="TEST",
        completed=False
    )
    db.session.add(new_order)
    db.session.commit()

    # Перенос в таблицу orderlines
    try:
        orderlines = db.session.add_all(
            [OrderLine(**cartline.to_dict(), order_id=new_order.id) for cartline in cartlines]
        )
        cartlines.delete()
    except Exception as ex:
        print(ex)
        db.session.rollback()
        db.session.delete(new_order)
        db.session.commit()
        return create_result(status=False, errors=[Errors.ORDER_CREATION_EXCEPTION])

    db.session.commit()
    return create_result(order=new_order)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_close_order(_obj, _info, **kwargs):
    pass
