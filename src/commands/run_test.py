from abc import ABC
import asyncio
from sanic.app import Sanic
from sanic.server import AsyncioServer
import typing
import logging
import sys
import os
from infrastructure.configs import ServerTypeEnum

from asgiref.typing import ASGIApplication

from uvicorn.config import (
    Config,
)

from uvicorn.server import Server
from uvicorn.supervisors import ChangeReload, Multiprocess

from infrastructure.configs import FactoryConfig, EnvStateEnum, get_cnf

from commands import cli, click

import aiotask_context as context

from app import init_app_test

import multiprocessing
from sanic.response import json, text

available_workers = multiprocessing.cpu_count()

class BaseServer(ABC):

    @classmethod
    def run(cls, app):
        raise NotImplementedError()

class UvicornServer(BaseServer):

    server: Server = None

    @classmethod
    def run(cls, app):
        
        cls.server = cls.__run(
            app=app,
            host=app.config["APP_HOST"],
            port=app.config["APP_PORT"],
            debug=app.config["APP_DEBUG"],
            workers=app.config["APP_WORKERS"],
            access_log=app.config["ACCESS_LOG"]
        )

    @classmethod
    def __run(cls, app: typing.Union[ASGIApplication, str], **kwargs: typing.Any) -> None:
        config = Config(app, **kwargs)
        server = Server(config=config)
        
        cls.server = server

        if (config.reload or config.workers > 1) and not isinstance(app, str):
            logger = logging.getLogger("uvicorn.error")
            logger.warning(
                "You must pass the application as an import string to enable 'reload' or "
                "'workers'."
            )
            sys.exit(1)

        if config.should_reload:
            sock = config.bind_socket()
            ChangeReload(config, target=server.run, sockets=[sock]).run()
        elif config.workers > 1:
            sock = config.bind_socket()
            Multiprocess(config, target=server.run, sockets=[sock]).run()
        else:
            server.run()
        if config.uds:
            os.remove(config.uds)
            
        return server

class SanicBuiltInServer(BaseServer):

    server: typing.Union[None, AsyncioServer] = None

    @classmethod
    def run(cls, app: Sanic):

        cls.server = app.create_server(
            host=app.config["APP_HOST"],
            port=app.config["APP_PORT"],
            debug=app.config["APP_DEBUG"],
            access_log=app.config["ACCESS_LOG"],
            return_asyncio_server=True
        )
        
        loop = asyncio.get_event_loop()
        loop.set_task_factory(context.task_factory)
        
        task = asyncio.ensure_future(cls.server)
        
        try:
            loop.run_forever()
        except:
            loop.stop()

@cli.command('run-test')
@click.option('-h', '--host', default=None, type=str)
@click.option('-p', '--port', default=None, type=int)
@click.option('-e', '--env', default='dev', type=click.Choice(EnvStateEnum.enum_values()))
@click.option('-wk', '--workers', default=1, type=int)
@click.option('-alg', '--access-log', default=False, type=bool)
@click.option('-st', '--server-type', default='uvicorn', type=click.Choice(ServerTypeEnum.enum_values()))
@click.option('-lsp', '--lifespan', default='on', type=str)
def run_test(
    host, 
    port, 
    env, 
    workers, 
    access_log, 
    server_type, 
    lifespan
):

    overwrite_args = {}
    
    if host is not None:
        
        overwrite_args['APP_HOST'] = host
        
    if port is not None:
        
        overwrite_args['APP_PORT'] = port
        
    if env is not None:
        
        overwrite_args['ENV_STATE'] = env

    if workers is not None:

        if workers == -1:

            overwrite_args['APP_WORKERS'] = available_workers
        
        else: overwrite_args['APP_WORKERS'] = workers

    if access_log is not None:
        
        overwrite_args['ACCESS_LOG'] = access_log

    if server_type is not None:

        overwrite_args['SERVER_TYPE'] = server_type
    
    if lifespan is not None:

        overwrite_args['APP_LIFESPAN'] = lifespan
        
    FactoryConfig(env, overwrite_args)()
    
    app = asyncio.run(init_app_test())
    
    if server_type == ServerTypeEnum.uvicorn.value:
        
        UvicornServer.run(app)
    
    else: 

        SanicBuiltInServer.run(app)
