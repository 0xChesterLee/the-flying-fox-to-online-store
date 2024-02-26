import misc
import json
import scrape
import database
import rewriter
import time

# Main Program Logic

# Scrape Data From Web Data Source
if misc.SCRAPE_HANDLER:
    productsData = []
    for url in scrape.getCollectionsURLs():
        collectionProductsData = scrape.extractCollectionProductsData(url)
        productsData.extend(collectionProductsData)
    # Save Updated product data to a JSON file
    with open(misc.SCRAPED_JSON_FILENAME, 'w') as file:
        json.dump(productsData, file, indent=4, ensure_ascii=False)
    print("Scrape JSON File Saved.")

# Save Scraped Data JSON to Database
if misc.SCRAPED_SAVE2DB_HANDLER:
    database.json2Database(misc.SCRAPED_JSON_FILENAME,misc.DB_SCRAPE_TABLE_NAME,True)
    print("Scrape Database Data Saved.")

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
if misc.AI_PRODUCT_REWRITER and productsData:
    RewriteProductsData = []
    for productData in productsData:
        # Prepair All Params To-Be Rewrite
        id = int(productData['id'])
        originalTitle = str(productData['title'])
        originalBody = str(productData['body_html'])
        originalTags = str(productData['tags'])
        vendor = str(productData['vendor'])
        price = float(productData['price'])
        images = str(productData['images'])

        # Use AI Rewriter To Rewrite The Product Information
        # TO-DO
        data = rewriter.productRewriter(originalTitle, originalBody, originalTags)
        title = data['title']
        body = data['body']
        tags = data['tags']
        print(f'Rewrited Product Information {id} - {title} - {tags} - {body}\n\n')

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

        # OpenAI Official Rules
        print('Waiting For The Next Rewrite, Please Wait...')
        time.sleep(20+1)

    # Save Rewrite Product data to a JSON file
    with open(misc.REWRITE_JSON_FILENAME, 'w') as file:
        json.dump(RewriteProductsData, file, indent=4, ensure_ascii=False)
    print("Rewrite JSON File Saved.")
        
# Save Rewrite Data JSON to Database
if misc.REWRITE_SAVE2DB_HANDLER:
    database.json2Database(misc.REWRITE_JSON_FILENAME,misc.DB_REWRITE_TABLE_NAME,True)
    print("Rewrite Database Data Saved.")


print('Bye! Done.')