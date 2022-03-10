import io
from uuid import UUID
from infrastructure.configs.language import LanguageEnum
from modules.translation_request.domain.entities.translation_history import TranslationHistoryProps
from core.value_objects import ID
from infrastructure.configs.task import (
    CreatorTypeEnum, 
    StepStatusEnum, 
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum,
    TranslationTask_NotYetTranslatedResultFileSchemaV1, 
    TranslationTask_LangUnknownResultFileSchemaV1
)
from modules.translation_request.database.translation_request.repository import (
    TranslationRequestRepository, TranslationRequestRepositoryPort
)
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps 
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultProps
from modules.translation_request.database.translation_request_result.repository import (
    TranslationRequestResultRepository, 
    TranslationRequestResultEntity,
    TranslationRequestResultRepositoryPort
)
from modules.translation_request.database.translation_history.repository import (
    TranslationHistoryEntity,
    TranslationHistoryRepositoryPort,
    TranslationHistoryRepository
)

from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus
from infrastructure.configs.main import StatusCodeEnum, get_mongodb_instance
from modules.translation_request.commands.create_file_translation_request.command import CreateFileTranslationRequestCommand
from modules.translation_request.commands.update_receiver_email.command import UpdateReceiverEmailCommand
from infrastructure.configs.translation_task import AllowedFileTranslationExtensionEnum, FileTranslationTask_LangUnknownResultFileSchemaV1, FileTranslationTask_NotYetTranslatedResultFileSchemaV1

from core.utils.file import extract_file_extension, get_doc_file_meta, get_presentation_file_meta, get_worksheet_file_meta

