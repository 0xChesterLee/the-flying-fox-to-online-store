import misc
import cloudinary
import cloudinary.uploader


def getCloudinaryAccessInfo():
    with open(misc.CLOUDINARY_ACCESS_INFO_FILE_NAME, 'r') as file:
        data = file.read().strip()
    data = data.split(':') # Split with : Format: CLOUDNAME:APIKEY:APISECRET
    return data

cloudinary.config(
    cloud_name = getCloudinaryAccessInfo()[0],
    api_key = getCloudinaryAccessInfo()[1],
    api_secret = getCloudinaryAccessInfo()[2],
    secure=True)

def delete(fileName):
    FILE_ID = fileName.split('.')[-2].split('/')[-1]
    if 'ok' in cloudinary.uploader.destroy(public_id=FILE_ID)['result']:
        return True
    elif 'ok' in cloudinary.uploader.destroy(public_id=FILE_ID,
                                             resource_type='video')['result']:
        return True
    else:
        return False

def upload_image(fileName):
    FILE_ID = fileName.split('.')[-2].split('/')[-1]
    data = cloudinary.uploader.upload(fileName,
                                      public_id=FILE_ID,
                                      resource_type='image')
    if 'https' in str(data['secure_url']):
        return str(data['secure_url'])
    else:
        return None