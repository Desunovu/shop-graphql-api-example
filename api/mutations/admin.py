import os

from api import app, db
from api.common import token_required, create_result, Roles, Errors
from api.common.resolvers_help_functions import add_product_images, delete_product_images, add_product_categories, remove_product_categories
from api.models import Product, User, Category


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_add_product(_obj, _info, **kwargs):
    """Админ-запрос для добавления товара"""
    self_status = True  # Флаг безошибочности выполнения
    errors = []

    # Создание записи в таблице products
    product = Product(**kwargs)
    db.session.add(product)
    db.session.commit()

    # Добавление изображений
    if "images" in kwargs:
        status = add_product_images(images=kwargs.get("images"), product_id=product.id)
        if not status:
            errors.append(Errors.IMAGES_NOT_UPLOADED)

    # Добавление категорий
    if "categoryIds" in kwargs:
        status = add_product_categories(category_ids=kwargs.get("categoryIds"), product_id=product.id)
        if not status:
            errors.append(Errors.CATEGORIES_NOT_SET)

    return create_result(status=self_status, errors=errors, product=product)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_update_product(_obj, _info, **kwargs):
    """Админ-запрос для изменения товара"""
    errors = []

    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # Обновление записи в таблице products
    product.update(**kwargs)
    db.session.commit()

    # Добавление изображений
    if kwargs.get("addImages"):
        status = add_product_images(images=kwargs.get("addImages"), product_id=product.id)
        if not status:
            errors.append(Errors.IMAGES_NOT_UPLOADED)

    # Удаление изображений
    if kwargs.get("removeImagesById"):
        status = delete_product_images(product_id=product.id, images_id=kwargs["removeImagesById"])
        if not status:
            errors.append(Errors.OBJECT_NOT_FOUND)
    if kwargs.get("deleteAllImages"):
        status = delete_product_images(product_id=product.id, delete_all=True)
        if not status:
            errors.append(Errors.OBJECT_NOT_FOUND)

    # Добавление/удаление категорий
    if "addCategoriesById" in kwargs:
        status = add_product_categories(category_ids=kwargs.get("addCategoriesById"), product_id=product.id)
        if not status:
            errors.append(Errors.CATEGORIES_NOT_SET)
    if "removeCategoriesById" in kwargs:
        status = remove_product_categories(category_ids=kwargs.get("removeCategoriesById"), product_id=product.id)
        if not status:
            errors.append(Errors.CATEGORIES_NOT_REMOVED)
    if "removeAllCategories" in kwargs:
        status = remove_product_categories(product_id=product.id, remove_all=True)
        if not status:
            errors.append(Errors.CATEGORIES_NOT_REMOVED)

    return create_result(errors=errors, product=product)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_product(_obj, _info, **kwargs):
    """
    Админ-запрос для удаления товара
    Возвращает ProductResult
    """
    # TODO удаление изображений
    # TODO удаление категорий
    product = db.session.query(Product).get(kwargs["id"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    db.session.delete(product)
    db.session.commit()
    return create_result(product=product)


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


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_add_category(_obj, _info, **kwargs):
    """Админ-запрос для добавления категории"""
    category_name = kwargs.get("name")
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()
    return create_result(category=category)


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_remove_category(_obj, _info, **kwargs):
    """Админ-запрос для удаления категории"""
    category = db.session.query(Category).get(kwargs["id"])
    db.session.delete(category)
    db.session.commit()
    return create_result()
