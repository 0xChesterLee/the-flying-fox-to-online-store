
# Program Logic Control
SCRAPE_HANDLER = False
SCRAPED_SAVE2DB_HANDLER = False
REWRITE_SAVE2DB_HANDLER = False
AI_PRODUCT_REWRITER = True
IMAGES_DOWNLOAD = True

# Resize Image Size When Scraping
RESIZE_IMAGES_WIDTH = 512
RESIZE_IMAGES_HEIGHT = 512

# The Folder Name Of Holding Images
IMAGES_FOLDER_NAME = 'images'

# Safari on iOS
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'

# The-Flying-Fox Store Front-end Base URL
TFF_BASE_FRONTEND_URL = 'https://www.theflyingfox.com.hk'

# The-Flying-Fox End Point
TFF_COLLECTIONS_ENDPOINT = 'collections.json'
TFF_PRODUCTS_ENDPOINT = 'products.json'

# Scraped Products Data JSON File Name
SCRAPED_JSON_FILENAME = 'ScrapedProductsData.json'

# Rewrite Products Data JSON File Name
REWRITE_JSON_FILENAME = 'RewriteProductsData.json'

# System SQLite Database File Name
DB_FILENAME = 'data.db'
DB_SCRAPE_TABLE_NAME = 'scrape_data'
DB_REWRITE_TABLE_NAME = 'rewrite_data'

# OpenAI API Key File Name
OPENAI_API_KEY_FILE_NAME = '.openai-secret'