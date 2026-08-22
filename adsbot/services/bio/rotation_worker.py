# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio
from datetime import datetime

from database.repository.bio_rotation_repo import (
    BioRotationRepository
)
from database.repository.bio_rotation_item_repo import (
    BioRotationItemRepository
)
from database.repository.account_repo import (
    AccountRepository
)
from database.repository.bio_repo import (
    BioRepository
)

from services.bio.set_bio import set_bio


async def rotation_worker():

    while True:

        try:

            rotations = await BioRotationRepository.get_running()

            for rotation in rotations:

                seconds = (
                    datetime.utcnow()
                    - rotation.last_changed
                ).total_seconds()

                if seconds < rotation.interval:
                    continue

                account = await AccountRepository.get_account(
                    rotation.account_id
                )

                if not account:
                    continue

                items = await BioRotationItemRepository.get_bios(
                    rotation.id
                )

                if len(items) < 2:
                    continue

                index = rotation.current_index

                if index >= len(items):
                    index = 0

                item = items[index]

                bio = await BioRepository.get_by_id(
                    item.bio_id
                )

                if not bio:
                    continue

                success = await set_bio(
                    account.session_string,
                    bio.text
                )

                if not success:

                    await AccountRepository.update_status(
                        account.id,
                        False
                    )

                    await BioRotationRepository.disable(
                        account.id
                    )

                    continue

                rotation.current_index = (
                    index + 1
                ) % len(items)

                rotation.last_changed = (
                    datetime.utcnow()
                )

                await BioRotationRepository.save(
                    rotation
                )

        except Exception as e:

            print(
                "BIO WORKER:",
                e
            )

        await asyncio.sleep(10)