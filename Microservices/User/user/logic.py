from typing import List

from specifications.tasks import Specifications as Specs
from specifications.tasks import Statuses
from user.models import User, db_session
from utils.celery import produce_task


class UserLogic:
    def register_user(self, name: str) -> None:
        """
        Creates user with specified name in database
        :param name: username
        :return: None
        """

        # Check if user presents in database
        user = db_session.query(User).filter_by(name=name)
        user = user.one_or_none()
        if user is not None:
            raise Exception('User already exists')

        user = User(name=name)
        db_session.add(user)
        db_session.commit()

    def remove_user(self, user_id: str) -> None:
        """
        Removes specified user from database
        :param user_id: id of user to be removed
        :return: None
        """

        # Check if user doesnt exists
        user = db_session.query(User).filter_by(id=user_id).one_or_none()
        if user is None:
            raise Exception('user doesnt exists')

        # Delete user from database (but dont commit!)
        db_session.query(User).filter_by(id=user_id).delete()

        # Cancel all user's orders
        task_def = Specs.Orders.CancelUserOrders
        result = produce_task(
            task_name=task_def.NAME,
            parameters={
                task_def.Params.USER_ID: user_id
            }
        )

        # Rollback changes in case of problems
        if result['status'] == Statuses.FAILURE:
            db_session.rollback()
            raise Exception(result['error'])

        # Commit changes if all is ok
        db_session.commit()

    def get_users(self) -> List[dict]:
        """
        :return: List of users in following format: { id: str, name: str}
        """

        # Get all users from database
        all_users = [
            {"id": user.id, "name": user.name}
            for user in db_session.query(User).all()
        ]

        return all_users
