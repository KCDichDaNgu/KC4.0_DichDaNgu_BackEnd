from modules.system_setting.queries.get_system_setting.http_controller import GetSystemSetting
from sanic import Blueprint
from infrastructure.configs import GlobalConfig, get_cnf
from modules.system_setting.commands.update_system_setting.http_controller import UpdateSystemSetting

config: GlobalConfig = get_cnf()

APP_CONFIG = config.APP_CONFIG

system_setting_bp = Blueprint(
    APP_CONFIG.ROUTES['system_setting']['name'],
    url_prefix=APP_CONFIG.ROUTES['system_setting']['path']
)

system_setting_bp.add_route(
    UpdateSystemSetting.as_view(),
    uri=APP_CONFIG.ROUTES['system_setting.update']['path'],
    methods=[
        APP_CONFIG.ROUTES['system_setting.update']['method']
    ]
)

system_setting_bp.add_route(
    GetSystemSetting.as_view(),
    uri=APP_CONFIG.ROUTES['system_setting.get']['path'],
    methods=[
        APP_CONFIG.ROUTES['system_setting.get']['method']
    ]
)
