import os

from api import app, db, minio_client
from api.models import ProductImage


def add_product_images(images: dict, product_id: int):
    for file in images:
        # Добавление в таблицу product_images
        product_image = ProductImage(product_id=product_id, image_name="no_name")
        db.session.add(product_image)
        db.session.commit()

        # Сохранение в хранилище minio
        # TODO проверка типа файла, проверка соединения/существования bucket
        file_ext = file.mimetype.split("/")[1]
        file_name = f"product_{product_id}_{product_image.id}.{file_ext}"  # product_1_15.png
        try:
            minio_client.put_object(bucket_name=app.config.get("PRODUCTS_BUCKET"),
                                    object_name=file_name,
                                    data=file,
                                    length=-1,
                                    part_size=10*1024*1024)
        # при ошибке удалить запись из БД
        except Exception as ex:
            print(f"--{ex}--")
            db.session.delete(product_image)
            db.session.commit()
            return False

        # Обновление имени в базе после сохранения изображения
        product_image.image_name = file_name
        db.session.commit()
    return True


def delete_product_images(product_id: int, images_id=None, delete_all=False):
    # Поиск и удаление записей в базе
    if delete_all:
        db.session.query(ProductImage).filter(ProductImage.product_id == product_id).delete()
    else:
        db.session.query(ProductImage).filter(ProductImage.product_id == product_id,
                                              ProductImage.id.in_(images_id)).delete()
    db.session.commit()

    # TODO удаление из хранилища

    return True
