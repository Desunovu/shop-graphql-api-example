from ariadne import ObjectType

from . import user, product, cartline, category

user_type = ObjectType("User")
user_type.set_field("id", user.resolve_user_id)
user_type.set_field("name", user.resolve_user_name)
user_type.set_field("email", user.resolve_user_email)
user_type.set_field("role", user.resolve_user_role)
user_type.set_field("avatarUrl", user.resolve_avatar_url)

product_type = ObjectType("Product")
product_type.set_field("id", product.resolve_product_id)
product_type.set_field("name", product.resolve_product_name)
product_type.set_field("price", product.resolve_product_price)
product_type.set_field("amount", product.resolve_product_amount)
product_type.set_field("description", product.resolve_product_description)
product_type.set_field("images", product.resolve_product_images)
product_type.set_field("categories", product.resolve_product_categories)

cartline_type = ObjectType("CartLine")
cartline_type.set_field("product", cartline.resolve_cartine_product)
cartline_type.set_field("amount", cartline.resolve_cartline_amount)

category_type = ObjectType("Category")
category_type.set_field("id", category.resolve_category_id)
category_type.set_field("name", category.resolve_category_name)
