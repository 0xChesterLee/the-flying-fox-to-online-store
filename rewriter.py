import os
import ast
import misc
import openai


def extractContentFromOpenAI(text):
    title = ""
    body = ""
    tags = ""

    # Split And Get The Content String After OpenAI Rewrite
    lines = text.split("\n")
    is_body = False
    for line in lines:
        if line.startswith("TITLE:"):
            title = line.lstrip("TITLE:").strip()
        elif line.startswith("BODY:"):
            is_body = True
            body = line.lstrip("BODY:").strip()
        elif line.startswith("TAGS:"):
            tags = line.lstrip("TAGS:").strip()
        elif is_body:
            body += line.strip()

    return title, body, tags


def productRewriter(title, body, tags):
    OPENAI_API_KEY_FILE_NAME = os.path.join(os.getcwd(),misc.OPENAI_API_KEY_FILE_NAME)

    # Get The OpenAI API Token Key
    with open(OPENAI_API_KEY_FILE_NAME, 'r') as file:
        openai.api_key = file.read().strip()

    # Convert And Fix Params To String
    tags = ','.join(ast.literal_eval(tags))

    # Starting Rewrite The Content From OpenAI
    messages = [{'role': 'user', 'content': misc.REWRITE_PROMPT.format(title, body, tags)}]
    response = openai.chat.completions.create(model='gpt-3.5-turbo',
                                              messages=messages,
                                              temperature=0.8,
                                              max_tokens=4096)
    response = response.choices[0].message.content.strip()

    productRewriter = {}
    productRewriter['title'], productRewriter['body'], productRewriter['tags'] = extractContentFromOpenAI(response)
    
    return productRewriter