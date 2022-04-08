from modules.background_tasks.detect_plain_text_language_created_by_public_request.main import read_task_result, execute_in_batch, mark_invalid_tasks, main
import pandas
from core.value_objects.id import ID
from infrastructure.configs.task import (
    LanguageDetectionTask_LangUnknownResultFileSchemaV1, 
    LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1,
    LanguageDetectionTaskNameEnum, 
    CreatorTypeEnum,
    LanguageDetectionTaskStepEnum, 
    StepStatusEnum
)
from infrastructure.configs.language_detection_history import (
    LanguageDetectionHistoryTypeEnum, LanguageDetectionHistoryStatus
)
from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository

from modules.language_detection_request.domain.entities.language_detection_request import LanguageDetectionRequestEntity, LanguageDetectionRequestProps
from modules.language_detection_request.domain.entities.language_detection_request_result import LanguageDetectionRequestResultEntity, LanguageDetectionRequestResultProps
from modules.language_detection_request.domain.entities.language_detection_history import LanguageDetectionHistoryEntity, LanguageDetectionHistoryProps
from modules.system_setting.database.repository import SystemSettingRepository

language_detection_request_repository = LanguageDetectionRequestRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()
language_detection_history = LanguageDetectionHistoryRepository()
system_setting_repository = SystemSettingRepository()

df = pandas.read_csv('src/tests/background_tasks/detect_plain_text_language_created_by_public_request/sample_data/task_file_data.csv')
async def test_read_task_result():
    print('====TEST READ_TASK_RESULT FUNTION====\n')
    #Test 1:
    try :
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result([], [], [])
        print("Test read_task_result in Test case 0: TRUE\n")
    except Exception as e:
        print(e)
        print("Test read_task_result in Test case 0: FALSE\n")
    
    #Test 2:
    for i, item in df.iterrows():
        try :
            language_detect_request_entity = LanguageDetectionRequestEntity(
                LanguageDetectionRequestProps(
                    creator_id= ID(None),
                    task_name= LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
                    creator_type= CreatorTypeEnum.end_user.value,
                    step_status= StepStatusEnum.closed.value,
                    current_step= LanguageDetectionTaskStepEnum.detecting_language.value
                )
            )
            tasks = [language_detect_request_entity]

            language_detect_request_result_entity = LanguageDetectionRequestResultEntity(
                LanguageDetectionRequestResultProps(
                    task_id= ID(None),
                    step= LanguageDetectionTaskStepEnum.detecting_language.value,
                    file_path= item['task_file_name']
                )
            )
            tasks_result = [language_detect_request_result_entity]

            language_detect_history_entity = LanguageDetectionHistoryEntity(
                LanguageDetectionHistoryProps(
                    creator_id= ID(None),
                    task_id= ID(item['task_id']),
                    language_detection_type= LanguageDetectionHistoryTypeEnum.public_plain_text_language_detection.value,
                    status= LanguageDetectionHistoryStatus.detecting.value,
                    file_path= item['task_file_name']
                )
            )
            language_detection_history = [language_detect_history_entity]

            valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
                tasks_result= tasks_result,
                tasks= tasks,
                language_detections_history= language_detection_history
            )
            print("Test read_task_result in Test case %d: TRUE\n", i+1)
            print(f"Tasks: ", tasks)
            print(f"Tasks_result: ", tasks_result)
            print(f"language_detect_history: ", language_detection_history)
            print(f"valid_tasks_mapper result:", valid_tasks_mapper)
            print(f"invalid_tasks_mapper result:", invalid_tasks_mapper)
        except Exception as e:
            print(e)
            print("Test read_task_result in Test case %d: FALSE\n", i+1)
        
