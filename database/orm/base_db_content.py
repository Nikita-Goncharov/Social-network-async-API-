from random import randint
from datetime import date

from faker import Faker
from werkzeug.security import check_password_hash, generate_password_hash

from models.main_models import User, Profile
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
                "followed": fake.pybool(),
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
                "password_hash": generate_password_hash(fake.password(length=10)),  # cpu bound operation # TODO: 5 seconds!
                "profile": profile,
            }
            user = await manager.create(User, user_data)

