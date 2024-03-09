import uuid
import strawberry
from . import couchbase as cb, env

@strawberry.type
class Product:
    id: str
    name: str

@strawberry.type
class IdeaSpace:
    type: str
    space_id: int
    ts: str
    final_idea: str

@strawberry.type
class IdeaInput:
    type: str
    input_id: int
    ts: str
    space_id: int
    input: str
    user_tag: str


def create_product(name: str) -> Product:
    id = str(uuid.uuid1())
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='products',
                         key=id,
                         data={'name': name}))
    return Product(id=id, name=name)
#
def get_product(id: str) -> Product | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='products',
                               key=id)):
        return Product(id=id, name=doc['name'])

def create_idea_space(type: str, space_id: int, final_idea: str) -> IdeaSpace:
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='ideas',
                         key=space_id,
                         data={'type': type, 'space_id': space_id, 'final_idea': final_idea})
    )
    return IdeaSpace(type=type, space_id=space_id, final_idea=final_idea)

def create_idea_input(type: str, input_id: int, space_id: int, input: str, user_tag: str) -> IdeaInput:
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='ideas',
                         key=input_id,
                         data={'type': type, 'input_id': input_id, 'space_id': space_id, 'input': input, 'user_tag': user_tag})
    )
    return IdeaInput(type=type, input_id=input_id, space_id=space_id, input=input, user_tag=user_tag)

def get_idea_space(space_id: int) -> IdeaSpace | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='ideas',
                               key=space_id)):
        return IdeaSpace(type=doc['type'], space_id=doc['space_id'], ts=doc['ts'], final_idea=doc['final_idea'])

def get_idea_input(input_id: int) -> IdeaInput | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='ideas',
                               key=input_id)):
        return IdeaInput(type=doc['type'], input_id=doc['input_id'], ts=doc['ts'], space_id=doc['space_id'], input=doc['input'], user_tag=doc['user_tag'])

def delete_product(id: str) -> None:
    cb.remove(env.get_couchbase_conf(),
              cb.DocRef(bucket=env.get_couchbase_bucket(),
                        collection='products',
                        key=id))

def list_products() -> list[Product]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.products"
    )
    return [Product(**r) for r in result]
