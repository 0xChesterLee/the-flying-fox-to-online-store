import misc
import database
import requests
import json
import ast
import bs4
import os
import time
from PIL import Image


def requestGetResponse(url):
    # Make the HTTPS request and retrieve the JSON response
    response = requests.get(url,
                            headers={'User-Agent': misc.HTTP_USER_AGENT})
    
    # If Web Server Status Code Not 200(OK) then Return None
    if not response.status_code == 200:
        return None
    
    # Set the response encoding to UTF-8
    response.encoding = 'utf-8'

    # For Scraping Safe Wait Time
    time.sleep(misc.SCRAPE_WAIT_TIME)
    
    return response

def getCollectionsURLs():
    # Define List Variable for Return
    collectionsURL = []

    # Prepair URL to Request
    url = '{0}/{1}'.format(misc.TFF_BASE_FRONTEND_URL,
                           misc.TFF_COLLECTIONS_ENDPOINT)
    
    # Request Get Response From Web Server
    response = requestGetResponse(url)

    # Set the Response to Json Format
    response = response.json()

    # Extract 'handle' Value
    for data in response['collections']:
        # Skip If Value Is 'all'
        if str(data['handle']).lower() == 'all':
            continue

        # Skip If Products Count Is Zero
        if int(data['products_count']) == 0:
            continue
        # Combind To Full Products URL
        url = '{0}/collections/{1}/{2}'.format(misc.TFF_BASE_FRONTEND_URL,
                                               data['handle'],
                                               misc.TFF_PRODUCTS_ENDPOINT)
        
        # Append List
        collectionsURL.append(url)

    # Return Collections Full URL in List
    return collectionsURL

def extractCollectionProductsData(url):
    # Define List Variable for Return
    collectionProductsData = []

    # Request Get Response From Web Server
    response = requestGetResponse(url)

    # Set the Response to Json Format
    response = response.json()
    # Extract The 'id' 'title' 'handle' 'body_html' 'vendor' 'product_type' 'tags' 'variants['sku']' 'variants['price']' 'images['src']' Value
    for data in response['products']:
        # Get Images URLs
        images = []
        for image in data['images']:
            # Convert URL To File Name
            fileName = urlToFileName(image['src'])

            # Fix File Name In New Format (id.filename)
            fileName = fixFileName(data['id'],fileName)

            # Download Image
            if misc.IMAGES_DOWNLOAD:
                downloadImage(image['src'],fileName)

            # Convert Image Size
            fileName = convertImage(fileName)

            # Append List
            images.append(fileName)

        # Get The Rewrite Status
        if database.getValues(misc.DB_SCRAPE_TABLE_NAME,['rewrite'],f'id={data['id']}','id') == []:
            rewrite = 0
        else:
            rewrite = 1
        
        # Define Dict For Product Data
        ProductData = {'id': int(data['id']),
                       'title': data['title'],
                       'handle': data['handle'],
                       'body_html': data['body_html'],
                       'vendor': data['vendor'],
                       'product_type': data['product_type'],
                       'tags': data['tags'],
                       'sku': data['variants'][-1]['sku'],
                       'price': float(data['variants'][-1]['price']),
                       'images': images,
                       'rewrite': rewrite
                       }
        
        # Fix Tags Issue
        ProductData = fixTags(ProductData)

        # Fix Body HTML Issue
        ProductData = fixBodyHTML(ProductData)

        # Print Out The Data What We're Scraping
        print(f'Scraping Product ID: {ProductData['id']} - {ProductData['title']}')

        # Append List
        collectionProductsData.append(ProductData)

    # Return Products Data in List
    return collectionProductsData

# Get The Correct File Name Only In URL String
def urlToFileName(url):
    fileName = str(os.path.basename(url))
    fileName = fileName.rsplit('?')[0]
    fileName = fileName.lower()
    return fileName

# Use Our Own Format Of File Name (ex: id.filename.jpg)
def fixFileName(id, fileName):
    id = str(id)
    fileName = str(fileName)
    fileName = '{0}.{1}'.format(id,fileName)
    return fileName

# Filter Out Useless Of Tags When Scraping
def fixTags(productData):
    # Remove Some Strings in Tags
    if 'tags' in productData:
        tags = productData['tags']
        tags = [tag.replace('Product Type_','') for tag in tags]
        tags = [tag.replace('Brand_','') for tag in tags]
        tags = [tag.replace('Age_','') for tag in tags]
        
        # Update List Value
        productData['tags'] = tags
    return productData

