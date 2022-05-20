from datetime import datetime, timedelta

from uuid import UUID
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    StepStatusEnum,
    get_task_result_file_path
)
from modules.task.database.task_result.repository import TasktResultRepository
from modules.task.database.task.repository import TaskRepository
from modules.system_setting.database.repository import SystemSettingRepository

from core.utils.file import delete_files, delete_folders
import asyncio
from infrastructure.adapters.logger import Logger
from infrastructure.configs.translation_task import (
    FILE_TRANSLATION_TASKS, 
    PLAIN_TEXT_TRANSLATION_TASKS, 
    get_file_translation_file_path
)
from infrastructure.configs.language_detection_task import (
    get_file_language_detection_file_path, 
    FILE_LANGUAGE_DETECTION_TASKS, 
    PLAIN_TEXT_LANGUAGE_DETECTION_TASKS
)

import mimetypes
import smtplib
from email.message import EmailMessage

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository

from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository

import time

from core.utils.mail import gmail_send_message_with_attachment

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

translation_history_repository = TranslationHistoryRepository()
language_detection_history_repository = LanguageDetectionHistoryRepository()
task_repository = TaskRepository()
task_result_repository = TasktResultRepository()
system_setting_repository = SystemSettingRepository()

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()

language_detection_request_repository = LanguageDetectionRequestRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()

logger = Logger('Task: delete_invalid_task')

async def main():

    logger.debug(
        msg=f'New task delete_invalid_task run in {datetime.now()}'
    )

    print(f'New task delete_invalid_task run in {datetime.now()}')

    try:
        
        system_setting = await system_setting_repository.find_one({})
        
        task_expired_duration = system_setting.props.task_expired_duration
        
        email_for_sending_email = system_setting.props.email_for_sending_email
        email_password_for_sending_email = system_setting.props.email_password_for_sending_email

        if not email_for_sending_email or not email_password_for_sending_email:
            print('Email not setup')
            return

        invalid_tasks = await task_repository.find_many(
           params={
                "$and": [
                    {
                        "$and": [
                            {
                                "step_status": {
                                    "$in": [
                                        StepStatusEnum.cancelled.value,
                                        StepStatusEnum.closed.value,
                                    ]
                                }
                            },
                            {"created_at": {"$lt": datetime.now() - timedelta(seconds=task_expired_duration)}},
                        ],
                    },
                    {
                       "task_name": {
                           "$in": [
                               *PLAIN_TEXT_TRANSLATION_TASKS, 
                               *FILE_TRANSLATION_TASKS, 
                               *PLAIN_TEXT_LANGUAGE_DETECTION_TASKS, 
                               *FILE_LANGUAGE_DETECTION_TASKS
                            ]
                       } 
                    }
                ]
            }
        )
        
        if len(invalid_tasks) == 0: return
        
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        smtp_server.ehlo()
        smtp_server.login(email_for_sending_email, email_password_for_sending_email)
        
        for task in invalid_tasks:
            
            email_id = round(time.time())
                
            msg = EmailMessage()
            
            msg['Subject'] = f'TranslationServerError - Lỗi phần mềm dịch #{email_id}'
            msg['To'] = email_for_sending_email
            msg['From'] = email_for_sending_email
            
            if task.props.task_name in PLAIN_TEXT_TRANSLATION_TASKS:
                
                await send_email_for_cancelled_plain_text_translation(task, msg)
                
            if task.props.task_name in FILE_TRANSLATION_TASKS:
                
                await send_email_for_cancelled_file_translation(task, msg)
                
            if task.props.task_name in PLAIN_TEXT_LANGUAGE_DETECTION_TASKS:
                
                await send_email_for_cancelled_plain_text_language_detection(task, msg)
                
            if task.props.task_name in FILE_LANGUAGE_DETECTION_TASKS:
                
                await send_email_for_cancelled_file_language_detection(task, msg)
                
            smtp_server.send_message(msg)
            
        smtp_server.close()
        
        invalid_tasks_ids = list(map(lambda task: task.id.value, invalid_tasks)) if not invalid_tasks is None else []

        invalid_tasks_results = []

        invalid_tasks_results = await task_result_repository.find_many(
            params={
                "task_id": {
                    "$in": [UUID(task_id) for task_id in invalid_tasks_ids]
                }
            }
        )

        invalid_tasks_file_paths = list(map(lambda task: task.props.file_path, invalid_tasks_results))
        task_results_file_paths, file_translation_folders, language_detection_folders = get_to_be_deleted_file_path(invalid_tasks_file_paths)

        if len(invalid_tasks_ids) == 0:
            logger.debug(
                msg=f'An task delete_invalid_task end in {datetime.now()}\n')

            print(f'An task delete_invalid_task end in {datetime.now()}\n')
            return
        
        async with db_instance.session() as session:

            async with session.start_transaction():

                clean_request = []

                clean_request.append(
                    language_detection_history_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    translation_history_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    task_result_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    task_repository.delete_many_by_condition(
                        conditions=[{"_id": invalid_tasks_ids}]
                    )
                )

                await delete_files(task_results_file_paths)

                await delete_folders(file_translation_folders + language_detection_folders)

                await asyncio.gather(*clean_request)

    except Exception as e:
        logger.error(e)

        import traceback
        
        print(traceback.print_exc())

    logger.debug(
        msg=f'An task delete_invalid_task end in {datetime.now()}\n'
    )
    
