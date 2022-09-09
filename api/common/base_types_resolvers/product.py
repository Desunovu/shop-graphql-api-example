def resolve_product_id(product_obj, _info):
    return product_obj.id


def resolve_product_name(product_obj, _info):
    return product_obj.name


def resolve_product_price(product_obj, _info):
    return product_obj.price


def resolve_product_amount(product_obj, _info):
    return product_obj.amount


def resolve_product_description(product_obj, _info):
    return product_obj.description
