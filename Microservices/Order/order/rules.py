from flask import request
from order.logic import OrderLogic
from specifications.apis import Specifications
from utils.flask import UrlRule

specs = Specifications.Orders


class CreateOrder(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.CreateOrder.RULE,
            endpoint=specs.CreateOrder.ENDPOINT,
            methods=specs.CreateOrder.METHODS,
            logic=OrderLogic()
        )

    def view(self):
        params = request.json
        product_id = params[specs.CreateOrder.Params.PRODUCT_ID]
        user_id = params[specs.CreateOrder.Params.USER_ID]
        amount = params[specs.CreateOrder.Params.AMOUNT]

        return self.logic_wrapper(
            func=self.logic.create_order,
            product_id=product_id,
            user_id=user_id,
            amount=amount
        )


class CancelOrder(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.CancelOrder.RULE,
            endpoint=specs.CancelOrder.ENDPOINT,
            methods=specs.CancelOrder.METHODS,
            logic=OrderLogic()
        )

    def view(self):
        params = request.json
        order_id = params[specs.CancelOrder.Params.ORDER_ID]

        return self.logic_wrapper(
            func=self.logic.cancel_order,
            order_id=order_id
        )


class GetOrderInfo(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.GetOrderInfo.RULE,
            endpoint=specs.GetOrderInfo.ENDPOINT,
            methods=specs.GetOrderInfo.METHODS,
            logic=OrderLogic()
        )

    def view(self):
        params = request.json
        order_id = params[specs.GetOrderInfo.Params.ORDER_ID]

        return self.logic_wrapper(
            func=self.logic.get_order_info(),
            order_id=order_id
        )


class GetOrders(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.GetOrders.RULE,
            endpoint=specs.GetOrders.ENDPOINT,
            methods=specs.GetOrders.METHODS,
            logic=OrderLogic()
        )

    def view(self):
        return self.logic_wrapper(
            func=self.logic.get_orders
        )


class GetOrdersByUser(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.GetOrdersByUser.RULE,
            endpoint=specs.GetOrdersByUser.ENDPOINT,
            methods=specs.GetOrdersByUser.METHODS,
            logic=OrderLogic()
        )

    def view(self):
        params = request.json
        user_id = params[specs.GetOrdersByUser.Params.USER_ID]

        return self.logic_wrapper(
            func=self.logic.get_orders_by_user,
            user_id=user_id
        )
