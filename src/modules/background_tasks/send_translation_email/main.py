from uuid import UUID
from imbox import Imbox
import mimetypes
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time
from infrastructure.configs.translation_task import (
    PLAIN_TEXT_TRANSLATION_TASKS, 
    FILE_TRANSLATION_TASKS, 
    TRANSLATION_PRIVATE_TASKS, 
    TRANSLATION_PUBLIC_TASKS
)

from infrastructure.adapters.logger import Logger
from modules.task.database.task.repository import TaskRepository
from modules.system_setting.database.repository import SystemSettingRepository
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository

from infrastructure.configs.task import (
    TranslationTaskStepEnum, 
    StepStatusEnum
)

import pymongo

logger = Logger('Task: send_translation_email')

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
system_setting_repository = SystemSettingRepository()

async def main():

    logger.debug(
        msg=f'New task send_translation_email run in {datetime.now()}'
    )

    print(f'New task send_translation_email run in {datetime.now()}')
    
    try:
        system_setting = await system_setting_repository.find_one({})
        
        email_for_sending_email = system_setting.props.email_for_sending_email
        email_password_for_sending_email = system_setting.props.email_password_for_sending_email
        
        tasks = await translation_request_repository.find_many(
            params={
                'task_name': { '$in': TRANSLATION_PRIVATE_TASKS + TRANSLATION_PUBLIC_TASKS },
                'current_step': TranslationTaskStepEnum.translating_language.value,
                'step_status': {
                    '$in': [
                        StepStatusEnum.completed.value
                    ]
                },
                'receiver_email': {
                    '$ne': None
                },
                'total_email_sent': { '$in': [None, 0] }
            },
            limit=1,
            order_by=[('created_at', pymongo.ASCENDING)]
        )
        
        if len(tasks) == 0: return
        
        try: 
            
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            
            smtp_server.ehlo()
            smtp_server.login(email_for_sending_email, email_password_for_sending_email)
            
            for task in tasks:
                email_id = round(time.time())
                
                msg = EmailMessage()
                
                msg['Subject'] = f'Kết quả dịch #{email_id}'
                msg['To'] = task.props.receiver_email
                msg['From'] = email_for_sending_email
                
                if task.props.task_name in PLAIN_TEXT_TRANSLATION_TASKS:
                    
                    msg = await send_email_result_for_text_translation(task, msg)
                    
                if task.props.task_name in FILE_TRANSLATION_TASKS:
                    
                    msg = await send_email_result_for_file_translation(task, msg)
                
                smtp_server.send_message(msg)
                
                total_email_sent = 0
                
                if task.props.total_email_sent == None: total_email_sent = 0
                else: total_email_sent = task.props.total_email_sent + 1
                
                await translation_request_repository.update(
                    task, 
                    dict(
                        total_email_sent=total_email_sent
                    )
                )
                    
            smtp_server.close()
                
        except Exception as e:
            logger.error(e)

    except Exception as e:
        logger.error(e)

        print(e)

    logger.debug(
        msg=f'An task send_translation_email end in {datetime.now()}\n'
    )
    
    print(f'An task send_translation_email end in {datetime.now()}\n')
    
async def send_email_result_for_text_translation(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value
    
    msg.set_content(
        f"""
        Xin chào,
        
        Chúng tôi xin gửi bạn kết quả dịch đã được yêu cầu vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}.
        
        Trân trọng,
        Nhóm phát triển 
        """
    )
    
    task_result = await translation_request_result_repository.find_one(
        params=dict(
            task_id=UUID(task.id.value)
        )
    )
    
    data = await task_result.read_data_from_file()
    
    source_text = data['source_text']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    target_text = data['target_text']
    
    msg.add_attachment(
        bytes(source_text, 'utf-16'),
        maintype='text', 
        subtype='plain',
        filename=f'{source_lang}.txt'
    )
    
    msg.add_attachment(
        bytes(target_text, 'utf-16'),
        maintype='text', 
        subtype='plain',
        filename=f'{target_lang}.txt'
    )
    
    return msg

async def send_email_result_for_file_translation(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value
    
    msg.set_content(
        f"""
        Xin chào,
            
        Chúng tôi xin gửi bạn kết quả dịch đã được yêu cầu vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}.
            
        Trân trọng,
        Nhóm phát triển 
        """
    )
    
    task_result = await translation_request_result_repository.find_one(
        params=dict(
            task_id=UUID(task.id.value)
        )
    )
    
    data = await task_result.read_data_from_file()
    
    original_file_full_path = data['original_file_full_path']
    target_file_full_path = data['target_file_full_path']
    
    ctype1, encoding1 = mimetypes.guess_type(original_file_full_path)
    
    if ctype1 is None or encoding1 is not None:
        ctype1 = 'application/octet-stream'
        
    maintype1, subtype1 = ctype1.split('/', 1)
    
    with open(original_file_full_path, 'rb') as fp:
        msg.add_attachment(
            fp.read(),
            maintype=maintype1, 
            subtype=subtype1,
            filename=original_file_full_path.split('/')[-1]
        )
    
    ctype2, encoding2 = mimetypes.guess_type(target_file_full_path)
    
    if ctype2 is None or encoding2 is not None:
        ctype2 = 'application/octet-stream'
        
    maintype2, subtype2 = ctype2.split('/', 1)
        
    with open(target_file_full_path, 'rb') as fp:
        msg.add_attachment(
            fp.read(),
            maintype=maintype2, 
            subtype=subtype2,
            filename=target_file_full_path.split('/')[-1]
        )
    
    return msg
