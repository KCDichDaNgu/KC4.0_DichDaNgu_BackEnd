from infrastructure.configs.translation_history import TranslationHistoryStatus
from infrastructure.configs.translation_task import TRANSLATION_PRIVATE_TASKS, TranslationTaskNameEnum, TranslationTaskStepEnum
from interface_adapters.dtos.base_response import BaseResponse
from uuid import UUID
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import TRANSLATION_PUBLIC_TASKS, StepStatusEnum, get_task_result_file_path
from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView

from modules.translation_history.dtos.translation_history_response import SingleTranslationHistoryResponse

from core.utils.file import get_full_path
from core.middlewares.authentication.core import get_me
from core.exceptions import NotFoundException

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSingleTranslationHistory(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
        from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
        from modules.system_setting.database.repository import SystemSettingRepository

        self.__translation_history_repository = TranslationHistoryRepository()
        self.__translation_request_repository = TranslationRequestRepository()
        self.__system_setting_repository = SystemSettingRepository()

    @doc.summary(APP_CONFIG.ROUTES['translation_history.get_single']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_history.get_single']['desc'])
    @doc.consumes(
        doc.String(
            description='Task Id',
            name='taskId'
        ), 
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='Translation History Id',
            name='translationHistoryId'
        ), 
        location="query"
    )
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )
    @doc.produces(SingleTranslationHistoryResponse)

    async def get(self, request):

        user = await get_me(request)
        
        task_id = request.args.get('taskId')        
        translation_history_id = request.args.get('translationHistoryId')

        query = {}

        if user:
            query['creator_id'] = UUID(user.id)
        else:
            query['creator_id'] = None
        
        if not task_id is None:
            query['task_id'] = UUID(task_id)
        if not translation_history_id is None:
            query['id'] = UUID(translation_history_id)
            
        translation_history: TranslationHistoryEntity = await self.__translation_history_repository.find_one(query)
        
        if not translation_history:
            return response.json(BaseResponse(**{
                'code': StatusCodeEnum.success.value,
                'data': [],
                'message': MESSAGES['success']
            }).dict())
        
        translation_request = await self.__translation_request_repository.find_one({'id': UUID(translation_history.props.task_id.value)})

        if translation_request.props.task_name in TRANSLATION_PRIVATE_TASKS and not user:
            raise SanicException('Server Error')
        
        
        pos_in_translation_queue = 0
        estimated_watting_time = 0
        
        
        if translation_history.props.status == TranslationHistoryStatus.translating.value:
        
            previous_trans_req = await self.__translation_request_repository.find_many({
                '$and': [
                    {'created_at': {'$lt': translation_request.created_at.value}},
                    {
                        '$or': [
                            {
                                '$and': [
                                    { 'current_step': TranslationTaskStepEnum.translating_language.value},
                                    { 
                                        'step_status': {
                                            '$in': [
                                                StepStatusEnum.not_yet_processed,
                                                StepStatusEnum.in_progress
                                            ]
                                        }
                                    }
                                ]
                            },
                            {
                                '$and': [
                                    { 'current_step': TranslationTaskStepEnum.detecting_language.value },
                                    {
                                        'step_status': {
                                            '$in': [
                                                StepStatusEnum.not_yet_processed
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    } 
                ]
            })
            
            pos_in_translation_queue = len(previous_trans_req) + 1

            system_setting = await self.__system_setting_repository.find_one({})
            
            translation_speed_for_each_character = system_setting.props.translation_speed_for_each_character 
            
            num_chars = sum([trans_req.props.num_chars for trans_req in previous_trans_req]) + translation_request.props.num_chars
            
            estimated_watting_time = translation_speed_for_each_character * num_chars
        

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': translation_request.id.value,
                'translationType': translation_history.props.translation_type,
                'id': translation_history.id.value,
                'status': translation_history.props.status,
                'updatedAt': str(translation_history.updated_at.value),
                'createdAt': str(translation_history.created_at.value),
                'resultUrl': translation_history.props.real_file_path,
                'posInTranslationQueue': pos_in_translation_queue,
                'estimatedWattingTime': estimated_watting_time
            },
            'message': MESSAGES['success']
        }).dict())
