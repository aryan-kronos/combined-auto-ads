# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio

from database.repository.user_repo import UserRepository
from database.repository.account_repo import AccountRepository
from database.repository.bio_rotation_repo import (
    BioRotationRepository
)

from services.sessions.session_checker import (
    check_session
)

from services.bio.default_bio import (
    apply_default_bio
)


async def default_bio_worker():

    print("🚀 Default Bio Worker Started")

    while True:

        try:

            users = await UserRepository.get_all()

            for user in users:

                # Premium users never receive default bio
                if user.is_premium:
                    continue

                accounts = await AccountRepository.get_accounts(
                    user.id
                )

                for account in accounts:

                    # Skip dead sessions
                    alive = await check_session(
                        account.session_string
                    )

                    if not alive:
                        continue

                    # Skip accounts using Auto Bio Rotation
                    rotation = await BioRotationRepository.get(
                        account.id
                    )

                    if rotation and rotation.enabled:
                        continue

                    # Apply default bio
                    await apply_default_bio(
                        account.session_string
                    )

        except Exception as e:

            print(
                "DEFAULT BIO WORKER:",
                e
            )

        # 15 minutes
        await asyncio.sleep(900)