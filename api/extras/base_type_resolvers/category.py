import api.models


def resolve_category_id(category_obj: api.models.Category, _info) -> int:
    return category_obj.id


def resolve_category_name(category_obj: api.models.Category, _info) -> str:
    return category_obj.name
