from modules.user.commands.auth.command import CreateUserCommand
from modules.user.domain.services.user_service import UserDService


class UserService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()

    async def create_user(self, command: CreateUserCommand):
        return await self.__user_domain_service.create_user(command=command)

