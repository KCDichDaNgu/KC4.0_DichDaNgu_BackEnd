
from datetime import datetime
from infrastructure.configs.user import UserRole
from interface_adapters.dtos.base_response import BaseResponse
from uuid import UUID
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import TRANSLATION_PUBLIC_TASKS, get_task_result_file_path, PLAIN_TEXT_TRANSLATION_TASKS
from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
 
from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_history.dtos.translation_history_feedback_response import ManyTranslationHistoryFeedbackResponse
import json
from core.utils.file import get_full_path
from core.middlewares.authentication.core import get_me
import aiofiles
from core.exceptions import NotFoundException
 
config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG
PAGINATION_CONFIG = config.PAGINATION
 
 
class GetManyTranslationHistoryFeedback(HTTPMethodView):
 
    def __init__(self) -> None:
        super().__init__()
 
        from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
        from modules.user.database.user.repository import UserRepository
        
        self.__translation_history_repository = TranslationHistoryRepository()
        self.__user_repository = UserRepository()
 
    @doc.summary(APP_CONFIG.ROUTES['translation_history.get_feedback_list']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_history.get_feedback_list']['desc'])

    # @doc.consumes(
    #     doc.String(
    #         description='Translation type',
    #         name='translationType'
    #     ),
    #     location="query"
    # )
    @doc.consumes(
        doc.String(
            description='Status',
            name='status'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='Status',
            name='rating'
        ),
        location="query"
    )
    @doc.consumes(
        doc.Integer(
            description='pagination__page',
            name='pagination__page'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='sort__field',
            name='sort_field'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='sort__direction',
            name='sort_direction'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='createdAt__from',
            name='createdAt__from'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='createdAt__to',
            name='createdAt__to'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='userUpdatedAt__from',
            name='createdAt__from'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='userUpdatedAt__to',
            name='createdAt__to'
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
    @doc.produces(ManyTranslationHistoryFeedbackResponse)

    async def get(self, request):

        user = await get_me(request)
        
        if user.role != UserRole.admin.value:
            return response.json(
                status=404,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['not_found']
                }
            )
        

        status = request.args['status'] if 'status' in request.args else []
        rating = request.args['rating'] if 'rating' in request.args else []
        
        created_at__from = request.args.get('createdAt__from', None)
        created_at__to = request.args.get('createdAt__to', None)
        
        user_updated_at__from = request.args.get('userUpdatedAt__from', None)
        user_updated_at__to = request.args.get('userUpdatedAt__to', None)
        
        page = request.args.get('pagination__page')
        sort = {
            "key": request.args.get('sort__field', 'created_at'),
            "direction": request.args.get('sort__direction', 1)
        }
           
        pagination = {
            'page': PAGINATION_CONFIG.DEFAULT_PAGE,
            'per_page': PAGINATION_CONFIG.DEFAULT_PER_PAGE
        }
 
        query = {
            'user_updated_at': {
                '$ne': None
            },
            'translation_type': {
                '$in': PLAIN_TEXT_TRANSLATION_TASKS
            }
        }
        
        if not rating is None:
            if type(rating) == list:
                query['rating'] = {'$in': rating}
                query['rating'] = {'$in': [None if r == 'not_rated' else r for r in rating]}
            else:
                query['rating'] = rating
                query['rating'] = None if rating == 'not_rated' else rating
        
        if not status is None:
            if type(status) == list:
                query['status'] = {'$in': status}
            else:
                query['status'] = status

        if not page is None:
            pagination['page'] = abs(int(page))
            
        if created_at__from is not None:
            query.update({
                'created_at': {
                    '$gte': datetime.fromtimestamp(float(created_at__from)/1000.0)
                }
            })
            
        if created_at__to is not None:
            
            if 'created_at' not in query:
                query.update({
                    'created_at': {
                        '$lte': datetime.fromtimestamp(float(created_at__to)/1000.0)
                    }
                })
            else:
                query['created_at'].update({
                    '$lte': datetime.fromtimestamp(float(created_at__to)/1000.0)
                })
            
        if user_updated_at__from is not None:
            query.update({
                'user_updated_at': {
                    '$gte': datetime.fromtimestamp(float(user_updated_at__from)/1000.0)
                }
            })
            
        if user_updated_at__to is not None:
            
            if 'user_updated_at' not in query:
                query.update({
                    'user_updated_at': {
                        '$lte': datetime.fromtimestamp(float(user_updated_at__to)/1000.0)
                    }
                })
            else:
                query['user_updated_at'].update({
                    '$lte': datetime.fromtimestamp(float(user_updated_at__to)/1000.0)
                })
 
        query_result = await self.__translation_history_repository.find_many_paginated(
            query,
            pagination,
            sort
        )
 
        translation_history: TranslationHistoryEntity = query_result.data
        
        translation_history_feedback = []
        
        for item in translation_history:
            
            result_url = get_full_path(get_task_result_file_path(item.props.file_path))
            
            async with aiofiles.open(result_url) as f:
            
                data = await f.read()
                
                data = json.loads(data)
                
            translation_history_feedback.append({
                'taskId': item.props.task_id.value,
                'translationType': item.props.translation_type,
                'creator_id': item.props.creator_id.value,
                'id': item.id.value,
                'status': item.props.status,
                'updatedAt': str(item.updated_at.value),
                'createdAt': str(item.created_at.value),
                'resultUrl': get_full_path(get_task_result_file_path(item.props.file_path)),
                'rating': item.props.rating,
                'sourceText': data['source_text'],
                'translatedText': data['target_text'],
                'userEditedTranslation': item.props.user_edited_translation,
                'userUpdatedAt': str(item.props.user_updated_at.value)
            })
        
        
        creator_in_db = await self.__user_repository.find_many({
            'id': {'$in': [UUID(cid['creator_id']) for cid in translation_history_feedback if cid['creator_id']]}
        })
        
        
        for thfb in translation_history_feedback:
            
            if not thfb['creator_id']: continue
            
            for _cid in creator_in_db:
                
                if _cid.id.value == thfb['creator_id']:
                    
                    thfb.update({'username': _cid.props.username})
            
 
        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                "per_page": query_result.per_page,
                "page": query_result.page,
                "total_entries": query_result.total_entries,
                "list": translation_history_feedback
            },
            'message': MESSAGES['success']
        }).dict())
