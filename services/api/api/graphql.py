import asyncio
from typing import AsyncGenerator
from functools import cached_property
import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.permission import BasePermission
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
import logging

from . import auth, db

logger = logging.getLogger(__name__)

#### Context ####

class Context(BaseContext):
    @cached_property
    def user(self) -> dict | None:
        if self.request:
            if auth_ := self.request.headers.get("Authorization"):
                method, token = auth_.split(" ")
                if method == 'Bearer':
                    if data := auth.decode_jwt(token):
                        return data

async def get_context() -> Context:
    return Context()

Info = _Info[Context, RootValueType]

#### Auth ####

class IsAuthenticated(BasePermission):
    message = "User is not authenticated."

    def has_permission(self, source, info: Info, **kwargs):
        return info.context.user is not None

#### Mutations ####

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def add_product(self, name: str) -> db.Product:
        return db.create_product(name)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def remove_product(self, id: str) -> None:
        db.delete_product(id)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def add_idea_space(self, type: str, space_id: int, final_idea: str) -> db.IdeaSpace:
        return db.create_idea_space(type, space_id, final_idea)
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def add_idea_input(self, type: str, input_id: int, space_id: int, input: str, user_tag: str) -> db.IdeaInput:
        return db.create_idea_input(type, input_id, space_id, input, user_tag)

#### Queries ####

@strawberry.type
class Query:
    @strawberry.field
    def products(self) -> list[db.Product]:
        return db.list_products()
    def idea_spaces(self) -> list[db.IdeaSpace]:
        return db.list_idea_spaces()
    def idea_inputs(self) -> list[db.IdeaInput]:
        return db.list_idea_inputs()
    def idea_space(self, space_id: int) -> db.IdeaSpace | None:
        return db.get_idea_space(space_id)
    def idea_input(self, input_id: int) -> db.IdeaInput | None:
        return db.get_idea_input(input_id)

#### Subscriptions ####

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def product_added(self) -> AsyncGenerator[db.Product, None]:
        # TODO: use a Kafka topic to avoid polling here
        seen = set(p.id for p in db.list_products())
        while True:
            for p in db.list_products():
                if p.id not in seen:
                    seen.add(p.id)
                    yield p
            await asyncio.sleep(0.5)

#### API ####

def get_app():
    return GraphQLRouter(
        strawberry.Schema(Query, mutation=Mutation, subscription=Subscription),
        context_getter=get_context
    )
