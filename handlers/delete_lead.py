import logging

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import ALLOWED_USER_IDS
from amo_client import amo_get_lead, amo_delete_lead

router = Router()
logger = logging.getLogger(__name__)


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    # /start можно оставить, тут проверка прав не обязательна,
    # но если хочешь — можно тоже завязать на is_allowed
    await message.answer(
        "Отправь <b>только ID сделки</b> сообщением.\n\n"
        "Пример: <code>32992653</code>"
    )


@router.message(F.text.regexp(r"^\d+$"))
async def handle_lead_id(message: Message):
    user_id = message.from_user.id

    # Не в ALLOWED — просто молча игнорим
    if not is_allowed(user_id):
        return

    lead_id = int(message.text.strip())

    try:
        lead = await amo_get_lead(lead_id)
    except Exception:
        logger.exception("Ошибка при получении сделки %s", lead_id)
        await message.answer("Ошибка поиска сделки")
        return

    if not lead:
        await message.answer("Ошибка поиска сделки")
        return

    name = lead.get("name") or "Без названия"
    price = lead.get("price") or 0

    text = (
        f"Найдена сделка:\n\n"
        f"<b>ID:</b> {lead_id}\n"
        f"<b>Название:</b> {name}\n"
        f"<b>Сумма:</b> {price}\n\n"
        f"Удалить эту сделку?"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data=f"del_yes:{lead_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data=f"del_no:{lead_id}",
                )
            ],
        ]
    )

    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("del_no:"))
async def cb_del_no(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Если не авторизован — игнор (даже без сообщений в чат)
    if not is_allowed(user_id):
        return

    try:
        await callback.answer()  # просто убираем "часики"
    except Exception:
        pass

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass


@router.callback_query(F.data.startswith("del_yes:"))
async def cb_del_yes(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Не в ALLOWED — полностью игнорим
    if not is_allowed(user_id):
        return

    try:
        lead_id = int(callback.data.split(":", 1)[1])
    except ValueError:
        try:
            await callback.answer()
        except Exception:
            pass
        return

    try:
        await callback.answer("Удаляю...")
    except Exception:
        pass

    ok, err = await amo_delete_lead(lead_id)

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    if ok:
        await callback.message.answer("Сделка удалена")
    else:
        # По ТЗ можно дать общую ошибку, но я оставляю чуть инфы
        await callback.message.answer(
            "Ошибка удаления сделки"
        )
