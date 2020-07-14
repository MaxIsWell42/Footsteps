import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

# How the api works, format is JSON, units is degrees
# https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
def get_location_from_zip(zipcode):
    # parameters = {'api_key': os.getenv('ZIPAPI_KEY'), 'format': 'info.JSON', 'zip_code': zipcode, 'units':'degrees'}
    
    api_key = os.getenv('ZIPAPI_KEY')
    url = 'https://www.zipcodeapi.com/rest'
    
    # Manually assembling the URL since the request syntax doesn't work with this API
    url = 'https://www.zipcodeapi.com/rest/' + str(api_key) + '/info.json/' + zipcode + '/degrees'
    # print(parameters['api_key'], zipcode)
    # print(api_key, zipcode)
    # print(os.environ)
    
    
    # If we need the spoof the user agent
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    headers = {'User-Agent': user_agent}

    # Make the request
    request = requests.get(url, headers=headers)
    # request = requests.get(url, params=parameters, headers=headers)
    
    print("URL: \n".format(str(request.url)))
    print("Response: \n".format(request.text))
    print(request.status_code)
    
    # Decode the JSON
    decode = json.loads(request.text)
    city = (decode["city"])
    
    return city

if __name__ == "__main__":
    get_location_from_zip('94102')