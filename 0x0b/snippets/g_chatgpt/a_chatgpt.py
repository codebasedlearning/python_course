# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about accessing ChatGPT.

Teaching focus
  - query OpenAIs LLM

Preparations
  - .env file with credentials, not part of the project; entries e.g.,
        OPENAI_API_KEY=xyz
  - virtual environment activated and libs installed, here:
        pip install openai python-dotenv
"""

import os
from typing import Iterable
from dotenv import load_dotenv

from openai import OpenAI
from anthropic import Anthropic

load_dotenv()                               # load from .env


def query_chatgpt(question):
    try:
        # question = "What is the capital of France?"
        model = "gpt-3.5-turbo"
        # from the terminal or in .venv (without 'export'):
        #   export OPENAI_API_KEY="key"
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        messages: Iterable[dict[str,str]] = [
             {  "role": "system",
                "content": "You are a helpful assistant." },
             {  "role": "user",
                "content": question }
        ]
        response = client.chat.completions.create(model=model,messages=messages)
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e)


def query_anthropic(question):
    try:

        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # or "claude-3-haiku", "claude-3-opus"
            max_tokens=1000,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        answer = response.content[0].text
        return answer
    except Exception as e:
        return str(e)

def input_question():
    """ input question and ask ChatGPT """
    print("\ninput_question\n==============\n")

    while question:=input("Your Question: "):
        answer = query_chatgpt(question)
        # answer = query_anthropic(question)
        print(f"-> {answer}")


if __name__ == "__main__":
    input_question()


"""
See 
  - https://openai.com
  - https://console.anthropic.com/dashboard
"""
