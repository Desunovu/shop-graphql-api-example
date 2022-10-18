from minio.deleteobjects import DeleteObject
from sqlalchemy import desc
from ariadne import convert_camel_case_to_snake

from api import app, db, minio_client
from api.models import ProductImage, ProductCategory, ProductCharacteristic

bucket_name = app.config.get("PRODUCTS_BUCKET")


def query_pagination(query, resolver_args):
    if "pagination" not in resolver_args:
        return query

    offset = resolver_args["pagination"]["offset"]
    limit = resolver_args["pagination"]["limit"]
    return query.limit(limit).offset(offset)


def query_sort(query, resolver_args):
    if "sort" not in resolver_args:
        return query

    field = convert_camel_case_to_snake(resolver_args["sort"]["field"])
    order = resolver_args["sort"]["order"]
    if order == "DESC":
        return query.order_by(desc(field))
    return query.order_by(field)


def add_product_images(images: dict, product_id: int):
    # TODO реализовать без цикла
    for file in images:
        # Добавление в таблицу product_images
        product_image = ProductImage(product_id=product_id, image_name="no_name")
        db.session.add(product_image)
        db.session.commit()

        # Сохранение в хранилище minio
        # TODO проверка типа файла
        file_ext = file.mimetype.split("/")[1]
        file_name = f"product_{product_id}_{product_image.id}.{file_ext}"  # product_1_15.png
        errors = minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=file,
            length=-1,
            part_size=10 * 1024 * 1024
        )

        # Обновление имени в базе после сохранения изображения
        product_image.image_name = file_name
        db.session.commit()
    return True


def delete_product_images(product_id: int, images_id=None, delete_all=False):
    # Выражение для запроса
    if delete_all:
        stmt = db.session.query(ProductImage).filter(
            ProductImage.product_id == product_id
        )
    else:
        stmt = db.session.query(ProductImage).filter(
            ProductImage.product_id == product_id,
            ProductImage.id.in_(images_id)
        )

    # Поиск в базе и удаление из хранилища
    product_images = stmt.all()
    objects_to_delete = [DeleteObject(product_image.image_name) for product_image in product_images]
    errors = minio_client.remove_objects(bucket_name=bucket_name, delete_object_list=objects_to_delete)
    for error in errors:
        print(f"error with {error}")

    # Удаление из базы
    stmt.delete()
    db.session.commit()

    return True


def add_product_categories(product_id, category_ids=None):
    try:
        product_categories = [ProductCategory(product_id=product_id, category_id=category_id) for category_id in
                              category_ids]
        db.session.bulk_save_objects(product_categories)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def remove_product_categories(product_id, category_ids=None, remove_all=False, ):
    # Выражение для запроса
    if remove_all:
        stmt = db.session.query(ProductCategory).filter(ProductCategory.product_id == product_id)
    else:
        stmt = db.session.query(ProductCategory).filter(
            ProductCategory.product_id == product_id,
            ProductCategory.category_id.in_(category_ids)
        )

    # Удаление записей в БД
    try:
        stmt.delete()
        db.session.commit()
        return True
    except Exception:
        return False


def get_cart_total(cartline_and_product_list=None):
    total = sum([cartline.amount * product.price for cartline, product in cartline_and_product_list])

    return total


def add_product_characteristics(product_id, characteristic_ids=None):
    try:
        product_characteristics = [
            ProductCharacteristic(
                product_id=product_id,
                characteristic_id=characteristic_id,
                value=None
            )
            for characteristic_id
            in characteristic_ids
        ]

        db.session.add_all(product_characteristics)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


def remove_product_characteristics(product_id, characteristic_ids=None, remove_all=False):
    # Выражение для запроса
    if remove_all:
        stmt = db.session.query(ProductCharacteristic).filter(ProductCharacteristic.product_id == product_id)
    else:
        stmt = db.session.query(ProductCharacteristic).filter(
            ProductCharacteristic.characteristic_id.in_(characteristic_ids)
        )

    # Удаление записей в БД
    try:
        stmt.delete()
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
