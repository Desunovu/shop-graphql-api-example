# В resolver верхнего уровня возвращается api.models.Product

from api.extras import create_simple_result
from api import db
from api.models import Category, ProductImage, ProductCategory


def resolve_product_id(product_obj, _info):
    return product_obj.id


def resolve_product_name(product_obj, _info):
    return product_obj.name


def resolve_product_price(product_obj, _info):
    return product_obj.price


def resolve_product_amount(product_obj, _info):
    return product_obj.amount


def resolve_product_description(product_obj, _info):
    return product_obj.description


def resolve_product_categories(product_obj, _info):
    # Поиск категорий по product.id
    categories = db.session.query(Category).join(ProductCategory).filter(
        ProductCategory.product_id == product_obj.id).all()

    # Создание словаря согласно определению типа Category в схеме
    return [create_simple_result(
                id=category.id,
                name=category.name
            ) for category in categories]


def resolve_product_images(product_obj, _info):
    # Поиск изображений по product.id
    images = db.session.query(ProductImage).filter(
        ProductImage.product_id == product_obj.id).all()

    # Создание словаря согласно определению типа Image в схеме
    return [create_simple_result(
                id=image.id,
                filename=image.image_name,
                url="TEST FUNC",
                isPreview=image.is_preview
            ) for image in images]
