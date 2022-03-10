

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from modules.background_tasks.delete_invalid_task.main import main as delete_invalid_task
    
    background_task_1_conf = BACKGROUND_TASKS['delete_invalid_task']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        delete_invalid_task,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG,
    )
    
    return background_task_scheduler
    