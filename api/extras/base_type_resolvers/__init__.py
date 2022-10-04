from ariadne import ObjectType

from . import user, product, cartline, category, review, order, orderline

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
product_type.set_field("reviews", product.resolve_product_reviews)

cartline_type = ObjectType("CartLine")
cartline_type.set_field("product", cartline.resolve_cartine_product)
cartline_type.set_field("amount", cartline.resolve_cartline_amount)

category_type = ObjectType("Category")
category_type.set_field("id", category.resolve_category_id)
category_type.set_field("name", category.resolve_category_name)

review_type = ObjectType("Review")
review_type.set_field("id", review.resolve_review_id)
review_type.set_field("userId", review.resolve_review_user_id)
review_type.set_field("productId", review.resolve_review_product_id)
review_type.set_field("rating", review.resolve_review_rating)
review_type.set_field("text", review.resolve_review_text)

order_type = ObjectType("Order")
order_type.set_field("id", order.resolve_order_id)
order_type.set_field("userId", order.resolve_order_user_id)
order_type.set_field("date", order.resolve_order_date)
order_type.set_field("deliveryAddress", order.resolve_order_delivery_address)
order_type.set_field("completed", order.resolve_order_completed)
order_type.set_field("orderLines", order.resolve_order_lines)

orderline_type = ObjectType("OrderLine")
orderline_type.set_field("amount", orderline.resolve_orderline_amount)
orderline_type.set_field("product", orderline.resolve_orderline_product)
