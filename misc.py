
# Images When Scraping
IMAGES_DOWNLOAD = True
SCRAPE_WAIT_TIME = 0.1

# Resize Image Size When Scraping
RESIZE_IMAGES_WIDTH = 512
RESIZE_IMAGES_HEIGHT = 512
DELETE_IMAGE_AFTER_RESIZE = True

# The Folder Name Of Holding Images
IMAGES_FOLDER_NAME = 'images'

# Safari on iOS
HTTP_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'

# The-Flying-Fox Store Front-end Base URL
TFF_BASE_FRONTEND_URL = 'https://www.theflyingfox.com.hk'

# The-Flying-Fox End Point
TFF_COLLECTIONS_ENDPOINT = 'collections.json'
TFF_PRODUCTS_ENDPOINT = 'products.json'

# Scraped Products Data JSON File Name
SCRAPED_JSON_FILENAME = 'data/ScrapedProductsData.json'

# Rewrite Products Data JSON File Name
REWRITE_JSON_FILENAME = 'data/RewriteProductsData.json'

# System SQLite Database File Name
DB_FILENAME = 'data/data.db'
DB_SCRAPE_TABLE_NAME = 'scrape_data'
DB_REWRITE_TABLE_NAME = 'rewrite_data'

# OpenAI API Key File Name
OPENAI_API_KEY_FILE_NAME = 'secret/.openai-secret'

# OpenAI Rewrite Prompt
REWRITE_PROMPT = '請使用繁體中文重寫以下文字，但保留"TITLE:"、"TAGS:"和"BODY:"。"TITLE:"和"BODY:"需要保留70%以上的繁體中文字、"TAGS:"需要保留100%的繁體中文字，並將重寫後的內容輸出。在重寫後的"TAGS:"內容上，根據"BODY:"後的內容額外生成最多6個主題標籤。如果重寫後的"TAGS:"內容為空白，請自行生成最多6個主題標籤，主題標籤不需要加上"#"字符號，但請用逗號分隔。\nTITLE:{0}\nTAGS:{2}\nBODY:{1}'

# Carousell Settings
CAROUSELL_BASE_FRONTEND_URL = 'https://www.carousell.com.hk'
CAROUSELL_COOKIES_FILE_NAME = 'secret/carousell.cookies.pkl'
MAILING_AND_DELIVERY_DESCRIPTION = '買滿$400以上包送貨，未滿$400運費到付。(只限香港)'

# Price Settings
PRODUCTS_DISCOUNT_RATE = 0.85

# Facebook Page Settings
FACEBOOK_PAGE_ID = 275521235637171

# Facebook Page Access Token File Name And Endpoint URL
FACEBOOK_TOKEN_FILE_NAME = 'secret/.facebook-secret'
FACEBOOK_POST_ENDPOINT_URL = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"

# Cloudinary Access Information File Name
CLOUDINARY_ACCESS_INFO_FILE_NAME = 'secret/.cloudinary-secret'
