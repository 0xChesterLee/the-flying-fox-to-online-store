import os
import ast
import misc
import openai

rewriterPrompt = '請使用繁體中文重寫以下文字，每段文章需要有80%以上的繁體中文字，但保留"TITLE:"，"BODY:"和"TAGS:"，並將重寫後的內容輸出。\n\nTITLE:{0}\n\nBODY:{1}\n\nTAGS:{2}\n\n'

def productRewriter(title, body, tags):
    OPENAI_API_KEY_FILE_NAME = os.path.join(os.getcwd(),misc.OPENAI_API_KEY_FILE_NAME)
    with open(OPENAI_API_KEY_FILE_NAME, 'r') as file:
        openai.api_key = file.read().strip()

    # Convert And Fix Params To String
    tags = ','.join(ast.literal_eval(tags))

    messages = [{'role': 'user', 'content': rewriterPrompt.format(title, body, tags)}]

    response = openai.chat.completions.create(model='gpt-3.5-turbo',
                                              messages=messages,
                                              temperature=0.7)
    
    response = response.choices[0].message.content.strip()

    productRewriter = {}
    productRewriter['title'] = response.split('TITLE:')[1].split('\n')[0]
    productRewriter['body'] = response.split('BODY:')[1]

    tags_start_index = response.find('TAGS:')
    if tags_start_index != -1:
        tags_end_index = response.find('\n', tags_start_index)
        productRewriter['tags'] = response[tags_start_index + len('TAGS:'):tags_end_index].strip()
    else:
        productRewriter['tags'] = ''

    return productRewriter



