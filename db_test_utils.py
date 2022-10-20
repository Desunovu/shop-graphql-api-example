import random
import string
from werkzeug.security import generate_password_hash

from api import db
from api.models import *


def create_user():
    user = User(
        email="".join(random.choice(string.ascii_lowercase) for _ in range(5)) +
              "@" + "".join(random.choice(string.ascii_lowercase) for _ in range(4)) +
              ".ru",
        password=generate_password_hash("password"),
        first_name="".join(random.choice(string.ascii_lowercase) for _ in range(7)),
        last_name="".join(random.choice(string.ascii_lowercase) for _ in range(7))
    )
    db.session.add(user)
    db.session.commit()


def create_category():
    category = Category(
        name="".join(random.choices(string.ascii_lowercase, k=8))
    )
    db.session.add(category)
    db.session.commit()


def create_product():
    product = Product(
        name="".join(random.choice(string.ascii_lowercase) for _ in range(7)),
        price=random.randint(10, 10000),
        amount=random.randint(1, 100),
        description=f"Description {random.randint(1, 999)}"
    )
    db.session.add(product)
    db.session.commit()

    random_category = random.choice(db.session.query(Category).all())
    product_category = ProductCategory(
        product_id=product.id,
        category_id=random_category.id
    )
    db.session.add(product_category)
    db.session.commit()
