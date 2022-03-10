

from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager


def add_fresh_jobs(background_task_scheduler: BackgroundTaskManager, BACKGROUND_TASKS):
    
    from modules.background_tasks.translate_plain_text_created_by_public_request.detect_content_language.main import main as detect_content_language
    from modules.background_tasks.translate_plain_text_created_by_public_request.translate_content.main import main as translate_content
    
    # background_task_1_conf = BACKGROUND_TASKS['translate_plain_text_created_by_public_request.detect_content_language']
    
    # if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
    #     background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    # background_task_scheduler.add_job(
    #     detect_content_language,
    #     id=background_task_1_conf.ID,
    #     trigger=background_task_1_conf.TRIGGER,
    #     **background_task_1_conf.CONFIG,
    # )
    
    background_task_2_conf = BACKGROUND_TASKS['translate_plain_text_created_by_public_request.translate_content']
    
    if background_task_scheduler.get_job(background_task_2_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_2_conf.ID)
 
    background_task_scheduler.add_job(
        translate_content,
        id=background_task_2_conf.ID,
        trigger=background_task_2_conf.TRIGGER,
        **background_task_2_conf.CONFIG,
    )
    
    return background_task_scheduler
    