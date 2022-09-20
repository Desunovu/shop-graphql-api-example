from ariadne import ObjectType

from . import cart, product, signin, user, category

query = ObjectType("Query")

# Signin
query.set_field("loginUser", signin.resolve_login_user)

# Cart
query.set_field("getCart", cart.resolve_get_cart)

# User/Users
query.set_field("getUser", user.resolve_get_user)
query.set_field("getUsers", user.resolve_get_users)

# Product/Products
query.set_field("getProduct", product.resolve_get_product)
query.set_field("getProducts", product.resolve_get_products)

# Category/Categories
query.set_field("getCategories", category.resolve_get_categories)
