from random import randint

from faker import Faker
from sqlalchemy import text


insert_user_query = text(
    """insert into users (username, img, status, followed, country, city) 
    values (:username, :img, :status, :followed, :country, :city)"""
)

select_all_users_query = text("select * from users")

update_user = text("update users set username= , img= , ")
delete_user = text("delete from users where id=")


async def add_default_users(db):
    fake = Faker()
    avatars = [
        "Smokey", "Annie", "Tigger",
        "Bella", "Midnight", "Cookie",
        "Luna", "Sheba", "Oreo",
        "Peanut", "Oliver", "Molly"]
    async with db.begin() as conn:
        await conn.execute(text(
            """
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
            """
        ))
        cursor = await conn.execute(select_all_users_query)
        if not len(cursor.all()):
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
                await conn.execute(insert_user_query, user_data)
        await conn.commit()
    await db.dispose()


async def select_all_users(db):
    async with db.begin() as conn:
        cursor = await conn.execute(select_all_users_query)
    await db.dispose()
    return cursor.all()  # TODO: if users a lot then do pagination


async def create_new_user(db, user_data):
    async with db.begin() as conn:
        await conn.execute(insert_user_query, user_data)
    await db.dispose()


async def update_user(db, user_data):
    pass


async def delete_user(db, id):
    pass
