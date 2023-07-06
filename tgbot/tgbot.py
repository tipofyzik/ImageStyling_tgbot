from tgbot.MSGNet import *

from aiogram import Bot, Dispatcher, executor, types
import os



# Создаём экземпляр модели.
# Делаем то же самое, что и в ноутбуке во время тестов
model = Net(ngf=128)
model_dict = torch.load('tgbot/21styles.model')
model_dict_clone = model_dict.copy()
for key, value in model_dict_clone.items():
    if key.endswith(('running_mean', 'running_var')):
        del model_dict[key]
model.load_state_dict(model_dict, False)

# Теперь необходимо реализовать функцию преобразования изображения
# Делаем то же самое, что и в ноутбуке во время тестов
def transform_image(original_image, style_image, image_size):
   content_image = tensor_load_rgbimage(original_image, size=image_size,keep_asp=True).unsqueeze(0)
   style = tensor_load_rgbimage(style_image, size=image_size).unsqueeze(0)
   style = preprocess_batch(style)
   style_v = Variable(style)
   content_image = Variable(preprocess_batch(content_image))
   model.setTarget(style_v)
   output = model(content_image)
   tensor_save_bgrimage(output.data[0], 'result.jpg', False)



# Инициализация бота
# Укажите свой API TOKEN
TG_BOT_TOKEN='6043479943:AAEX0HYLP0sAAx6llQ4jJbt7sQ-9QBLc1KU'
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot)

global original, style
global x, y
x=y=original=style=None


def firstkeyboard():
   button=[
      [types.KeyboardButton(text="/help"),
      types.KeyboardButton(text="/transfer_style"),
      types.KeyboardButton(text="/restart")]
   ]
   keyboard = types.ReplyKeyboardMarkup(
      keyboard=button, 
      resize_keyboard=True)
   return keyboard

def keyboard():
   buttons=[
      [types.KeyboardButton(text="/original_image"),
      types.KeyboardButton(text="/style_image"),
      types.KeyboardButton(text="/restart")]
   ]
   if x is not None and y is not None:
      buttons[0].insert(-1, types.KeyboardButton(text="/result"))

   keyboard = types.ReplyKeyboardMarkup(
      keyboard=buttons, 
      resize_keyboard=True)
   return keyboard



@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем. 
async def send_welcome(message: types.Message):
   global original, style
   global x, y
   x=y=original=style=None
   await message.answer("""Привет! 
Я бот, который поможет тебе перенести стиль одного изображения на другое.\n
Дабы узнать функционал, воспользуйся командой /help.
Дабы перейти к загрузке фото, воспользуйся командой /transfer_style.
""", reply_markup=firstkeyboard()) #Так как код работает асинхронно, то обязательно пишем await.

@dp.message_handler(commands=['help'])
async def get_images(message: types.Message):
   text=f"""/transfer\_style - позволяет перейти к загрузке фотографий.
/original\_image - позволяет загрузить фото, _на которое_ будет переноситься стиль.
/style\_image - позволяет загрузить, _c которого_ будет браться стиль.
/result - в случае загруки обоих изображений позволяет увидеть результат.
/restart - если хотите вернуться в исходное меню. Команда доступна всегда.

/tests - тут показаны результаты тестов разработчика. Нажми или введи /test, чтобы узнать больше. Команда никак не влияет на работу бота.

Приятного времяпровождения!"""
   await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['transfer_style'])
async def get_images(message: types.Message):
   await message.answer("""Можешь приступить к загрузке фотографий.  Не забудь указать тип загружаемой фотографии - original или style! 
Для этого нажми на соответствующую кнопку или введи команду вручную.""", reply_markup=keyboard())

@dp.message_handler(commands=['original_image'])
async def get_original_images(message):
   global original, style
   await message.answer("Загрузи фотографию, _на которую_ ты хочешь перенести стиль", 
                        parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard())
   original=True
   style=False

@dp.message_handler(commands=['style_image'])
async def get_style_images(message):
   global style, original
   await message.answer("Загрузи фотографию, _с которой_ ты хочешь перенести стиль", 
                        parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard())
   style=True
   original=False

