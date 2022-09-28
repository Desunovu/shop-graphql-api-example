from api.extras.auth_wrapper import token_required
from api.extras.common_constants import Errors, Roles
from api.extras.creation_utils import create_result
from api import db
from api.models import Review, Product


@token_required()
def resolve_add_review(_obj, info, **kwargs):
    """Запрос для создания/обновления отзыва к товару"""

    # Проверка существует ли товар
    product = db.session.query(Product).get(kwargs["productId"])
    if not product:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # TODO Проверка был ли у пользователя такой заказ

    # Добавление/обновление отзыва
    review = db.session.query(Review).filter(
        Review.user_id == info.context.current_user.id,
        Review.product_id == kwargs["productId"]
    ).first()

    if review:
        review.update(rating=kwargs["rating"], text=kwargs.get("text"))
        db.session.commit()
        return create_result(review=review)

    review = Review(
        user_id=info.context.current_user.id,
        product_id=kwargs["productId"],
        rating=kwargs["rating"],
        text=kwargs.get("text")
    )
    db.session.add(review)
    db.session.commit()
    return create_result(review=review)


@token_required()
def resolve_remove_review(_obj, info, **kwargs):
    review = db.session.query(Review).get(kwargs["id"])
    if not review:
        return create_result(status=False, errors=[Errors.OBJECT_NOT_FOUND])

    # Если не-админ удаляет не свой отзыв
    if review.product_id != info.context.current_user.id and info.context.current_user.role != Roles.ADMIN:
        return create_result(status=False, errors=[Errors.ACCESS_DENIED])

    db.session.delete(review)
    db.session.commit()
    return create_result()
