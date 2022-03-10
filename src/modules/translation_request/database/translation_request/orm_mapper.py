from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps

from modules.task.database.task.orm_mapper import TaskOrmMapper

from typing import get_args

class TranslationRequestOrmMapper(
    TaskOrmMapper,
    OrmMapperBase[
        TranslationRequestEntity, 
        TranslationRequestOrmEntity
    ]
):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[1])[1]

    def to_orm_props(self, entity: TranslationRequestEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id.value,
            'task_name': props.task_name,
            'creator_type': props.creator_type,
            'step_status': props.step_status,
            'current_step': props.current_step,
            'num_chars': props.num_chars,
            'total_email_sent': props.total_email_sent,
            'receiver_email': props.receiver_email,
            'file_type': props.file_type,
            # 'expired_date': props.expired_date.value,
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: TranslationRequestOrmEntity):
        
        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_name': orm_entity.task_name,
            'creator_type': orm_entity.creator_type,
            'step_status': orm_entity.step_status,
            'current_step': orm_entity.current_step,
            'num_chars': orm_entity.num_chars,
            'total_email_sent': orm_entity.total_email_sent,
            'receiver_email': orm_entity.receiver_email,
            'file_type': orm_entity.file_type,
            # 'expired_date': DateVO(orm_entity.expired_date)
        }

        return props
