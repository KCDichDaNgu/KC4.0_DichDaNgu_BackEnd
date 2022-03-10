from modules.user.commands.auth.command import CreateUserCommand
from modules.user.domain.services.user_service import UserDService

class GetUserStatisticService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()

    async def get(self, user_id: str):
        return await self.__user_domain_service.get_user_statistic(user_id=user_id)
