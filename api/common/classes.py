from .functions import create_error


class Roles:
    ADMIN = "Admin"
    CUSTOMER = "Customer"


class Errors:
    ACCESS_DENIED = create_error(1, "Действие запрещено для вашей роли")
    USER_ALREADY_EXISTS = create_error(2, "Пользователь с данным email уже существует")
    WRONG_EMAIL_OR_PASSWORD = create_error(3, "Неверный email или пароль")
    OBJECT_NOT_FOUND = create_error(4, "Данных по запросу не найдено")


class UnauthorizedError(Exception):
    extension = {"code": 401}


class ForbiddenError(Exception):
    extension = {"code": 403}
