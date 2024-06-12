from telethon.sync import TelegramClient
import asyncio
from datetime import datetime, timedelta, timezone
import openai
import time
from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, Message
from aiogram.filters import Command
from dataclasses import dataclass
import re

# Инициализация телеграм-бота
@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту

@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    return Config(tg_bot=TgBot(token=''))

config = load_config()
bot = Bot(token=config.tg_bot.token)

# Initialize module-level router
router = Router()



client = TelegramClient(phone, api_id, api_hash)

messages_dict = {}

def escape_html(text: str) -> str:
    escape_chars = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    text = re.sub(r'([&<>"\'])', lambda match: escape_chars[match.group(0)], text)
    # Заменяем двойные звёздочки на теги <b> и </b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    return text

async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(router)

    # Этот хэндлер будет срабатывать на команду /start
    @router.message(Command(commands=["start"]))
    async def process_start_command(message: Message):
        await message.answer(
            text='Этот бот будет ежедневно присылать вам новости из SEO телеграм-каналов'
        )

    # Этот хэндлер будет срабатывать на команду /getnews
    @router.message(Command(commands=["getnews"]))
    async def process_getnews_command(message: Message):
        if not messages_dict:
            await message.answer("Нет новостей за последний день.")
            return

        news_text = ""
        for url, text in messages_dict.items():
            news_text += f'<b>Ссылка:</b> <a href="{escape_html(url)}">{escape_html(url)}</a>\n\n{escape_html(text)}\n\n🤖'

        # Ограничение длины сообщения в Telegram составляет 4096 символов.
        # Если текст превышает это количество, его нужно разбить на части.
        MAX_MESSAGE_LENGTH = 4096
        for chunk in [news_text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(news_text), MAX_MESSAGE_LENGTH)]:
            await message.answer(chunk, parse_mode="HTML")

    try:
        await client.start()
        print("Client started successfully")

        me = await client.get_me()
        print(f"Logged in as {me.username}")

        dialogs = await client.get_dialogs()
        print(f"Retrieved {len(dialogs)} dialogs")

        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)

        global messages_dict

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

    except Exception as e:
        print(f"An error occurred: {e}")

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
