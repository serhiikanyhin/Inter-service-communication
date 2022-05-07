from flask import request
from product.logic import ProductLogic
from specifications.apis import Specifications
from utils.flask import UrlRule

specs = Specifications.Products


class CreateProduct(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.CreateProduct.RULE,
            endpoint=specs.CreateProduct.ENDPOINT,
            methods=specs.CreateProduct.METHODS,
            logic=ProductLogic()
        )

    def view(self):
        params = request.json
        name = params[specs.CreateProduct.Params.NAME]

        return self.logic_wrapper(
            func=self.logic.create_product,
            name=name,
        )


class GetProductInfo(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.GetProductInfo.RULE,
            endpoint=specs.GetProductInfo.ENDPOINT,
            methods=specs.GetProductInfo.METHODS,
            logic=ProductLogic()
        )

    def view(self):
        params = request.json
        product_id = params[specs.GetProductInfo.Params.PRODUCT_ID]

        return self.logic_wrapper(
            func=self.logic.get_product_info,
            product_id=product_id,
        )


class UpdateProductAmount(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.UpdateProductAmount.RULE,
            endpoint=specs.UpdateProductAmount.ENDPOINT,
            methods=specs.UpdateProductAmount.METHODS,
            logic=ProductLogic()
        )

    def view(self):
        params = request.json
        product_id = params[specs.UpdateProductAmount.Params.PRODUCT_ID]
        amount = params[specs.UpdateProductAmount.Params.AMOUNT]
        action_type = params[specs.UpdateProductAmount.Params.ACTION_TYPE]

        return self.logic_wrapper(
            func=self.logic.update_product_amount,
            product_id=product_id,
            amount=amount,
            action_type=action_type
        )


class GetAllProducts(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.GetAllProducts.RULE,
            endpoint=specs.GetAllProducts.ENDPOINT,
            methods=specs.GetAllProducts.METHODS,
            logic=ProductLogic()
        )

    def view(self):
        return self.logic_wrapper(
            func=self.logic.get_all_products,
        )
