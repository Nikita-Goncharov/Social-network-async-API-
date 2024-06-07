import sys
import asyncio
import hashlib
from datetime import date
from random import randint

from faker import Faker

sys.path.append("../")  # TODO: refactor, without it can`t import models/manager from models module

from models.manager import Manager
from models.main_models import User, Profile, Post, Dialog, Message, FollowProfile, Base
from database.base_orm import database_engine, async_session_factory

fake = Faker()


async def create_profile_posts(manager, profile_id):
    random_post_count = randint(0, 4)
    for _ in range(random_post_count):
        post_data = {
            "title": " ".join(fake.text().split()[:2]),
            "description": fake.text(),
            "profile": profile_id
        }
        await manager.create(Post, post_data)


async def create_dialog_messages(session, dialog_id, first_profile_id, second_profile_id):
    messages_count = randint(0, 50)
    for message_id in range(messages_count):
        manager = Manager(session)
        message_data = {
            "text": fake.sentence(nb_words=10),
            "owner": first_profile_id if randint(0, 1) else second_profile_id,
            "dialog": dialog_id
        }
        await manager.create(Message, message_data)


async def create_profiles_dialogs(session):
    manager = Manager(session)

    profiles_count = await manager.count(Profile)
    profiles = await manager.all(Profile)

    for profile in profiles:
        profile = profile[0]
        second_profile_id = profile.id

        while second_profile_id == profile.id:
            random_profile = profiles[randint(0, profiles_count-1)]
            second_profile_id = random_profile[0].id

        dialog_data = {
            "first_profile": profile.id,
            "second_profile": second_profile_id
        }
        dialog = await manager.create(Dialog, dialog_data)
        await create_dialog_messages(session, dialog.id, profile.id, second_profile_id)


async def create_profiles_following(session):
    manager = Manager(session)

    profiles_count = await manager.count(Profile)
    profiles = await manager.all(Profile)

    for profile in profiles:
        profile = profile[0]
        followings_count = randint(0, profiles_count-1)

        for _ in range(followings_count):
            second_profile_id = profile.id

            while second_profile_id == profile.id:
                second_profile_id = profiles[randint(0, profiles_count-1)][0].id

            data = {
                "follower": profile.id,
                "who_are_followed": second_profile_id
            }
            await manager.create(FollowProfile, data)


async def create_users_profiles(session):
    manager = Manager(session)
    avatars = [
        "Smokey", "Annie", "Tigger",
        "Bella", "Midnight", "Cookie",
        "Luna", "Sheba", "Oreo",
        "Peanut", "Oliver", "Molly"
    ]

    total_count = await manager.count(User)
    # Create 40 users/profiles if not exists
    if total_count == 0:  # TODO: remove ?
        for i in range(40):
            avatar_name = avatars[randint(0, 11)]
            profile_data = {
                "img": f"https://api.dicebear.com/7.x/adventurer/svg?seed={avatar_name}",
                "status": fake.sentence(nb_words=10),
                "country": fake.country(),
                "city": fake.city(),
                "education": "High school",
                "web_site": "Site link",
                "birth_date": date.today()
            }

            profile = await manager.create(Profile, profile_data)
            user_data = {
                "username": fake.name(),
                "email": fake.email(),
                "password_hash": hashlib.md5(fake.password(length=10).encode("utf-8")).hexdigest(),  # cpu bound operation # TODO: 3 seconds do smaller!
                "profile": profile
            }
            user = await manager.create(User, user_data)
            # Create posts for profile
            await create_profile_posts(manager, profile.id)


async def create_default_data(session):
    await create_users_profiles(session)
    await create_profiles_dialogs(session)
    await create_profiles_following(session)


async def fill_db():  # TODO: show start time, end time and 
    async with database_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)  # because we should wait until tables will create
    async with async_session_factory() as session:
        task = asyncio.create_task(create_default_data(session))
        await task
    await database_engine.dispose()


if __name__ == "__main__":
    asyncio.run(fill_db())
