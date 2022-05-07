from typing import List

from order.models import Order, db_session
from specifications.tasks import Specifications as Specs
from specifications.tasks import Statuses
from utils.celery import produce_task


class OrderLogic:

    def create_order(self, product_id: str, user_id: str, amount: int) -> None:
        order = Order(
            amount=amount,
            product_id=product_id,
            user_id=user_id
        )
        db_session.add(order)

        # update available amount of product (add amount from the order)
        task_def = Specs.Products.UpdateAvailableAmount
        result = produce_task(
            task_name=task_def.NAME,
            parameters={
                task_def.Params.PRODUCT_ID: order.product_id,
                task_def.Params.AMOUNT: amount,
                task_def.Params.ACTION: task_def.Params.Actions.SUBTRACT
            }
        )

        # If there will be any problems - rollback transaction
        if result['status'] != Statuses.SUCCESS:
            db_session.rollback()
            raise Exception(result['error'])

        # If no problems - save changes in database
        db_session.commit()

    def cancel_order(self, order_id: str) -> None:
        # Get order if exists
        order = db_session.query(Order).filter_by(id=order_id)
        order = order.one_or_none()

        # If not exists - return error
        if order is None:
            raise Exception('order doesnt exists')

        # Delete order from database (but dont commit!)
        db_session.query(Order).filter_by(id=order_id).delete()

        # update available amount of product (add amount from the order)
        task_def = Specs.Products.UpdateAvailableAmount
        result = produce_task(
            task_name=task_def.NAME,
            parameters={
                task_def.Params.PRODUCT_ID: order.product_id,
                task_def.Params.AMOUNT: order.amount,
                task_def.Params.ACTION: task_def.Params.Actions.ADD
            }
        )

        # If there will be any problems - rollback transaction
        if result['status'] != Statuses.SUCCESS:
            db_session.rollback()
            raise Exception(result['error'])

        # If all is ok - commit changes
        db_session.commit()

    def get_order_info(self, order_id: str) -> dict:
        # Get order from database
        order = db_session.query(Order).filter_by(id=order_id)
        order = order.one_or_none()

        # Return error if order doesnt exists
        if order is None:
            raise Exception('order doesnt exists')

        # If order exists - return it`s info
        return {
            'id': order.id,
            'amount': order.amount,
            'user_id': order.user_id,
            'product_id': order.product_id
        }

    def get_orders(self) -> list:
        all_products = [
            {
                'id': order.id,
                'amount': order.amount,
                'user_id': order.user_id,
                'product_id': order.product_id
             }
            for order in db_session.query(Order).all()
        ]
        return all_products

    def get_orders_by_user(self, user_id: str) -> List[dict]:
        # Set query for database
        query = db_session.query(Order).filter_by(user_id=user_id)

        # Get data from database and convert it to list of dicts
        user_products = [
            {
                'id': order.id,
                'amount': order.amount,
                'user_id': order.user_id,
                'product_id': order.product_id
             }
            for order in query.all()
        ]

        # Return user orders
        return user_products

    def cancel_orders_by_user(self, user_id: str) -> None:
        orders = db_session.query(Order).filter_by(user_id=user_id).all()
        for order in orders:
            self.cancel_order(order_id=order.id)
