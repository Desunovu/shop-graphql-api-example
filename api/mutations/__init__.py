from ariadne import ObjectType

from . import admin, cart, signup, review, order, user

mutation = ObjectType("Mutation")

# Admin
mutation.set_field("addProduct", admin.resolve_add_product)
mutation.set_field("updateProduct", admin.resolve_update_product)
mutation.set_field("deleteProduct", admin.resolve_delete_product)
mutation.set_field("assignAdmin", admin.resolve_assign_admin)
mutation.set_field("deleteUser", admin.resolve_delete_user)
mutation.set_field("addCategory", admin.resolve_add_category)
mutation.set_field("removeCategory", admin.resolve_remove_category)

# Signup/User
mutation.set_field("createUser", signup.resolve_create_user)
mutation.set_field("updateUser", user.resolve_update_user)


# Cart
mutation.set_field("addProductToCart", cart.resolve_add_product_to_cart)
mutation.set_field("removeProductFromCart", cart.resolve_remove_product_from_cart)

# Review
mutation.set_field("addReview", review.resolve_add_review)
mutation.set_field("removeReview", review.resolve_remove_review)

# Order
mutation.set_field("createOrder", order.resolve_create_order)
mutation.set_field("updateOrderStatus", order.resolve_update_order_status)
