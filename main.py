from telethon.sync import TelegramClient
import asyncio
from datetime import datetime, timedelta, timezone
import openai
import time


client = TelegramClient(phone, api_id, api_hash)

async def main():
    try:
        await client.start()
        print("Client started successfully")

        me = await client.get_me()
        print(f"Logged in as {me.username}")

        dialogs = await client.get_dialogs()
        print(f"Retrieved {len(dialogs)} dialogs")

        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        messages_dict = {}
        messages_dict_ua = {}

        my_groups = ('Англоязычное SEO', 'Николай Кодий: SEO, PBN, ГЕМБЛА, МЫСЛИ', 'Searchengines - новости seo, продвижение сайтов, контекст, маркетинг, digital',
                     'Лайфхаки по SEO | Кирилл Рамирас', 'SEO для роботов', 'DrMax SEO', 'SEO без воды', 'АлаичЪ про SEO, бизнес и …', 'SEO продуктовое')
        my_groups_ua = ('SEO BAZA', 'Python для SEO 🇺🇦', 'SEO inside', 'SEObox', 'Robots.txt 🇺🇦')

        for dialog in dialogs:
            if dialog.name in my_groups or dialog.name in my_groups_ua:
                entity = await client.get_entity(dialog)
                async for message in client.iter_messages(entity):
                    message_date = message.date.replace(tzinfo=timezone.utc)
                    if message_date >= one_day_ago:
                        if hasattr(entity, 'username') and entity.username:
                            message_link = f"https://t.me/{entity.username}/{message.id}"
                        else:
                            message_link = f"https://t.me/c/{entity.id}/{message.id}"
                        messages_dict[message_link] = message.text
                        time.sleep(1)
                    else:
                        break
                    await asyncio.sleep(1)

        await client.disconnect()
        print("Client disconnected successfully")
        print(messages_dict)
        return messages_dict

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
