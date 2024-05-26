import hashlib

from random import randint
from datetime import date

from faker import Faker

from models.main_models import User, Profile, Post
from models.manager import Manager


async def fill_db_with_default_data(session):
    fake = Faker()
    manager = Manager(session)
    avatars = [
        "Smokey", "Annie", "Tigger",
        "Bella", "Midnight", "Cookie",
        "Luna", "Sheba", "Oreo",
        "Peanut", "Oliver", "Molly"
    ]

    total_count = await manager.count(User)
    if total_count == 0:
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
                "password_hash": hashlib.md5(fake.password(length=10).encode("utf-8")).hexdigest(),  # cpu bound operation # TODO: 3 seconds!
                "profile": profile,
            }
            user = await manager.create(User, user_data)
            # Create posts for profile
            random_post_count = randint(0, 4)
            for _ in range(random_post_count):
                post_data = {
                    "title": " ".join(fake.text().split()[:2]),
                    "description": fake.text(),
                    "profile": profile.id
                }
                post = await manager.create(Post, post_data)
