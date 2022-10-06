from .creation_utils import create_error


class OrderStatus:
    PROCESSING = "PROCESSING"
    SHIPPING = "SHIPPING"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class Roles:
    ADMIN = "Admin"
    CUSTOMER = "Customer"


class Errors:
    ACCESS_DENIED = create_error(1, "Действие запрещено для вашей роли")
    USER_ALREADY_EXISTS = create_error(2, "Пользователь с данным email уже существует")
    WRONG_EMAIL_OR_PASSWORD = create_error(3, "Неверный email или пароль")
    OBJECT_NOT_FOUND = create_error(4, "Данных по запросу не найдено")
    USER_ALREADY_HAS_ADMIN_ROLE = create_error(5, "Пользователь уже имеет роль Администратор")
    CANT_ADD_MORE_PRODUCTS = create_error(6, "Нельзя добавить больше товаров")
    IMAGES_NOT_UPLOADED = create_error(7, "При загрузке изображений товара произошла ошибка")
    CATEGORIES_NOT_SET = create_error(8, "При задании категорий товара произошла ошибка")
    CATEGORIES_NOT_REMOVED = create_error(8, "При удалении категорий товара произошла ошибка")
    NO_PRODUCTS_IN_CART = create_error(9, "Корзина пользователя пуста")
    NOT_ENOUGH_PRODUCT = create_error(10, "Некоторые товары недоступны для заказа в количестве, указанном в корзине. "
                                          "Проверьте отредактированную корзину и выполните заказ еще раз.")
    ORDER_CREATION_EXCEPTION = create_error(11, "Ошибка при переносе товара в заказ")
    WRONG_ORDER_STATUS = create_error(12, "Нельзя применить статус к заказу")


class UnauthorizedError(Exception):
    extension = {"code": 401}


class ForbiddenError(Exception):
    extension = {"code": 403}


class NotEnoughProduct(Exception):
    def __init__(self, message="В корзине товара больше чем доступно для покупки"):
        self.message = message
        super().__init__(self.message)
