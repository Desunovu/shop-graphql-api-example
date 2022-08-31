import os

from api import app, db
from api.common import token_required, create_result, Roles, Errors
from api.models import Product, ProductImage, User


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
def resolve_upload_product_images(_obj, _info, **kwargs):
    """
    Админ-запрос для загрузки изображений товара
    Возвращает
        ProductResult: dict
    """
    product = db.session.query(Product).get(kwargs.get("product_id"))
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    for file in kwargs["images"]:
        product_image = ProductImage(product_id=product.id)
        db.session.add(product_image)
        db.session.commit()
        filename = str(product_image.id) + ".jpeg"
        file.save(os.path.join(app.config["APP_DIR"], app.config['UPLOAD_FOLDER'], filename))

    return create_result()


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_product_images(_obj, _info, **kwargs):
    """
    Админ-запрос для удаления изображений у товара
    Возвращает
        ProductResult: dict
    """
    product = db.session.query(Product).get(kwargs.get("product_id"))
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    if kwargs.get("all"):
        db.session.query(ProductImage).filter(ProductImage.product_id == product.id).delete()
        db.session.commit()
        return create_result()

    return create_result()


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
