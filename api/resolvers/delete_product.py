from api import db
from api.common import create_result, token_required, Roles, Errors
from api.models import Product


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_product(_obj, _info, **kwargs):
    """
    Админ-запрос для удаления товара
    Обязательные параметры
        id: str
    Возвращает
        ProductResult (def in schema)
    """
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    db.session.delete(product)
    db.session.commit()
    return create_result(product=product.to_dict())
