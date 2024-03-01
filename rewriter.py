import os
import ast
import misc
import openai


rewriterPrompt = '請使用繁體中文重寫以下文字，但保留"TITLE:"、"TAGS:"和"BODY:"。"TITLE:"和"BODY:"需要保留70%以上的繁體中文字、"TAGS:"需要保留100%的繁體中文字，並將重寫後的內容輸出。在重寫後的"TAGS:"內容上，根據"BODY:"後的內容額外生成最多6個主題標籤。如果重寫後的"TAGS:"內容為空白，請自行生成最多6個主題標籤，主題標籤不需要加上"#"字符號，但請用逗號分隔。\nTITLE:{0}\nTAGS:{2}\nBODY:{1}'


def extract_strings(text):
    title = ""
    body = ""
    tags = ""

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
    with open(OPENAI_API_KEY_FILE_NAME, 'r') as file:
        openai.api_key = file.read().strip()

    # Convert And Fix Params To String
    tags = ','.join(ast.literal_eval(tags))

    messages = [{'role': 'user', 'content': rewriterPrompt.format(title, body, tags)}]

    response = openai.chat.completions.create(model='gpt-3.5-turbo',
                                              messages=messages,
                                              temperature=0.8,
                                              max_tokens=4096)
    
    print(f'\n\n{response}\n\n')
    
    response = response.choices[0].message.content.strip()

    productRewriter = {}
    productRewriter['title'], productRewriter['body'], productRewriter['tags'] = extract_strings(response)
    
    return productRewriter



