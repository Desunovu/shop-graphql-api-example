from api.common import token_required, create_result, Roles
from api.models import Product
from api import db


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_add_product(_obj, _info, **kwargs):
    product = Product(**kwargs)
    db.session.add(product)
    db.session.commit()
    return create_result(product=product.to_dict())
