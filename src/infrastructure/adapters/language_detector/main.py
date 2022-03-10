from pydantic.main import BaseModel
from infrastructure.configs.language import LanguageEnum
from typing import Any
import aiohttp

from core.ports.language_detector import LanguageDetectorPort
from infrastructure.configs.main import GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()

PUBLIC_LANGUAGE_DETECTION_API_CONF = config.PUBLIC_LANGUAGE_DETECTION_API
PUBLIC_LANGUAGE_DETECTION_API_URL = PUBLIC_LANGUAGE_DETECTION_API_CONF.URL

class LanguageDetectionResponse(BaseModel):

    lang: str 
    lang_str: str
    lang: LanguageEnum

    class Config:
        use_enum_values = True
class LanguageDetector(LanguageDetectorPort):

    async def detect(
        self, 
        text: str, 
        session: aiohttp.ClientSession = None,
        public_request: bool = True
    ):

        if public_request:

            headers = {'Content-Type': 'application/json'}

            if not session:

                async with aiohttp.ClientSession() as session:
                    async with session.post(PUBLIC_LANGUAGE_DETECTION_API_URL, json={"data": text}, headers=headers) as response:
                        result = (await response.json())['data']

                        result['lang'] = result['lang'] if result['lang'] in LanguageEnum.enum_values() else LanguageEnum.unknown.value

                        return LanguageDetectionResponse(**result)

            else:
                async with session.post(PUBLIC_LANGUAGE_DETECTION_API_URL, json={"data": text}, headers=headers) as response:
                    result = (await response.json())['data']

                    result['lang'] = result['lang'] if result['lang'] in LanguageEnum.enum_values() else LanguageEnum.unknown.value

                    return LanguageDetectionResponse(**result)
