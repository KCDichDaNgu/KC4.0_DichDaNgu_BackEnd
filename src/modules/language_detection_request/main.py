from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.language_detection_request.commands.create_plain_text_language_detection_request.http_controller import CreatePlainTextLanguageDetectionRequest
from modules.language_detection_request.commands.create_file_language_detection_request.http_controller import CreateFileLanguageDetectionRequest

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

language_detection_request_bp = Blueprint(
    APP_CONFIG.ROUTES['language_detection_request']['name'], 
    url_prefix=APP_CONFIG.ROUTES['language_detection_request']['path']
)

language_detection_request_bp.add_route(
    CreatePlainTextLanguageDetectionRequest.as_view(), 
    uri=APP_CONFIG.ROUTES['language_detection_request.text_language_detection.create']['path'],
    methods=[APP_CONFIG.ROUTES['language_detection_request.text_language_detection.create']['method']]
)

language_detection_request_bp.add_route(
    CreateFileLanguageDetectionRequest.as_view(), 
    uri=APP_CONFIG.ROUTES['language_detection_request.doc_language_detection.create']['path'],
    methods=[APP_CONFIG.ROUTES['language_detection_request.doc_language_detection.create']['method']]
)
