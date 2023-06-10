import os
from typing import Any, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def locations_id(city: Optional[str]) -> dict[str, str]:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {
        "q": f"{city}",
        "locale": "en_US",
        "langid": "1033",
        "siteid": "300000001",
    }

    headers = {
        "X-RapidAPI-Key": f"{os.getenv('API_TOKEN')}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    data = []
    for item in response["sr"]:
        if item["type"] not in ("HOTEL" "AIRPORT"):
            data.append((item["gaiaId"], item["regionNames"]["displayName"]))
    return data


def hotels_list_id(id: str, sort: str, check_in: list, check_out: list) -> List[Any]:
    year_in, month_in, day_in = check_in
    year_out, month_out, day_out = check_out
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

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
        "resultsSize": 50,
        "sort": f"{sort}",
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": f"{os.getenv('API_TOKEN')}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    response = requests.post(url, json=payload, headers=headers).json()
    data = []
    for info in response["data"]["propertySearch"]["properties"]:
        data.append(info["id"])
    return data


def detail_information(hotel_id) -> dict[str, Any]:
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
        "X-RapidAPI-Key": f"{os.getenv('API_TOKEN')}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    response = requests.post(url, json=payload, headers=headers).json()

    hotel_name = response["data"]["propertyInfo"]["summary"]["name"]
    address = response["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"]
    users_rating = response["data"]["propertyInfo"]["reviewInfo"]["summary"]["overallScoreWithDescriptionA11y"]["value"]
    around = "\n".join(response["data"]["propertyInfo"]["summary"]["location"]["whatsAround"]["editorial"]["content"])
    about = response["data"]["propertyInfo"]["propertyContentSectionGroups"]["aboutThisProperty"]["sections"][0]["bodySubSections"][0]["elements"][0]["items"][0]["content"].get("text", "No Description")
    latitude = response["data"]["propertyInfo"]["summary"]["location"]["coordinates"]["latitude"]
    longitude = response["data"]["propertyInfo"]["summary"]["location"]["coordinates"]["longitude"]
    photos = []
    for photo in response["data"]["propertyInfo"]["propertyGallery"]["images"]:
        photos.append(photo["image"]["url"])
    try:
        rating = response["data"]["propertyInfo"]["summary"]["overview"]["propertyRating"]["rating"]
    except (KeyError, TypeError):
        rating = "No Stars"

    return {
        "hotel_name": hotel_name,
        "address": address,
        "rating": rating,
        "around": around,
        "users_rating": users_rating,
        "about": about,
        "photos": photos,
        "latitude": latitude,
        "longitude": longitude,
    }
