import os
from minio.deleteobjects import DeleteObject
from api import app, db, minio_client
from api.models import ProductImage

bucket_name = app.config.get("PRODUCTS_BUCKET")


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
