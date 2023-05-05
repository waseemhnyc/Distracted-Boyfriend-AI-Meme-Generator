from langchain.schema import SystemMessage
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

import os, random, openai, requests

openai.api_key = os.getenv("OPENAI_API_KEY")
IMGFLIP_USERNAME = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_PASSWORD")


def get_random_temperature():
    return random.choice([0.1 * i for i in range(1, 11)])

def get_meme_text(user_input):
    chat_model = ChatOpenAI(temperature=get_random_temperature(), model_name="gpt-4")

    response_schemas = [
        ResponseSchema(name="distracted_boyfriend", description="distracted boyfriend, checking out hot girl"),
        ResponseSchema(name="girlfriend", description="jealous girlfriend looking at boyfriend"),
        ResponseSchema(name="hot_girl", description="good looking girl that the boyfriend is looking at")
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(content="You can create viral memes and specialize in the distracted boyfriend meme. The boyfriend is me and I'm distracted and checking out the hot girl walking away. The girlfriend is not me and is jealous. The hot girl is walking away. Memes must be short, easy to read and understand. Memes must relatable, brief, unexpected, ironic and funny. Do not use the word me"),
            HumanMessagePromptTemplate.from_template("Generate a meme about:\n{topic}.\n{format_instructions}")
        ],
        input_variables=["topic"],
        partial_variables={"format_instructions": format_instructions}
    )
    _input = prompt.format_prompt(topic=str(user_input))
    output = chat_model(_input.to_messages())
    response = output_parser.parse(output.content)
    print(user_input)
    print(response)
    return response

def distracted_boyfriend_meme_generator(user_input):
    response = get_meme_text(user_input=user_input)
    distracted_boyfriend = response['distracted_boyfriend']
    girlfriend = response['girlfriend']
    hot_girl = response['hot_girl']

    url = "https://api.imgflip.com/caption_image"

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    text_data = [hot_girl, distracted_boyfriend, girlfriend]

    params = {
        "template_id": 112126428,
        "username": IMGFLIP_USERNAME,
        "password": IMGFLIP_PASSWORD,
        "font": "impact",
    }

    for i in range(len(text_data)):
        params[f"boxes[{i}][text]"] = text_data[i]
        params[f"boxes[{i}][color]"] = "#ffffff"
        params[f"boxes[{i}][outline_color]"] = "#000000"

    response = requests.post(url, headers=headers, data=params)

    try:
        new_image_url = response.json()['data']['url']
        return new_image_url
    except:
        print(response.json())
