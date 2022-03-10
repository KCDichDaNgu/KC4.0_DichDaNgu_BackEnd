from infrastructure.configs.language_detection_history import LanguageDetectionHistoryStatus
from infrastructure.configs.language_detection_task import LanguageDetectionTaskNameEnum, LanguageDetectionTaskStepEnum
from interface_adapters.dtos.base_response import BaseResponse
from uuid import UUID
from modules.language_detection_request.domain.entities.language_detection_history import LanguageDetectionHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import LANGUAGE_DETECTION_PUBLIC_TASKS, StepStatusEnum
from infrastructure.configs.message import MESSAGES
from sanic import response
from modules.language_detection_history.queries.get_single_language_detection_history.request_dto import GetSingleLanguageDetectionHistoryRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.language_detection_history.dtos.language_detection_history_response import SingleLanguageDetectionHistoryResponse

from core.utils.file import get_full_path

from core.exceptions import NotFoundException

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSingleLanguageDetectionHistory(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository
        from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository
        from modules.system_setting.database.repository import SystemSettingRepository
        
        self.__language_detection_history_repository = LanguageDetectionHistoryRepository()
        self.__language_detection_request_repository = LanguageDetectionRequestRepository()
        self.__system_setting_repository = SystemSettingRepository()

    @doc.summary(APP_CONFIG.ROUTES['language_detection_history.get_single']['summary'])
    @doc.description(APP_CONFIG.ROUTES['language_detection_history.get_single']['desc'])
    @doc.consumes(
        doc.String(
            description='Task Id',
            name='taskId'
        ), 
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='LanguageDetection History Id',
            name='languageDetectionHistoryId'
        ), 
        location="query"
    )
    @doc.produces(SingleLanguageDetectionHistoryResponse)

    async def get(self, request):
        
        task_id = request.args.get('taskId')
        
        language_detection_history_id = request.args.get('languageDetectionHistoryId')

        query = {}
        
        if not task_id is None:
            query['task_id'] = UUID(task_id)

        if not language_detection_history_id is None:
            query['id'] = UUID(language_detection_history_id)
            
        language_detection_history: LanguageDetectionHistoryEntity = await self.__language_detection_history_repository.find_one(query)
        
        if not language_detection_history:
            raise NotFoundException('LanguageDetection not found')
        
        
        task = await self.__language_detection_request_repository.find_one({'id': UUID(language_detection_history.props.task_id.value)})

        if task.props.task_name not in LANGUAGE_DETECTION_PUBLIC_TASKS:
            raise SanicException('Server Error')
        
        
        pos_in_lang_detection_queue = 0
        estimated_watting_time = 0
        
        if language_detection_history.props.status == LanguageDetectionHistoryStatus.detecting.value:
        
            previous_lang_detection_req = await self.__language_detection_request_repository.find_many({
                '$and': [
                    {'created_at': {'$lt': task.created_at.value}},
                    {
                        '$and': [
                            { 'current_step': LanguageDetectionTaskStepEnum.detecting_language.value },
                            { 
                                'step_status': {
                                    '$in': [
                                        StepStatusEnum.not_yet_processed
                                    ]
                                }
                            }
                        ],
                    } 
                ]
            })
            
            pos_in_lang_detection_queue = len(previous_lang_detection_req) + 1

            system_setting = await self.__system_setting_repository.find_one({})
            
            language_detection_speed = system_setting.props.language_detection_speed 
            
            estimated_watting_time = language_detection_speed * pos_in_lang_detection_queue

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': task.id.value,
                'language_detectionType': language_detection_history.props.language_detection_type,
                'id': language_detection_history.id.value,
                'status': language_detection_history.props.status,
                'updatedAt': str(language_detection_history.updated_at.value),
                'createdAt': str(language_detection_history.created_at.value),
                'resultUrl': language_detection_history.props.real_file_path,
                'posInLangDetectionQueue': pos_in_lang_detection_queue,
                'estimatedWattingTime': estimated_watting_time
            },
            'message': MESSAGES['success']
        }).dict())
