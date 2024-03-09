from . import db

def generate_solution(space_id: str) -> str:
    inputs = db.get_idea_inputs(space_id)
    return ','.join([input.input for input in inputs])

