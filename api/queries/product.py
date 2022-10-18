from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import token_required, create_result, Errors
from api.extras.resolver_utils import query_pagination, query_sort
from api.models import Product


@token_required()
def resolve_get_product(_obj, _info, **kwargs):
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    return create_result(product=product)


@token_required()
@convert_kwargs_to_snake_case
def resolve_get_products(_obj, _info, **kwargs):
    # Выражение
    query = db.session.query(Product)
    query = query_sort(query=query, resolver_args=kwargs)
    query = query_pagination(query=query, resolver_args=kwargs)

    products = query.all()

    return create_result(products=products)
