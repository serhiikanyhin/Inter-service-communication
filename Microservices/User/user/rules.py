from flask import request
from specifications.apis import Specifications
from user.logic import UserLogic
from utils.flask import UrlRule

specs = Specifications.User


class RegisterUser(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.RegisterUser.RULE,
            endpoint=specs.RegisterUser.ENDPOINT,
            methods=specs.RegisterUser.METHODS,
            logic=UserLogic()
        )

    def view(self):
        params = request.json
        name = params[specs.RegisterUser.Params.NAME]

        return self.logic_wrapper(
            func=self.logic.register_user,
            name=name
        )


class RemoveUser(UrlRule):

    def __init__(self):
        super().__init__(
            rule=specs.RemoveUser.RULE,
            endpoint=specs.RemoveUser.ENDPOINT,
            methods=specs.RemoveUser.METHODS,
            logic=UserLogic()
        )

    def view(self):
        params = request.json
        user_id = params[specs.RemoveUser.Params.USER_ID]

        return self.logic_wrapper(
            func=self.logic.remove_user,
            user_id=user_id
        )


class GetUsers(UrlRule):
    def __init__(self):
        super().__init__(
            rule=specs.GetUsers.RULE,
            endpoint=specs.GetUsers.ENDPOINT,
            methods=specs.GetUsers.METHODS,
            logic=UserLogic()
        )

    def view(self):
        return self.logic_wrapper(
            func=self.logic.get_users
        )
