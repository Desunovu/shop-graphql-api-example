# obj = [cartline, product]

def resolve_cartine_product(obj, _info):
    return obj[1]


def resolve_cartline_amount(obj, _info):
    return obj[0].amount
