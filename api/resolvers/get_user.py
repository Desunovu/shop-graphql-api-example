from flask import session

from api.common.common import create_result
from api.common.auth import token_required
from api.common.enum_types import ErrorEnum, RoleEnum
from api.models import User
from api import app, db


@token_required()
def resolve_get_user(_obj, _info, **kwargs):
    user_id = session["current_user"]["id"]
    if "id" in kwargs:
        user_id = kwargs["id"]
        if session["current_user"]["role"] != RoleEnum.ADMIN.value:
            return create_result(status=False, errors=[ErrorEnum.ACCESS_DENIED.value])

    user = db.session.query(User).get(user_id)
    if not user:
        return create_result(status=False, errors=[ErrorEnum.OBJECT_NOT_FOUND.value])
    return create_result(user=user.to_dict())
