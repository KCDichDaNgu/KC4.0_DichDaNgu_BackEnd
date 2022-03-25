def add_fresh_jobs(background_task_scheduler, BACKGROUND_TASKS):
    
    from tests.background_tasks.translate_file_created_by_private_request.translate_content.docx.main import test_all

    background_task_1_conf = BACKGROUND_TASKS['test_translate_file_created_by_private_request.translate_content.docx']


    if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_1_conf.ID)


    background_task_scheduler.add_job(
        test_all,
        id=background_task_1_conf.ID,
        trigger=background_task_1_conf.TRIGGER,
        **background_task_1_conf.CONFIG
    )

    return background_task_scheduler