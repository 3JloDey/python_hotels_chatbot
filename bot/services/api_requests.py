import re
from typing import Any

import httpx
import jmespath as jp
import orjson


class API_interface:
    def __init__(self, api_token) -> None:
        self.__headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{api_token}",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

    async def get_variants_locations(self, city_from_user: str) -> list[tuple[str, str]]:
        """
        Fetches a list of location IDs and names that match the given search query.

        Args:
            city_from_user: string representing the user's search query

        Returns:
            A list of tuples containing each location's ID and name as strings.
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
            deserialized = orjson.loads(response.text)

            cities = jp.search("sr[*].regionNames.displayName", deserialized)
            cities_id = jp.search("sr[*].gaiaId", deserialized)
            types = jp.search("sr[*].type", deserialized)
            data = [(id, city) for id, city, type in zip(cities_id, cities, types)
                    if type in ("CITY", "NEIGHBORHOOD")]
            return data

    async def get_list_hotels_id(self, regId: str, sort: str, check_in: str, check_out: str) -> list[tuple[str, str]]:
        """
        Fetches a list of hotel IDs and prices from RapidAPI.

        Args:
            regId: string representing the ID of the region
            sort: string representing how to sort the hotels, e.g. "PRICE_LOW_TO_HIGH"
            check_in: string representing the check-in date in YYYY-MM-DD format
            check_out: string representing the check-out date in YYYY-MM-DD format

        Returns:
            A list of tuples containing each hotel's ID and price as strings.
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
            deserialized = orjson.loads(response.text)
            ids = jp.search('data.propertySearch.properties[*].id', deserialized)
            price = jp.search('data.propertySearch.properties[*].price.displayMessages[1].lineItems[0].value', deserialized)
            return list(zip(ids, price))

    async def get_detail_information(self, hotel) -> dict[str, Any]:
        """
        Fetches detailed information about a hotel from the RapidAPI and returns a dictionary of relevant data.

        Args:
            hotel: a tuple containing the hotel ID and its price

        Returns:
            A dictionary containing the following keys:

            - "hotel_name": string representing the name of the hotel
            - "address": string representing the address of the hotel
            - "rating": string representing the rating of the hotel
            - "price": float representing the price of the hotel
            - "around": string representing things around the hotel
            - "users_rating": string representing the user rating of the hotel
            - "about": string representing information about the hotel
            - "photos": list of tuples, each containing a string URL of a photo and a string description.
            - "latitude": float representing the latitude of the hotel's location
            - "longitude": float representing the longitude of the hotel's location
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

        async with httpx.AsyncClient(timeout=httpx.Timeout(12.0)) as ahtx:
            response = await ahtx.post(url, json=payload, headers=self.__headers)
            deserialized = orjson.loads(response.text)

            lctn = "data.propertyInfo.summary.location"
            prprt = "data.propertyInfo"
            smmr = "data.propertyInfo.summary"
            glr = "data.propertyInfo.propertyGallery.images[*].image"

            hotel_name = jp.search(f"{smmr}.name", deserialized)
            address = jp.search(f"{lctn}.address.addressLine", deserialized)
            rating = jp.search(f"{smmr}.overview.propertyRating.rating", deserialized) or 'No stars'
            user_rating = jp.search(f"{prprt}.reviewInfo.summary.overallScoreWithDescriptionA11y.value", deserialized) or 'No user rating'
            about = jp.search(f"{prprt}.propertyContentSectionGroups.aboutThisProperty.sections[0].bodySubSections[0].elements[0].items[0].content.text", deserialized) or "No Data"
            around = jp.search(f"{lctn}.whatsAround.editorial.content[0]", deserialized) or 'No Data'
            longitude = jp.search(f"{lctn}.coordinates.longitude", deserialized)
            latitude = jp.search(f"{lctn}.coordinates.latitude", deserialized)

            dirty_urls = jp.search(f"{glr}.url", deserialized)
            clean_urls = [re.sub(r'\?.*$', '', url) for url in dirty_urls]
            image_description = jp.search(f"{glr}.description", deserialized)

            photos = list(zip(clean_urls, image_description))

            return {
                "hotel_name": hotel_name,
                "address": address,
                "rating": rating,
                "price": price,
                "around": around,
                "users_rating": user_rating,
                "about": about,
                "photos": photos,
                "latitude": latitude,
                "longitude": longitude,
            }
