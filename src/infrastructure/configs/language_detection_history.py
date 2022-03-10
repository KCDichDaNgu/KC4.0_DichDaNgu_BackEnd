from core.types import ExtendedEnum

class LanguageDetectionHistoryTypeEnum(str, ExtendedEnum):

    private_file_language_detection = 'private_file_language_detection'
    private_plain_text_language_detection = 'private_plain_text_language_detection'

    public_file_language_detection = 'public_file_language_detection'
    public_plain_text_language_detection = 'public_plain_text_language_detection'

TRANSLATION_HISTORY_PUBLIC_TYPES = [
    LanguageDetectionHistoryTypeEnum.public_file_language_detection.value,
    LanguageDetectionHistoryTypeEnum.public_plain_text_language_detection.value
]

TRANSLATION_HISTORY_PRIVATE_TYPES = [
    LanguageDetectionHistoryTypeEnum.private_file_language_detection.value,
    LanguageDetectionHistoryTypeEnum.private_plain_text_language_detection.value
]

class LanguageDetectionHistoryStatus(str, ExtendedEnum):

    detecting = 'detecting'
    detected = 'detected'

    closed ='closed'
    cancelled = 'cancelled'
