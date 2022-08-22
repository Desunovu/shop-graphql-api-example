from werkzeug.security import generate_password_hash

from api.common.common import create_result
from api.common.enum_types import ErrorEnum, RoleEnum
from api.models import User
from api import db


def resolve_create_user(obj, info, **kwargs):
    user = db.session.query(User).filter(User.email == kwargs["email"]).first()
    if user:
        return create_result(status=False, errors=[ErrorEnum.USER_ALREADY_EXISTS.value])

    user = User(**kwargs, role=RoleEnum.CUSTOMER.value)
    user.password = generate_password_hash(kwargs["password"])
    db.session.add(user)
    db.session.commit()
    return create_result(user=user.to_dict())
