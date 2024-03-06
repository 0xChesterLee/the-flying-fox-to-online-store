import misc
import uploader
import json
import requests


def postProduct(productData=dict):
    # Define Product Data
    id = productData['id']
    title = productData['title']
    body = productData['body']
    vendor = productData['vendor']
    tags = productData['tags']
    price = productData['price']
    images = productData['images']

    print(images)

    message = ''

    input('Press Enter To Do Next...')
    
    return False
    return True
