from abc import abstractmethod
from core.middlewares.authentication.user import User


class AuthInjectionInterface:

    @abstractmethod
    def create_token(self, user, platform):
        raise NotImplementedError()

    @abstractmethod
    def get_token(self, access_token):
        raise NotImplementedError()

    @abstractmethod
    def refresh_token(self, refresh_token):
        raise NotImplementedError()

    @abstractmethod
    def revoke_token(self, access_token):
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, token) -> User:
        raise NotImplementedError()
    