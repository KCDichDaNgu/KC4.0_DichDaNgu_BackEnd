from core.types import ExtendedEnum

class TranslationHistoryTypeEnum(str, ExtendedEnum):

    private_file_translation = 'private_file_translation'
    private_plain_text_translation = 'private_plain_text_translation'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'

TRANSLATION_HISTORY_PUBLIC_TYPES = [
    TranslationHistoryTypeEnum.public_file_translation.value,
    TranslationHistoryTypeEnum.public_plain_text_translation.value
]

TRANSLATION_HISTORY_PRIVATE_TYPES = [
    TranslationHistoryTypeEnum.private_file_translation.value,
    TranslationHistoryTypeEnum.private_plain_text_translation.value
]

class TranslationHistoryStatus(str, ExtendedEnum):

    translating = 'translating'
    translated = 'translated'

    closed = 'closed'
    cancelled = 'cancelled'
