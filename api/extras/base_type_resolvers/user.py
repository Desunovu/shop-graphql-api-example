# В resolver верхнего уровня возвращается объект api.models.User

def resolve_user_id(user_obj, _info):
    return user_obj.id


def resolve_user_email(user_obj, _info):
    return user_obj.email


def resolve_user_role(user_obj, _info):
    return user_obj.role


def resolve_user_avatar_url(user_obj, _info):
    return "TEST NONE"


def resolve_user_first_name(user_obj, _info):
    return user_obj.first_name


def resolve_user_last_name(user_obj, _info):
    return user_obj.last_name


def resolve_user_address(user_obj, _info):
    return user_obj.address


def resolve_user_phone_number(user_obj, _info):
    return user_obj.phone_number
