from sorcery import dict_of


def create_error(code=0, message="Нет доступа"):
    return dict_of(code, message)


def create_result(status=True, errors=None, **kwargs):
    if errors is None:
        errors = []
    result = {
        "status": status,
        "errors": errors
    }
    return result | kwargs

