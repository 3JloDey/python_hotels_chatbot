import orjson
import re
from typing import Any

import httpx


class API_interface:
    def __init__(self, api_token) -> None:
        self.__headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{api_token}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

    async def get_variants_locations(self, city_from_user: str) -> list[tuple[str, str]]:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {
            "q": f"{city_from_user}",
            "locale": "en_US",
            "langid": "1033",
            "siteid": "300000001",
        }
        async with httpx.AsyncClient() as ahtx:
            response = await ahtx.get(url, headers=self.__headers, params=querystring)
            data: list[tuple[str, str]] = []
            for item in orjson.loads(response.text)["sr"]:
                if item["type"] not in ("HOTEL", "AIRPORT"):
                    data.append((item["gaiaId"], item["regionNames"]["displayName"]))
            return data

    async def get_list_hotels_id(self, regId: str, sort: str, check_in: list, check_out: list) -> list[tuple[str, str]]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        year_in, month_in, day_in = check_in
        year_out, month_out, day_out = check_out

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": f"{regId}"},
            "checkInDate": {"day": day_in, "month": month_in, "year": year_in},
            "checkOutDate": {"day": day_out, "month": month_out, "year": year_out},
            "rooms": [{"adults": 1}],
            "resultsStartingIndex": 0,
            "resultsSize": 50,
            "sort": f"{sort}",
            "availableFilter": "SHOW_AVAILABLE_ONLY"
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(12.0)) as ahtx:
            response = await ahtx.post(url, json=payload, headers=self.__headers)
            data: list[tuple[str, str]] = []
            for info in orjson.loads(response.text)["data"]["propertySearch"]["properties"]:
                try:
                    hotel_id = info["id"]
                    price = info["price"]["displayMessages"][1]["lineItems"][0].get("value", 'No Data')
                    data.append((hotel_id, price))
                except (TypeError, KeyError):
                    continue
            return data

    async def get_detail_information(self, hotel) -> dict[str, Any]:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        id, price = hotel
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": f"{id}",
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(12.0)) as ahtx:
            response = await ahtx.post(url, json=payload, headers=self.__headers)
            des = orjson.loads(response.text)
            photos: list[tuple[str, str]] = []
            for data in des["data"]["propertyInfo"]["propertyGallery"]["images"]:
                clean_url = re.sub(r'\?.*$', '', data["image"]["url"])
                description = data["image"]["description"] or 'No description'
                photos.append((clean_url, description))

            try:
                #  If the key comes with an EMPTY string, then the default value is set
                stars = des["data"]["propertyInfo"]["summary"]["overview"]["propertyRating"]["rating"] or 'No Stars'
                user_rating = des["data"]["propertyInfo"]["reviewInfo"]["summary"]["overallScoreWithDescriptionA11y"]["value"] or 'No User Rating'
                around = des["data"]["propertyInfo"]["summary"]["location"]["whatsAround"]["editorial"]["content"][0] or 'No Data'
                about = des["data"]["propertyInfo"]["propertyContentSectionGroups"]["aboutThisProperty"]["sections"][0]["bodySubSections"][0]["elements"][0]["items"][0]["content"]["text"] or 'No Data'

            #  If an error occurs in the dictionary key, it is checked in which variable the error occurred and the default key is set
            except (AttributeError, KeyError, TypeError) as exc:
                if 'stars' in str(exc):
                    stars = 'No Stars'
                elif 'user_rating' in str(exc):
                    user_rating = 'No User Rating'
                elif 'around' in str(exc):
                    around = 'No Data'
                elif 'about' in str(exc):
                    about = 'No Data'

            return {
                "hotel_name": des["data"]["propertyInfo"]["summary"]["name"],
                "address": des["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"],
                "rating": stars,
                "price": price,
                "around": around,
                "users_rating": user_rating,
                "about": about,
                "photos": photos,
                "latitude": float(des["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("latitude", 0)),
                "longitude": float(des["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("longitude", 0)),
            }
