from uuid import UUID
from core.middlewares.authentication.user import User
from infrastructure.configs.user import UserQuota
from modules.user.commands.login.command import LoginCommand
from core.value_objects.id import ID
from modules.user.database.user.repository import UserRepositoryPort, UserRepository
from modules.user.domain.entities.user import UserEntity, UserProps 
from modules.user.commands.auth.command import CreateUserCommand

from modules.user.database.user_statistic.repository import UserStatisticRepositoryPort, UserStatisticRepository
from modules.user.domain.entities.user_statistic import UserStatisticEntity, UserStatisticProps 

from infrastructure.configs.main import get_mongodb_instance

class UserDService():

    def __init__(self) -> None:
        self.__user_repository: UserRepositoryPort = UserRepository()
        self.__user_statistic_repository: UserStatisticRepositoryPort = UserStatisticRepository()
        self.__db_instance = get_mongodb_instance()

    async def create_user(self, command: CreateUserCommand):
        async with self.__db_instance.session() as session:
             async with session.start_transaction():
                user = await self.__user_repository.find_one({'email': command.email})

                if user is None:

                    new_user = UserEntity(
                        UserProps(
                            username=command.username,
                            first_name=command.first_name,
                            last_name=command.last_name,
                            email=command.email,
                            password=command.password,
                            role=command.role,
                            status=command.status,
                            avatar=''
                        )
                    )
                    user = await self.__user_repository.create(new_user)

                    new_user_statistic = UserStatisticEntity(
                        UserStatisticProps(
                            user_id=ID(user.id.value),
                            total_translated_text={
                                'vi-zh': 0, 
                                'vi-en': 0,
                                'vi-km': 0,
                                'vi-lo': 0,
                            },
                            text_translation_quota={
                                'vi-zh': command.text_translation_quota['vi-zh'],
                                'vi-en': command.text_translation_quota['vi-en'],
                                'vi-lo': command.text_translation_quota['vi-lo'],
                                'vi-km': command.text_translation_quota['vi-km'],
                            },
                        )
                    )
                    await self.__user_statistic_repository.create(new_user_statistic)

                return user
    
    async def login(self, command: LoginCommand):
        async with self.__db_instance.session() as session:
             async with session.start_transaction():
                user = await self.__user_repository.find_one({'username': command.username})

                if user is not None:
                    if user.validate_password(command.password):
                        return user;
                    else:
                        return 'blank'
                
                return None
    
    async def get_user(self, user_id):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user_entity = await self.__user_repository.find_one({'id': UUID(user_id)})

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

    async def update_user(self, command):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_repository.find_one({'id': UUID(command.id)})
                if user is None:
                    return None

                changes = dict(command)

                del changes["id"]
                del changes["text_translation_quota"]

                updated_user = await self.__user_repository.update(user, changes)

                if updated_user is not None:
                    user_statistic = await self.__user_statistic_repository.find_one({'user_id': UUID(updated_user.id.value)})

                    changes = dict(command)
                    changes = {'text_translation_quota':changes['text_translation_quota']}
                    
                    if user is None:
                        return None
                    updated_user_statistic = await self.__user_statistic_repository.update(user_statistic, changes)
                
                return updated_user
    
    async def get_user_statistic(self,user_id):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_statistic_repository.find_one({'user_id': UUID(user_id)})
                
                if user is None:
                    return None

                return user

    async def update_user_statistic(self,command):
        async with self.__db_instance.session() as session:
            async with session.start_transaction():
                user = await self.__user_statistic_repository.find_one({'user_id': UUID(command.user_id)})
                
                if user is None:
                    return None

                changes = dict(command)

                del changes["user_id"]

                updated_user_statistic = await self.__user_statistic_repository.update(user, changes)

                return updated_user_statistic
