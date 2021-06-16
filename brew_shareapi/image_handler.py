from django.core.files.base import ContentFile
import uuid
import base64

def base64_image_handler(base64_string, file_id):
    format, imagestring = base64_string.split(';base64')
    ext = format.split('/'[-1])
    data = ContentFile(base64.b64decode(imagestring), name=f'{file_id}-{uuid.uuid4()}.{ext}')
    return data