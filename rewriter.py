

rewriterPrompt = '請使用繁體中文重寫產品資訊，並以以下格式回應我。\nTITLE: BODY: TAGS:\nTITLE:{0}\nBODY:{1}\nTAGS:{2}'

def productRewriter(title, body, tags):
    productRewriter = {}

    productRewriter['title'] = title
    productRewriter['body'] = body
    productRewriter['tags'] = tags

    return productRewriter