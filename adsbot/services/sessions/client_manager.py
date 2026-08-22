# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from pyrogram import Client
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
)

from config import config


class ClientManager:

    def __init__(self):
        self.clients = {}
        self.phone_codes = {}


    async def create_client(self, user_id: int):


        print("=" * 50)
        print(f"API_ID: {config.API_ID}")
        print(f"API_HASH: {config.API_HASH}")
        print("=" * 50)


        client = Client(
            name=f"temp_{user_id}",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            in_memory=True,
        )

        await client.connect()

        self.clients[user_id] = client

        return client


    async def send_code(self, user_id: int, phone: str):

        client = await self.create_client(user_id)

        sent_code = await client.send_code(phone)

        self.phone_codes[user_id] = sent_code.phone_code_hash

        return sent_code


    async def verify_code(
        self,
        user_id: int,
        phone: str,
        code: str
    ):

        client = self.clients[user_id]

        try:

            await client.sign_in(
                phone_number=phone,
                phone_code_hash=self.phone_codes[user_id],
                phone_code=code
            )

            return await self.success(client)


        except SessionPasswordNeeded:

            return {
                "status": "password_required"
            }


        except (
            PhoneCodeInvalid,
            PhoneCodeExpired
        ):

            return {
                "status": "wrong_code"
            }



    async def verify_password(
        self,
        user_id: int,
        password: str
    ):

        client = self.clients[user_id]

        await client.check_password(password)

        return await self.success(client)



    async def success(self, client):

        session = await client.export_session_string()

        me = await client.get_me()

        return {
            "status": "success",
            "session": session,
            "user": me
        }



    async def remove(self,user_id:int):

        client = self.clients.get(user_id)

        if client:

            await client.disconnect()

            del self.clients[user_id]


client_manager = ClientManager()