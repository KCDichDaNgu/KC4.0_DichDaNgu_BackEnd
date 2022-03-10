

from infrastructure.adapters.background_task_manager.main import BackgroundTaskManager


def add_fresh_jobs(background_task_scheduler: BackgroundTaskManager, BACKGROUND_TASKS):
    
    from modules.background_tasks.translate_file_created_by_public_request.detect_content_language.main import main as detect_content_language
    
    from modules.background_tasks.translate_file_created_by_public_request.translate_content.docx.main import main as translate_content_docx
    from modules.background_tasks.translate_file_created_by_public_request.translate_content.pptx.main import main as translate_content_pptx
    from modules.background_tasks.translate_file_created_by_public_request.translate_content.txt.main import main as translate_content_txt
    from modules.background_tasks.translate_file_created_by_public_request.translate_content.xlsx.main import main as translate_content_xlsx
    
    # background_task_1_conf = BACKGROUND_TASKS['translate_file_created_by_public_request.detect_content_language']
    
    # if background_task_scheduler.get_job(background_task_1_conf.ID) != None:
    #     background_task_scheduler.remove_job(background_task_1_conf.ID)
 
    # background_task_scheduler.add_job(
    #     detect_content_language,
    #     id=background_task_1_conf.ID,
    #     trigger=background_task_1_conf.TRIGGER,
    #     **background_task_1_conf.CONFIG,
    # )
    
    background_task_2_conf = BACKGROUND_TASKS['translate_file_created_by_public_request.translate_content.docx']
    
    if background_task_scheduler.get_job(background_task_2_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_2_conf.ID)
 
    background_task_scheduler.add_job(
        translate_content_docx,
        id=background_task_2_conf.ID,
        trigger=background_task_2_conf.TRIGGER,
        **background_task_2_conf.CONFIG,
    )
    
    background_task_3_conf = BACKGROUND_TASKS['translate_file_created_by_public_request.translate_content.pptx']
    
    if background_task_scheduler.get_job(background_task_3_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_3_conf.ID)
 
    background_task_scheduler.add_job(
        translate_content_pptx,
        id=background_task_3_conf.ID,
        trigger=background_task_3_conf.TRIGGER,
        **background_task_3_conf.CONFIG,
    )
    
    background_task_4_conf = BACKGROUND_TASKS['translate_file_created_by_public_request.translate_content.txt']
    
    if background_task_scheduler.get_job(background_task_4_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_4_conf.ID)
 
    background_task_scheduler.add_job(
        translate_content_txt,
        id=background_task_4_conf.ID,
        trigger=background_task_4_conf.TRIGGER,
        **background_task_4_conf.CONFIG,
    )
    
    background_task_5_conf = BACKGROUND_TASKS['translate_file_created_by_public_request.translate_content.xlsx']
    
    if background_task_scheduler.get_job(background_task_5_conf.ID) != None:
        background_task_scheduler.remove_job(background_task_5_conf.ID)
 
    background_task_scheduler.add_job(
        translate_content_xlsx,
        id=background_task_5_conf.ID,
        trigger=background_task_5_conf.TRIGGER,
        **background_task_5_conf.CONFIG,
    )
    
    return background_task_scheduler
    