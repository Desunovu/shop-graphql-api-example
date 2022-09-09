from api import db
from api.common import token_required, create_result, Errors
from api.models import Product


@token_required()
def resolve_get_product(_obj, _info, **kwargs):
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    return create_result(product=product)


@token_required()
def resolve_get_products(_obj, _info):
    products = db.session.query(Product).all()

    return create_result(products=[product for product in products])
