class Statuses:
    SUCCESS = 'success'
    FAILURE = 'failure'


class Specifications:
    class Orders:
        class CancelUserOrders:
            NAME = 'cancel_user_orders'

            class Params:
                USER_ID = 'user_id'

    class Products:
        class UpdateAvailableAmount:
            NAME = 'update_available_product_amount'

            class Params:
                PRODUCT_ID = 'product_id'
                AMOUNT = 'amount'
                ACTION = 'action_type'

                class Actions:
                    ADD = 'add'
                    SUBTRACT = 'subtract'
