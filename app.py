import clarifai_wapper as clarifai
import os
from dotenv import load_dotenv
import requests
import json



class ImageProcessor:
    def __inint__(self)->None:
        pass
    

    def scale_down(self, filename, scale=0.5):
        from PIL import Image
        import math
        
        # Load the image
        img = Image.open(filename)

        # Define the new size for the scaled down image
        new_size = (math.ceil(img.size[0]*scale), math.ceil(img.size[1]*scale))

        # Resize the image
        scaled_img = img.resize(new_size)

        # Save the scaled down image to disk
        scaled_img.save('output_image.jpg')
        
def logmeal_api():
    img = 'output_image.jpg'
    api_user_token = '19b7a8630687986ab0308c13eea0e170b31b719b'
    headers = {'Authorization': 'Bearer ' + api_user_token}

    # Single/Several Dishes Detection
    url = 'https://api.logmeal.es/v2/image/segmentation/complete'
    resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)

    # Nutritional information
    url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
    resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
    print(resp.json()) # display nutritional info
 
    # save to json file
    open ('nutritional_info.json', 'w').write(json.dumps(resp.json()))
 
# load api key from .env file
load_dotenv()
# get API key from environment variable
api_key=os.getenv("CLARIFAI_API_KEY")


api = clarifai.ClarifaiApi(api_key=api_key)

# list files in folder images and classify them using ClarifaiApi
# supported formats jpeg, jpg, png, gif, bmp, tiff
# Define supported formats as constant
SUPPORTED_FORMATS=[".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff"]


def classify_all_images():

    # list all files in folder images
    for file in os.listdir("images"):
        # check if file is supported
        if file.endswith(tuple(SUPPORTED_FORMATS)):
            # clasify file
            api.classify_from_file(f"images/{file}")
            # print results
            print(f"File: {file} \n {api.get_above_threshold(0.5)} \n")
        
def clasify_url(url):
    # clasify file
    api.clasify_from_url(url)
    # print results
    print(f"Url: {url} \n {api.get_above_threshold(0.5)} \n")
    
if __name__ == "__main__":
    #classify_all_images()
    #url="https://www.foodiesfeed.com/wp-content/uploads/2021/01/fried-egg-and-guacamole-sandwiches.jpg"
    #clasify_url(url)
    
    img_processing=ImageProcessor()
    #img_processing.scale_down("images/fried-egg-and-guacamole-sandwiches.webp")
    logmeal_api()
    