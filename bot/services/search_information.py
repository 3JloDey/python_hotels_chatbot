import os
from typing import Any, List
import json
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
            if item["type"] not in ("HOTEL" "AIRPORT"):
                data.append((item["gaiaId"], item["regionNames"]["displayName"]))
        return data

    def hotels_list_id(self, city_id: str, sort: str, check_in: list, check_out: list) -> List[Any]:
        year_in, month_in, day_in = check_in
        year_out, month_out, day_out = check_out
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{city_id}"},
            "checkInDate": {"day": day_in, "month": month_in, "year": year_in},
            "checkOutDate": {"day": day_out, "month": month_out, "year": year_out},
            "rooms": [{"adults": 1, }],
            "resultsStartingIndex": 0,
            "resultsSize": 100,
            "sort": f"{sort}",
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
        with open('conflict_response.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=4)

        hotel_name = response["data"]["propertyInfo"]["summary"]["name"]
        address = response["data"]["propertyInfo"]["summary"]['location']["address"]["addressLine"]
        users_rating = response["data"]["propertyInfo"]["reviewInfo"]['summary']['overallScoreWithDescriptionA11y']['value'] 
        around = '\n'.join(response["data"]["propertyInfo"]["summary"]['location']['whatsAround']['editorial']['content'])
        about = response["data"]["propertyInfo"]['propertyContentSectionGroups']['aboutThisProperty']['sections'][0]['bodySubSections'][0]['elements'][0]["items"][0]['content'].get("text", 'No Description')
        try:
            rating = response["data"]["propertyInfo"]["summary"]['overview']['propertyRating']['rating']
        except (KeyError, TypeError):
            rating = 'No Stars'

        return {
            "hotel_name": hotel_name,
            "address": address,
            'rating': rating,
            'around': around,
            'users_rating': users_rating,
            'about': about
        }
