import datetime
from ariadne import convert_kwargs_to_snake_case

from api import db
from api.extras import token_required, create_result, create_simple_result, Errors
from api.models import CartLine, Product, FavoriteProduct


@token_required()
@convert_kwargs_to_snake_case
def resolve_product_add_to_favorites(_obj, info, **kwargs):
    product = db.session.query(Product).get(kwargs["product_id"])
    if not product:
        create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    db.session.add(
        FavoriteProduct(
            user_id=info.context.current_user.id,
            product_id=product.id,
            addition_date=datetime.date.today()
        )
    )
    db.session.commit()
    return create_result(product=product)

