from api import db
from api.models import OrderLine


def resolve_order_id(order_obj, _info):
    return order_obj.id


def resolve_order_user_id(order_obj, _info):
    return order_obj.user_id


def resolve_order_creation_date(order_obj, _info):
    # возвращает datetime.date, преобразуется к строке в serializer в schema.py
    return order_obj.creation_date


def resolve_order_completion_date(order_obj, _info):
    return order_obj.completion_date


def resolve_order_delivery_address(order_obj, _info):
    return order_obj.delivery_address


def resolve_order_status(order_obj, _info):
    return order_obj.status


def resolve_order_lines(order_obj, _info):
    orderlines = db.session.query(OrderLine).filter(OrderLine.order_id == order_obj.id).all()
    return orderlines
