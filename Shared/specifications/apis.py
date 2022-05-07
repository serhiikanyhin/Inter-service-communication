class Specifications:
    class User:
        class RegisterUser:
            RULE = '/users/register/'
            ENDPOINT = 'register_user'
            METHODS = ["POST"]

            class Params:
                NAME = 'name'

        class RemoveUser:
            RULE = '/users/remove/'
            ENDPOINT = 'remove_user'
            METHODS = ["POST"]

            class Params:
                USER_ID = 'user_id'

        class GetUsers:
            RULE = '/users/'
            ENDPOINT = 'get_users'
            METHODS = ["GET"]

    class Orders:
        class CreateOrder:
            RULE = '/orders/create/'
            ENDPOINT = 'create_order'
            METHODS = ["POST"]

            class Params:
                PRODUCT_ID = 'product_id'
                USER_ID = 'user_id'
                AMOUNT = 'amount'

        class CancelOrder:
            RULE = '/orders/cancel/'
            ENDPOINT = 'cancel_order'
            METHODS = ["POST"]

            class Params:
                ORDER_ID = 'order_id'

        class GetOrderInfo:
            RULE = '/orders/info/'
            ENDPOINT = 'get_order_info'
            METHODS = ["GET"]

            class Params:
                ORDER_ID = 'order_id'

        class GetOrders:
            RULE = '/orders/'
            ENDPOINT = 'get_orders'
            METHODS = ["GET"]

        class GetOrdersByUser:
            RULE = '/orders/by_user'
            ENDPOINT = 'get_orders_by_user'
            METHODS = ["GET"]

            class Params:
                USER_ID = 'user_id'

    class Products:
        class CreateProduct:
            RULE = '/products/create/'
            ENDPOINT = 'create_product'
            METHODS = ["POST"]

            class Params:
                NAME = 'name'

        class GetProductInfo:
            RULE = '/products/info/'
            ENDPOINT = 'get_product_info'
            METHODS = ["GET"]

            class Params:
                PRODUCT_ID = 'product_id'

        class UpdateProductAmount:
            RULE = '/products/amount/'
            ENDPOINT = 'update_product_amount'
            METHODS = ["POST"]

            class Params:
                PRODUCT_ID = 'product_id'
                AMOUNT = 'amount'
                ACTION_TYPE = 'action_type'

        class GetAllProducts:
            RULE = '/products/'
            ENDPOINT = 'get_all_products'
            METHODS = ["GET"]
