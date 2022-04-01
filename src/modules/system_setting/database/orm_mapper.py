from modules.system_setting.database.orm_entity import SystemSettingOrmEntity
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from core.value_objects.id import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

class SystemSettingOrmMapper(OrmMapperBase[SystemSettingEntity, SystemSettingOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: SystemSettingEntity):
        props = entity.get_props_copy()

        orm_props = {
            'editor_id': props.editor_id.value,
            'task_expired_duration': props.task_expired_duration,
            'translation_api_url': props.translation_api_url,
            'translation_api_allowed_concurrent_req': props.translation_api_allowed_concurrent_req,
            'language_detection_api_url': props.language_detection_api_url,
            'language_detection_api_allowed_concurrent_req': props.language_detection_api_allowed_concurrent_req,
            'translation_speed_for_each_character': props.translation_speed_for_each_character,
            'language_detection_speed': props.language_detection_speed,
            'email_for_sending_email': props.email_for_sending_email,
            'email_password_for_sending_email': props.email_password_for_sending_email,
            'allowed_total_chars_for_text_translation': props.allowed_total_chars_for_text_translation,
            'allowed_file_size_in_mb_for_file_translation': props.allowed_file_size_in_mb_for_file_translation,
        }

        return orm_props

    def to_domain_props(self, orm_entity: SystemSettingOrmEntity):
        props = {
            'editor_id':  ID(str(orm_entity.editor_id)),
            'task_expired_duration': orm_entity.task_expired_duration,
            'translation_api_url': orm_entity.translation_api_url,
            'translation_api_allowed_concurrent_req': orm_entity.translation_api_allowed_concurrent_req,
            'language_detection_api_url': orm_entity.language_detection_api_url,
            'language_detection_api_allowed_concurrent_req': orm_entity.language_detection_api_allowed_concurrent_req,
            'translation_speed_for_each_character': orm_entity.translation_speed_for_each_character,
            'language_detection_speed': orm_entity.language_detection_speed,
            'email_for_sending_email': orm_entity.email_for_sending_email,
            'email_password_for_sending_email': orm_entity.email_password_for_sending_email,
            'allowed_total_chars_for_text_translation': orm_entity.allowed_total_chars_for_text_translation,
            'allowed_file_size_in_mb_for_file_translation': orm_entity.allowed_file_size_in_mb_for_file_translation,
        }

        return props
