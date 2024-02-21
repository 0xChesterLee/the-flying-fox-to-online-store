import scrape
import json
import pprint

# Main
productsData = []
for url in scrape.getCollectionsURLs():
    collectionProductsData = scrape.extractCollectionProductsData(url)
    productsData.extend(collectionProductsData)


# Save the updated product data to a JSON file
with open('output.json', 'w') as file:
    json.dump(productsData, file, indent=4, ensure_ascii=False)
print("Data Saved.")