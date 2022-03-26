

def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):

    from tests.background_tasks.send_translation_email.main import test_send_email_result_for_text_translation
    
    background_task_1_conf = BACKGROUND_TASKS['test_send_email_result_for_text_translation']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_send_email_result_for_text_translation,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler
    

def add_fresh_jobs_1(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.send_translation_email.main import test_send_email_result_for_file_translation
    
    background_task_1_conf = BACKGROUND_TASKS['test_send_email_result_for_file_translation']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_send_email_result_for_file_translation,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler



def add_fresh_jobs_3(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.send_translation_email.main import test_send_email_result_for_text_translation
    from tests.background_tasks.send_translation_email.main import test_main
    
    background_task_1_conf = BACKGROUND_TASKS['test_send_translation_email_main']
    
    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    background_task_scheduler.add_job(
        test_main,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )
    
    return background_task_scheduler
    
    