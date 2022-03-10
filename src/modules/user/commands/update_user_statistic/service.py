from sanic import response
from modules.user.domain.services.user_service import UserDService
from modules.user.commands.update_user_statistic.command import UpdateUserStatisticCommand
from infrastructure.configs.main import StatusCodeEnum
from infrastructure.configs.message import MESSAGES

class UpdateUserStatisticService():

    def __init__(self) -> None:
        self.__user_domain_service = UserDService()

    async def update(self, command: UpdateUserStatisticCommand):
        return await self.__user_domain_service.update_user_statistic(command)
    
    async def update_text_translate_statistic(self, user_id, pair, text_length):
        
        user_statistic = await self.__user_domain_service.get_user_statistic(user_id)

        increase_total_translated_text_result = user_statistic.increase_total_translated_text(pair, text_length)

        if increase_total_translated_text_result['code'] == StatusCodeEnum.failed.value:

            return increase_total_translated_text_result
        else:

            user_statistic_command = UpdateUserStatisticCommand(
                user_id=user_id,
                total_translated_text=increase_total_translated_text_result['data'],
                text_translation_quota=user_statistic.props.text_translation_quota,
            )

            user_statistic = await self.__user_domain_service.update_user_statistic(user_statistic_command)

            return increase_total_translated_text_result
    
    async def update_user_quota(self, user_id, command):

        user_statistic = await self.__user_domain_service.get_user_statistic(user_id)

        user_statistic_command = UpdateUserStatisticCommand(
            user_id=user_id,
            total_translated_text=user_statistic.props.total_translated_text,
            text_translation_quota=command.text_translation_quota,
        )

        user_statistic = await self.__user_domain_service.update_user_statistic(user_statistic_command)

        return user_statistic