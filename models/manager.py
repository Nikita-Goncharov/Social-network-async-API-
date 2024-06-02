import hashlib

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.main_models import Post, User, Profile, FollowProfile, Dialog, Message


class Manager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model, data):
        instance = model(**data)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, model, data):
        instance_id = int(data.pop("id"))
        await self.session.execute(update(model).where(model.id == instance_id).values(data))
        await self.session.commit()

    async def delete(self, model, instance_id):
        await self.session.execute(delete(model).where(id=instance_id))
        await self.session.commit()

    async def filter(self, model, **kwargs):
        cursor = await self.session.execute(select(model).where(**kwargs))
        return cursor.all()

    async def get_by_id(self, model, instance_id):
        return await self.session.get(model, instance_id)

    async def pagination_getting(self, model, page=1, count=10):
        record_start_from = (page - 1) * count

        cursor = await self.session.execute(select(model).limit(count).offset(record_start_from))

        count_records = select(func.count("*").label("total")).select_from(model)
        total_count_cursor = await self.session.execute(count_records)
        instances = cursor.all()
        total_count = total_count_cursor.mappings().first()
        return instances, dict(total_count)["total"]

    async def all(self, model):
        cursor = await self.session.execute(select(model))
        return cursor.all()

    async def count(self, model):
        cursor = await self.session.execute(select(func.count("*").label("total")).select_from(model))
        return cursor.first().total


class PostManager(Manager):
    async def pagination_getting_posts_from_profile(self, profile_id, page=1, count=10):
        record_start_from = (page - 1) * count

        cursor = await self.session.execute(select(Post).where(Post.profile == profile_id).limit(count).offset(record_start_from))

        count_records = select(func.count("*").label("total")).select_from(Post).where(Post.profile == profile_id)
        total_count_cursor = await self.session.execute(count_records)
        instances = cursor.all()
        total_count = total_count_cursor.mappings().first()
        return instances, dict(total_count)["total"]


class UserManager(Manager):
    async def is_user_exists(self, email, password):
        cursor = await self.session.execute(select(User).where(User.email == email))
        user_tuple = cursor.first()
        if user_tuple is not None:
            user = user_tuple[0]
            if user.password_hash == hashlib.md5(password.encode("utf-8")).hexdigest():
                return True, user
        return False, ()

    async def is_user_exists_by_token(self, token):
        cursor = await self.session.execute(select(User).where(User.token == token))
        user_tuple = cursor.first()
        if user_tuple is not None:
            user = user_tuple[0]
            return True, user
        return False, ()

    async def get_profile_by_token(self, token):
        cursor = await self.session.execute(select(User).where(User.token == token))
        user_tuple = cursor.first()
        if user_tuple is not None:
            user = user_tuple[0]
            return True, user.profile
        return False, ()

    async def is_profile_exists(self, profile_id: int) -> bool:
        cursor = await self.session.execute(select(Profile).where(Profile.id == profile_id))
        profile_tuple = cursor.first()
        if profile_tuple is not None:
            return True
        return False

    async def remove_user_token(self, token):
        await self.session.execute(update(User).where(User.token == token).values(token=""))
        await self.session.commit()


class FollowProfileManager(Manager):
    async def delete_following(self, follower_id: int, profile_id: int) -> None:
        await self.session.execute(delete(FollowProfile).where(
            FollowProfile.follower == follower_id,
            FollowProfile.who_are_followed == profile_id
        ))
        await self.session.commit()

    async def is_following_exists(self, follower_id: int, who_are_followed: int) -> bool:
        cursor = await self.session.execute(select(FollowProfile).where(
            FollowProfile.follower == follower_id, FollowProfile.who_are_followed == who_are_followed
        ))
        following_tuple = cursor.first()
        if following_tuple is not None:
            return True
        return False

    async def get_followed_profile_ids(self, follower_id: int) -> list[int, ...]:
        cursor = await self.session.execute(select(FollowProfile).where(FollowProfile.follower == follower_id))
        followed_profiles = cursor.all()
        profile_ids = []
        for profile in followed_profiles:
            profile = profile[0]
            profile_ids.append(profile.who_are_followed)
        return profile_ids


class DialogManager(Manager):
    async def pagination_getting_dialogs_for_profile(self, profile_id: int, page: int, count: int):  # TODO: hints
        record_start_from = (page - 1) * count

        cursor = await self.session.execute(
            select(Dialog).where(
                (Dialog.first_profile == profile_id) | (Dialog.second_profile == profile_id)
            ).limit(count).offset(record_start_from)
        )

        count_records = select(
            func.count("*").label("total")
        ).select_from(Dialog).where((Dialog.first_profile == profile_id) | (Dialog.second_profile == profile_id))

        total_count_cursor = await self.session.execute(count_records)
        instances = cursor.all()
        total_count = total_count_cursor.mappings().first()
        return instances, dict(total_count)["total"]
