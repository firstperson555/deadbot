import logging
import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from states.states import OrderStates
from keyboards.keyboards import (
    get_main_menu_keyboard,
    get_platform_keyboard,
    get_service_keyboard,
    get_admin_order_keyboard,
    get_back_keyboard,
    get_link_input_keyboard,
    get_payment_keyboard
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Admin credentials
ADMIN_USER_ID = 7846160465
ADMIN_USERNAME = "@nev3rdead"

# In-memory storage for orders (for demo purposes)
orders = {}
order_counter = 0


def validate_tiktok_link(link: str) -> bool:
    """Validate TikTok link format"""
    patterns = [
        r'https?://(www\.)?tiktok\.com/@[\w.-]+',
        r'https?://(www\.)?tiktok\.com/[\w.-]+/video/\d+',
        r'https?://vm\.tiktok\.com/\w+',
        r'https?://vt\.tiktok\.com/\w+'
    ]
    return any(re.match(pattern, link) for pattern in patterns)


def validate_telegram_link(link: str) -> bool:
    """Validate Telegram link format"""
    patterns = [
        r'https?://t\.me/[\w]+',
        r'https?://t\.me/[\w]+/\d+',
        r'@[\w]+',
        r'https?://telegram\.me/[\w]+'
    ]
    return any(re.match(pattern, link) for pattern in patterns)


def validate_youtube_link(link: str) -> bool:
    """Validate YouTube link format"""
    patterns = [
        r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://(www\.)?youtube\.com/shorts/[\w-]+',
        r'https?://(www\.)?youtube\.com/@[\w.-]+',
        r'https?://(www\.)?youtube\.com/channel/[\w-]+',
        r'https?://youtu\.be/[\w-]+'
    ]
    return any(re.match(pattern, link) for pattern in patterns)


def get_link_request_text(platform: str, service: str) -> str:
    """Generate dynamic link request text based on platform and service"""
    platform_lower = platform.lower()
    service_lower = service.lower()

    if platform_lower == "tiktok":
        if "просмотры" in service_lower:
            return "🔗 Отправьте ссылку на TikTok видео или профиль:"
        elif "лайки" in service_lower:
            return "🔗 Отправьте ссылку на TikTok видео:"
        elif "подписчики" in service_lower:
            return "🔗 Отправьте ссылку на TikTok профиль:"
    elif platform_lower == "telegram":
        if "просмотры" in service_lower:
            return "🔗 Отправьте ссылку на Telegram пост или канал:"
        elif "лайки" in service_lower:
            return "🔗 Отправьте ссылку на Telegram пост:"
        elif "подписчики" in service_lower:
            return "🔗 Отправьте ссылку на Telegram канал:"
    elif platform_lower == "youtube":
        if "просмотры" in service_lower:
            return "🔗 Отправьте ссылку на YouTube видео или канал:"
        elif "лайки" in service_lower:
            return "🔗 Отправьте ссылку на YouTube видео:"
        elif "подписчики" in service_lower:
            return "🔗 Отправьте ссылку на YouTube канал:"

    return "🔗 Отправьте ссылку на пост, канал или профиль:"


def get_router(bot: Bot) -> Router:
    """Create and configure the router with bot instance"""
    router = Router()

    @router.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext):
        """Handle /start command"""
        await state.clear()
        user_id = message.from_user.id
        username = message.from_user.username or "не указан"

        logger.info(f"User {user_id} (@{username}) started the bot")

        welcome_text = (
            "👋 Добро пожаловать в DeadBoot\n\n"
            "Мы — приватный сервис продвижения в TikTok, "
            "Telegram и YouTube.\n\n"
            "✨ Работаем только с проверенными методами "
            "и закрытыми алгоритмами.\n\n"
            "� Цены:\n"
            "• 1000 — 100 Stars\n"
            "• 5000 — 500 Stars\n"
            "• 10000 — 1000 Stars\n\n"
            "💎 Услуги: Просмотры, Лайки, Подписчики\n\n"
            "ℹ️ Справка: /help\n\n"
            "Выберите услугу ниже:"
        )

        await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())

    @router.message(Command("help"))
    async def cmd_help(message: Message):
        """Handle /help command"""
        help_text = (
            "ℹ️ Справка DeadBoot\n\n"
            "📊 Поддерживаемые платформы:\n"
            "• TikTok\n"
            "• Telegram\n"
            "• YouTube\n\n"
            "💎 Услуги:\n"
            "• Просмотры\n"
            "• Лайки\n"
            "• Подписчики\n\n"
            "💰 Цены:\n"
            "• 1000 — 100 Stars\n"
            "• 5000 — 500 Stars\n"
            "• 10000 — 1000 Stars\n\n"
            "📢 Наш канал с помощью в переводе звёзд: https://t.me/deadbothelp\n\n"
            "💳 Для оплаты услуг переведите Stars "
            "на @byesocial"
        )

        await message.answer(help_text)

    @router.callback_query(F.data == "start_order")
    async def callback_start_order(callback: CallbackQuery, state: FSMContext):
        """Handle start order callback"""
        await state.clear()
        await state.set_state(OrderStates.choosing_platform)

        await callback.message.edit_text(
            "🎯 Выберите платформу:",
            reply_markup=get_platform_keyboard()
        )
        await callback.answer()

    @router.callback_query(F.data == "about_service")
    async def callback_about_service(callback: CallbackQuery):
        """Handle about service callback"""
        about_text = (
            "ℹ️ О сервисе DeadBoot\n\n"
            "📊 Поддерживаемые платформы:\n"
            "• TikTok\n"
            "• Telegram\n"
            "• YouTube\n\n"
            "💎 Услуги:\n"
            "• Просмотры\n"
            "• Лайки\n"
            "• Подписчики\n\n"
            "⚠️ Важно: Все оплаты проходят через "
            "нашего официального финансового партнёра "
            "@byesocial для безопасности и конфиденциальности."
        )

        await callback.message.edit_text(
            about_text,
            reply_markup=get_back_keyboard()
        )
        await callback.answer()

    @router.callback_query(F.data == "back_to_main")
    async def callback_back_to_main(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu callback"""
        await state.clear()

        await callback.message.edit_text(
            "👋 Добро пожаловать в DeadBoot\n\n"
            "Мы — приватный сервис продвижения в TikTok, "
            "Telegram и YouTube.\n\n"
            "✨ Работаем только с проверенными методами "
            "и закрытыми алгоритмами.\n\n"
            "� Цены:\n"
            "• 1000 — 100 Stars\n"
            "• 5000 — 500 Stars\n"
            "• 10000 — 1000 Stars\n\n"
            "💎 Услуги: Просмотры, Лайки, Подписчики\n\n"
            "ℹ️ Справка: /help\n\n"
            "Выберите услугу ниже:",
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer()

    @router.callback_query(F.data == "cancel_order")
    async def callback_cancel_order(callback: CallbackQuery, state: FSMContext):
        """Handle order cancellation callback"""
        await state.clear()

        await callback.message.edit_text(
            "❌ Заказ отменён.\n\n"
            "👋 Добро пожаловать в DeadBoot\n\n"
            "Мы — приватный сервис продвижения в TikTok, "
            "Telegram и YouTube.\n\n"
            "✨ Работаем только с проверенными методами "
            "и закрытыми алгоритмами.\n\n"
            "� Цены:\n"
            "• 1000 — 100 Stars\n"
            "• 5000 — 500 Stars\n"
            "• 10000 — 1000 Stars\n\n"
            "💎 Услуги: Просмотры, Лайки, Подписчики\n\n"
            "ℹ️ Справка: /help\n\n"
            "Выберите услугу ниже:",
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer()

    @router.callback_query(
        OrderStates.choosing_platform,
        F.data.startswith("platform_")
    )
    async def callback_choose_platform(
        callback: CallbackQuery,
        state: FSMContext
    ):
        """Handle platform selection"""
        platform = callback.data.replace("platform_", "")
        platform_names = {
            "tiktok": "TikTok",
            "telegram": "Telegram",
            "youtube": "YouTube"
        }

        await state.update_data(platform=platform_names[platform])
        await state.set_state(OrderStates.choosing_service)

        await callback.message.edit_text(
            f"📱 Выбрана платформа: {platform_names[platform]}\n\n"
            "🎯 Выберите тип услуги:",
            reply_markup=get_service_keyboard()
        )
        await callback.answer()

    @router.callback_query(F.data == "back_to_platform")
    async def callback_back_to_platform(
        callback: CallbackQuery,
        state: FSMContext
    ):
        """Handle back to platform selection"""
        await state.set_state(OrderStates.choosing_platform)

        await callback.message.edit_text(
            "🎯 Выберите платформу:",
            reply_markup=get_platform_keyboard()
        )
        await callback.answer()

    @router.callback_query(F.data == "back_to_service")
    async def callback_back_to_service(
        callback: CallbackQuery,
        state: FSMContext
    ):
        """Handle back to service selection"""
        await state.set_state(OrderStates.choosing_service)

        data = await state.get_data()
        platform = data.get("platform", "")

        await callback.message.edit_text(
            f"📱 Выбрана платформа: {platform}\n\n"
            "🎯 Выберите тип услуги:",
            reply_markup=get_service_keyboard()
        )
        await callback.answer()

    @router.callback_query(
        OrderStates.choosing_service,
        F.data.startswith("service_")
    )
    async def callback_choose_service(
        callback: CallbackQuery,
        state: FSMContext
    ):
        """Handle service type selection"""
        service = callback.data.replace("service_", "")
        service_names = {
            "views": "Просмотры",
            "likes": "Лайки",
            "subscribers": "Подписчики"
        }

        await state.update_data(service=service_names[service])
        await state.set_state(OrderStates.entering_link)

        data = await state.get_data()
        platform = data.get("platform", "")

        link_request_text = get_link_request_text(
            platform,
            service_names[service]
        )

        await callback.message.edit_text(
            f"📱 Платформа: {platform}\n"
            f"📋 Услуга: {service_names[service]}\n\n"
            f"{link_request_text}",
            reply_markup=get_link_input_keyboard()
        )
        await callback.answer()

    @router.message(OrderStates.entering_link)
    async def message_enter_link(message: Message, state: FSMContext):
        """Handle link input"""
        link = message.text.strip()

        data = await state.get_data()
        platform = data.get("platform", "").lower()

        is_valid = False
        error_msg = ""

        if platform == "tiktok":
            if validate_tiktok_link(link):
                is_valid = True
            else:
                error_msg = (
                    "❌ Некорректная ссылка TikTok.\n"
                    "Формат: https://tiktok.com/@username "
                    "или https://vm.tiktok.com/..."
                )
        elif platform == "telegram":
            if validate_telegram_link(link):
                is_valid = True
            else:
                error_msg = (
                    "❌ Некорректная ссылка Telegram.\n"
                    "Формат: @username или https://t.me/username"
                )
        elif platform == "youtube":
            if validate_youtube_link(link):
                is_valid = True
            else:
                error_msg = (
                    "❌ Некорректная ссылка YouTube.\n"
                    "Формат: https://youtube.com/watch?v=... "
                    "или https://youtube.com/@username"
                )
        else:
            error_msg = "❌ Ошибка: платформа не выбрана."

        if not is_valid:
            await message.answer(error_msg)
            return

        await state.update_data(link=link)
        await state.set_state(OrderStates.entering_quantity)

        await message.answer(
            f"✅ Ссылка сохранена: {link}\n\n"
            "🔢 Укажите количество (например: 1000, 5000, 10000):"
        )

    @router.message(OrderStates.entering_quantity)
    async def message_enter_quantity(message: Message, state: FSMContext):
        """Handle quantity input"""
        quantity_text = message.text.strip()

        # Fixed pricing
        price_map = {
            1000: 100,
            5000: 500,
            10000: 1000
        }

        try:
            quantity = int(quantity_text)
            if quantity not in price_map:
                await message.answer(
                    "❌ Доступные количества: 1000, 5000, 10000. "
                    "Пожалуйста, выберите одно из этих значений."
                )
                return
        except ValueError:
            await message.answer(
                "❌ Некорректное число. "
                "Пожалуйста, укажите количество (1000, 5000 или 10000)."
            )
            return

        price = price_map[quantity]

        await state.update_data(quantity=quantity, price=price)

        data = await state.get_data()

        payment_text = (
            f"📋 Ваш заказ:\n\n"
            f"📱 Платформа: {data['platform']}\n"
            f"📋 Услуга: {data['service']}\n"
            f"🔗 Ссылка: {data['link']}\n"
            f"🔢 Количество: {quantity:,}\n\n"
            f"💰 Стоимость: {price} Stars\n\n"
            f"💳 Для оплаты:\n"
            f"1. Сделайте перевод {price} Stars на @byesocial\n"
            f"2. После оплаты отправьте в этот бот скриншот\n"
            f"3. Добавьте подпись к скриншоту:\n"
            f"   «Оплата за {data['service']} для {data['link']} — {quantity}»"
        )

        await state.set_state(OrderStates.waiting_payment)
        await message.answer(payment_text, reply_markup=get_payment_keyboard())

    @router.message(OrderStates.waiting_payment)
    async def message_payment_proof(message: Message, state: FSMContext):
        """Handle payment screenshot with caption"""
        global order_counter
        order_counter += 1

        data = await state.get_data()

        # Check if message has photo or text with proper format
        has_photo = message.photo is not None
        caption = message.caption or message.text or ""

        if not has_photo:
            await message.answer(
                "❌ Пожалуйста, отправьте скриншот оплаты "
                "с подписью."
            )
            return

        # Save order
        order = {
            "id": order_counter,
            "user_id": message.from_user.id,
            "username": message.from_user.username or "не указан",
            "platform": data.get("platform"),
            "service": data.get("service"),
            "link": data.get("link"),
            "quantity": data.get("quantity"),
            "price": data.get("price"),
            "photo_id": message.photo[-1].file_id,
            "caption": caption,
            "status": "pending"
        }

        orders[order_counter] = order

        logger.info(
            f"New order #{order_counter} from user "
            f"{message.from_user.id} (@{order['username']})"
        )

        # Send confirmation to user
        await message.answer(
            "✅ Ваш заказ отправлен на рассмотрение.\n\n"
            "Админ проверит оплату и одобрит или отклонит заказ. "
            "Ожидайте уведомления."
        )

        # Send notification to admin
        try:
            admin_text = (
                f"🔔 Новый заказ #{order_counter}\n\n"
                f"👤 Пользователь: {order['username']} (ID: {order['user_id']})\n"
                f"📱 Платформа: {order['platform']}\n"
                f"📋 Услуга: {order['service']}\n"
                f"🔗 Ссылка: {order['link']}\n"
                f"🔢 Количество: {order['quantity']:,}\n"
                f"💰 Стоимость: {order['price']} Stars\n\n"
                f"📝 Подпись: {order['caption']}"
            )

            await bot.send_photo(
                chat_id=ADMIN_USER_ID,
                photo=order['photo_id'],
                caption=admin_text,
                reply_markup=get_admin_order_keyboard(order_counter)
            )

            logger.info(f"Order #{order_counter} sent to admin")

        except Exception as e:
            logger.error(f"Failed to send order to admin: {e}")

        await state.clear()

    # Admin handlers
    @router.callback_query(F.data.startswith("approve_"))
    async def callback_approve_order(callback: CallbackQuery):
        """Handle order approval by admin"""
        if callback.from_user.id != ADMIN_USER_ID:
            await callback.answer(
                "❌ У вас нет прав для этого действия",
                show_alert=True
            )
            return

        order_id = int(callback.data.split("_")[1])
        order = orders.get(order_id)

        if not order:
            await callback.answer("Заказ не найден", show_alert=True)
            return

        order["status"] = "approved"

        # Notify user
        try:
            await bot.send_message(
                chat_id=order["user_id"],
                text=(
                    f"✅ Заказ #{order_id} одобрен!\n\n"
                    f"Накрутка начнётся в течение 30–60 минут. "
                    f"Следите за статистикой.\n\n"
                    f"Если возникнут вопросы, обращайтесь к @byesocial"
                )
            )
            logger.info(f"Order #{order_id} approved, user notified")
        except Exception as e:
            logger.error(f"Failed to notify user for order #{order_id}: {e}")

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Заказ одобрен")

    @router.callback_query(F.data.startswith("reject_"))
    async def callback_reject_order(callback: CallbackQuery):
        """Handle order rejection by admin"""
        if callback.from_user.id != ADMIN_USER_ID:
            await callback.answer(
                "❌ У вас нет прав для этого действия",
                show_alert=True
            )
            return

        order_id = int(callback.data.split("_")[1])
        order = orders.get(order_id)

        if not order:
            await callback.answer("Заказ не найден", show_alert=True)
            return

        order["status"] = "rejected"

        # Notify user
        try:
            await bot.send_message(
                chat_id=order["user_id"],
                text=(
                    f"❌ Заказ #{order_id} отклонён.\n\n"
                    f"Если вы считаете это ошибкой, "
                    f"обратитесь к @byesocial с скриншотом оплаты."
                )
            )
            logger.info(f"Order #{order_id} rejected, user notified")
        except Exception as e:
            logger.error(f"Failed to notify user for order #{order_id}: {e}")

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Заказ отклонён")

    @router.callback_query(F.data.startswith("contact_"))
    async def callback_contact_user(callback: CallbackQuery):
        """Handle contact user by admin"""
        if callback.from_user.id != ADMIN_USER_ID:
            await callback.answer(
                "❌ У вас нет прав для этого действия",
                show_alert=True
            )
            return

        order_id = int(callback.data.split("_")[1])
        order = orders.get(order_id)

        if not order:
            await callback.answer("Заказ не найден", show_alert=True)
            return

        username = order["username"]
        if username != "не указан":
            contact_info = f"@{username}"
        else:
            contact_info = f"ID: {order['user_id']}"

        await callback.answer(
            f"👤 Связаться с пользователем: {contact_info}",
            show_alert=True
        )

    return router
