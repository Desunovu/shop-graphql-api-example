from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Characteristic
from api.extras import token_required, Roles


@token_required(allowed_roles=Roles.ADMIN)
@convert_kwargs_to_snake_case
def resolve_get_characteristics(_obj, info, **kwargs):
    characteristics = db.session.query(Characteristic).all()

    return characteristics
