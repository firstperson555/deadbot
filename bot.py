import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin user_id
ADMIN_ID = int(os.getenv("ADMIN_ID", "7846160465"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM States
class OrderStates(StatesGroup):
    waiting_for_package_type = State()
    waiting_for_country = State()
    waiting_for_quantity = State()
    waiting_for_payment = State()

class AdminStates(StatesGroup):
    waiting_for_response = State()

# Countries with flags
COUNTRIES = {
    "RU": {"name": "Россия", "flag": "🇷🇺"},
    "UA": {"name": "Украина", "flag": "🇺🇦"},
    "US": {"name": "США", "flag": "🇺🇸"},
    "BE": {"name": "Бельгия", "flag": "🇧🇪"},
    "NL": {"name": "Нидерланды", "flag": "🇳🇱"},
    "SE": {"name": "Швеция", "flag": "🇸🇪"},
    "DE": {"name": "Германия", "flag": "🇩🇪"},
    "PL": {"name": "Польша", "flag": "🇵🇱"},
    "FR": {"name": "Франция", "flag": "🇫🇷"},
    "KZ": {"name": "Казахстан", "flag": "🇰🇿"}
}

# Pricing
PRICE_PER_NUMBER = 25
PACK_PRICE = 100  # 6 numbers
PACK_SIZE = 6

# Orders storage (in-memory for demo)
orders = {}
order_counter = 0

# Keyboards
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🛒 Купить номера", callback_data="make_order"))
    builder.add(InlineKeyboardButton(text="ℹ️ Как это работает", callback_data="how_it_works"))
    builder.adjust(1)
    return builder.as_markup()

def get_package_type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=f"📦 Пакет 6 номеров — {PACK_PRICE} ⭐️", callback_data="package_pack"))
    builder.add(InlineKeyboardButton(text=f"📱 Одиночный номер — {PRICE_PER_NUMBER} ⭐️", callback_data="package_single"))
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"))
    builder.adjust(1)
    return builder.as_markup()

def get_country_keyboard():
    builder = InlineKeyboardBuilder()
    for code, data in COUNTRIES.items():
        builder.add(InlineKeyboardButton(text=f"{data['flag']} {data['name']}", callback_data=f"country_{code}"))
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"))
    builder.adjust(2)
    return builder.as_markup()

def get_quantity_keyboard(max_qty: int):
    builder = InlineKeyboardBuilder()
    for i in range(1, max_qty + 1):
        builder.add(InlineKeyboardButton(text=f"{i} шт.", callback_data=f"qty_{i}"))
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"))
    builder.adjust(3)
    return builder.as_markup()

def get_payment_keyboard(order_id: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid_{order_id}"))
    builder.add(InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cancel_order"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_keyboard(order_id: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Одобрить заказ", callback_data=f"admin_approve_{order_id}"))
    builder.add(InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{order_id}"))
    builder.add(InlineKeyboardButton(text="💬 Связаться с клиентом", callback_data=f"admin_contact_{order_id}"))
    builder.adjust(1)
    return builder.as_markup()

def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="◀️ В главное меню", callback_data="back_to_main"))
    return builder.as_markup()

# Handlers
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "🚀 <b>DeadBoot — номера на реальных SIM-картах</b>\n\n"
        "Предоставляем номера на реальных SIM-картах для Telegram. "
        "Все номера не регистрировались в Telegram ранее.\n\n"
        "💰 <b>Цены:</b>\n"
        f"📦 Пакет 6 номеров — <b>{PACK_PRICE} ⭐️</b>\n"
        f"📱 Одиночный номер — <b>{PRICE_PER_NUMBER} ⭐️</b>\n\n"
        "🌍 <b>Доступные страны:</b>\n"
    )
    countries_list = "\n".join([f"{data['flag']} {data['name']}" for data in COUNTRIES.values()])
    await message.answer(text + countries_list + "\n\nВыберите действие ниже:", parse_mode="HTML", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "make_order")
async def make_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "📋 <b>Оформление заказа</b>\n\n"
        "Выберите формат покупки:\n\n"
        f"📦 Пакет 6 номеров — <b>{PACK_PRICE} ⭐️</b>\n"
        f"📱 Одиночный номер — <b>{PRICE_PER_NUMBER} ⭐️</b>\n\n"
        "Номера выдаются после проверки оплаты."
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_package_type_keyboard())
    await state.set_state(OrderStates.waiting_for_package_type)
    await callback.answer()

