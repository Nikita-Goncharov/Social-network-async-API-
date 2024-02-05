from random import randint

from sqlalchemy import select, func, insert, delete, update
from faker import Faker

from models.main_models import User, Profile
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
    # print(query)
    total_count_cursor = await session.execute(count_users_query)
    total_count = total_count_cursor.first()._asdict()
    # print(total_count)

    if total_count["total_users"] == 0:
        for i in range(40):
            avatar_name = avatars[randint(0, 11)]
            user_data = {
                "username": fake.name(),
                "img": f"https://api.dicebear.com/7.x/adventurer/svg?seed={avatar_name}",
                "status": fake.sentence(nb_words=10),
                "followed": fake.pybool(),
                "country": fake.country(),
                "city": fake.city(),
            }
            create_user_query = insert(User).values(**user_data)
            # print(query)
            await session.execute(create_user_query)
            await session.commit()


async def select_users(session, page=1, count=10):
    record_start_from = (page - 1) * count

    # , {"count_users": count, "start_from": record_start_from}
    users_cursor = await session.execute(select(User).limit(count).offset(record_start_from))
    count_users_query = select(func.count("*").label("total_users")).select_from(User)
    total_count_cursor = await session.execute(count_users_query)
    users = users_cursor.all()  # .mappings().
    total_count = total_count_cursor.mappings().first()
    return users, total_count


async def create_new_user(session, user_data):
    await session.execute(insert(User).values(**user_data))
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
