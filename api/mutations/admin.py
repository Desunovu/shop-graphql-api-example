from api import db
from api.common import token_required, create_result, Roles, Errors
from api.models import Product, User


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_add_product(_obj, _info, **kwargs):
    """
    Админ-запрос для добавления товара
    Обязательные параметры
        id: str
    Возвращает
        ProductResult: dict
    """
    product = Product(**kwargs)
    db.session.add(product)
    db.session.commit()
    return create_result(product=product.to_dict())


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_update_product(_obj, _info, **kwargs):
    """
    Админ-запрос для изменения товара
    Возвращает
        ProductResult: dict
    """
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    product.update(**kwargs)
    db.session.commit()
    return create_result(product=product.to_dict())


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_product(_obj, _info, **kwargs):
    """
    Админ-запрос для удаления товара
    Возвращает
        ProductResult: dict
    """
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    db.session.delete(product)
    db.session.commit()
    return create_result(product=product.to_dict())


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_assign_admin(_obj, _info, **kwargs):
    """
    Админ-запрос для назначения администратора
    Возвращает
        UserResult: dict
    """
    user_to_be_admin = db.session.query(User).get(kwargs["id"])
    if not user_to_be_admin:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])
    if user_to_be_admin.role == Roles.ADMIN:
        return create_result(status=False, errors=[Errors.USER_ALREADY_HAS_ADMIN_ROLE])

    user_to_be_admin.update(role=Roles.ADMIN)
    db.session.commit()
    return create_result(user=user_to_be_admin)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_user(_obj, _info, **kwargs):
    """
    Админ-запрос для удаления пользователя
    Возвращает
        UserResult: dict
    """
    user = db.session.query(User).get(kwargs["id"])
    if not user:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    if user.role == Roles.ADMIN:
        return create_result(status=False, errors=[Errors.ACCESS_DENIED])

    db.session.delete(user)
    db.session.commit()
    return create_result(user=user.to_dict())
