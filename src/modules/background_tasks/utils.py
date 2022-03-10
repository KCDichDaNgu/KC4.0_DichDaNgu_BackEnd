# from asyncio import Task

# from numpy import record
# from infrastructure.configs.task import LanguageDetectionTaskNameEnum, TranslationTaskNameEnum

# from modules.translation_request.database.translation_request.repository import TranslationRequestRepository

# translation_request_repository = TranslationRequestRepository()

# async def get_activation_conditions(task_id):
    
#     if task_id == TranslationTaskNameEnum.private_file_translation.value:
        
#         records = await translation_request_repository.find_many({}, limit=1, order_by={'created_at': 1})
        
#         if len(records) == 0: return False
        
#         if records[0].props.task_name != TranslationTaskNameEnum.private_file_translation.value: return False
        
#         return True 
        
#     elif task_id == TranslationTaskNameEnum.public_file_translation.value:
        
#         records = await translation_request_repository.find_many({}, limit=1, order_by={'created_at': 1})
        
#         if len(records) == 0: return False
        
#         if records[0].props.task_name != TranslationTaskNameEnum.private_file_translation.value: return False
        
#         return True 
    
#     elif task_id == TranslationTaskNameEnum.public_plain_text_translation.value:
        
#         records = await translation_request_repository.find_many({}, limit=1, order_by={'created_at': 1})
        
#         if len(records) == 0: return False
        
#         if records[0].props.task_name != TranslationTaskNameEnum.public_plain_text_translation.value: return False
        
#         return True 
    
#     elif task_id == TranslationTaskNameEnum.private_plain_text_translation.value:
        
#         records = await translation_request_repository.find_many({}, limit=1, order_by={'created_at': 1})
        
#         if len(records) == 0: return False
        
#         if records[0].props.task_name != TranslationTaskNameEnum.private_plain_text_translation.value: return False
        
#         return True 
        
#     return True
    