async def send_email_for_cancelled_plain_text_translation(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value
    
    msg.set_content(
        f"""
        Đã xảy ra lỗi!
        
        Yêu cầu được tạo ra vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}
            
        Chi tiết lỗi: 
        
        {task.props.error_message}
        
        Chi tiết yêu cầu nằm trong những tệp đính kèm
        
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
    
    msg.add_attachment(
        bytes(source_text, 'utf-16'),
        maintype='text', 
        subtype='plain',
        filename=f'{source_lang}.txt'
    )
    
    return msg

async def send_email_for_cancelled_plain_text_language_detection(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value

    msg.set_content(
        f"""
        Đã xảy ra lỗi!
        
        Yêu cầu được tạo ra vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}
            
        Chi tiết lỗi: 
        
        {task.props.error_message}
        
        Chi tiết yêu cầu nằm trong những tệp đính kèm
        
        Trân trọng,
        Nhóm phát triển 
        """
    )
    
    task_result = await language_detection_request_result_repository.find_one(
        params=dict(
            task_id=UUID(task.id.value)
        )
    )
    
    data = await task_result.read_data_from_file()
    
    source_text = data['source_text']
    
    msg.add_attachment(
        bytes(source_text, 'utf-16'),
        maintype='text', 
        subtype='plain',
        filename=f'source_text.txt'
    )
    
    return msg


async def send_email_for_cancelled_file_translation(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value
    
    # to_mail = msg['to_mail']
    # from_mail = msg['from_mail']
    # subject = msg['subject']
    
    msg.set_content(
        f"""
        Đã xảy ra lỗi!
        
        Yêu cầu được tạo ra vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}
            
        Chi tiết lỗi: 
        
        {task.props.error_message}
        
        Chi tiết yêu cầu nằm trong những tệp đính kèm
        
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
    
    # files = [original_file_full_path]
        
    # msg = gmail_send_message_with_attachment(
    #     to_mail=to_mail,
    #     from_mail=from_mail,
    #     message=message,
    #     files=files,
    #     subject=subject
    # )
    
    return msg
    
async def send_email_for_cancelled_file_language_detection(task, msg: EmailMessage):
    
    task_created_at = task.created_at.value
    
    # to_mail = msg['to_mail']
    # from_mail = msg['from_mail']
    # subject = msg['subject']
    
    msg.set_content(
        f"""
        Đã xảy ra lỗi!
        
        Yêu cầu được tạo ra vào {task_created_at.hour} giờ {task_created_at.minute} phút ngày {task_created_at.day}/{task_created_at.month}/{task_created_at.year}
            
        Chi tiết lỗi: 
        
        {task.props.error_message}
        
        Chi tiết yêu cầu nằm trong những tệp đính kèm
        
        Trân trọng,
        Nhóm phát triển 
        """
    )
    
    task_result = await language_detection_request_result_repository.find_one(
        params=dict(
            task_id=UUID(task.id.value)
        )
    )
    
    data = await task_result.read_data_from_file()
    
    source_file_full_path = data['source_file_full_path']
    
    ctype1, encoding1 = mimetypes.guess_type(source_file_full_path)
    
    if ctype1 is None or encoding1 is not None:
        ctype1 = 'application/octet-stream'
        
    maintype1, subtype1 = ctype1.split('/', 1)
    
    with open(source_file_full_path, 'rb') as fp:
        msg.add_attachment(
            fp.read(),
            maintype=maintype1, 
            subtype=subtype1,
            filename=source_file_full_path.split('/')[-1]
        )
        
    # files = [source_file_full_path]
        
    # msg = gmail_send_message_with_attachment(
    #     to_mail=to_mail,
    #     from_mail=from_mail,
    #     message=message,
    #     files=files,
    #     subject=subject
    # )
    
    return msg

def get_task_id_from_task_result_file_path(file_path):

    return (file_path.split('.')[0]).split('__')[-1]

def get_to_be_deleted_file_path(invalid_file_paths):

    task_results_file_paths = list(
        map(
            lambda f_path: get_task_result_file_path(f_path),
            invalid_file_paths,
        )
    )
    task_ids = list(
        map(
            lambda f_path: get_task_id_from_task_result_file_path(f_path),
            invalid_file_paths,
        )
    )

    file_translation_folders = list(
        map(
            lambda f_path: get_file_translation_file_path(f_path, ""),
            task_ids,
        )
    )
    language_detection_folders = list(
        map(
            lambda f_path: get_file_language_detection_file_path(f_path, ""),
            task_ids,
        )
    )

    return task_results_file_paths, file_translation_folders, language_detection_folders
