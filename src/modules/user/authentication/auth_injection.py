from datetime import datetime, timedelta
from infrastructure.configs.main import GlobalConfig, get_cnf
from infrastructure.configs.token import TokenType, Scope
from core.value_objects.id import ID
from modules.user.domain.entities.token import TokenEntity, TokenProps
from uuid import UUID
from core.middlewares.authentication.auth_injection_interface import AuthInjectionInterface
from core.middlewares.authentication.user import User
from modules.user.database.token.repository import TokenRepository
from modules.user.database.user.repository import UserRepository

config: GlobalConfig = get_cnf()

class AuthInjection(AuthInjectionInterface):

    def __init__(self) -> None:
        self.__user_repository: UserRepository = UserRepository()
        self.__token_repository : TokenRepository = TokenRepository()

    async def create_token(self, user, platform):
        try:
            token = TokenEntity(
                TokenProps(
                    access_token=ID.generate(),
                    refresh_token=ID.generate(),
                    token_type=TokenType.bearer.value,
                    scope=[Scope.profile.value],
                    platform=platform,
                    user_id=ID(user.id.value),
                    access_expires_in=config.ACCESS_TOKEN_TTL,
                    refresh_expires_in=config.REFRESH_TOKEN_TTL,
                    revoked=False
                )
            )
            result = await self.__token_repository.create(token)
            return result
        except Exception:
            return None

    async def get_token(self, access_token):
        try:
            return await self.__token_repository.find_one({'access_token': UUID(access_token)})   
        except Exception:
            return None

    async def refresh_token(self, refresh_token):
        try:
            token = await self.__token_repository.find_one({'refresh_token': UUID(refresh_token)})
            if token is None:
                return None

            if token.props.revoked:
                return None

            if datetime.now() > token.created_at.value + timedelta(seconds=token.props.refresh_expires_in):
                await self.__token_repository.update(token, {'revoked': True})    
                return None
            result = await self.__token_repository.update(token, {'access_token': ID.generate().value, 'refresh_token': ID.generate().value})
            return result
        except Exception:
            return None

    async def revoke_token(self, access_token):
        try:
            token = await self.__token_repository.find_one({'access_token': UUID(access_token)})
            if token is None:
                return None

            if token.props.revoked:
                return None
            
            return await self.__token_repository.update(token, {'revoked': True})
        except Exception:
            return None

    async def get_user(self, token) -> User:
        try:
            user_entity = await self.__user_repository.find_one({'id': UUID(token.props.user_id.value)})
            if user_entity is None:
                return None
            return User(
                id=user_entity.id.value,
                username=user_entity.props.username,
                first_name=user_entity.props.first_name,
                last_name=user_entity.props.last_name,
                avatar=user_entity.props.avatar,
                email=user_entity.props.email,
                role=user_entity.props.role,
                status=user_entity.props.status,
                created_at=str(user_entity.created_at.value),
                updated_at=str(user_entity.updated_at.value)
            )
        except Exception:
            return None
        