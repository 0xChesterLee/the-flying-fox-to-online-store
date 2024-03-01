import sys
import misc
import json
import scrape
import database
import rewriter
import time
import os
import ast


def FinalFixJsonFormat(json_file):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
     
        item['title'] = str(item['title']).strip()
        item['body'] = str(item['body']).strip()
        try:
            item['originalTags'] = ast.literal_eval(item['originalTags'])
        except Exception as e:
            pass
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

        try:
            item['images'] = ast.literal_eval(item['images'])
        except Exception as e:
            pass
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True


# Main Program
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
    
    FinalFixJsonFormat(misc.REWRITE_JSON_FILENAME)
    print("Final Fixed Rewrite JSON File Saved.")
    
    # Save Rewrite Data JSON to Database
    database.json2Database(misc.REWRITE_JSON_FILENAME,misc.DB_REWRITE_TABLE_NAME,'id',True)
    print("Rewrite Database Data Saved.")
else:
    print('Param Error.')
print('Bye.')