async def test_mark_invalid_tasks():
    print('====TEST MARK_INVALID_TASKS FUNTION====\n')
    #Test 1:
    try :
        invalid_tasks_mapper = {}
        await mark_invalid_tasks(invalid_tasks_mapper)
        print("Test mark_invalid_task in Test Case 0: TRUE\n")
    except Exception as e:
        print(e)
        print("Test mark_invalid_task in Test Case 0: FALSE\n")
    
    #Test 2:
    for i, item in df.iterrows():
        try :
            language_detect_request_entity = LanguageDetectionRequestEntity(
                LanguageDetectionRequestProps(
                    creator_id= ID(None),
                    task_name= LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
                    creator_type= CreatorTypeEnum.end_user.value,
                    step_status= StepStatusEnum.closed.value,
                    current_step= LanguageDetectionTaskStepEnum.detecting_language.value
                )
            )
            tasks = [language_detect_request_entity]

            language_detect_request_result_entity = LanguageDetectionRequestResultEntity(
                LanguageDetectionRequestResultProps(
                    task_id= ID(item['task_id']),
                    step= LanguageDetectionTaskStepEnum.detecting_language.value,
                    file_path= item['task_file_name']
                )
            )
            tasks_result = [language_detect_request_result_entity]

            language_detect_history_entity = LanguageDetectionHistoryEntity(
                LanguageDetectionHistoryProps(
                    creator_id= ID(None),
                    task_id= ID(item['task_id']),
                    language_detection_type= LanguageDetectionHistoryTypeEnum.public_plain_text_language_detection.value,
                    status= LanguageDetectionHistoryStatus.detecting.value,
                    file_path= item['task_file_name']
                )
            )
            language_detection_history = [language_detect_history_entity]

            invalid_tasks_mapper = {0: {
                "task_result": tasks_result,
                "trans_history": language_detection_history,
                "task": tasks
            }}
            await mark_invalid_tasks(invalid_tasks_mapper)
            print("Test mark_invalid_task in Test Case %d: TRUE\n", i+1)
        except Exception as e:
            print(e)
            print("Test mark_invalid_task in Test Case %d: FALSE\n", i+1)

async def test_execute_in_batch():
    print('====TEST EXECUTE_IN_BATCH FUNTION====\n')
    system_setting = await system_setting_repository.find_one({})
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.translation_api_allowed_concurrent_req
    #Test 1:
    try :
        valid_tasks_mapper = []
        await execute_in_batch(
            valid_tasks_mapper= valid_tasks_mapper,
            tasks_id= [],
            allowed_concurrent_request= ALLOWED_CONCURRENT_REQUEST
        )
        print("Test excute_in_batch in Test case 0: TRUE\n")
    except Exception as e:
        print(e)
        print("Test excute_in_batch in Test case 0: FALSE\n")
    
    #Test 2:
    for i, item in df.iterrows():
        try :
            language_detect_request_entity = LanguageDetectionRequestEntity(
                LanguageDetectionRequestProps(
                    creator_id= ID(None),
                    task_name= LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value,
                    creator_type= CreatorTypeEnum.end_user.value,
                    step_status= StepStatusEnum.closed.value,
                    current_step= LanguageDetectionTaskStepEnum.detecting_language.value
                )
            )
            tasks = [language_detect_request_entity]

            language_detect_request_result_entity = LanguageDetectionRequestResultEntity(
                LanguageDetectionRequestResultProps(
                    task_id= ID(item['task_id']),
                    step= LanguageDetectionTaskStepEnum.detecting_language.value,
                    file_path= item['task_file_name']
                )
            )
            tasks_result = [language_detect_request_result_entity]

            language_detect_history_entity = LanguageDetectionHistoryEntity(
                LanguageDetectionHistoryProps(
                    creator_id= ID(None),
                    task_id= ID(item['task_id']),
                    language_detection_type= LanguageDetectionHistoryTypeEnum.public_plain_text_language_detection.value,
                    status= LanguageDetectionHistoryStatus.detecting.value,
                    file_path= item['task_file_name']
                )
            )
            language_detection_history = [language_detect_history_entity]
            data = await tasks_result.read_data_from_file()
            
            if data['status'] == LanguageDetectionTask_LangUnknownResultFileSchemaV1(
                source_text='',
                task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
            ).status:

                valid_tasks_mapper = {0: {
                    'task_result_content': data,
                    'task_result': tasks_result,
                    'trans_history': language_detection_history,
                    'task': tasks
                }}
            
            await execute_in_batch(
                valid_tasks_mapper= valid_tasks_mapper,
                tasks_id= tasks[0].id,
                allowed_concurrent_request= ALLOWED_CONCURRENT_REQUEST
            )
            print("Test excute_in_batch in Test case %d: TRUE\n", i+1)
        except Exception as e:
            print(e)
            print("Test excute_in_batch in Test case %d: FALSE\n", i+1)

async def test_main():
    print('====TEST MAIN FUNTION====\n')
    try :
        await main()
        print("Test main in Test case: TRUE\n")
    except Exception as e:
        print(e)
        print("Test main in Test case: FALSE\n")

async def test_all():
    await test_read_task_result()
    await test_mark_invalid_tasks()
    await test_execute_in_batch()
    await test_main()
    
