import celery
from order.logic import OrderLogic
from specifications.tasks import Specifications as Specs


class CancelUserOrders(celery.Task):
    name = Specs.Orders.CancelUserOrders.NAME

    def run(self, *args, **kwargs):
        params = Specs.Orders.CancelUserOrders.Params
        user_id = kwargs[params.USER_ID]

        logic = OrderLogic()
        logic.cancel_orders_by_user(user_id=user_id)
