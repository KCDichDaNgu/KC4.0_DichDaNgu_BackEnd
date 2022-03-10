from infrastructure.configs.language import LanguageEnum
from modules.language_detection_request.domain.entities.language_detection_history import LanguageDetectionHistoryProps
from core.value_objects import ID
from infrastructure.configs.task import (
    CreatorTypeEnum, StepStatusEnum, 
    LanguageDetectionTaskNameEnum, 
    LanguageDetectionTaskStepEnum,
    LanguageDetectionTask_LangUnknownResultFileSchemaV1
)
from modules.language_detection_request.database.language_detection_request.repository import (
    LanguageDetectionRequestRepository, LanguageDetectionRequestRepositoryPort
)
from modules.language_detection_request.commands.create_plain_text_language_detection_request.command import CreatePlainTextLanguageDetectionRequestCommand
from modules.language_detection_request.domain.entities.language_detection_request import LanguageDetectionRequestEntity, LanguageDetectionRequestProps 
from modules.language_detection_request.domain.entities.language_detection_request_result import LanguageDetectionRequestResultProps
from modules.language_detection_request.database.language_detection_request_result.repository import (
    LanguageDetectionRequestResultRepository, 
    LanguageDetectionRequestResultEntity
)
from modules.language_detection_request.database.language_detection_history.repository import (
    LanguageDetectionHistoryEntity,
    LanguageDetectionHistoryRepositoryPort,
    LanguageDetectionHistoryRepository
)

from infrastructure.configs.language_detection_history import LanguageDetectionHistoryTypeEnum, LanguageDetectionHistoryStatus
from infrastructure.configs.main import get_mongodb_instance
from modules.language_detection_request.commands.create_file_language_detection_request.command import CreateFileLanguageDetectionRequestCommand
from core.utils.file import extract_file_extension, get_doc_file_meta
from infrastructure.configs.language_detection_task import FileLanguageDetectionTask_LangUnknownResultFileSchemaV1

TEXT_LANGUAGE_DETECTION_TASKS = [
    LanguageDetectionTaskNameEnum.private_plain_text_language_detection.value, 
    LanguageDetectionTaskNameEnum.public_plain_text_language_detection
]

class LanguageDetectionRequestDService():

    def __init__(self) -> None:
        
        self.__language_detection_request_repository: LanguageDetectionRequestRepositoryPort = LanguageDetectionRequestRepository()
        self.__language_detection_request_result_repository : LanguageDetectionRequestRepositoryPort = LanguageDetectionRequestResultRepository()
        self.__language_detection_history_repository: LanguageDetectionHistoryRepositoryPort = LanguageDetectionHistoryRepository()
        self.__db_instance = get_mongodb_instance()

    async def create(self, command: CreatePlainTextLanguageDetectionRequestCommand):

        begin_step = LanguageDetectionTaskStepEnum.detecting_language.value

        saved_content = LanguageDetectionTask_LangUnknownResultFileSchemaV1(
            source_text=command.source_text,
            task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
        )
            
        new_request = LanguageDetectionRequestEntity(
            LanguageDetectionRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        
        new_task_result_entity = LanguageDetectionRequestResultEntity(
            LanguageDetectionRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )
        
        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_language_detection_history_entity = LanguageDetectionHistoryEntity(
                LanguageDetectionHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    language_detection_type=LanguageDetectionHistoryTypeEnum.public_plain_text_language_detection.value,
                    status=LanguageDetectionHistoryStatus.detecting.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():
                    
                    created_request = await self.__language_detection_request_repository.create(
                        new_request
                    )

                    await self.__language_detection_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_language_detection_record = await self.__language_detection_history_repository.create(
                        new_language_detection_history_entity
                    )
                    
                    return created_request, created_language_detection_record

    async def create_file_detection_request(self, command: CreateFileLanguageDetectionRequestCommand):

        begin_step = LanguageDetectionTaskStepEnum.detecting_language.value        
            
        new_request = LanguageDetectionRequestEntity(
            LanguageDetectionRequestProps(
                creator_id=ID(None),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=LanguageDetectionTaskNameEnum.public_file_language_detection.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        
        new_task_result_entity = LanguageDetectionRequestResultEntity(
            LanguageDetectionRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )
        original_file_ext = extract_file_extension(command.source_file.name)
        create_file_result = await new_task_result_entity.create_required_files_for_file_language_detection_task(command.source_file)


        saved_content = FileLanguageDetectionTask_LangUnknownResultFileSchemaV1(
            source_file_full_path=create_file_result.data['source_file_full_path'],
            task_name=LanguageDetectionTaskNameEnum.public_file_language_detection.value,
            file_type=original_file_ext
        )
        
        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_language_detection_history_entity = LanguageDetectionHistoryEntity(
                LanguageDetectionHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    language_detection_type=LanguageDetectionHistoryTypeEnum.public_file_language_detection.value,
                    status=LanguageDetectionHistoryStatus.detecting.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():
                    
                    created_request = await self.__language_detection_request_repository.create(
                        new_request
                    )

                    await self.__language_detection_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_language_detection_record = await self.__language_detection_history_repository.create(
                        new_language_detection_history_entity
                    )
                    
                    return created_request, created_language_detection_record
