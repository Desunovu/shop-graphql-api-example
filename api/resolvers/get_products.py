from api.common import token_required, create_result, Errors
from api.models import Product
from api import db


@token_required()
def resolve_get_products(_obj, _info):
    products = db.session.query(Product).all()

    return create_result(products=[product.to_dict() for product in products])
