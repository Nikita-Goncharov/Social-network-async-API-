from datetime import date, datetime

from sqlalchemy import select, update

from models.main_models import Profile


def create_profile_instance(profile_data):
    # education, web_site, birth_date
    birth_date = profile_data.get("birth_date", date.today())
    if type(birth_date) == str:
        profile_data["birth_date"] = datetime.strptime(birth_date, "%Y-%m-%d").date()

    profile = Profile(**profile_data)
    return profile


async def get_profile(session, profile_id):
    profile = await session.execute(select(Profile).where(Profile.id == profile_id))
    return profile.first()


async def update_profile(session, updated_profile):
    id = updated_profile.pop("profile_id")
    await session.execute(update(Profile).where(Profile.id == id).values(updated_profile))
    await session.commit()
