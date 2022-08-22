from werkzeug.security import generate_password_hash

from api.common.common import create_result, CUSTOMER_ROLE, USER_ALREADY_EXIST_ERROR
from api.models import User, Role
from api import db


def resolve_create_user(obj, info, **kwargs):
    user = db.session.query(User).filter(User.email == kwargs["email"]).first()
    if user:
        return create_result(status=False, errors=[USER_ALREADY_EXIST_ERROR])
    # TODO проверить необходимость исключений
    else:
        user = User(**kwargs)
        user.password = generate_password_hash(kwargs["password"])
        user.role_id = db.session.query(Role.id).filter(Role.name == CUSTOMER_ROLE)
        db.session.add(user)
        db.session.commit()
        return create_result(**user.to_dict())