def fixBodyHTML(productData):
    if 'body_html' in productData :
        body_html = productData['body_html']
        
        # Remove Some New Line in Body HTML
        body_html = bs4.BeautifulSoup(body_html, 'html.parser')
        body_html = body_html.get_text('\n')
        body_html = body_html.replace('\n\n','')
        
        # Update List Value
        productData['body_html'] = body_html

        return productData

def downloadImage(url, fileName):
    # Prepair Dir And Full File Path
    fileDir = os.path.join(os.getcwd(), misc.IMAGES_FOLDER_NAME)
    fileName = os.path.join(fileDir,fileName)
    
    # Create the output directory if it doesn't exist
    os.makedirs(fileDir,exist_ok=True)
    
    # Define Base File Name For Return
    baseName = os.path.basename(fileName)

    # Skip Download Image If File Exist
    if os.path.exists(fileName):
        return None
    
    # Request Get Response From Web Server
    response = requestGetResponse(url)
    
    # Server Error Handle
    if not response:
        print('ERROR Downloading Image From Web Server: ',baseName)
        return None
    
    # Write Image To File
    with open(fileName, "wb") as file:
        file.write(response.content)

    # For Scraping Safe Waiting Time
    time.sleep(misc.SCRAPE_WAIT_TIME)

    return baseName

def convertImage(fileName):
    # Prepair Full File Name
    fileDir = os.path.join(os.getcwd(),misc.IMAGES_FOLDER_NAME)
    fileName = os.path.join(fileDir,fileName)

    # Check If Supported Image Format
    if not fileName.lower().endswith(('.jpg','.jpeg','.png')):
        print('Unsupported Image Format. Please provide a JPG, JPEG, or PNG file.',fileName)
        exit(-1)
        return None
    
    # Open Image File
    image = Image.open(fileName)

    # Check Image Size
    width, height = image.size
    if width != misc.RESIZE_IMAGES_WIDTH or height != misc.RESIZE_IMAGES_HEIGHT:
        # Resize Image
        resizedImage = image.resize((misc.RESIZE_IMAGES_WIDTH, misc.RESIZE_IMAGES_HEIGHT),
                                    Image.LANCZOS)
        
        # Delete Image After Resize
        if misc.DELETE_IMAGE_AFTER_RESIZE:
            # Check if the file exists
            if os.path.exists(fileName):
                # Delete the file
                os.remove(fileName)
        else:
            # Rename Original File Name Ext Name .bak
            os.rename(fileName, '{0}.bak'.format(fileName))

        # Save Resized Image
        extName = fileName.rsplit('.')[-1].lower()
        if extName.endswith(('jpg','jpeg')):
            resizedImage.save(fileName, "JPEG")
        elif extName.endswith(('png')):
            resizedImage.save(fileName, "PNG")

    # Define Base File Name For Return
    baseName = os.path.basename(fileName)

    return baseName

def finalFixJsonFormat(json_file):
    # Open The JSON File First
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        # Fix The 'title' And 'Body' Space Problem
        item['title'] = str(item['title']).strip()
        item['body'] = str(item['body']).strip()

        # Fix The 'originalTags' Problem To Correct Format
        try:
            item['originalTags'] = ast.literal_eval(item['originalTags'])
        except Exception as e:
            pass
        
        # Fix The 'tags' Problem To Correct Format
        item['tags'] = str(item['tags']).strip()
        item['tags'] = str(item['tags']).replace('，',',')
        item['tags'] = str(item['tags']).replace(', ',',')
        try:
            if item['tags'][0] != '[' and item['tags'][-1] != ']':
                item['tags'] = str(item['tags']).split(',')
            else:
                item['tags'] = ast.literal_eval(item['tags'])
        except Exception as e:
            pass
        
        # Fix The 'images' Problem To Correct Format
        try:
            item['images'] = ast.literal_eval(item['images'])
        except Exception as e:
            pass
        
        # Add The Listed Key (listCarousell, listFacebookPage, listFacebookMarket) Into The JSON File
        if not 'listCarousell' in item:
            item['listCarousell'] = 0
        if not 'listFacebookPage' in item:
            item['listFacebookPage'] = 0
        if not 'listFacebookMarket' in item:
            item['listFacebookMarket'] = 0

    
    # Write Back To JSON File with Pretty Format
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return True