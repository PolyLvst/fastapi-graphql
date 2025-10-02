from strawberry import Info
from service.auth import AuthService
from strawberry_graphql.strawberry_input import UserCreate, UserUpdate, UserUpdateBase
from strawberry_graphql.strawberry_type import UserType
from service.user import UserService
import strawberry

@strawberry.type
class Query:

    @strawberry.field
    def users(self) -> list[UserType]:
        return UserService.list_users()

    @strawberry.field
    def get_user_by_id(self, id: int) -> UserType | None:
        return UserService.get_user_by_id(id=id)


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(self, user:UserCreate, info:Info) -> UserType:
        AuthService.allowed_roles_only(allowed_roles=["admin"], current_user=info.context["current_user"])
        return UserService.create_user(user=user)
    
    @strawberry.mutation
    def delete_user(self, id:int, info:Info) -> str:
        AuthService.allowed_roles_only(allowed_roles=["admin"], current_user=info.context["current_user"])
        return UserService.delete_user(id=id)
    
    @strawberry.mutation
    def update_user(self, id:int, user:UserUpdate, info:Info) -> UserType | None:
        AuthService.allowed_roles_only(allowed_roles=["admin"], current_user=info.context["current_user"])
        return UserService.update_user(id=id, user=user)
    
    @strawberry.mutation
    def update_my_user(self, user:UserUpdateBase, info:Info) -> UserType | None:
        current_user:dict = AuthService.allowed_roles_only(allowed_roles=["admin", "user"], current_user=info.context["current_user"])
        id = current_user.get("user_id")
        return UserService.update_user(id=id, user=user)