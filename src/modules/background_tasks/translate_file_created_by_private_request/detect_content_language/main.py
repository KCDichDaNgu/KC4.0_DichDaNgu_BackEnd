from datetime import datetime
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from core.utils.common import chunk_arr
from docx import Document
from typing import List
from uuid import UUID
import pymongo
from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum, 
    StepStatusEnum
)

from infrastructure.adapters.content_translator.main import ContentTranslator 

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger
from infrastructure.configs.translation_task import RESULT_FILE_STATUS, FileTranslationTask_NotYetTranslatedResultFileSchemaV1, FileTranslationTask_TranslationClosedResultFileSchemaV1
from infrastructure.adapters.language_detector.main import LanguageDetector
from infrastructure.configs.message import MESSAGES

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
transation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

languageDetector = LanguageDetector()

logger = Logger('Task: translate_file_created_by_private_request.detect_content_language')

async def read_task_result(
    tasks_result: List[TranslationRequestResultEntity], 
    tasks: List[TranslationRequestEntity],
    translations_history: List[TranslationHistoryEntity]
):
    
    valid_tasks_mapper = {}

    task_id_1 = list(map(lambda t: t.id.value, tasks))
    task_id_2 = list(map(lambda ts: ts.props.task_id.value, tasks_result))
    task_id_3 = list(map(lambda th: th.props.task_id.value, translations_history))

    intersection_tasks_id = list(set(task_id_1) & set(task_id_2) & set(task_id_3))
    
    for task_id in intersection_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, translations_history))[0]

        try: 
            data = await task_result.read_data_from_file()

            if data['status'] == RESULT_FILE_STATUS['language_not_yet_detected']:

                valid_tasks_mapper[task_id] = {
                    'task_result_content': data,
                    'task_result': task_result,
                    'trans_history': trans_history,
                    'task': task
                }

        except Exception as e:
            logger.error(e)
            print(e)

    valid_tasks_id = valid_tasks_mapper.keys()

    invalid_tasks = list(filter(lambda t: t.id.value not in valid_tasks_id, tasks))

    invalid_tasks_id = list(map(lambda t: t.id.value, invalid_tasks))

    invalid_tasks_mapper = {}
    
    for task_id in invalid_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, translations_history))[0]

        invalid_tasks_mapper[task_id] = {
            'task_result': task_result,
            'trans_history': trans_history,
            'task': task
        }

    return valid_tasks_mapper, invalid_tasks_mapper

async def mark_invalid_tasks(invalid_tasks_mapper):

    result = []
    
    async with db_instance.session() as session:
        async with session.start_transaction():

            update_request = []
            
            for task_id in invalid_tasks_mapper.keys():
                task_result = invalid_tasks_mapper[task_id]['task_result'],
                trans_history = invalid_tasks_mapper[task_id]['trans_history'],
                task = invalid_tasks_mapper[task_id]['task']

                if isinstance(task_result, tuple):
                    task_result = task_result[0]

                if isinstance(trans_history, tuple):
                    trans_history = trans_history[0]
                    
                update_request.append(
                    translation_request_repository.update(
                        task, 
                        dict(step_status=StepStatusEnum.cancelled.value),
                        conditions={}
                    )
                )
                
                update_request.append(
                    transation_history_repository.update(
                        trans_history, 
                        dict(
                            status=TranslationHistoryStatus.cancelled.value
                        )
                    )
                )

            result = await asyncio.gather(*update_request)

    return result

async def main():
    
    system_setting = await system_setting_repository.find_one({})
    
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.language_detection_api_allowed_concurrent_req
    
    if ALLOWED_CONCURRENT_REQUEST <= 0: return

    logger.debug(
        msg=f'New task translate_file_created_by_private_request.detect_content_language run in {datetime.now()}'
    )

    print(f'New task translate_file_created_by_private_request.detect_content_language run in {datetime.now()}')
    
    try:
        tasks = await translation_request_repository.find_many(
            params=dict(
                task_name=TranslationTaskNameEnum.private_file_translation.value,
                current_step=TranslationTaskStepEnum.detecting_language.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                # expired_date={
                #     "$gt": datetime.now()
                # }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            logger.debug(
                msg=f'An task translate_file_created_by_private_request.detect_content_language end in {datetime.now()}\n'
            )
            print(f'An task translate_file_created_by_private_request.detect_content_language end in {datetime.now()}\n')
            return

        tasks_result_and_trans_history_req = [
            translation_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=TranslationTaskStepEnum.detecting_language.value
                )
            ),
            transation_history_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

        tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            translations_history=translations_history
        )

        await mark_invalid_tasks(invalid_tasks_mapper)

        valid_tasks_id = list(map(lambda t: t.id.value, tasks))

        chunked_tasks_id = list(chunk_arr(valid_tasks_id, ALLOWED_CONCURRENT_REQUEST))

        for chunk in chunked_tasks_id:
            
            await execute_in_batch(valid_tasks_mapper, chunk, ALLOWED_CONCURRENT_REQUEST)

    except Exception as e:
        logger.error(e)
        
        print(e)

    logger.debug(
        msg=f'An task translate_file_created_by_private_request.detect_content_language end in {datetime.now()}\n'
    )

    print(f'An task translate_file_created_by_private_request.detect_content_language end in {datetime.now()}\n')
            

