from infrastructure.configs.main import GlobalConfig
from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def init_test_background_tasks(config: GlobalConfig):

    from tests.background_tasks.delete_invalid_file import add_fresh_jobs as add_fresh_jobs_1
    from tests.background_tasks.delete_invalid_task import add_fresh_jobs as add_fresh_jobs_2
    from tests.background_tasks.detect_file_language_created_by_private_request import add_fresh_jobs as add_fresh_jobs_3
    from tests.background_tasks.detect_file_language_created_by_public_request import add_fresh_jobs as add_fresh_jobs_4
    from tests.background_tasks.detect_plain_text_language_created_by_private_request import add_fresh_jobs as add_fresh_jobs_5
    from tests.background_tasks.detect_plain_text_language_created_by_public_request import add_fresh_jobs as add_fresh_jobs_6
    from tests.background_tasks.send_translation_email import add_fresh_jobs1 as add_fresh_jobs_7
    from tests.background_tasks.send_translation_email import add_fresh_jobs_2 as add_fresh_jobs_8
    from tests.background_tasks.translate_file_created_by_private_request.translate_content.docx import add_fresh_jobs as add_fresh_jobs_9
    from tests.background_tasks.translate_file_created_by_private_request.translate_content.pptx import add_fresh_jobs as add_fresh_jobs_10
    from tests.background_tasks.translate_file_created_by_private_request.translate_content.txt import add_fresh_jobs as add_fresh_jobs_11
    from tests.background_tasks.translate_file_created_by_private_request.translate_content.xlsx  import add_fresh_jobs as add_fresh_jobs_12
    from tests.background_tasks.translate_file_created_by_public_request.translate_content.docx import add_fresh_jobs as add_fresh_jobs_13
    from tests.background_tasks.translate_file_created_by_public_request.translate_content.pptx import add_fresh_jobs as add_fresh_jobs_14
    from tests.background_tasks.translate_file_created_by_public_request.translate_content.txt import add_fresh_jobs as add_fresh_jobs_15
    from tests.background_tasks.translate_file_created_by_public_request.translate_content.xlsx  import add_fresh_jobs as add_fresh_jobs_16
    from tests.background_tasks.translate_plain_text_created_by_private_request import add_fresh_jobs as add_fresh_jobs_17
    from tests.background_tasks.translate_plain_text_created_by_public_request import add_fresh_jobs as add_fresh_jobs_18
    
    
    BACKGROUND_TASKS = config.APP_CONFIG.TEST_BACKGROUND_TASKS

    new_background_task_scheduler = BackgroundTaskManager(AsyncIOScheduler())

    new_background_task_scheduler.remove_all_jobs()

    new_background_task_scheduler = add_fresh_jobs_1(new_background_task_scheduler, BACKGROUND_TASKS)       
    new_background_task_scheduler = add_fresh_jobs_2(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_3(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_4(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_5(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_6(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_7(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_8(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_9(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_10(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_11(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_12(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_13(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_14(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_15(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_16(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_17(new_background_task_scheduler, BACKGROUND_TASKS)
    new_background_task_scheduler = add_fresh_jobs_18(new_background_task_scheduler, BACKGROUND_TASKS)