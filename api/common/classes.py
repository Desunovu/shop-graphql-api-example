from .functions import create_error


class Roles:
    ADMIN = "Admin"
    CUSTOMER = "Customer"


class Errors:
    ACCESS_DENIED = create_error(1, "Действие запрещено для вашей роли")
    USER_ALREADY_EXISTS = create_error(2, "Пользователь с данным email уже существует")
    WRONG_EMAIL_OR_PASSWORD = create_error(3, "Неверный email или пароль")
    OBJECT_NOT_FOUND = create_error(4, "Данных по запросу не найдено")
    USER_ALREADY_HAS_ADMIN_ROLE = create_error(5, "Пользователь уже имеет роль Администратор")
    CANT_ADD_MORE_PRODUCTS = create_error(6, "Нельзя добавить больше товаров")
    IMAGES_NOT_UPLOADED = create_error(7, "При загрузке изображений товара произошла ошибка")
    CATEGORIES_NOT_SET = create_error(8, "При задании категорий товара произошла ошибка")
    CATEGORIES_NOT_REMOVED = create_error(8, "При удалении категорий товара произошла ошибка")


class UnauthorizedError(Exception):
    extension = {"code": 401}


class ForbiddenError(Exception):
    extension = {"code": 403}