async def execute_in_batch(valid_tasks_mapper, tasks_id, allowed_concurrent_request):

    loop = asyncio.get_event_loop()

    connector = aiohttp.TCPConnector(limit=allowed_concurrent_request)

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:

        api_requests = []

        for task_id in tasks_id:
            task_result_content = valid_tasks_mapper[task_id]['task_result_content']
            original_file_full_path = task_result_content['original_file_full_path']

            doc = Document(original_file_full_path)
            source_text = ''
            
            for paragraph in doc.paragraphs:
                source_text = source_text + paragraph.text
            
            api_requests.append(
                languageDetector.detect(
                    text=source_text, 
                    session=session
                )
            )
            
        api_results = await asyncio.gather(*api_requests)

        async with db_instance.session() as session:

            async with session.start_transaction():
                
                update_request = []
                
                for task_id, api_result in zip(tasks_id, api_results):     

                    task_result = valid_tasks_mapper[task_id]['task_result'],
                    trans_history = valid_tasks_mapper[task_id]['trans_history'],
                    task = valid_tasks_mapper[task_id]['task']
                    task_result_content = valid_tasks_mapper[task_id]['task_result_content']

                    original_file_full_path = task_result_content['original_file_full_path']
                    binary_progress_file_full_path = task_result_content['binary_progress_file_full_path']
                    total_paragraphs = task_result_content['statistic']['total_paragraphs']
                    processed_paragraph_index = task_result_content['current_progress']['processed_paragraph_index']
                    
                    if api_result.lang == LanguageEnum.unknown.value:

                        new_saved_content = FileTranslationTask_TranslationClosedResultFileSchemaV1(
                            original_file_full_path=original_file_full_path,
                            binary_progress_file_full_path=binary_progress_file_full_path,
                            source_lang=api_result.lang,
                            file_type=task_result_content['file_type'],
                            statistic=dict(
                                total_paragraphs=total_paragraphs,
                            ),
                            current_progress=dict(
                                processed_paragraph_index=processed_paragraph_index
                            ),
                            message=MESSAGES['content_language_is_not_supported'],
                            target_lang=task_result_content['target_lang'],
                            task_name=TranslationTaskNameEnum.private_file_translation.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]
                    
                        update_request.append(
                            translation_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.closed.value
                                )
                            )
                        )
                        
                        update_request.append(
                            transation_history_repository.update(
                                trans_history, 
                                dict(
                                    status=TranslationHistoryStatus.closed.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )
                   
                    elif api_result.lang == task_result_content['target_lang']:

                        new_saved_content = FileTranslationTask_TranslationClosedResultFileSchemaV1(
                            original_file_full_path=original_file_full_path,
                            binary_progress_file_full_path=binary_progress_file_full_path,
                            file_type=task_result_content['file_type'],
                            source_lang=api_result.lang,
                            statistic=dict(
                                total_paragraphs=total_paragraphs,
                            ),
                            current_progress=dict(
                                processed_paragraph_index=processed_paragraph_index
                            ),
                            message=MESSAGES['source_lang_and_target_lang_are_the_same'],
                            target_lang=task_result_content['target_lang'],
                            task_name=TranslationTaskNameEnum.private_file_translation.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]
                    
                        update_request.append(
                            translation_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.closed.value
                                )
                            )
                        )
                        
                        update_request.append(
                            transation_history_repository.update(
                                trans_history, 
                                dict(
                                    status=TranslationHistoryStatus.closed.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )
                    
                    else:

                        new_saved_content = FileTranslationTask_NotYetTranslatedResultFileSchemaV1(
                            original_file_full_path=original_file_full_path,
                            file_type=task_result_content['file_type'],
                            binary_progress_file_full_path=binary_progress_file_full_path,
                            source_lang=api_result.lang,
                            statistic=dict(
                                total_paragraphs=total_paragraphs,
                            ),
                            current_progress=dict(
                                processed_paragraph_index=processed_paragraph_index
                            ),
                            target_lang=task_result_content['target_lang'],
                            task_name=TranslationTaskNameEnum.private_file_translation.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]
                    
                        update_request.append(
                            translation_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.not_yet_processed.value,
                                    current_step=TranslationTaskStepEnum.translating_language.value
                                )
                            )
                        )

                        update_request.append(
                            translation_request_result_repository.update(
                                task_result, 
                                dict(
                                    step=TranslationTaskStepEnum.translating_language.value
                                )
                            )
                        )
                        
                        update_request.append(
                            transation_history_repository.update(
                                trans_history, 
                                dict(
                                    status=TranslationHistoryStatus.translating.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )

                await asyncio.gather(*update_request)