@dp.callback_query(F.data == "how_it_works")
async def how_it_works(callback: CallbackQuery):
    text = (
        "ℹ️ <b>Как это работает</b>\n\n"
        "🔹 <b>Что мы предлагаем:</b>\n"
        "Номера на реальных SIM-картах для регистрации в Telegram. "
        "Номера не регистрировались в Telegram ранее.\n\n"
        "🔹 <b>Процесс заказа:</b>\n"
        "1. Выберите формат (пакет или одиночный номер)\n"
        "2. Укажите страну и количество\n"
        "3. Оплатите через @byesocial\n"
        "4. Получите номера после проверки оплаты\n\n"
        "🔹 <b>Гарантии:</b>\n"
        "Все номера проверяются перед выдачей. "
        "Если номер не работает при получении SMS — замена бесплатно.\n\n"
        "🔹 <b>Конфиденциальность:</b>\n"
        "Данные номеров используются только для вашей регистрации."
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_back_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "🏠 <b>DeadBoot — главное меню</b>\n\n"
        "Выберите действие:"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data.startswith("package_"), OrderStates.waiting_for_package_type)
async def select_package_type(callback: CallbackQuery, state: FSMContext):
    package_type = callback.data.split("_")[1]
    
    if package_type == "pack":
        await state.update_data(package_type="pack", quantity=PACK_SIZE, price=PACK_PRICE)
        text = (
            f"📦 <b>Пакет 6 номеров</b>\n"
            f"💰 Стоимость: <b>{PACK_PRICE} ⭐️</b>\n\n"
            "Выберите страну:"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_country_keyboard())
        await state.set_state(OrderStates.waiting_for_country)
    else:
        await state.update_data(package_type="single", price=PRICE_PER_NUMBER)
        text = (
            f"📱 <b>Одиночный номер</b>\n"
            f"💰 Стоимость: <b>{PRICE_PER_NUMBER} ⭐️</b>\n\n"
            "Выберите страну:"
        )
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_country_keyboard())
        await state.set_state(OrderStates.waiting_for_country)
    
    await callback.answer()

@dp.callback_query(F.data.startswith("country_"), OrderStates.waiting_for_country)
async def select_country(callback: CallbackQuery, state: FSMContext):
    country_code = callback.data.split("_")[1]
    country = COUNTRIES[country_code]
    
    await state.update_data(country_code=country_code, country_name=country["name"])
    
    user_data = await state.get_data()
    
    if user_data["package_type"] == "pack":
        # Pack - go straight to payment
        await create_order(callback, state)
    else:
        # Single number - auto-set to 1 and go to payment
        await state.update_data(quantity=1)
        await create_order(callback, state)
    
    await callback.answer()

@dp.callback_query(F.data.startswith("qty_"), OrderStates.waiting_for_quantity)
async def select_quantity(callback: CallbackQuery, state: FSMContext):
    quantity = int(callback.data.split("_")[1])
    price = quantity * PRICE_PER_NUMBER
    
    await state.update_data(quantity=quantity, price=price)
    
    await create_order(callback, state)
    await callback.answer()

async def create_order(callback: CallbackQuery, state: FSMContext):
    # Generate order ID
    global order_counter
    order_counter += 1
    order_id = f"DB{order_counter:06d}"
    
    user_data = await state.get_data()
    
    # Save order
    orders[order_id] = {
        "order_id": order_id,
        "user_id": callback.from_user.id,
        "username": callback.from_user.username,
        "package_type": user_data["package_type"],
        "country_code": user_data["country_code"],
        "country_name": user_data["country_name"],
        "quantity": user_data.get("quantity", PACK_SIZE),
        "price": user_data["price"],
        "status": "pending_payment",
        "payment_proof": None
    }
    
    await state.update_data(order_id=order_id)
    
    if user_data["package_type"] == "pack":
        order_details = f"📦 Пакет 6 номеров\n🌍 Страна: {user_data['country_name']}"
    else:
        order_details = f"📱 {user_data['quantity']} номер(ов)\n🌍 Страна: {user_data['country_name']}"
    
    text = (
        f"📋 <b>Заказ #{order_id}</b>\n\n"
        f"{order_details}\n"
        f"💰 Стоимость: <b>{user_data['price']} ⭐️</b>\n\n"
        f"💳 <b>Оплата через @byesocial</b>\n\n"
        f"📝 <b>Инструкция:</b>\n"
        f"1. Перейдите к @byesocial\n"
        f"2. Отправьте подарок на {user_data['price']} ⭐️\n"
        f"3. Сделайте скриншот\n"
        f"4. Нажмите кнопку «Я оплатил» ниже\n"
        f"5. Отправьте скриншот с подписью: #{order_id}"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_payment_keyboard(order_id))
    await state.set_state(OrderStates.waiting_for_payment)

