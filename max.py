import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("MAX_TOKEN")
BASE_URL = "https://platform-api2.max.ru"


async def send_newsletter(user_id: int, name: str):
    if not BOT_TOKEN:
        raise RuntimeError("MAX_BOT_TOKEN is not set")
    headers = {
        "Authorization": BOT_TOKEN,  # без Bearer, просто токен
        "Content-Type": "application/json",
    }

    payload = {
        "text": f"Привет, <b>{name}</b>! 🌯\n\nДобро пожаловать в рассылку <b>Шаурмании</b>!\n\n🎁 Скидка 10% на первый заказ: <code>ШАУРМАНИЯ10</code>",
        "format": "html",
        "attachments": [
            {
                "type": "inline_keyboard",
                "payload": {
                    "buttons": [
                        [
                            {
                                "type": "link",
                                "text": "🌐 Наш сайт",
                                "url": "https://shaurmania.ru",
                            }
                        ]
                    ]
                },
            }
        ],
    }

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(
            f"{BASE_URL}/messages",
            params={"user_id": user_id},  # user_id передаётся как query-параметр
            json=payload,
            headers=headers,
        ) as response:
            result = await response.json()
            print(result)


asyncio.run(send_newsletter(user_id=125309132, name="Александр"))
