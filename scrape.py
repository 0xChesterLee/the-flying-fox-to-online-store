import misc
import requests
import bs4
import os
import time
from PIL import Image

def requestGetResponse(url):
    # Make the HTTPS request and retrieve the JSON response
    response = requests.get(url,
                            headers={'User-Agent': misc.USER_AGENT})
    # If Web Server Status Code Not OK then Return None
    if not response.status_code == 200:
        return None
    # Set the response encoding to UTF-8
    response.encoding = 'utf-8'
    # For Safe
    time.sleep(0.25)
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
                       'rewrite': 0
                       }
        # Fix Tags Issue
        ProductData = fixTags(ProductData)
        # Fix Body HTML Issue
        ProductData = fixBodyHTML(ProductData)
        # Append List
        collectionProductsData.append(ProductData)
    # Return Products Data in List
    return collectionProductsData

def urlToFileName(url):
    fileName = str(os.path.basename(url))
    fileName = fileName.rsplit('?')[0]
    fileName = fileName.lower()
    return fileName

def fixFileName(id, fileName):
    id = str(id)
    fileName = str(fileName)
    fileName = '{0}.{1}'.format(id,fileName)
    return fileName

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
    # Request Get Response From Web Server
    response = requestGetResponse(url)
    # Server Error Handle
    if not response:
        print('ERROR Downloading Image: ',baseName)
        return None
    # Skip Download Image If File Exist
    if os.path.exists(fileName):
        print('Image Exist, Skipping: ',baseName)
        return None
    # Write Image To File
    with open(fileName, "wb") as file:
        file.write(response.content)
    print('Image Downloaded: ',baseName)
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
        # Rename Original File Name
        os.rename(fileName, '{0}.bak'.format(fileName))
        # Save Resized Image
        extName = fileName.rsplit('.')[-1].lower()
        if extName.endswith(('jpg','jpeg')):
            resizedImage.save(fileName, "JPEG")
        elif extName.endswith(('png')):
            resizedImage.save(fileName, "PNG")
        print('Image Resized.')
    # Define Base File Name For Return
    baseName = os.path.basename(fileName)
    return baseName
