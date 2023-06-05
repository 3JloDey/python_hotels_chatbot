import os

import requests
from dotenv import load_dotenv


class Search:
    def __init__(self) -> None:
        load_dotenv()
        self.__api_key = os.getenv("API_TOKEN")

    def locations_id(self, city: str) -> list:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"

        querystring = {
            "q": f"{city}",
            "locale": "en_US",
            "langid": "1033",
            "siteid": "300000001",
        }

        headers = {
            "X-RapidAPI-Key": f"{self.__api_key}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        data = []
        for item in response["sr"]:
            if item["type"] != "HOTEL":
                data.append((item["gaiaId"], item["regionNames"]["displayName"]))
        return data
