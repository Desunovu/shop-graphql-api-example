from api import db
from api.models import Characteristic, ProductCharacteristic


def resolve_characteristic_id(characteristic_obj, _info):
    return characteristic_obj.id


def resolve_characteristic_name(characterictic_obj, _info):
    return characterictic_obj.name


# OBJ: (ProductCharacteristic, Characteristic)
def resolve_product_characteristic_name(product_characteristic_objects, _info):
    return product_characteristic_objects[1].name


# OBJ: (ProductCharacteristic, Characteristic)
def resolve_product_characteristic_value(product_characteristic_objects, _info):
    return product_characteristic_objects[0].value
