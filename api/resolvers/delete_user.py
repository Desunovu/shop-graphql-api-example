from api import db
from api.common import token_required, create_result, Errors, Roles
from api.models import User


@token_required(allowed_roles=[Roles.ADMIN])
def resolve_delete_user(_obj, _info, **kwargs):
    user = db.session.query(User).get(kwargs["id"])
    if not user:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    if user.role == Roles.ADMIN:
        return create_result(status=False, errors=[Errors.ACCESS_DENIED])

    db.session.delete(user)
    db.session.commit()
    return create_result(user=user.to_dict())
