# В resolver верхнего уровня возвращается объект api.models.Review

def resolve_review_id(review_obj, _info):
    return review_obj.id


def resolve_review_user_id(review_obj, _info):
    return review_obj.user_id


def resolve_review_product_id(review_obj, _info):
    return review_obj.product_id


def resolve_review_rating(review_obj, _info):
    return review_obj.rating


def resolve_review_text(review_obj, _info):
    return review_obj.text