class TranslationRequestDService():

    def __init__(self) -> None:
        
        self.__translation_request_repository: TranslationRequestRepositoryPort = TranslationRequestRepository()
        self.__translation_request_result_repository : TranslationRequestResultRepositoryPort = TranslationRequestResultRepository()
        self.__translation_history_repository: TranslationHistoryRepositoryPort = TranslationHistoryRepository()
        self.__db_instance = get_mongodb_instance()

    async def create(self, command: CreatePlainTextTranslationRequestCommand):
        
        if command.creator_id.value != None:
            task_name = TranslationTaskNameEnum.private_plain_text_translation.value
        else:
            task_name = TranslationTaskNameEnum.public_plain_text_translation.value

        if command.source_lang in LanguageEnum.enum_values():

            begin_step = TranslationTaskStepEnum.translating_language.value

            saved_content = TranslationTask_NotYetTranslatedResultFileSchemaV1(
                source_text=command.source_text,
                source_lang=command.source_lang,
                target_lang=command.target_lang,
                task_name=task_name
            )

        else:
            
            begin_step = TranslationTaskStepEnum.detecting_language.value

            saved_content = TranslationTask_LangUnknownResultFileSchemaV1(
                source_text=command.source_text,
                target_lang=command.target_lang,
                task_name=task_name
            )
            
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=command.creator_id,
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=task_name,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step
            )
        )
        
        await new_request.update_num_chars(command.source_text)
        
        new_task_result_entity = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step
            )
        )

        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_translation_history_entity = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    translation_type=task_name,
                    status=TranslationHistoryStatus.translating.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )
            
            async with self.__db_instance.session() as session:
                async with session.start_transaction():
                    
                    created_request = await self.__translation_request_repository.create(
                        new_request
                    )

                    await self.__translation_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_translation_record = await self.__translation_history_repository.create(
                        new_translation_history_entity
                    )
                    
                    return created_request, created_translation_record
                
    async def update_receiver_email(self, command: UpdateReceiverEmailCommand): 
        
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                
                translation_request = await self.__translation_request_repository.find_one({'id': UUID(command.id.value)})
                
                translation_request = await self.__translation_request_repository.update(
                    translation_request,
                    dict(receiver_email=command.receiver_email)
                )
                
                return translation_request

    async def create_file_translation_request(self, command: CreateFileTranslationRequestCommand):
        
        if command.creator_id.value != None:
            task_name = TranslationTaskNameEnum.private_file_translation.value
        else:
            task_name = TranslationTaskNameEnum.public_file_translation.value
        
        original_file_ext = extract_file_extension(command.source_file.name)

        if command.source_lang in LanguageEnum.enum_values() and command.source_lang != 'unknown':
            begin_step = TranslationTaskStepEnum.translating_language.value
        else:
            begin_step = TranslationTaskStepEnum.detecting_language.value
        
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=command.creator_id,
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=task_name,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=begin_step,
                file_type=original_file_ext
            )
        )
        
        await new_request.update_num_chars(command.source_file)
        
        new_task_result_entity = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step,
            )
        ) 
        
        binary_doc, total_paragraphs, total_slides, total_sheets= (None, 0, 0, 0)

        if original_file_ext == AllowedFileTranslationExtensionEnum.docx.value:

            binary_doc, total_paragraphs, character_count = get_doc_file_meta(command.source_file)
            create_files_result = await new_task_result_entity.create_required_files_for_file_translation_task(binary_doc, original_file_ext)
        
        elif original_file_ext == AllowedFileTranslationExtensionEnum.pptx.value:
            
            binary_presentation, total_paragraphs, total_slides, character_count = get_presentation_file_meta(command.source_file)
            create_files_result = await new_task_result_entity.create_required_files_for_file_translation_task(binary_presentation, original_file_ext)
        
        elif original_file_ext == AllowedFileTranslationExtensionEnum.xlsx.value:
            binary_worksheet, total_sheets, total_cells, character_count = get_worksheet_file_meta(command.source_file)
            create_files_result = await new_task_result_entity.create_required_files_for_file_translation_task(binary_worksheet, original_file_ext)
        else:
            create_files_result = await new_task_result_entity.create_required_files_for_txt_file_translation_task(command.source_file)
        
        if command.source_lang in LanguageEnum.enum_values() and command.source_lang != 'unknown':
            
            saved_content = FileTranslationTask_NotYetTranslatedResultFileSchemaV1(
                original_file_full_path=create_files_result.data['original_file_full_path'],
                binary_progress_file_full_path=create_files_result.data.get('binary_progress_file_full_path', ''),
                target_file_path=None,
                file_type=original_file_ext,
                statistic=dict(
                    total_paragraphs=total_paragraphs,
                    total_slides=total_slides,
                    total_sheets=total_sheets,
                ),
                current_progress=dict(
                    processed_paragraph_index=-1,
                    processed_slide_index=-1,
                    processed_sheet_index=-1,
                    last_row= 1,
                    last_col= 0
                ),
                source_lang=command.source_lang,
                target_lang=command.target_lang,
                task_name=task_name
            )

        else:

            saved_content = FileTranslationTask_LangUnknownResultFileSchemaV1(
                original_file_full_path=create_files_result.data['original_file_full_path'],
                binary_progress_file_full_path=create_files_result.data.get('binary_progress_file_full_path', ''),
                target_file_path=None,
                file_type=original_file_ext,
                statistic=dict(
                    total_paragraphs=total_paragraphs,
                    total_slides=total_slides,
                    total_sheets=total_sheets,
                ),
                current_progress=dict(
                    processed_paragraph_index=-1,
                    processed_slide_index=-1,
                    processed_sheet_index=-1,
                    last_row= 1,
                    last_col= 0
                ),
                target_lang=command.target_lang,
                task_name=task_name
            )

        saving_content_result = await new_task_result_entity.save_request_result_to_file(
            content=saved_content.json()
        )

        if saving_content_result:
        
            new_translation_history_entity = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request.props.creator_id,
                    task_id=new_request.id,
                    translation_type=task_name,
                    status=TranslationHistoryStatus.translating.value,
                    file_path=new_task_result_entity.props.file_path
                )
            )

            async with self.__db_instance.session() as session:
                async with session.start_transaction():

                    created_request = await self.__translation_request_repository.create(
                        new_request
                    )
                    
                    create_request_result = await self.__translation_request_result_repository.create(
                        new_task_result_entity
                    )
                    
                    created_translation_record = await self.__translation_history_repository.create(
                        new_translation_history_entity
                    )

                    return created_request, created_translation_record
