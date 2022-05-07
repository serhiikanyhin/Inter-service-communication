import os

from order.rules import (CancelOrder, CreateOrder, GetOrderInfo, GetOrders,
                         GetOrdersByUser)
from order.tasks import CancelUserOrders
from utils.celery import CeleryConsumer
from utils.flask import FlaskApp


class OrderMicroservice:
    def __init__(self):
        self.consumer = CeleryConsumer(
            name='order_consumer',
            tasks_list=[CancelUserOrders]
        )
        self.flask = FlaskApp(
            host=os.getenv('ORDER_SERVICE_HOST'),
            port=int(os.getenv('ORDER_SERVICE_PORT')),
            import_name='order_app',
            url_rules=[
                CreateOrder,
                CancelOrder,
                GetOrders,
                GetOrderInfo,
                GetOrdersByUser
            ]
        )

    def run_locally(self):
        self.consumer.start_thread()
        self.flask.start_thread()


if __name__ == '__main__':
    order_microservice = OrderMicroservice()
    order_microservice.run_locally()

