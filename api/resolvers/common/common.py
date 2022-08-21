from sorcery import dict_of

CUSTOMER_ROLE = "Customer"
CUSTOMER_ACCESS_LEVEL = 0


def create_error(code=0, message="Нет доступа"):
    return dict_of(code, message)


ACCESS_DENIED_ERROR = create_error(1, "Нет доступа")
USER_ALREADY_EXIST_ERROR = create_error(2, "Пользователь уже существует")
WRONG_EMAIL_OR_PASSWORD_ERROR = create_error(3, "Неверный email или пароль")


def create_result(status=True, errors=None, **kwargs):
    if errors is None:
        errors = []
    result = {
        "status": status,
        "errors": errors
    }
    return result | kwargs
