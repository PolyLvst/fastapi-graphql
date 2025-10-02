from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.database_model import Base
from config.connection import engine
import query
import query.graphql
import router
import router.auth
from service.auth import AuthService

class FastAPIGraphQLBackend:
    def __init__(self):
        self.__app = FastAPI(title="FastAPI GraphQL Backend", version="1.0.0")

    def register_routers(self):
        self.__app.include_router(router=query.graphql.graphql_app, prefix="/graphql", tags=["GraphQL"])
        self.__app.include_router(router=router.auth.router, prefix="/token", tags=["Token JWT"])
    
    def setup_config_app(self):
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def startup_event(self):
        self.__app.add_event_handler("startup", AuthService.create_admin_if_not_exists)

    def get_app(self):
        self.startup_event()
        self.register_routers()
        self.setup_config_app()
        return self.__app

Base.metadata.create_all(bind=engine)
fastapi_graphql_backend = FastAPIGraphQLBackend()
app = fastapi_graphql_backend.get_app()