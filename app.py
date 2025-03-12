# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
# from chainlit.types import Prompt, PromptMessage  # importing prompt tools
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful assistant who always speaks in a pleasant tone!
"""

user_template = """{input}
Think through your response step by step.
"""

def system_message(content):
    return {
        "role": "system",
        "content": content,
    }

def user_message(content):
    
    return {
        "role": "user",
        "content": user_template.format(input=content),
    }




@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    settings = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,

    }

    cl.user_session.set("settings", settings)


@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")

    client = AsyncOpenAI()

    print(message.content)

   
    msg = cl.Message(content="")

    # Call OpenAI
    async for stream_resp in await client.chat.completions.create(
        messages=[system_message(system_template),user_message(content=message.content)], stream=True, **settings
    ):
        token = stream_resp.choices[0].delta.content
        if not token:
            token = ""
        await msg.stream_token(token)

   
    # Send and close the message stream
    await msg.send()
