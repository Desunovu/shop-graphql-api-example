import os

from ariadne import load_schema_from_path, make_executable_schema, upload_scalar

from api.mutations import mutation
from api.queries import query

type_defs = load_schema_from_path(
    os.path.join(os.path.dirname(__file__), "schema")
)

schema = make_executable_schema(type_defs, query, mutation, upload_scalar)
