import cloudinary
import environ
env = environ.Env()
environ.Env.read_env()

def upload_image(imageString, folderName):
    cloudinary.config(cloud_name = 'brewshare',
                            api_key = env("CLOUDINARY_API_KEY"),
                            api_secret = env("CLOUDINARY_SECRET_KEY"))
    upload_pic = cloudinary.uploader.upload(imageString, folder=folderName)
    return upload_pic