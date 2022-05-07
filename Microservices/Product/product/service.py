import os

from product.rules import (CreateProduct, GetAllProducts, GetProductInfo,
                           UpdateProductAmount)
from product.tasks import UpdateAvailableAmount
from utils.celery import CeleryConsumer
from utils.flask import FlaskApp


class ProductMicroservice:
    def __init__(self):
        self.consumer = CeleryConsumer(
            name='product_consumer',
            tasks_list=[UpdateAvailableAmount]
        )
        self.flask = FlaskApp(
            host=os.getenv('PRODUCT_SERVICE_HOST'),
            port=int(os.getenv('PRODUCT_SERVICE_PORT')),
            import_name='product_app',
            url_rules=[
                CreateProduct,
                GetAllProducts,
                GetProductInfo,
                UpdateProductAmount
            ]
        )

    def run_locally(self):
        self.consumer.start_thread()
        self.flask.start_thread()


if __name__ == '__main__':
    product_microservice = ProductMicroservice()
    product_microservice.run_locally()

