

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from modules.background_tasks.detect_file_language_created_by_public_request.main import main as detect_file_language_created_by_public_request
    
    background_task_1_conf = BACKGROUND_TASKS['detect_file_language_created_by_public_request']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        detect_file_language_created_by_public_request,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG,
    )
    
    return background_task_scheduler
    