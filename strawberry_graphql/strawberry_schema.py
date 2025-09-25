from strawberry_graphql.strawberry_input import UserInput
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
    def create_user(self, user:UserInput) -> UserType:
        return UserService.create_user(user=user)
    
    @strawberry.mutation
    def delete_user(self, id:int) -> str:
        return UserService.delete_user(id=id)
    
    @strawberry.mutation
    def update_user(self, id:int, user:UserInput) -> UserType | None:
        return UserService.update_user(id=id, user=user)