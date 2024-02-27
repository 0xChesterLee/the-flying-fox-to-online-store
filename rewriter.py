import os
import ast
import misc
import openai

rewriterPrompt = '請使用繁體中文重寫產品資訊，用簡單易明之繁體中文句字或繁體中文說明，最後用英文作開頭，用以下格式回應我。\nTITLE: BODY: TAGS:\nTITLE:{0}\nBODY:{1}\nTAGS:{2}'

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
    productRewriter['title'] = response.split('TITLE: ')[1].split('\n')[0]
    productRewriter['body'] = response.split('BODY: ')[1]

    tags_start_index = response.find('TAGS: ')
    if tags_start_index != -1:
        tags_end_index = response.find('\n', tags_start_index)
        productRewriter['tags'] = response[tags_start_index + len('TAGS: '):tags_end_index].strip()
    else:
        productRewriter['tags'] = ''

    return productRewriter



