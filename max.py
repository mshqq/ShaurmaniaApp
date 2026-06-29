import asyncio
import aiohttp

BOT_TOKEN = "f9LHodD0cOLOzXJtHXJTx0EAwgCgG6P2_kF8lbsYq3MsuEwcGaHccCZU164uvJWQclLdJ--f2QravQaffPJS"
BASE_URL = "https://platform-api2.max.ru"


async def send_newsletter(user_id: int, name: str):
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
