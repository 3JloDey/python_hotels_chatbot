import os
from typing import Any, List

import requests
from dotenv import load_dotenv


class Search:
    def __init__(self) -> None:
        load_dotenv()
        self.__api_key = os.getenv("API_TOKEN")

    def locations_id(self, city: str) -> List[Any]:
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

    def hotels_list_id(self, city_id) -> List[Any]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{city_id}"},
            "checkInDate": {"day": 10, "month": 6, "year": 2023},
            "checkOutDate": {"day": 15, "month": 6, "year": 2023},
            "rooms": [{"adults": 2, "children": [{"age": 5}, {"age": 7}]}],
            "resultsStartingIndex": 0,
            "resultsSize": 200,
            "sort": "PRICE_LOW_TO_HIGH",
            # "filters": {"price": {"max": 150, "min": 100}},
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{self.__api_key}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

        response = requests.post(url, json=payload, headers=headers).json()
        data = []
        for info in response["data"]["propertySearch"]["properties"]:
            data.append(info["id"])
        return data

    def detail_information(self, hotel_id) -> dict[str, Any]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": f"{hotel_id}",
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{self.__api_key}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

        response = requests.post(url, json=payload, headers=headers).json()

        hotel_name = response["data"]["propertyInfo"]["summary"]["name"]
        address = response["data"]["propertyInfo"]["summary"]['location']["address"]["addressLine"]
        rating = response["data"]["propertyInfo"]["summary"]['overview']['propertyRating']['accessibility']

        return {
            "hotel_name": hotel_name,
            "address": address,
            'rating': rating,
        }
