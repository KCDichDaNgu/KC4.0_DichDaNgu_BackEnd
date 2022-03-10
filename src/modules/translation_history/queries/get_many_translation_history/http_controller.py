from interface_adapters.dtos.base_response import BaseResponse
from uuid import UUID
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity
from sanic.exceptions import SanicException
from infrastructure.configs.task import TRANSLATION_PUBLIC_TASKS, get_task_result_file_path
from infrastructure.configs.message import MESSAGES
from sanic import response
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
 
from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_history.dtos.translation_history_response import ManyTranslationHistoryResponse
import json
from core.utils.file import get_full_path
from core.middlewares.authentication.core import get_me
 
from core.exceptions import NotFoundException
 
config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG
PAGINATION_CONFIG = config.PAGINATION
 
 
class GetManyTranslationHistory(HTTPMethodView):
 
    def __init__(self) -> None:
        super().__init__()
 
        from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
 
        self.__translation_history_repository = TranslationHistoryRepository()
 
    @doc.summary(APP_CONFIG.ROUTES['translation_history.list']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_history.list']['desc'])
    @doc.consumes(
        doc.String(
            description='Task Id',
            name='taskId'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='Translation type',
            name='translationType'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='Status',
            name='status'
        ),
        location="query"
    )
    @doc.consumes(
        doc.Integer(
            description='page',
            name='page'
        ),
        location="query"
    )
    @doc.consumes(
        doc.Integer(
            description='perPage',
            name='perPage'
        ),
        location="query"
    )
    @doc.consumes(
        doc.String(
            description='sort',
            name='sort'
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
    @doc.produces(ManyTranslationHistoryResponse)

    async def get(self, request):

        user = await get_me(request)

        task_id = request.args.get('taskId')
        status = request.args.get('status')
        translation_type = request.args.get('translationType')
        per_page = request.args.get('perPage')
        page = request.args.get('page')
        sort = {
            "key": 'created_at',
            "direction": request.args.get('sort', -1)
        }
           
        pagination = {
            'page': PAGINATION_CONFIG.DEFAULT_PAGE,
            'per_page': PAGINATION_CONFIG.DEFAULT_PER_PAGE
        }
 
        query = {}
        
        if user:
            query['creator_id'] = UUID(user.id)
        else:
            query['creator_id'] = None

        if not task_id is None:
            query['task_id'] = UUID(task_id)

        if not status is None:
            query['status'] = status

        if not translation_type is None:
            query['translation_type'] = translation_type

        if not page is None:
            pagination['page'] = abs(int(page))

        if not per_page is None:
            pagination['per_page'] = abs(int(per_page))
 
        query_result = await self.__translation_history_repository.find_many_paginated(
            query,
            pagination,
            sort
        )
 
        translation_history: TranslationHistoryEntity = query_result.data

        tasks = list(
            map(lambda item: {
                'taskId': item.props.task_id.value,
                'translationType': item.props.translation_type,
                'id': item.id.value,
                'status': item.props.status,
                'updatedAt': str(item.updated_at.value),
                'createdAt': str(item.created_at.value),
                'resultUrl': get_full_path(get_task_result_file_path(item.props.file_path))
            }, translation_history)
        )
 
        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                "per_page": query_result.per_page,
                "page": query_result.page,
                "total_entries": query_result.total_entries,
                "list": tasks
            },
            'message': MESSAGES['success']
        }).dict())
