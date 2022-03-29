

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.delete_invalid_task.main import test_all
    
    background_task_conf = BACKGROUND_TASKS['delete_invalid_task.test_all']
    
    if background_task_scheduler.get_job(background_task_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_conf.ID)
 
    background_task_scheduler.add_job(
        test_all,
        id=background_task_conf.ID,
        trigger=background_task_conf.TRIGGER,
        **background_task_conf.CONFIG
    )
    
    return background_task_scheduler