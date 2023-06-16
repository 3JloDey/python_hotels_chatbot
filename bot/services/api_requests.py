from contextlib import suppress
from typing import Any

import requests


class API_interface:
    def __init__(self, api_token) -> None:
        self.__headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{api_token}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

    def get_variants_locations(self, city_from_user: str) -> list[tuple[str, str]]:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {
            "q": f"{city_from_user}",
            "locale": "en_US",
            "langid": "1033",
            "siteid": "300000001",
        }
        response = requests.get(url, headers=self.__headers, params=querystring).json()
        data: list[tuple[str, str]] = []
        for item in response["sr"]:
            if item["type"] not in ("HOTEL" "AIRPORT"):
                city_id = str(item["gaiaId"])
                city_name = str(item["regionNames"]["displayName"])

                data.append((city_id, city_name))
        return data

    def get_list_hotels_id(self, id: str, sort: str, check_in: list, check_out: list) -> list[tuple[str, str]]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        year_in, month_in, day_in = check_in
        year_out, month_out, day_out = check_out

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{id}"},
            "checkInDate": {"day": day_in, "month": month_in, "year": year_in},
            "checkOutDate": {"day": day_out, "month": month_out, "year": year_out},
            "rooms": [
                {
                    "adults": 1,
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 100,
            "sort": f"{sort}",
        }

        response = requests.post(url, json=payload, headers=self.__headers).json()
        data: list[tuple[str, str]] = []
        hotel_id, price = '', 'No data'
        for info in response["data"]["propertySearch"]["properties"]:
            with suppress(TypeError):
                hotel_id = str(info["id"])
                price = str(info["price"]["displayMessages"][1]["lineItems"][0]["value"])
            data.append((hotel_id, price))
        return data

    def get_detail_information(self, hotel) -> dict[str, Any]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        id, price = hotel
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": f"{id}",
        }
        response = requests.post(url, json=payload, headers=self.__headers).json()

        return {
            "hotel_name": response["data"]["propertyInfo"]["summary"]["name"],
            "address": response["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"],
            "rating": response["data"]["propertyInfo"]["summary"]["overview"]["propertyRating"].get("rating") or "No rating",
            "price": price,
            "around": response["data"]["propertyInfo"]["summary"]["location"]["whatsAround"]["editorial"]["content"][0],
            "users_rating": response["data"]["propertyInfo"]["reviewInfo"]["summary"]["overallScoreWithDescriptionA11y"].get("value") or "No user rating",
            "about": response["data"]["propertyInfo"]["propertyContentSectionGroups"]["aboutThisProperty"]["sections"][0]["bodySubSections"][0]["elements"][0]["items"][0]["content"].get('text') or "No data",
            "photos": [(data["image"]["url"], data["image"]["description"]) for data in response["data"]["propertyInfo"]["propertyGallery"]["images"]],
            "latitude": float(response["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("latitude", 0)),
            "longitude": float(response["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("longitude", 0)),
        }
