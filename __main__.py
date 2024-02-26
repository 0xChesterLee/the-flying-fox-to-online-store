import misc
import json
import scrape
import database
import rewriter
import pprint

# Main Program Logic

# Scrape Data From Web Data Source
if misc.SCRAPE_HANDLER:
    productsData = []
    for url in scrape.getCollectionsURLs():
        collectionProductsData = scrape.extractCollectionProductsData(url)
        productsData.extend(collectionProductsData)
    # Save the updated product data to a JSON file
    with open(misc.SCRAPED_JSON_FILENAME, 'w') as file:
        json.dump(productsData, file, indent=4, ensure_ascii=False)
    print("Scrape JSON File Saved.")

# Save Scraped Data JSON to Database
if misc.SCRAPED_SAVE2DB_HANDLER:
    database.json2Database(misc.SCRAPED_JSON_FILENAME,'scrape_data',True)
    print("Scrape Database Data Saved.")

# TO-BE-DONE
