from datetime import datetime

from infrastructure.configs.message import MESSAGES
from infrastructure.configs.translation_task import TranslationTask_TranslationClosedResultFileSchemaV1
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from core.utils.common import chunk_arr


from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance, MAX_RETRIES
from infrastructure.configs.task import (
    TranslationTask_LangUnknownResultFileSchemaV1, 
    TranslationTask_NotYetTranslatedResultFileSchemaV1, 
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum, 
    StepStatusEnum
)

from infrastructure.adapters.language_detector.main import LanguageDetector

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger

from core.utils.common import get_exception_log

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
transation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

languageDetector = LanguageDetector()

logger = Logger('Task: translate_plain_text_in_public_request.detect_content_language')

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
            
            if data['status'] == TranslationTask_LangUnknownResultFileSchemaV1(
                source_text='', 
                target_lang=LanguageEnum.vi.value,
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value
            ).status:

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
    
    try:
        system_setting = await system_setting_repository.find_one({})
        
        ALLOWED_CONCURRENT_REQUEST = system_setting.props.language_detection_api_allowed_concurrent_req

        logger.debug(
            msg=f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}'
        )

        print(f'New task translate_plain_text_in_public_request.detect_content_language run in {datetime.now()}')

        tasks = await translation_request_repository.find_many(
            params=dict(
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value,
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
                msg=f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n'
            )

            print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n')
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
        
        error_message = get_exception_log(e)
        
        async with db_instance.session() as session:
            async with session.start_transaction():
        
                for task in tasks:
                    
                    retry = task.props.retry + 1
                    
                    changes = dict(
                        retry=retry,
                        error_message=error_message
                    )
                    
                    if retry > MAX_RETRIES: 
                        changes = dict(
                            step_status=StepStatusEnum.cancelled.value
                        )
                        
                        transation_history_repository_record = await transation_history_repository.find_one(
                            params=dict(
                                task_id=UUID(task.id.value)
                            )
                        )
                        
                        await transation_history_repository.update(transation_history_repository_record, dict(
                            status=TranslationHistoryStatus.cancelled.value
                        ))
                    
                    await translation_request_repository.update(task, changes)
        
        print(e)

    logger.debug(
        msg=f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n'
    )

    print(f'An task translate_plain_text_in_public_request.detect_content_language end in {datetime.now()}\n')
            

async def execute_in_batch(valid_tasks_mapper, tasks_id, allowed_concurrent_request):

    loop = asyncio.get_event_loop()

    connector = aiohttp.TCPConnector(limit=allowed_concurrent_request)

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:
        
        api_requests = []

        for task_id in tasks_id:
            
            source_text = valid_tasks_mapper[task_id]['task_result_content']['source_text']

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

                    if api_result.lang == LanguageEnum.unknown.value:

                        new_saved_content = TranslationTask_TranslationClosedResultFileSchemaV1(
                            source_text=task_result_content['source_text'],
                            source_lang=api_result.lang,
                            target_lang=task_result_content['target_lang'],
                            message=MESSAGES['content_language_is_not_supported'],
                            task_name=TranslationTaskNameEnum.public_plain_text_translation.value
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

                        new_saved_content = TranslationTask_TranslationClosedResultFileSchemaV1(
                            source_text=task_result_content['source_text'],
                            source_lang=api_result.lang,
                            target_lang=task_result_content['target_lang'],
                            message=MESSAGES['source_lang_and_target_lang_are_the_same'],
                            task_name=TranslationTaskNameEnum.public_plain_text_translation.value
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
                   
                        new_saved_content = TranslationTask_NotYetTranslatedResultFileSchemaV1(
                            source_text=task_result_content['source_text'],
                            source_lang=api_result.lang,
                            target_lang=task_result_content['target_lang'],
                            task_name=TranslationTaskNameEnum.public_plain_text_translation.value
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
