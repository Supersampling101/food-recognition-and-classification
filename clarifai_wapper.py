

# class for the food recognition clarifai api calls // wrapper class
import json
import requests
import base64

# ClarifaiApi class for the food recognition clarifai api calls // wrapper class
# The Clarifai pretrained food model gives lits of items on the image
# Does not suffice for some deep estimations, may be used in some cases tho.

# Use cases : cheaper item list from image and this can be pushed to some recepie API 
# to suggest recepies etc..

class ClarifaiApi:
    def __init__(self, api_key,
                 model="bd367be194cf45149e75f01d59f77ba7",
                 ) -> None:
        self.model = model
        self._api_key = api_key
        self.last_response = None

    def clasify_from_url(self, url="https://i.imgur.com/a5djbnv.jpeg"):

        # Define the headers for the API request
        headers = {
            "Authorization": f"Key {self._api_key}",
            "Content-Type": "application/json"
        }

        # Define the payload for the API request
        payload = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "url": url
                        }
                    }
                }
            ],
            "model": {
                "id": self.model,
                "output_info": {
                    "output_config": {
                        "concepts_mutually_exclusive": True
                    }
                }
            }
        }

        # Call the Clarifai Food Model API to detect food in the image
        response = requests.post("https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs",
                                 headers=headers, data=json.dumps(payload))
        # parse response to json
        response_json = json.loads(response.content)
        
        # save response for post processing
        self.last_response = response_json["outputs"][0]["data"]["concepts"]
        # returns the items
        return self.last_response
    
    # Clasifies from file
    def classify_from_file(self, filename):
        # Define the headers for the API request
        headers = {
            "Authorization": f"Key {self._api_key}",
            "Content-Type": "application/json"
        }

        # Read the image data from the file
        with open(filename, "rb") as image_file:
            encoded_image_data = base64.b64encode(image_file.read()).decode("utf-8")

        # Define the payload for the API request
        payload = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "base64": encoded_image_data
                        }
                    }
                }
            ],
            "model": {
                "id": self.model,
                "output_info": {
                    "output_config": {
                        "concepts_mutually_exclusive": True
                    }
                }
            }
        }
        # Call the Clarifai Food Model API to detect food in the image
        response = requests.post("https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs",
                                 headers=headers, data=json.dumps(payload))

        # Parse the response to JSON
        response_json = json.loads(response.content)

        self.last_response = response_json["outputs"][0]["data"]["concepts"]
        # returns the items
        return self.last_response
    
    
    #Saves response to json file
    def clasify_from_url_to_file(self,filename="response.json",url="https://i.imgur.com/a5djbnv.jpeg"):
        #save to file
        response = self.clasify_from_url(url)
        open (filename, "w").write(json.dumps(response))
        return filename, response
    
    #Saves response to json file
    def clasify_from_file_to_file(self,filename_input, filename_output="response.json"):
        #save to file
        response = self.classify_from_file(filename_input)
        open (filename_output, "w").write(json.dumps(response))
        return filename_output, response
    
    # returns the items that are < threshold
    def get_bellow_threshold(self, threshold=0.9):
        # returns the items
        return [item for item in self.last_response if item["value"] < threshold]
    
    # returns the items that are > threshold
    def get_above_threshold(self, threshold=0.9):
        # returns the items
        return [item for item in self.last_response if item["value"] > threshold]


        


def main():
    # load api key from .env file
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key=os.getenv("CLARIFAI_API_KEY")

    
    # create clarifai api object
    api = ClarifaiApi(api_key)
    url = "https://i.imgur.com/a5djbnv.jpeg"
    # api.get_items(url)
    print(api.clasify_from_file_to_file("images/test_image.jpeg"))
    print(api.get_bellow_threshold(0.9))

if __name__ == "__main__":
    main()