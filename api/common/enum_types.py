from enum import Enum

from api.common.common import create_error


class RoleEnum(Enum):
    ADMIN = "Admin"
    CUSTOMER = "Customer"

    def __repr__(self):
        return self.value


class ErrorEnum(Enum):
    ACCESS_DENIED = create_error(1, "Нет доступа")
    USER_ALREADY_EXISTS = create_error(2, "Пользователь уже существует")
    WRONG_EMAIL_OR_PASSWORD = create_error(3, "Неверный email или пароль")
    OBJECT_NOT_FOUND = create_error(4, "Данных по запросу не найдено")