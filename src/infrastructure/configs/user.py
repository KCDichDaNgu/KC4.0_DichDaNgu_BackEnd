from core.types import ExtendedEnum 

class UserStatus(str, ExtendedEnum):
    active = 'active'
    inactive = 'inactive'

class UserRole(str, ExtendedEnum):
    admin = 'admin'
    member = 'member'

class UserQuota(int, ExtendedEnum):
    default_text_translation_quota = 100

class TranslationPairEnum(str, ExtendedEnum):
    vi_en = 'vi-en',
    en_vi = 'en-vi',
    zh_vi = 'zh-vi',
    vi_zh = 'vi-zh',

TRANSLATION_PAIR_VI_EN = [TranslationPairEnum.vi_en.value, TranslationPairEnum.en_vi.value]

TRANSLATION_PAIR_VI_ZH = [TranslationPairEnum.vi_zh.value, TranslationPairEnum.zh_vi.value]