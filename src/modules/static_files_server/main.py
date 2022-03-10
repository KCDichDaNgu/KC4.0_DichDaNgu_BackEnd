from posixpath import join
from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.translation_history.queries.get_single_translation_history.http_controller import GetSingleTranslationHistory

import os

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

static_files_server_bp = Blueprint(
    APP_CONFIG.ROUTES['static_files']['name'], 
    url_prefix=APP_CONFIG.ROUTES['static_files']['path']
)

current_dir = os.path.dirname(os.path.abspath(__file__))

current_dir_path = '/'.join(current_dir.split('/')[:-3])

static_dir = os.path.join(current_dir_path, 'static')

static_files_server_bp.static('', static_dir)
