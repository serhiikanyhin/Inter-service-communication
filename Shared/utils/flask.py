from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable, List

from flask import Flask


class UrlRule(ABC):
    def __init__(self, rule: str, endpoint: str, methods: List[str],
                 logic) -> None:
        self.rule = rule
        self.endpoint = endpoint
        self.methods = methods
        self.logic = logic
        self.view_func = self.view

    @abstractmethod
    def view(self):
        raise NotImplementedError()

    def logic_wrapper(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            response = {'status': 'success'}
            if result is not None:
                response['result'] = result
            return response, 200

        except Exception as err:
            response = {
                'status': 'failure',
                'error': str(err)
            }
            return response, 400


class FlaskApp(Flask):

    def __init__(self, host: str, port: int, import_name: str,
                 url_rules: list):
        super().__init__(
            import_name=import_name
        )
        self.host = host
        self.port = port
        self.url_rules = url_rules

    def start_locally(self) -> None:
        for rule in self.url_rules:
            rule = rule()
            self.add_url_rule(
                rule=rule.rule,
                view_func=rule.view_func,
                endpoint=rule.endpoint,
                methods=rule.methods
            )
        self.run(
            host=self.host,
            port=self.port
        )

    def start_thread(self) -> None:
        thread = Thread(target=self.start_locally, name='flask')
        thread.start()
