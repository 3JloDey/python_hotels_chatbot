import re
from typing import Any

import httpx
import orjson


class API_interface:
    def __init__(self, api_token) -> None:
        self.__headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{api_token}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

    @staticmethod
    async def get_value(data, keys, default='No Data') -> str | Any:
        """Get the value of a key in a nested dictionary.

        Args:
            data (dict): The dictionary to search for the key.
            keys (list): A list of keys to traverse through the nested dictionary.
            default (Any, optional): The default value to return if the key is not found. Defaults to 'No Data'.

        Returns:
            str | Any: The value of the specified key or the default value if the key is not found.
        """
        for key in keys:
            try:
                data = data[key]
            except (TypeError, KeyError, AttributeError):
                return default
        return data or default

    async def get_variants_locations(self, city_from_user: str) -> list[tuple[str, str]]:
        """Get a list of location variants for a given city.

        Args:
            city_from_user (str): The name of the city to search for.

        Returns:
            list[tuple[str, str]]: A list of tuples containing the location ID and display name.
        """
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

    async def get_list_hotels_id(self, regId: str, sort: str, check_in: str, check_out: str) -> list[tuple[str, str]]:
        """Get a list of hotel IDs and prices for a given region ID and date range.

        Args:
            regId (str): The ID of the region to search in.
            sort (str): The sorting method to use.
            check_in (str): The check-in date in YYYY-MM-DD format.
            check_out (str): The check-out date in YYYY-MM-DD format.

        Returns:
            list[tuple[str, str]]: A list of tuples containing the hotel ID and price.
        """
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        year_in, month_in, day_in = list(map(int, check_in.split("-")))
        year_out, month_out, day_out = list(map(int, check_out.split("-")))

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
        """Get detailed information about a hotel.

        Args:
            hotel (tuple[str, str]): A tuple containing the hotel ID and price.

        Returns:
            dict[str, Any]: A dictionary containing detailed information about the hotel.
        """
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        id, price = hotel
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": f"{id}",
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as ahtx:
            response = await ahtx.post(url, json=payload, headers=self.__headers)
            data = orjson.loads(response.text)
            photos: list[tuple[str, str]] = []

            for image in data["data"]["propertyInfo"]["propertyGallery"]["images"]:
                image_url = re.sub(r'\?.*$', '', image["image"]["url"])
                image_description = image["image"]["description"] or 'No description'
                photos.append((image_url, image_description))

            stars = await self.get_value(data, ["data", "propertyInfo", "summary", "overview", "propertyRating", "rating"], 'No Stars')

            user_rating = await self.get_value(data, ["data", "propertyInfo", "reviewInfo", "summary",
                                                        "overallScoreWithDescriptionA11y", "value"], 'No User Rating')

            around = await self.get_value(data, ["data", "propertyInfo", "summary", "location", "whatsAround",
                                                   "editorial", "content", 0])

            about = await self.get_value(data, ["data", "propertyInfo", "propertyContentSectionGroups",
                                                  "aboutThisProperty", "sections", 0, "bodySubSections",
                                                  0, "elements", 0, "items", 0, "content", "text"])
            return {
                "hotel_name": data["data"]["propertyInfo"]["summary"]["name"],
                "address": data["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"],
                "rating": stars,
                "price": price,
                "around": around,
                "users_rating": user_rating,
                "about": about,
                "photos": photos,
                "latitude": data["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("latitude"),
                "longitude": data["data"]["propertyInfo"]["summary"]["location"]["coordinates"].get("longitude"),
            }
