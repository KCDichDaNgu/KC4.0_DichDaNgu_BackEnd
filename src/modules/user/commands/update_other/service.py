from modules.user.commands.update_other.command import UpdateOtherUserCommand
from modules.user.domain.services.user_service import UserDService


class UserService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()

    async def update_user(self, command: UpdateOtherUserCommand):
        return await self.__user_domain_service.update_user(command=command)