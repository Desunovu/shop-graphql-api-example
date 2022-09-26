from api import db
from api.extras import token_required, create_result, Errors
from api.models import Product, ProductCategory


@token_required()
def resolve_get_product(_obj, _info, **kwargs):
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    return create_result(product=product)


@token_required()
def resolve_get_products(_obj, _info, **kwargs):
    # Выражение
    stmt = db.session.query(Product)

    # Присутствует фильтр по категории
    try:
        stmt = stmt.join(ProductCategory, Product.id == ProductCategory.product_id).filter(
            ProductCategory.category_id == kwargs["input"]["filter"]["categoryId"]
        )
    except KeyError:
        pass

    # Поиск в БД
    products = stmt.all()
    if not products:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    return create_result(products=[product for product in products])