@dp.message_handler(content_types=['photo'])
async def save_image(message):
   global original, style
   global x, y
   if original is None and style is None:
      await message.answer("""Не был указан тип фотографии!
Пожалуйста, выберите тип фотографии, введя соответствующую команду, и затем загрузите фото заново.""")
   elif original:
      await message.photo[-1].download(destination_file='original_image.jpg')
      await message.answer("Оригинал получен!")
      x=True
      if x and y:
         await message.answer("Ура, все фотографии есть!", reply_markup=keyboard())
   elif style:
      await message.photo[-1].download(destination_file='style_image.jpg')
      await message.answer("Стиль получен!")
      y=True
      if x and y:
         await message.answer("Ура, все фотографии есть! Можно посмотреть на результат", reply_markup=keyboard())

# Функция по обработке изображений и получения результата
@dp.message_handler(commands=['result'])
async def result(message: types.Message):
   global x, y
   # Если хочется изменить размер изображения при обработке - поменяйте цифру в строке ниже
   image_size=512

   if x is None and y is None:
      await message.answer("Не было получено ни одного фото! Воспользуйся /transfer_style, чтобы перейти к загрузке.")
   elif x is None:
      await message.answer("Оригинал не был получен! Чтобы загрузить его, воспользуйся /original_image.")
   elif y is None:
      await message.answer("Стиль не был получен! Чтобы загрузить его, воспользуйся /style_image.")
   else:
      await message.answer("Подождите, идёт обработка изображения...")
      transform_image('original_image.jpg', 'style_image.jpg', image_size=image_size)
      await bot.send_photo(chat_id=message.chat.id, photo=open('result.jpg', 'rb'), 
                           caption='Ваша изменённая фотография!', reply_markup=keyboard())

# Функция возврата в меню start
@dp.message_handler(commands=['restart'])
async def cancel_act(message: types.Message):
   if os.path.exists('original_image.jpg'):   
      os.remove('original_image.jpg')
   if os.path.exists('style_image.jpg'):      
      os.remove('style_image.jpg')
   if os.path.exists('result.jpg'):   
      os.remove('result.jpg')
   await message.answer("Загруженные изображения, если они были, удалены! Начнём заново.")
   await send_welcome(message)



@dp.message_handler(commands=['tests'])
async def show_tests(message: types.Message):
   await message.answer("""
Эта функция показывает тесты. Тут 5 картинок, каждая является результатом двух фотографий ниже.
Первая - черепаха - на неё переносился стиль второй фотографии - заката.""", reply_markup=firstkeyboard())
   media_group = types.MediaGroup() 
   media_group.attach_photo(types.InputFile('tgbot/tests/turtle.jpeg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/real_sunset.jpg'))
   await bot.send_media_group(chat_id=message.chat.id, media=media_group)

   await message.answer("""
Вот результаты переноса при разных image_size: 512 -> 768 -> 1024 -> 1536 -> 2048 от первого до последнего фото, соответственно.
Можно легко заметить изменения даже в сжатых файлах, если просто полистать фотографии""", reply_markup=firstkeyboard())
   media_group = types.MediaGroup() 
   media_group.attach_photo(types.InputFile('tgbot/tests/512.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/768.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/1024.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/1536.jpg'))
   media_group.attach_photo(types.InputFile('tgbot/tests/2048.jpg'))
   await bot.send_media_group(chat_id=message.chat.id, media=media_group)

   await message.answer("""
image_size=2048 заставил мой компьютер чутка поглючить, а с image_size=4096 вообще не справился.
Для оптимизации времени обработки image_size был выставлен равным 512 - изображения обрабатываются шустро, да и результат не заставляет себя ждать.
Однако если хочется повысить качество переноса - рекомендую выставить размер равный 1024 или 1536. 
Дальнейшее увеличение размера действительно улучшает качество, но несущественно. 

Изменить размер можно в функции result - под это выделена переменная.""", reply_markup=firstkeyboard())



@dp.message_handler()
async def echo(message: types.Message):
   await message.reply("""Извини, но я не понимаю этой команды! 
Воспользуйся командой /help для ознакомления с моим функционалом.""")
   
