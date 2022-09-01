import os

from api import app, db
from api.models import ProductImage


def add_product_images(images: dict, product_id: int):
    for file in images:
        # Добавление в таблицу product_images
        product_image = ProductImage(product_id=product_id, image_name="no_name")
        db.session.add(product_image)
        db.session.commit()

        # Сохранение в хранилище
        # TODO проверка типа файла
        file_ext = file.mimetype.split("/")[1]
        file_name = f"product_{product_id}_{product_image.id}.{file_ext}"  # product_1_15.png
        file.save(os.path.join(app.config["APP_DIR"], app.config['UPLOAD_FOLDER'], file_name))

        # Обновление имени в базе
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
