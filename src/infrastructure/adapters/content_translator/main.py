from typing import Any
from infrastructure.configs.main import GlobalConfig, get_cnf

import aiohttp
from pydantic import BaseModel
from core.ports.content_translator import ContentTranslatorPort
from infrastructure.configs.main import GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()

PUBLIC_TRANSLATION_API_CONF = config.PUBLIC_TRANSLATION_API
PUBLIC_TRANSLATION_API_URL = PUBLIC_TRANSLATION_API_CONF.URL

class ContentTranslationResponse(BaseModel):

    data: Any

class ContentTranslator(ContentTranslatorPort):

    async def translate(
        self,  
        source_lang: str, 
        target_lang: str, 
        source_text: str, 
        session: aiohttp.ClientSession = None,
        public_request: bool = True
    ):

        if public_request:

            direction = f'{source_lang}-{target_lang}'

            data = {
                'direction': direction,
                'data': source_text
            }

            headers = {'Content-Type': 'application/json'}

            if not session:

                async with aiohttp.ClientSession() as session:
                    async with session.post(PUBLIC_TRANSLATION_API_URL, json=data, headers=headers) as response:
                        result = (await response.json())['data']

                        return ContentTranslationResponse(**result)

            else:
                async with session.post(PUBLIC_TRANSLATION_API_URL, json=data, headers=headers) as response:
                    result = (await response.json())['data']

                    return ContentTranslationResponse(**result)
