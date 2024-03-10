import misc
import uploader
import json
import ast
import requests
import time
import re


def postProduct(productData=dict):
    # Define Product Data
    id = productData['id']
    title = productData['title']
    body = productData['body']
    vendor = productData['vendor']
    tags = productData['tags']
    price = productData['price']
    images = productData['images']

    # Re-Format vendor, tags
    vendor = str(vendor).replace(' ','') # Remove the Space in Vendor string
    tags = str(re.sub(r'(#\w+)\s+', r'\1', tags)).replace('#', ' #').lstrip().replace('  ',' ') # Remove the Space inside the hash tag

    # Get Meta Access Token From File
    accessToken = ''
    with open(misc.FACEBOOK_TOKEN_FILE_NAME, 'r') as file:
        accessToken = file.read().strip()

    print(f"Prepair To Post Facebook Page {id} - {title}\n")

    # Upload Images To Cloudinary To Get Images URL
    images_url = []
    for image in images:
        image_url = uploader.upload_image(image)
        if 'https' in image_url:
            images_url.append(image_url)
            time.sleep(0.1) # For Safe
        else:
            print(f"Failed Uploaded Images To Cloudinary.")
    
    # Post Images To Facebook First To Get Images IDs First
    photoIDs = []
    for image_url in images_url:
        data = {
            'published': 'false',
            'url': image_url
        }
        response = requests.post(misc.FACEBOOK_PAGE_PHOTO_ENDPOINT_URL,
                                 data=data,
                                 headers={'Authorization': f"Bearer {accessToken}"})
        if response.status_code == 200:
            response = response.json()
            if 'id' in response:
                photoIDs.append(response['id'])
        else:
            print(f"Error To Get Photo IDs, Facebook Web Response Code: {response.status_code}")
            return False

    # Post Message To Facebook Page with Photo IDs
    vendor = str('#' + str(vendor).strip())
    price = str('HK$' + str(price))
    message = f"{title}\n\n\n品牌：{vendor}\n\n\n產品介紹：\n{body}\n\n\n價錢：{price}\n\n\n\n{'**'+misc.MAILING_AND_DELIVERY_DESCRIPTION}\n\n\n\n{'https://www.carousell.com.hk/u/thebabyshark/'}\n\n\n\n{tags}"
    data = {
        'message': message,
        'published': True
    }
    # Add The Photo IDs into Requests Post Data
    for i, photoID in enumerate(photoIDs, start=1):
        data[f'attached_media[{i}]'] = f'{{"media_fbid":"{photoID}"}}'
    # Do The Post Requests to META Server
    response = requests.post(misc.FACEBOOK_PAGE_POST_ENDPOINT_URL,
                             data=data,
                             headers={'Authorization': f"Bearer {accessToken}"})
    response = response.json()
    # Print the Final Post Results
    if 'id' in response:
        print(f"Facebook Page Post Successfully with ID Returned: {response['id']}")
    else:
        print('ERROR: Facebook Page Post Failed.')
        return False
    
    # Delete And CleanUp Images From Cloudinary
    for image_url in images_url:
        if not uploader.delete(image_url):
            print(f"Clean Up {image_url} Failed.")

    return True