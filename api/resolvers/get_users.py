from api import db
from api.common import create_result, token_required, Roles
from api.models import User


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_get_users(_obj, _info, **kwargs):
    users = db.session.query(User).all()

    return create_result(users=[user.to_dict() for user in users])
