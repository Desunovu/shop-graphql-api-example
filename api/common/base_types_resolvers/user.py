# В resolver верхнего уровня возвращается объект api.models.User


def resolve_user_id(user_obj, _info):
    return user_obj.id


def resolve_user_name(user_obj, _info):
    return user_obj.name


def resolve_user_email(user_obj, _info):
    return user_obj.email


def resolve_user_role(user_obj, _info):
    return user_obj.role


def resolve_avatar_url(user_obj, _info):
    return "test functionality"
