import misc
import uploader
import json
import ast
import requests
import time


def postProduct(productData=dict):
    # Define Product Data
    id = productData['id']
    title = productData['title']
    body = productData['body']
    vendor = productData['vendor']
    tags = productData['tags']
    price = productData['price']
    images = productData['images']

    print(id, title, body, vendor, tags, price, images)

    # Tags
    print(tags)
    exit(-1)

    # Upload Images To Cloudinary First
    images_url = []
    for image in images:
        image_url = uploader.upload_image(image)
        if 'https' in image_url:
            images_url.append(image_url)
            # For Safe
            time.sleep(0.5)
    
    



    input('Press Enter To Do Next...')

    return False # Debug
    return True
