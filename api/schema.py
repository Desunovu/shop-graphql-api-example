import os

from ariadne import load_schema_from_path, make_executable_schema, upload_scalar

from api.mutations import mutation
from api.queries import query
from api.common.base_types_resolvers import user_type, product_type, cartline_type

type_defs = load_schema_from_path(
    os.path.join(os.path.dirname(__file__), "schema")
)

schema = make_executable_schema(type_defs, [query, mutation, user_type, product_type, cartline_type, upload_scalar])
