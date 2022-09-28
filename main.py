import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

token = 'TOKEN'

storage = MemoryStorage()

bot = Bot(token)

dp = Dispatcher(bot, storage=storage)

Nikita = 539057262
Dasha = 1464660098


class RPS(StatesGroup):

    Nikita_Choise = State()
    Dasha_Choise = State()
    winner = State()



@dp.message_handler(commands=['Start'], state=None)
async def Starter(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Камень🤜')
    btn2 = types.KeyboardButton('Ножницы✌')
    btn3 = types.KeyboardButton('Бумага✋')
    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    if message.from_user.id == Nikita:
        await bot.send_message(Dasha, 'Запущена новая игра от Никиты')
    else:
        await bot.send_message(Nikita,'Запущена новая игра от Даши')
    await message.answer('Игра началась Ваш ход:', reply_markup=keyboard)

    if message.from_user.id == Nikita:
        await RPS.Nikita_Choise.set()
    else:
        await RPS.Dasha_Choise.set()

@dp.message_handler(state=RPS.Nikita_Choise)
async def waiter(message: types.Message, state: FSMContext):
    choise = message.text
    await state.update_data(Nikita_Choise=choise)
    await bot.send_message(Nikita, 'Ждем ответа другого игрока')
    await bot.send_message(Dasha, 'Игрок Никита сделал свой')
    await asyncio.sleep(3)
    if await Truer() == True:
        await Winner()

@dp.message_handler(state=RPS.Dasha_Choise)
async def waiter(message: types.Message, state: FSMContext):
    choise = message.text
    await state.update_data(Dasha_Choise=choise)
    await bot.send_message(Dasha, 'Ждем ответа другого игрока')
    await bot.send_message(Nikita, 'Игрок Даша сделал свой ход')
    await asyncio.sleep(3)
    if await Truer() == True:
        await Winner()


async def Truer(NikitaC: FSMContext = dp.current_state(user=Nikita), DashaC: FSMContext = dp.current_state(user=Dasha)):
    try:
        async with NikitaC.proxy() as data:
            Nikita_choise = data['Nikita_Choise']
        async with DashaC.proxy() as data:
            Dasha_Choise = data['Dasha_Choise']
        return True
    except:
        return False



async def Winner(NikitaC: FSMContext = dp.current_state(user=Nikita), DashaC: FSMContext = dp.current_state(user=Dasha)):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/start')

    async with NikitaC.proxy() as data:
        Nikita_choise = data['Nikita_Choise']
    async with DashaC.proxy() as data:
        Dasha_Choise = data['Dasha_Choise']

    if Nikita_choise == Dasha_Choise:
        msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n НИЧЬЯ'
        await bot.send_message(Nikita, msg, reply_markup=markup)
        await bot.send_message(Dasha, msg, reply_markup=markup)
    elif Nikita_choise == 'Камень🤜':
        if Dasha_Choise == 'Ножницы✌':
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Никита победил!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
        else:
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Даша победила!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
    elif Nikita_choise == 'Бумага✋':
        if Dasha_Choise == 'Камень🤜':
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Никита победил!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
        else:
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Даша победила!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
    elif Nikita_choise == 'Бумага✋':
        if Dasha_Choise == 'Ножницы✌':
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Даша победила!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
        else:
            msg = 'Ход Даши: ' + Dasha_Choise + '\nХод Никиты: ' + Nikita_choise + '\n Никита победил!'
            await bot.send_message(Nikita, msg, reply_markup=markup)
            await bot.send_message(Dasha, msg, reply_markup=markup)
    else:
        await bot.send_message(Nikita, 'Произошла ошибка, Никита уже разбирается!', reply_markup=markup)
        await bot.send_message(Dasha, 'Произошла ошибка, Никита уже разбирается!', reply_markup=markup)

    await NikitaC.finish()
    await DashaC.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)