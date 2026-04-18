from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_keyboard():
    """Main menu keyboard with service options"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🚀 Начать заказ",
        callback_data="start_order"
    ))
    builder.add(InlineKeyboardButton(
        text="ℹ️ О сервисе",
        callback_data="about_service"
    ))
    builder.adjust(1)
    return builder.as_markup()


def get_platform_keyboard():
    """Platform selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Instagram",
        callback_data="platform_instagram"
    ))
    builder.add(InlineKeyboardButton(
        text="TikTok",
        callback_data="platform_tiktok"
    ))
    builder.add(InlineKeyboardButton(
        text="Telegram",
        callback_data="platform_telegram"
    ))
    builder.add(InlineKeyboardButton(
        text="YouTube",
        callback_data="platform_youtube"
    ))
    builder.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_main"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_order"
    ))
    builder.adjust(2)
    return builder.as_markup()


def get_service_keyboard():
    """Service type selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="👁️ Просмотры",
        callback_data="service_views"
    ))
    builder.add(InlineKeyboardButton(
        text="❤️ Лайки",
        callback_data="service_likes"
    ))
    builder.add(InlineKeyboardButton(
        text="👥 Подписчики",
        callback_data="service_subscribers"
    ))
    builder.add(InlineKeyboardButton(
        text=" Назад",
        callback_data="back_to_platform"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_order"
    ))
    builder.adjust(2)
    return builder.as_markup()


def get_admin_order_keyboard(order_id: int):
    """Admin keyboard for order approval"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="✅ Одобрить",
        callback_data=f"approve_{order_id}"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отклонить",
        callback_data=f"reject_{order_id}"
    ))
    builder.add(InlineKeyboardButton(
        text="💬 Связаться",
        callback_data=f"contact_{order_id}"
    ))
    builder.adjust(3)
    return builder.as_markup()


def get_back_keyboard():
    """Simple back button with cancel"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_main"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_order"
    ))
    builder.adjust(2)
    return builder.as_markup()


def get_link_input_keyboard():
    """Keyboard for link input stage - goes back to service selection"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_service"
    ))
    builder.add(InlineKeyboardButton(
        text="❌ Отменить",
        callback_data="cancel_order"
    ))
    builder.adjust(2)
    return builder.as_markup()


def get_payment_keyboard():
    """Payment stage keyboard with cancel"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить заказ",
        callback_data="cancel_order"
    ))
    return builder.as_markup()
