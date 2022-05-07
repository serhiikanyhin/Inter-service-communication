import os

from user.rules import GetUsers, RegisterUser, RemoveUser
from utils.flask import FlaskApp


class UserMicroservice:
    def __init__(self):
        self.flask = FlaskApp(
            host=os.getenv('USER_SERVICE_HOST'),
            port=int(os.getenv('USER_SERVICE_PORT')),
            import_name='user_app',
            url_rules=[
                RegisterUser,
                RemoveUser,
                GetUsers
            ]
        )

    def run_locally(self):
        self.flask.start_thread()


if __name__ == '__main__':
    user_microservice = UserMicroservice()
    user_microservice.run_locally()

