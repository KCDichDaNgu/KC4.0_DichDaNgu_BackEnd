from core.types import ExtendedEnum 

class TokenType(str, ExtendedEnum):
    bearer = 'bearer'

class Scope(str, ExtendedEnum):
    profile = 'profile'

class Platform(str, ExtendedEnum):
    web = 'web'
    android = 'android'
    ios = 'ios'
