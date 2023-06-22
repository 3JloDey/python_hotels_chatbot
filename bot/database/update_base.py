from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.models.hotel import Hotel


async def update_table(clb: CallbackQuery, manager: DialogManager, session_maker: async_sessionmaker) -> None:
    id_user = int(clb.from_user.id)
    hotel_name = str(manager.dialog_data["hotel_name"])
    address = str(manager.dialog_data["address"])
    rating = str(manager.dialog_data["rating"])
    price = str(manager.dialog_data["price"])
    around = str(manager.dialog_data["around"])
    users_rating = str(manager.dialog_data["users_rating"])
    about = str(manager.dialog_data["about"])
    photos_url = []
    photos_description = []
    latitude = float(manager.dialog_data["latitude"])
    longitude = float(manager.dialog_data["longitude"])

    for url, description in manager.dialog_data["photos"]:
        photos_url.append(str(url))
        photos_description.append(str(description))

    async with session_maker() as session:
        async with session.begin():
            session.add(
                Hotel(
                    id_user=id_user,
                    hotel_name=hotel_name,
                    address=address,
                    rating=rating,
                    price=price,
                    around=around,
                    users_rating=users_rating,
                    about=about,
                    photos_url=photos_url,
                    photos_description=photos_description,
                    latitude=latitude,
                    longitude=longitude,
                )
            )
