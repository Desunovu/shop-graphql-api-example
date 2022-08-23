from api import db
from api.common import token_required, create_result, Roles, Errors
from api.models import Product


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_update_product(_obj, _info, **kwargs):
    """
    Админ-запрос для изменения товара
    Обязательные параметры
        id: str
    Возвращает
        ProductResult (def in scheme)
    """
    # stmt = db.update(Product).where(Product.id == kwargs["id"]).values(**kwargs)
    # result = db.session.execute(stmt)
    # db.session.commit()
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    product.update(**kwargs)
    db.session.commit()
    return create_result(product=product.to_dict())
