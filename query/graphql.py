import strawberry
from strawberry.fastapi import GraphQLRouter

from strawberry_graphql.strawberry_schema import Mutation, Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)