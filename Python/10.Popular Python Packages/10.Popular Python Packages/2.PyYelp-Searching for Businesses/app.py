import requests
import config


url = "https://api.yelp.com/v3/businesses/search"
headers = {
    "Authorization": "Bearer " + config.api_key
}
params = {
    "term": "restaurant",
    "location": "NYC"
}
response = requests.get(url, headers=headers, params=params)
businesses = response.json()["businesses"]
names = [(business["id"], business["name"], business["rating"])
         for business in businesses if business["rating"] > 4.1]
print(names)
# for business in businesses:
#     print(business["name"])
