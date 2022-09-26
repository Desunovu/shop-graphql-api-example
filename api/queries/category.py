from api import db
from api.extras import create_result, token_required, Errors, Roles
from api.models import Category


@token_required()
def resolve_get_categories(_obj, _info, **kwargs):
    categories = db.session.query(Category).all()
    return create_result(categories=categories)
