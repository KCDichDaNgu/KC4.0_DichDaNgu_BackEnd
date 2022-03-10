from modules.translation_history.queries.get_single_translation_history.http_controller import GetSingleTranslationHistory
from modules.translation_history.queries.get_many_translation_history.http_controller import GetManyTranslationHistory
from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

translation_history_bp = Blueprint(
    APP_CONFIG.ROUTES['translation_history']['name'], 
    url_prefix=APP_CONFIG.ROUTES['translation_history']['path']
)

translation_history_bp.add_route(
    GetSingleTranslationHistory.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_history.get_single']['path'],
    methods=[APP_CONFIG.ROUTES['translation_history.get_single']['method']]
)

translation_history_bp.add_route(
    GetManyTranslationHistory.as_view(), 
    uri=APP_CONFIG.ROUTES['translation_history.list']['path'],
    methods=[APP_CONFIG.ROUTES['translation_history.list']['method']]
)
