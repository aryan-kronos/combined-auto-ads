# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from database.repository.account_repo import AccountRepository
from database.repository.campaign_repo import CampaignRepository
from database.repository.bio_repo import BioRepository
from database.repository.bio_rotation_repo import BioRotationRepository


class DashboardRepository:

    @staticmethod
    async def get(user):

        accounts = await AccountRepository.get_accounts(
            user.id
        )

        active_accounts = 0
        expired_accounts = 0
        running_rotations = 0

        for account in accounts:

            if account.active:
                active_accounts += 1
            else:
                expired_accounts += 1

            rotation = await BioRotationRepository.get(
                account.id
            )

            if rotation and rotation.enabled:
                running_rotations += 1

        campaigns = await CampaignRepository.get_user_campaigns(
    user.id
)

        total_campaigns = len(campaigns)

        running_campaigns = 0
        stopped_campaigns = 0
        completed_campaigns = 0

        total_sent = 0
        failed_sent = 0

        for campaign in campaigns:

            total_sent += campaign.total_sent
            failed_sent += campaign.failed_sent

            if campaign.completed:
                completed_campaigns += 1

            elif campaign.running:
                running_campaigns += 1

            else:
                stopped_campaigns += 1

        bios = await BioRepository.get_bios(
            user.id
        )

        return {

            "active_accounts": active_accounts,
            "expired_accounts": expired_accounts,
            "total_accounts": len(accounts),
            "account_limit": (
                10 if user.is_premium else 1
            ),

            "saved_bios": len(bios),
            "rotation_enabled": running_rotations,

            "total_campaigns": total_campaigns,
            "running_campaigns": running_campaigns,
            "stopped_campaigns": stopped_campaigns,
            "completed_campaigns": completed_campaigns,

            "total_sent": total_sent,
            "failed_sent": failed_sent,

            "premium": user.is_premium
        }