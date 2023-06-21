from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.orm import sessionmaker
from bot.database.create_table import engine, Hotel


async def update_table(clb: CallbackQuery, manager: DialogManager) -> None:
    id_user = clb.from_user.id
    hotel_name = manager.dialog_data["hotel_name"]
    address = manager.dialog_data["address"]
    rating = manager.dialog_data["rating"]
    price = manager.dialog_data["price"]
    around = manager.dialog_data["around"]
    users_rating = manager.dialog_data["users_rating"]
    about = manager.dialog_data["about"]
    photos_url = []
    photos_description = []
    latitude = manager.dialog_data["latitude"]
    longitude = manager.dialog_data["longitude"]

    for url, description in manager.dialog_data['photos']:
        photos_url.append(url)
        photos_description.append(description)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(Hotel(id_user=id_user,
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
                      longitude=longitude
                      ))
    # Сохраняем изменения
    session.commit()

    # Закрываем сессию
    session.close()
