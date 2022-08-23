from api import db
from api.common import token_required, create_result
from api.models import Product


@token_required()
def resolve_get_products(_obj, _info):
    products = db.session.query(Product).all()

    return create_result(products=[product.to_dict() for product in products])
