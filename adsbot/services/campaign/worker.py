# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio

from pyrogram import Client

from database.repository.campaign_repo import CampaignRepository
from database.repository.account_repo import AccountRepository

from config import config



async def run_campaign(campaign_id):

    campaign = await CampaignRepository.get_campaign(
        campaign_id
    )

    if not campaign:
        return


    account = await AccountRepository.get_account(
        campaign.account_id
    )


    if not account:
        return


    app = Client(
        f"campaign_{campaign_id}",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=account.session_string,
        in_memory=True
    )


    try:

        await app.start()


        while True:

            campaign = await CampaignRepository.get_campaign(
                campaign_id
            )


            if not campaign:
                break


            if not campaign.running:
                break



            sent = 0


            async for dialog in app.get_dialogs():

                if dialog.chat.type in [
                    "group",
                    "supergroup"
                ]:

                    try:

                        await app.send_message(
                            dialog.chat.id,
                            campaign.post_data
                        )

                        sent += 1

                        campaign.total_sent += 1


                    except Exception:
                        pass



            await CampaignRepository.save(
                campaign
            )


            await asyncio.sleep(
                campaign.send_delay
            )


    except Exception as e:

        print(
            "Campaign Error:",
            e
        )


    finally:

        await app.stop()