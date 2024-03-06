import misc
import json
import requests





# Get The Facebook Access Token Key
with open(misc.FACEBOOK_TOKEN_FILE_NAME, 'r') as file:
    facebookToken = file.read().strip()

msg = 'Test123'
post_url = f'https://graph.facebook.com/{misc.FACEBOOK_PAGE_ID}/feed'

payload = {
'message': msg,
'access_token': facebookToken
}

r = requests.post(post_url, data=payload)
print(r.text)