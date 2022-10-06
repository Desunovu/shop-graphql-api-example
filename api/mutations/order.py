import datetime
from sqlalchemy import update

from api import db
from api.models import CartLine, OrderLine, Order, User, Product
from api.extras import token_required, create_result, create_error, OrderStatus, Errors, Roles, NotEnoughProduct


@token_required()
def resolve_create_order(_obj, info, **kwargs):
    # Выражение для исправления корзины в соответствии с доступностью товаров
    update_cartlines_stmt = update(CartLine.__table__)\
        .values(amount=Product.__table__.c.amount)\
        .where(CartLine.__table__.c.user_id == info.context.current_user.id)\
        .where(CartLine.__table__.c.product_id == Product.__table__.c.id)\
        .where(CartLine.__table__.c.amount > Product.__table__.c.amount)\
        .execution_options(synchronize_session="fetch")

    # Выражение для переноса товаров из доступных в зарезервированные
    update_products_stmt = update(Product.__table__)\
        .values(
            amount=Product.__table__.c.amount - OrderLine.__table__.c.amount,
            reserved=Product.__table__.c.reserved + OrderLine.__table__.c.amount
        )\
        .where(OrderLine.__table__.c.user_id == info.context.current_user.id)\
        .where(OrderLine.__table__.c.product_id == Product.__table__.c.id) \
        .execution_options(synchronize_session="fetch")

    # Получить недоступные к заказу строки и разрешенное количество, чтобы исправить их и вернуть ошибку
    update_result = db.session.execute(update_cartlines_stmt)
    db.session.commit()  # TODO протестировать необходиомсть
    if update_result.rowcount:
        return create_result(status=False, errors=[Errors.NOT_ENOUGH_PRODUCT])

    # Запрос строк корзины, если нет возврат ошибки
    cartlines = db.session.query(CartLine).filter(CartLine.user_id == info.context.current_user.id)
    if not cartlines:
        return create_result(status=False, errors=[Errors.NO_PRODUCTS_IN_CART])

    # запись в таблице orders
    new_order = Order(
        user_id=info.context.current_user.id,
        creation_date=datetime.date.today(),
        status=OrderStatus.PROCESSING
    )
    new_order.delivery_address = info.context.current_user.address
    if "deliveryAddress" in kwargs:
        new_order.delivery_address = kwargs["deliveryAddress"]
    db.session.add(new_order)
    db.session.commit()

    # Перенос в таблицу orderlines, очистка корзины, резервация, уменьшение доступного количества товара
    # TODO TRY-EXCEPT
    db.session.add_all(
        [OrderLine(**cartline.to_dict(), order_id=new_order.id) for cartline in cartlines]
    )
    db.session.commit()
    print(db.session.execute(update_products_stmt).rowcount)
    cartlines.delete()

    db.session.commit()
    return create_result(order=new_order)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_update_order_status(_obj, info, **kwargs):
    new_status = kwargs["orderStatus"]

    # Выражение для уменьшения поля products.reserved при отправке
    update_shipped_products_stmt = update(Product.__table__)\
        .values(
            reserved=Product.__table__.c.reserved - OrderLine.__table__.c.amount
        )\
        .where(OrderLine.__table__.c.user_id == info.context.current_user.id)\
        .where(OrderLine.__table__.c.product_id == Product.__table__.c.id) \
        .execution_options(synchronize_session="fetch")

    # Выражение для изменения products при отмене заказа
    update_cancelled_products_stmt = update(Product.__table__) \
        .values(
            amount=Product.__table__.c.amount + OrderLine.__table__.c.amount,
            reserved=Product.__table__.c.reserved - OrderLine.__table__.c.amount
        ) \
        .where(OrderLine.__table__.c.user_id == info.context.current_user.id) \
        .where(OrderLine.__table__.c.product_id == Product.__table__.c.id) \
        .execution_options(synchronize_session="fetch")

    # Поиск заказа, вернуть ошибку если заказа не существует
    order = db.session.query(Order).get(kwargs["id"])
    if not order:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # [PROCESSING] (заглушка)
    if new_status == OrderStatus.PROCESSING:
        return create_result(status=False, errors=[Errors.WRONG_ORDER_STATUS])

    # [SHIPPING] возможен после processing, очищаются строки резерва
    if new_status == OrderStatus.SHIPPING:
        if order.status != OrderStatus.PROCESSING:
            return create_result(status=False, errors=[Errors.WRONG_ORDER_STATUS])
        db.session.execute(update_shipped_products_stmt)
        order.status = new_status

    # [DONE] возможен после shipping
    if new_status == OrderStatus.DONE:
        if order.status != OrderStatus.SHIPPING:
            return create_result(status=False, errors=[Errors.WRONG_ORDER_STATUS])
        order.status = new_status
        order.completion_date = datetime.date.today()

    # [CANCELLED] возможен после processing, вернуть товары из резерва в доступные
    if new_status == "CANCELLED":
        if order.status != OrderStatus.PROCESSING:
            return create_result(status=False, errors=[Errors.WRONG_ORDER_STATUS])
        db.session.execute(update_cancelled_products_stmt)
        order.status = new_status
        order.completion_date = datetime.date.today()

    db.session.commit()
    return create_result(order=order)
