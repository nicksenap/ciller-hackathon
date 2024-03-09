from datetime import datetime
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
    space_id: str
    ts: str
    final_idea: str

@strawberry.type
class IdeaInput:
    type: str
    input_id: str
    ts: str
    space_id: str
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

def create_idea_space(type: str, space_id: str, final_idea: str) -> IdeaSpace:
    now = datetime.now()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='_default',
                         key="s" + space_id,
                         data={'type': type, 'space_id': space_id, 'ts': timestamp_str, 'final_idea': final_idea})
    )

    return IdeaSpace(type=type, space_id=space_id, ts=timestamp_str, final_idea=final_idea)

def create_idea_input(type: str, input_id: str, space_id: str, input: str, user_tag: str) -> IdeaInput:
    now = datetime.now()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='_default',
                         key="i" + input_id,
                         data={'type': type, 'input_id': input_id, 'ts': timestamp_str, 'space_id': space_id, 'input': input, 'user_tag': user_tag})
    )
    
    return IdeaInput(type=type, input_id=input_id, ts=timestamp_str, space_id=space_id, input=input, user_tag=user_tag)

def update_idea_space(space_id: str, final_idea: str) -> IdeaSpace:
    now = datetime.now()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

    # Constructing the document specification for deletion
    delete_doc_spec = cb.DocRef(bucket=env.get_couchbase_bucket(), collection='_default', key="s" + space_id)
    # Attempt to delete the existing document
    try:
        cb.remove(env.get_couchbase_conf(), delete_doc_spec)
    except Exception as e:
        print(f"Document with key {delete_doc_spec.key} could not be deleted: {e}")

    # Constructing the document specification for insertion
    insert_doc_spec = cb.DocSpec(bucket=env.get_couchbase_bucket(),
                                 collection='_default',
                                 key="s" + space_id,
                                 data={'type': "idea_space", 'space_id': space_id, 'ts': timestamp_str, 'final_idea': final_idea})
    # Inserting the new document
    cb.insert(env.get_couchbase_conf(), insert_doc_spec)

    return IdeaSpace(type="idea_space", space_id=space_id, ts=timestamp_str, final_idea=final_idea)

def get_idea_spaces() -> list[IdeaSpace]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT type, space_id, ts, final_idea FROM {env.get_couchbase_bucket()}._default._default WHERE type='idea_space' ORDER BY ts DESC"
    )
    return [IdeaSpace(**r) for r in result]

def get_idea_inputs() -> list[IdeaSpace]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT type, input_id, ts, space_id, input, user_tag FROM {env.get_couchbase_bucket()}._default._default WHERE type='idea_input' ORDER BY ts DESC"
    )
    return [IdeaInput(**r) for r in result]

def get_idea_inputs_by_space_id(space_id: str) -> list[IdeaInput]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT type, input_id, ts, space_id, input, user_tag FROM {env.get_couchbase_bucket()}._default._default WHERE space_id='{space_id}' AND type = 'idea_input' ORDER BY ts DESC"
    )
    return [IdeaInput(**r) for r in result]

def get_idea_space(space_id: str) -> IdeaSpace | None:
    # Fetch all idea spaces and then filter by space_id
    all_idea_spaces = get_idea_spaces()  # Assuming this function works correctly
    for idea_space in all_idea_spaces:
        if idea_space.space_id == space_id:
            return idea_space
    return None

def get_idea_input(input_id: str) -> IdeaInput | None:
    # Fetch all idea inputs and then filter by input_id
    all_idea_inputs = get_idea_inputs()  # Assuming this function works correctly
    for idea_input in all_idea_inputs:
        if idea_input.input_id == input_id:
            return idea_input
    return None


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
