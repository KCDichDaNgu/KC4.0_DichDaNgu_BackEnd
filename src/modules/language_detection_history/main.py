from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.language_detection_history.queries.get_single_language_detection_history.http_controller import GetSingleLanguageDetectionHistory

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

language_detection_history_bp = Blueprint(
    APP_CONFIG.ROUTES['language_detection_history']['name'], 
    url_prefix=APP_CONFIG.ROUTES['language_detection_history']['path']
)

language_detection_history_bp.add_route(
    GetSingleLanguageDetectionHistory.as_view(), 
    uri=APP_CONFIG.ROUTES['language_detection_history.get_single']['path'],
    methods=[APP_CONFIG.ROUTES['language_detection_history.get_single']['method']]
)
