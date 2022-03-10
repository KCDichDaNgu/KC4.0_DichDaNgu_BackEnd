

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from modules.background_tasks.send_translation_email.main import main as send_translation_email
    
    background_task_1_conf = BACKGROUND_TASKS['send_translation_email']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        send_translation_email,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG,
    )
    
    return background_task_scheduler
    