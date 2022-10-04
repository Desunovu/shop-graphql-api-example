from api import db
from api.extras.common_constants import Roles
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey


class BaseMixin(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=Roles.CUSTOMER)


class Product(BaseMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default="DefaultProductName")
    price = Column(Integer, nullable=False, default=0)
    amount = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=False, default="DefaultDescription")


class Category(BaseMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ProductImage(BaseMixin):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    image_name = Column(String, nullable=False)
    is_preview = Column(Boolean, nullable=False, default=False)


class ProductCategory(BaseMixin):
    __tablename__ = "product_categories"

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)


class CartLine(BaseMixin):
    __tablename__ = "cartlines"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    amount = Column(Integer, nullable=False, default=1)


class Review(BaseMixin):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False, default=5)
    text = Column(String)


class Order(BaseMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    date = Column(Date, nullable=False)
    delivery_address = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)


class OrderLine(BaseMixin):
    __tablename__ = "orderlines"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Integer, nullable=False)
