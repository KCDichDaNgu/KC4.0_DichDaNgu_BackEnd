from core.types import ExtendedEnum

class LanguageEnum(str, ExtendedEnum):

    zh = 'zh'
    vi = 'vi'
    km = 'km'
    lo = 'lo'
    en = 'en'

    unknown = 'unknown'
