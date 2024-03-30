from random import randint
from datetime import date

from sqlalchemy import select, func, insert, delete, update
from faker import Faker
from werkzeug.security import check_password_hash, generate_password_hash

from models.main_models import User
from .profiles_managment_orm import create_profile_instance
# TODO: configure them in class


async def add_default_users(session):
    fake = Faker()
    avatars = [
        "Smokey", "Annie", "Tigger",
        "Bella", "Midnight", "Cookie",
        "Luna", "Sheba", "Oreo",
        "Peanut", "Oliver", "Molly"
    ]
    count_users_query = select(func.count("*").label("total_users")).select_from(User)
    total_count_cursor = await session.execute(count_users_query)
    total_count = total_count_cursor.first()._asdict()

    if total_count["total_users"] == 0:
        for i in range(40):
            avatar_name = avatars[randint(0, 11)]
            profile = create_profile_instance({"education": "High school", "web_site": "Site link", "birth_date": date.today()})
            session.add(profile)
            await session.commit()
            user_data = {
                "username": fake.name(),
                "img": f"https://api.dicebear.com/7.x/adventurer/svg?seed={avatar_name}",
                "email": fake.email(),
                "password": generate_password_hash(fake.password(length=10)),  # check_password_hash
                "status": fake.sentence(nb_words=10),
                "followed": fake.pybool(),
                "country": fake.country(),
                "city": fake.city(),
                "profile": profile
            }
            session.add(User(**user_data))
            await session.commit()


async def select_users(session, page=1, count=10):
    record_start_from = (page - 1) * count

    users_cursor = await session.execute(select(User).limit(count).offset(record_start_from))
    count_users_query = select(func.count("*").label("total_users")).select_from(User)
    total_count_cursor = await session.execute(count_users_query)
    users = users_cursor.all()
    total_count = total_count_cursor.mappings().first()
    return users, total_count


async def create_new_user(session, user_data):
    if password := user_data.get("password"):  # TODO handle else
        password_hash = generate_password_hash(password)
        user_data["password_hash"] = password_hash
        session.add(User(**user_data))
        await session.commit()
    else:
        pass


async def create_profile_for_user(session, user_id, profile_data):
    profile = create_profile_instance(profile_data)
    session.add(profile)
    user = await session.execute(select(User).where(User.id == user_id))
    user.first()[0].profile = profile
    await session.commit()


async def update_user(session, user_data):
    if user_data.get("id", False):  # FIXME: What will if "id": 0
        data = user_data.copy()  # clear function, we can`t change params
        id, data_for_update = data.pop("id"), data
        await session.execute(update(User).where(User.id == id).values(**data))
        await session.commit()


async def delete_user(session, user_data):
    if user_data.get("id", False):
        await session.execute(delete(User).where(User.id == user_data["id"]))
        await session.commit()
