from ariadne import ObjectType

from . import admin, cart, signup

mutation = ObjectType("Mutation")

# Admin
mutation.set_field("addProduct", admin.resolve_add_product)
mutation.set_field("updateProduct", admin.resolve_update_product)
mutation.set_field("deleteProduct", admin.resolve_delete_product)
mutation.set_field("addProductImages", admin.resolve_add_product_images)
mutation.set_field("deleteProductImage", admin.resolve_delete_product_image)
mutation.set_field("assignAdmin", admin.resolve_assign_admin)
mutation.set_field("deleteUser", admin.resolve_delete_user)

# Signup
mutation.set_field("createUser", signup.resolve_create_user)

# Cart
mutation.set_field("addProductToCart", cart.resolve_add_product_to_cart)
mutation.set_field("removeProductFromCart", cart.resolve_remove_product_from_cart)
