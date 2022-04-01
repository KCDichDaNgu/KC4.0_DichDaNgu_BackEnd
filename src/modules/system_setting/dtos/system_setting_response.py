from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    taskExpiredDuration = doc.Integer(
        description='taskExpiredDuration'
    )
    
    translationApiUrl = doc.String(
        description='translationApiUrl'
    )
    
    translationApiAllowedConcurrentReq = doc.Integer(
        description='translationApiAllowedConcurrentReq'
    )
    
    languageDetectionApiUrl = doc.String(
        description='languageDetectionApiUrl'
    )
    
    languageDetectionApiAllowedConcurrentReq = doc.Integer(
        description='languageDetectionApiAllowedConcurrentReq'
    )
    
    translationSpeedForEachCharacter = doc.Float(
        description='translationSpeedForEachCharacter'
    )
    
    languageDetectionSpeed = doc.Float(
        description='languageDetectionSpeed'
    )
    
    emailForSendingEmail = doc.String(
        description='emailForSendingEmail'
    )
    
    emailPasswordForSendingEmail = doc.String(
        description='emailPasswordForSendingEmail'
    )
    
    allowedTotalCharsForTextTranslation = doc.Integer(
        description='allowedTotalCharsForTextTranslation'
    )
    
    allowedFileSizeInMbForFileTranslation = doc.Float(
        description='allowedFileSizeInMbForFileTranslation'
    )

class SystemSettingResponse(ResponseBase):

    data: DataStructure
