from infrastructure.configs.main import get_mongodb_instance
from modules.system_setting.commands.update_system_setting.command import UpdateSystemSettingCommand

class SystemSettingDService():

    def __init__(self) -> None:
        from modules.system_setting.database.repository import SystemSettingRepository, SystemSettingRepositoryPort
        self.__system_setting_repository: SystemSettingRepositoryPort = SystemSettingRepository()
        self.__db_instance = get_mongodb_instance()
    
    async def get(self):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                system_setting = await self.__system_setting_repository.find_one({})
                
                return system_setting

    async def update(self, command: UpdateSystemSettingCommand):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                
                saved_setting = await self.__system_setting_repository.find_one({})

                conditions = dict(
                    task_expired_duration=command.task_expired_duration,
                    translation_api_url=command.translation_api_url,
                    translation_api_allowed_concurrent_req=command.translation_api_allowed_concurrent_req,
                    language_detection_api_url=command.language_detection_api_url,
                    language_detection_api_allowed_concurrent_req=command.language_detection_api_allowed_concurrent_req,
                    translation_speed_for_each_character=command.translation_speed_for_each_character,
                    language_detection_speed=command.language_detection_speed,
                    email_for_sending_email=command.email_for_sending_email,
                    email_password_for_sending_email=command.email_password_for_sending_email,
                    allowed_total_chars_for_text_translation=command.allowed_total_chars_for_text_translation,
                    allowed_file_size_in_mb_for_file_translation=command.allowed_file_size_in_mb_for_file_translation,
                )
                
                updated_setting = await self.__system_setting_repository.update(saved_setting, conditions)

                return updated_setting