@dp.callback_query(F.data.startswith("paid_"), OrderStates.waiting_for_payment)
async def payment_confirmation(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split("_")[1]
    
    text = (
        f"✅ <b>Отлично!</b>\n\n"
        f"Отправьте скриншот оплаты в этот чат.\n\n"
        f"Добавьте подпись к скрину: <code>#{order_id}</code>\n\n"
        f"После проверки выдадим номера."
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()

@dp.message(OrderStates.waiting_for_payment, F.photo)
async def process_payment_proof(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    order_id = user_data["order_id"]
    
    # Get photo file_id
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    
    # Get caption
    caption = message.caption or ""
    
    # Update order
    if order_id in orders:
        orders[order_id]["payment_proof"] = photo_file_id
        orders[order_id]["payment_caption"] = caption
        orders[order_id]["status"] = "awaiting_admin_review"
    
    await state.clear()
    
    text = (
        f"✅ <b>Скриншот получен!</b>\n\n"
        f"Заказ #{order_id} на проверке.\n\n"
        f"⏳ Ожидайте подтверждения (обычно 5–15 минут).\n\n"
        f"Номера выдадим после проверки оплаты."
    )
    await message.answer(text, parse_mode="HTML", reply_markup=get_main_keyboard())
    
    # Send notification to admin
    order = orders[order_id]
    admin_text = (
        f"🔔 <b>Новый заказ #{order_id}</b>\n\n"
        f"👤 Клиент: @{order['username']} (ID: {order['user_id']})\n"
        f"📦 Тип: {'Пакет 6 номеров' if order['package_type'] == 'pack' else f"{order['quantity']} номер(ов)"}\n"
        f"🌍 Страна: {order['country_name']}\n"
        f"💰 Сумма: {order['price']} ⭐\n\n"
        f"📸 Скриншот оплаты получен.\n"
        f"💬 Подпись: {caption}\n\n"
        f"Выберите действие:"
    )
    
    try:
        await bot.send_photo(
            ADMIN_ID,
            photo_file_id,
            caption=admin_text,
            parse_mode="HTML",
            reply_markup=get_admin_keyboard(order_id)
        )
    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML", reply_markup=get_admin_keyboard(order_id))

@dp.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    order_id = user_data.get("order_id")
    
    if order_id and order_id in orders:
        orders[order_id]["status"] = "cancelled"
    
    await state.clear()
    text = (
        "❌ <b>Заказ отменён</b>\n\n"
        "Можно оформить новый заказ."
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())
    await callback.answer()

# Admin handlers
@dp.callback_query(F.data.startswith("admin_approve_"))
async def admin_approve(callback: CallbackQuery):
    order_id = callback.data.split("_")[2]
    
    if order_id in orders:
        orders[order_id]["status"] = "approved"
        
        # Notify user
        user_id = orders[order_id]["user_id"]
        user_text = (
            f"✅ Заказ #{order_id} оплачен\n\n"
            f"В течение 1–5 минут номер(а) будут выданы вам администратором."
        )
        try:
            await bot.send_message(user_id, user_text, parse_mode="HTML", reply_markup=get_main_keyboard())
        except Exception as e:
            logger.error(f"Failed to notify user: {e}")
    
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await bot.send_message(
        callback.message.chat.id,
        f"✅ Заказ #{order_id} оплачен\n\nКлиент уведомлён. Свяжитесь с ним для выдачи номеров."
    )

@dp.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery):
    order_id = callback.data.split("_")[2]
    
    if order_id in orders:
        orders[order_id]["status"] = "rejected"
        
        # Notify user
        user_id = orders[order_id]["user_id"]
        user_text = (
            f"❌ Заказ #{order_id} отклонён\n\n"
            f"Мы не можем принять этот заказ.\n\n"
            f"Причина: ошибка в оплате или недостаточная сумма."
        )
        try:
            await bot.send_message(user_id, user_text, parse_mode="HTML", reply_markup=get_main_keyboard())
        except Exception as e:
            logger.error(f"Failed to notify user: {e}")
    
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await bot.send_message(
        callback.message.chat.id,
        f"❌ Заказ #{order_id} отклонён\n\nКлиент уведомлён."
    )

@dp.callback_query(F.data.startswith("admin_contact_"))
async def admin_contact(callback: CallbackQuery):
    order_id = callback.data.split("_")[2]
    
    if order_id in orders:
        user_id = orders[order_id]["user_id"]
        username = orders[order_id].get("username", "не указан")
        
    await callback.answer()
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await bot.send_message(
        callback.message.chat.id,
        f"💬 Связь с клиентом\n\nЗаказ #{order_id}\n@{username}\nID: {user_id}\n\nНапишите клиенту напрямую."
    )

# Message handler for non-photo messages in payment state
@dp.message(OrderStates.waiting_for_payment)
async def wrong_payment_format(message: types.Message):
    text = (
        "⚠️ <b>Отправьте скриншот оплаты</b>\n\n"
        "Нужно фото чата с @byesocial, подтверждающее отправку подарка.\n\n"
        "Добавьте подпись с номером заказа."
    )
    await message.answer(text, parse_mode="HTML")

async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
