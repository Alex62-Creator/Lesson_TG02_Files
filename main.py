import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
# Файл config с ключами необходимо создавать дополнительно
from config import TOKEN

# Создаем объекты классов Bot (отвечает за взаимодействие с Telegram bot API) и Dispatcher (управляет обработкой входящих сообщений и команд)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот!\nКоманды моего управления можно посмотреть в меню")

# Обработка команды /help
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start - приветствие\n/help - список команд\n/voice текст - озвучивает введенный текст")

# Обработка команды /voice с аргументом В качестве аргумента передается текст, для озвучки
@dp.message(Command('voice'))
async def voice(message: Message):
    # Выделяем текст
    user_text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if user_text:
        # Создаем объект класса GoogleTTS Передаем ему текст для озвучки и язык
        tts = gTTS(text=user_text, lang='ru')
        # Сохраняем полученный объект в файл
        tts.save("text.ogg")
        # Создаем объект класса FSInputFile Передаем ему сохраненный файл
        audio = FSInputFile("text.ogg")
        # Отправляем в наш бот audio
        await bot.send_voice(chat_id=message.chat.id, voice=audio)
        # Удаляем файл text.ogg
        os.remove("text.ogg")
    else:
        await message.answer("Пожалуйста, укажите текст после команды /voice")

# Сохранение фото в папке img
@dp.message(F.photo)
async def download_photo(message: Message):
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer("Фото загружено")

# Перевод любого введенного сообщения с русского на английский
@dp.message()
async def translate(message: Message):
    # Получаем введенный текст
    user_text = message.text
    # Прописываем переменную, куда будет сохраняться переведенный текст
    text_translate = translate_to_en(user_text)
    # Выводим перевод
    await message.answer(f"Перевод на английский:\n{text_translate}")

# Создаём функцию, которая будет переводить на английский
def translate_to_en(text):
    # Создаём объект GoogleTranslator
    translator = GoogleTranslator(source='ru', target='en')
    # Переводим
    result = translator.translate(text)
    # Возвращаем результат перевода
    return result

# Создаем асинхронную функцию main, которая будет запускать наш бот
async def main():
    await dp.start_polling(bot)

# Запускаем асинхронную функцию main
if __name__ == "__main__":
    asyncio.run(main())