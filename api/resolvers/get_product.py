from api.common import token_required, create_result, Errors
from api.models import Product
from api import db


@token_required()
def resolve_get_product(_obj, _info, **kwargs):
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    return create_result(product=product.to_dict())
