from random import randint

from faker import Faker
from sqlalchemy import text


# TODO: configure them in class
def insert_user_query():
    return text("""
        insert into users (username, img, status, followed, country, city) 
        values (:username, :img, :status, :followed, :country, :city)
    """)


def select_users_query():
    return text("select * from users limit (:count_users) offset (:start_from)")


def users_count():
    return text("select count(*) as total_users from users")


def update_user_query(data_keys):
    updated_fields = ""
    count_keys = len(data_keys)
    for i, key in enumerate(data_keys):
        updated_fields += f"{key}=(:{key})"
        if i < count_keys-1:
            updated_fields += ", "
    return text(f"""
        update users
        set {updated_fields}
        where id=(:id)
    """)


def delete_user_query():
    return text(f"delete from users where id=(:id)")


async def add_default_users(db):
    fake = Faker()
    avatars = [
        "Smokey", "Annie", "Tigger",
        "Bella", "Midnight", "Cookie",
        "Luna", "Sheba", "Oreo",
        "Peanut", "Oliver", "Molly"
    ]
    async with db.begin() as conn:
        await conn.execute(text("""
            create table if not exists users 
            (
            id serial primary key,
            username varchar,
            img varchar,
            status varchar,
            followed bool,
            country varchar,
            city varchar
            )
        """))
        total_count_cursor = await conn.execute(users_count())
        total_count = total_count_cursor.first()._asdict()
        
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
                await conn.execute(insert_user_query(), user_data)
        await conn.commit()
    await db.dispose()


async def select_users(db, page=1, count=10):
    async with db.begin() as conn:
        record_start_from = (page-1) * count
        users_cursor = await conn.execute(select_users_query(), {"count_users": count, "start_from": record_start_from})
        total_count_cursor = await conn.execute(users_count())
        users = users_cursor.mappings().all()
        total_count = total_count_cursor.mappings().first()
    await db.dispose()
    return users, total_count


async def create_new_user(db, user_data):
    async with db.begin() as conn:
        await conn.execute(insert_user_query(), user_data)
    await db.dispose()


async def update_user(db, user_data):
    async with db.begin() as conn:
        await conn.execute(update_user_query(user_data.keys()), user_data)
    await db.dispose()


async def delete_user(db, user_data):
    async with db.begin() as conn:
        await conn.execute(delete_user_query(), user_data)
    await db.dispose()
