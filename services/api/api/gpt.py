from . import db
import openai

def generate_solution(space_id: str) -> db.GPTOutput:
    inputs = db.get_idea_inputs_by_space_id(space_id)
    OPENAI_API_KEY = 'sk-'
    # use rest to call openai api for text completion
    # openai api key is stored in the environment variable OPENAI_API_KEY
    client = openai.Client(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a idea mixer, which takes user inputs and combines them to generate a innovative idea which incorporates all the inputs. You try to present the output in form of bullet points for the group to take action. Also mention user name where ever required, to make it more natural. Generate the output in a report format with heading for each section. Report should be in markdown format. Report must have a title and description, along with other required points."},
        {"role": "user", "content": ','.join([input.input for input in inputs])},
    ]
    )
    print(response)
    text_output = response.choices[0].message.content

    return db.GPTOutput(output=text_output)

