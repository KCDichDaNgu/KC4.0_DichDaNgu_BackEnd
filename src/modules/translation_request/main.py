from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.translation_request.commands.create_plain_text_translation_request.http_controller import CreatePlainTextTranslationRequest
from modules.translation_request.commands.create_file_translation_request.http_controller import CreateFileTranslationRequest
from modules.translation_request.commands.update_receiver_email.http_controller import UpdateReceiverEmail

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

translation_request_bp = Blueprint(
    APP_CONFIG.ROUTES['translation_request']['name'], 
    url_prefix=APP_CONFIG.ROUTES['translation_request']['path']
)

translation_request_bp.add_route(
    CreatePlainTextTranslationRequest.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_request.text_translation.create']['path'],
    methods=[APP_CONFIG.ROUTES['translation_request.text_translation.create']['method']]
)

translation_request_bp.add_route(
    CreateFileTranslationRequest.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_request.doc_translation.create']['path'],
    methods=[APP_CONFIG.ROUTES['translation_request.doc_translation.create']['method']]
)

translation_request_bp.add_route(
    UpdateReceiverEmail.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_request.update_receiver_email']['path'],
    methods=[APP_CONFIG.ROUTES['translation_request.update_receiver_email']['method']]
)
