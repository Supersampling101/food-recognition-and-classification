import clarifai_wapper as clarifai
import os
from dotenv import load_dotenv


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



            
if __name__ == "__main__":
    classify_all_images()