import misc
import requests
import os
import time

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
    time.sleep(0.1)
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
        # Except 'all' Value
        if str(data['handle']).lower() == 'all':
            continue
        # Combind To Full Products URL
        url = '{0}/collections/{1}/{2}'.format(misc.TFF_BASE_FRONTEND_URL,
                                               data['handle'],
                                               misc.TFF_PRODUCTS_ENDPOINT)
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
            # Download Image
            downloadImage(image['src'])
            images.append(urlToFileName(image['src']))
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
                       'images': images
                       }
        # Append the List
        collectionProductsData.append(ProductData)
    # Fix Tags
    collectionProductsData = fixTags(collectionProductsData)
    # Return Products Data in List
    return collectionProductsData

def urlToFileName(url):
    fileName = str(os.path.basename(url))
    fileName = fileName.rsplit('?')[0]
    return fileName

def fixTags(collectionProductsData):
    # Remove Some Strings in Tags
    for productData in collectionProductsData:
        if 'tags' in productData:
            tags = productData['tags']
            tags = [tag.replace('Product Type_','') for tag in tags]
            tags = [tag.replace('Brand_','') for tag in tags]
            tags = [tag.replace('Age_','') for tag in tags]
            productData['tags'] = tags
    return collectionProductsData

def downloadImage(url):
    # Prepair Full File Path
    fileDir = os.path.join(os.getcwd(), misc.IMAGES_FOLDER_NAME)
    # Create the output directory if it doesn't exist
    os.makedirs(fileDir, exist_ok=True)
    # Final Full File Path
    fileName = os.path.join(fileDir, os.path.basename(url))
    fileName = fileName.rsplit('?')[0]
    # Request Get Response From Web Server
    response = requestGetResponse(url)
    if not response:
        return None
    # Skip Download Image Again If File Exist
    if os.path.exists(fileName):
        print('Image Already Exist.', fileName)
        return fileName
    # Write Image To File
    with open(fileName, "wb") as file:
        file.write(response.content)
    print('Image downloaded and saved as', fileName)
    return fileName
