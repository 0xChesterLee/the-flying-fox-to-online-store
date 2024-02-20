import scrape
import json

# Main
productsData = []
for url in scrape.getCollectionsURLs():
    collectionProductsData = scrape.extractCollectionProductsData(url)
    if collectionProductsData:
        productsData.append(collectionProductsData)

# Save the updated product data to a JSON file
with open('output.json', 'w') as file:
    json.dump(productsData, file, indent=4, ensure_ascii=False)
print("Data Saved.")