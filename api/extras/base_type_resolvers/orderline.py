from api import db
from api.models import Product


def resolve_orderline_amount(orderline_obj, _info):
    return orderline_obj.amount


def resolve_orderline_product(orderline_obj, _info):
    product = db.session.query(Product).filter(Product.id == orderline_obj.product_id).first()
    return product
