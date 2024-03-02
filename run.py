import sys
import misc
import json
import scrape
import database
import rewriter
import time
import os
import ast


# Main Program
try:
    print(f'Program Start With Params: {sys.argv[1:][0]}')
except Exception as e:
    print('No Program Params.')
    exit(-1)

# For Scrape
if sys.argv[1:][0].upper() == 'SCRAPE':
    productsData = []
    for url in scrape.getCollectionsURLs():
        collectionProductsData = scrape.extractCollectionProductsData(url)
        productsData.extend(collectionProductsData)

    # Save Updated product data to a JSON file
    with open(misc.SCRAPED_JSON_FILENAME, 'w') as file:
        json.dump(productsData, file, indent=4, ensure_ascii=False)
    
    # Save Scraped Data JSON to Database
    database.json2Database(misc.SCRAPED_JSON_FILENAME,misc.DB_SCRAPE_TABLE_NAME,'id',True)
    print("Scrape Database Data Saved.")

    # Save Scraped Database to JSON
    database.database2JSON(misc.DB_SCRAPE_TABLE_NAME,misc.SCRAPED_JSON_FILENAME)
    print("Scrape JSON File Saved.")

# For Rewrite
elif sys.argv[1:][0].upper() == 'REWRITE':
    # Get All Products Data Scraped
    productsData = []
    productsData = database.getValues(misc.DB_SCRAPE_TABLE_NAME,
                                    ['id',
                                    'title',
                                    'body_html',
                                    'vendor',
                                    'tags',
                                    'price',
                                    'images'],'rewrite=0', 'id')
    
    # Rewrite All Products Data
    if productsData:
        for productData in productsData:
            # Open Existing Rewrite Product Data JSON file
            file = os.path.join(os.getcwd(),misc.REWRITE_JSON_FILENAME)
            if os.path.exists(file):
                with open(file, 'r') as file:
                    RewriteProductsData = json.load(file)
            else:
                RewriteProductsData = []
            
            # Prepair All Params To-Be Rewrite
            id = int(productData['id'])
            originalTitle = str(productData['title'])
            originalBody = str(productData['body_html'])
            originalTags = str(productData['tags'])
            vendor = productData['vendor']
            price = float(productData['price'])
            images = productData['images']

            # Use AI Rewriter To Rewrite The Product Information
            print(f'Prepair To Rewrite {id}:{originalTitle}\n')
            data = rewriter.productRewriter(originalTitle, originalBody, originalTags)
            title = data['title']
            body = data['body']
            tags = data['tags']
            print(f'Rewrited Product Information ({id}) - ({title}) - ({tags})\n\n{body}\n\n\n\n')

            # Define Product Data Dict
            ProductData = {'id': id,
                        'originalTitle': originalTitle,
                        'originalBody': originalBody,
                        'originalTags': originalTags,
                        'title': title,
                        'body': body,
                        'tags': tags,
                        'vendor': vendor,
                        'price': price,
                        'images': images}
            
            # Append Rewrite Products Data List
            RewriteProductsData.append(ProductData)

            # Update Rewrite Status To 1
            database.updateValue(misc.DB_SCRAPE_TABLE_NAME,'rewrite',1,f'id={id}')

            # Save Rewrite Product Data to a JSON file
            file = os.path.join(os.getcwd(),misc.REWRITE_JSON_FILENAME)
            with open(file, 'w') as file:
                json.dump(RewriteProductsData, file, indent=4, ensure_ascii=False)
            print("Rewrite JSON File Saved.")

            # OpenAI Official Rules
            print('[Official Waiting Rules] Waiting For The Next Rewrite, Please Wait...')
            time.sleep(60)
    
    # Final Fix JSON File Format and Scraping String Bug etc.
    scrape.finalFixJsonFormat(misc.REWRITE_JSON_FILENAME)
    print("Final Fixed Rewrite JSON File Saved.")
    
    # Save Rewrite Data JSON to Database
    database.json2Database(misc.REWRITE_JSON_FILENAME,misc.DB_REWRITE_TABLE_NAME,'id',True)
    print("Rewrite Database Data Saved.")
else:
    print('Params Error.')
print('Good Bye.')