from modules.user.commands.update_self.command import UpdateUserCommand
from modules.user.domain.services.user_service import UserDService


class UserService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()

    async def update_user(self, command: UpdateUserCommand):
        return await self.__user_domain_service.update_user(command=command)