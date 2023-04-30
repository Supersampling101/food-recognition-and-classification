import requests

# Using straight Dexcom API is not viable because its accessible only in US


url = "https://api.dexcom.com/v3/users/self/dataRange"

query = {
  "lastSyncTime": "2019-08-24T14:15:22Z"
}

token="SvCOnnvfxYpbPtw5"

headers = {"Authorization": "Bearer token"}

response = requests.get(url, headers=headers, params=query)

data = response.json()
print(data)