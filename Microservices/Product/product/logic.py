from typing import List

from product.models import Product, db_session
from specifications.tasks import Specifications as Specs


class ProductLogic:

    def create_product(self, name: str) -> None:
        # Check if product exists
        product = db_session.query(Product).filter_by(name=name)
        product = product.one_or_none()

        # If exists - raise error
        if product is not None:
            raise Exception('product already exists')

        # If not exists - save product to database
        product = Product(name=name)
        db_session.add(product)
        db_session.commit()

    def get_product_info(self, product_id: str) -> dict:
        # Get product if exists
        product = db_session.query(Product).filter_by(id=product_id)
        product = product.one_or_none()

        # If not exists - return error
        if product is None:
            raise Exception('product doesnt exists')

        return {
            'id': product.id,
            'name': product.name,
            'amount': product.amount,
        }

    def update_product_amount(self, product_id: str, amount: int,
                              action_type: str) -> dict:
        # Get product if exists
        product = db_session.query(Product).filter_by(id=product_id)
        product = product.one_or_none()

        # If not exists - return error
        if product is None:
            raise Exception('product doesnt exists')

        actions = Specs.Products.UpdateAvailableAmount.Params.Actions

        # Get current available amount
        current_product_amount = product.amount

        # Set available amount of product
        if action_type == actions.ADD:
            product.amount = current_product_amount + amount

        elif action_type == actions.SUBTRACT:

            if current_product_amount - amount < 0:
                raise Exception('Not enough products in stock')

            product.amount = current_product_amount - amount

        else:
            raise Exception('Not supported product amount action')

        # Commit changes
        db_session.commit()

        return {
            'id': product.id,
            'name': product.name,
            'amount': product.amount,
        }

    def get_all_products(self) -> List[dict]:
        all_products = [
            {
                "id": product.id,
                "name": product.name,
                "amount": product.amount
            }
            for product in db_session.query(Product).all()
        ]
        return all_products
