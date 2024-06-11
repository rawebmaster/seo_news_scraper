from telethon.sync import TelegramClient
import asyncio
from datetime import datetime, timedelta, timezone


client = TelegramClient(phone, api_id, api_hash)

async def main():
    await client.start()
    me = await client.get_me()
    dialogs = await client.get_dialogs()

    # Создаем datetime с временной зоной UTC
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)

    messages_dict = {}

    my_groups = ('Англоязычное SEO', 'Николай Кодий: SEO, PBN, ГЕМБЛА, МЫСЛИ', 'Searchengines - новости seo, продвижение сайтов, контекст, маркетинг, digital',
                 'Лайфхаки по SEO | Кирилл Рамирас', 'SEO для роботов', 'DrMax SEO', 'SEO без воды', 'АлаичЪ про SEO, бизнес и …', 'SEO продуктовое')
    my_groups_ua = ('SEO BAZA', 'Python для SEO 🇺🇦', 'SEO inside', 'SEObox')

    for dialog in dialogs:
        if dialog.name == 'SEO BAZA':
            entity = await client.get_entity(dialog)
            async for message in client.iter_messages(entity):
                # Приводим дату сообщения к UTC для корректного сравнения
                message_date = message.date.replace(tzinfo=timezone.utc)
                if message_date >= one_day_ago:
                    # Формируем ссылку на сообщение вручную
                    if hasattr(entity, 'username') and entity.username:
                        message_link = f"https://t.me/{entity.username}/{message.id}"
                    else:
                        message_link = f"https://t.me/c/{entity.id}/{message.id}"
                    messages_dict[message_link] = message.text
                else:
                    break  # Если сообщение старше одного дня, выходим из цикла
                await asyncio.sleep(1)
    await client.disconnect()
    return messages_dict

if __name__ == "__main__":
    messages_dict = asyncio.run(main())
    print(messages_dict)
