import celery
from product.logic import ProductLogic
from specifications.tasks import Specifications as Specs


class UpdateAvailableAmount(celery.Task):
    name = Specs.Products.UpdateAvailableAmount.NAME

    def run(self, *args, **kwargs):
        params = Specs.Products.UpdateAvailableAmount.Params
        product_id = kwargs[params.PRODUCT_ID]
        amount = kwargs[params.AMOUNT]
        action_type = kwargs[params.ACTION]

        logic = ProductLogic()
        logic.update_product_amount(
            product_id=product_id,
            amount=amount,
            action_type=action_type
        )
