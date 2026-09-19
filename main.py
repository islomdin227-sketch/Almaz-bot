import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------------------------------------------------------
# ТАНЗИМОТ (ТОКЕН, АДМИН ВА FIRELOOT API)
# ---------------------------------------------------------
BOT_TOKEN = "8668882369:AAF63la5XiE5GjjrtqSnBn9qOFKPUp-2bIA"
ADMIN_ID = 8727925331  # ID-и Telegram-и худатон

# Танзимоти FireLoot API
FIRELOOT_API_KEY = "API_KEY_И_ХУДРО_АЗ_FIRELOOT_ИНҶО_НЕЗОНЕД"
FIRELOOT_API_URL = "https://fireloot.com/api/v1/order"  # Эзоҳ: URL-и дақиқи API-ро аз ҳуҷҷатҳои FireLoot санҷед

# Реквизитҳои шумо
CARD_DUSHANBE = "933313738"
ALIF_ACCOUNT = "933313738"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

users_db = {}
orders_counter = 490


# ---------------------------------------------------------
# ФУНКСИЯИ ПАЙВАСТ БА FIRELOOT API
# ---------------------------------------------------------
async def send_to_fireloot(player_id: str, service_id: str):
    """
    Функсия барои фиристодани алмосҳо тавассути API-и FireLoot
    """
    payload = {
        "api_key": FIRELOOT_API_KEY,
        "player_id": player_id,
        "service": service_id,  # ID-и бастаи алмосҳо дар FireLoot
    }

    headers = {"Content-Type": "application/json"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                FIRELOOT_API_URL, json=payload, headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # Агар FireLoot ҷавоби мусбат диҳад
                    if result.get("success") or result.get("status") == "success":
                        return True, "Муваффақият"
                    else:
                        return False, result.get(
                            "message", "Хатогии номаълум дар FireLoot"
                        )
                else:
                    return False, f"Хатогии сервер: {response.status}"
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------
# FSM (Ҳолатҳо)
# ---------------------------------------------------------
class GameOrder(StatesGroup):
    waiting_for_id = State()
    confirm_account = State()


class TopUp(StatesGroup):
    waiting_for_receipt = State()


# ---------------------------------------------------------
# КЛАВИАТУРАҲО
# ---------------------------------------------------------
def main_menu():
    kb = [
        [InlineKeyboardButton(text="💎 Алмосҳо", callback_data="category_diamonds")],
        [InlineKeyboardButton(text="🎟 Ваучерҳо", callback_data="category_vouchers")],
        [
            InlineKeyboardButton(
                text="💳 Пур кардани ҳисоб", callback_data="top_up_balance"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# ---------------------------------------------------------
# ХАНДЛЕРҲО
# ---------------------------------------------------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0}

    text = (
        "САЛОМ! БА ALMAZ TJ ХУШ ОМАДЕД 👋\n\n"
        "Мо арзонтарин донат барои FREE FIRE ҳастем ⚡️\n\n"
        "✅ Супурдаш: 1-5 дақиқа\n"
        "✅ Пардохт: DC Pay, Alif Mobi\n"
        "✅ 100% Бехатар\n\n"
        "Барои нарх ва заказ тугмаи поэниро пахш кунед 👇"
    )
    await message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data == "main_menu")
async def process_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    balance = users_db.get(user_id, {}).get("balance", 0.0)

    text = (
        "🔥 **Free Fire**\n\n"
        "Маҳсулотро интихоб кунед.\n"
        f"💳 Ҳисоби шумо: **{balance:.2f} с.**"
    )
    await callback.message.edit_text(
        text, reply_markup=main_menu(), parse_mode="Markdown"
    )


# --- КАТЕГОРИЯИ АЛМОСҲО (Кодҳои service_id-ро мувофиқи FireLoot гузоред) ---
@dp.callback_query(F.data == "category_diamonds")
async def show_diamonds(callback: types.CallbackQuery):
    # Формат: buy_{номи_пакет}_{нарх}_{service_id_дар_fireloot}
    kb = [
        [
            InlineKeyboardButton(
                text="💎 110 Алмаз — 9.00 с.",
                callback_data="buy_110 Алмаз_9.0_110diamond",
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 341 Алмаз — 28.00 с.",
                callback_data="buy_341 Алмаз_28.0_341diamond",
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 572 Алмаз — 45.00 с.",
                callback_data="buy_572 Алмаз_45.0_572diamond",
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 1166 Алмаз — 89.90 с.",
                callback_data="buy_1166 Алмаз_89.9_1166diamond",
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 2398 Алмаз — 177.00 с.",
                callback_data="buy_2398 Алмаз_177.0_2398diamond",
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 6160 Алмаз — 429.00 с.",
                callback_data="buy_6160 Алмаз_429.0_6160diamond",
            )
        ],
        [InlineKeyboardButton(text="🏠 Менюи асосӣ", callback_data="main_menu")],
    ]
    await callback.message.edit_text(
        "🔥 **Free Fire · 💎 Алмосҳо**\n\nМаҳсулотро интихоб кунед.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown",
    )


# --- ИНТИХОБИ МАҲСУЛОТ ВА ВУРУДИ ID ---
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    item_name = parts[1]
    price = float(parts[2])
    service_id = parts[3]

    await state.update_data(item_name=item_name, price=price, service_id=service_id)
    await state.set_state(GameOrder.waiting_for_id)

    kb = [[InlineKeyboardButton(text="🏠 Менюи асосӣ", callback_data="main_menu")]]
    await callback.message.edit_text(
        f"🛒 **💎 {item_name} — {price:.2f} с.**\n\n"
        "ID-и бозигари Free Fire-ро нависед — танҳо рақамҳо.\n\n"
        "Намуна: 123456789",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown",
    )


@dp.message(GameOrder.waiting_for_id)
async def process_id(message: types.Message, state: FSMContext):
    player_id = message.text.strip()
    if not player_id.isdigit():
        await message.answer("❌ ИЛТИМОС ТАНҲО РАҚАМҲОРО НАВИСЕД!")
        return

    await state.update_data(player_id=player_id)
    await state.set_state(GameOrder.confirm_account)

    kb = [
        [
            InlineKeyboardButton(
                text="✅ Ҳа, аккаунти ман аст", callback_data="confirm_acc_yes"
            )
        ],
        [InlineKeyboardButton(text="❌ Бекор кардан", callback_data="main_menu")],
    ]

    text = (
        "🔎 **Тафтиши аккаунт**\n\n"
        "🔥 Бахш: Free Fire\n"
        f"🆔 ID: {player_id}\n\n"
        "Ин аккаунти шумост?"
    )
    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "confirm_acc_yes")
async def confirm_purchase(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    balance = users_db.get(user_id, {}).get("balance", 0.0)
    price = data["price"]

    if balance < price:
        kb = [
            [
                InlineKeyboardButton(
                    text="💳 Пур кардани ҳисоб", callback_data="top_up_balance"
                )
            ],
            [InlineKeyboardButton(text="🏠 Менюи асосӣ", callback_data="main_menu")],
        ]
        text = (
            "❌ **Маблағ кифоя нест**\n\n"
            f"💰 Нарх: {price:.2f} с.\n"
            f"💳 Ҳисоби шумо: {balance:.2f} с.\n\n"
            "Ҳисобро пур кунед ва аз нав кӯшиш кунед."
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
            parse_mode="Markdown",
        )
    else:
        # Балансро захира мекунем, аммо танҳо пас аз тасдиқи админ кам мекунем
        kb_admin = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Тасдиқ ва фиристодани Алмос (API)",
                        callback_data=f"send_api_{user_id}_{data['service_id']}_{data['player_id']}_{price}",
                    ),
                    InlineKeyboardButton(
                        text="❌ Рад кардан", callback_data=f"cancel_order_{user_id}"
                    ),
                ]
            ]
        )

        await callback.message.edit_text(
            "⏳ **Фармоиш ба админ фиристода шуд.**\n\n"
            "Пас аз тасдиқи админ алмосҳо ба таври автоматикӣ ба аккаунти шумо гузаронида мешаванд.",
            reply_markup=main_menu(),
        )

        # Огоҳӣ ба Админ
        await bot.send_message(
            ADMIN_ID,
            f"📦 **ЗАКАЗИ НАВ БАРОИ ТАСДИҚ!**\n\n"
            f"👤 Корбар: @{callback.from_user.username} (ID: {user_id})\n"
            f"💎 Мол: {data['item_name']}\n"
            f"🆔 Free Fire ID: `{data['player_id']}`\n"
            f"💰 Нарх: {price:.2f} с.",
            reply_markup=kb_admin,
            parse_mode="Markdown",
        )
        await state.clear()


# --- ТАСДИҚИ АДМИН ВА ИҶРОИ АВТОМАТИКИИ FIRELOOT API ---
@dp.callback_query(F.data.startswith("send_api_"))
async def process_admin_approve(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    user_id = int(parts[2])
    service_id = parts[3]
    player_id = parts[4]
    price = float(parts[5])

    await callback.message.edit_text(
        "⏳ Дархост ба FireLoot API фиристода шуда истодааст..."
    )

    # Фиристодани дархост ба FireLoot API
    success, msg = await send_to_fireloot(player_id, service_id)

    if success:
        # Кам кардани баланси корбар
        if user_id in users_db:
            users_db[user_id]["balance"] -= price

        await callback.message.edit_text(
            f"✅ **Фармоиш иҷРО ШУД!**\n\nАлмосҳо ба ID: `{player_id}` худкор гузаштанд.",
            parse_mode="Markdown",
        )
        await bot.send_message(
            user_id,
            f"🎉 **Фармоиши шумо иҷро шуд!**\n\n{service_id} ба ID-и `{player_id}` муваффақона гузаронида шуд.",
            parse_mode="Markdown",
        )
    else:
        await callback.message.edit_text(
            f"❌ **Хатогӣ дар FireLoot API:**\n{msg}\n\nМаблағ аз ҳисоби корбар кам нашуд."
        )


# --- ПУР КАРДАНИ ҲИСОБ ВА ЧЕКҲО ---
@dp.callback_query(F.data == "top_up_balance")
async def top_up_start(callback: types.CallbackQuery):
    kb = [
        [
            InlineKeyboardButton(text="20.00 с.", callback_data="amount_20"),
            InlineKeyboardButton(text="50.00 с.", callback_data="amount_50"),
        ],
        [
            InlineKeyboardButton(text="100.00 с.", callback_data="amount_100"),
            InlineKeyboardButton(text="200.00 с.", callback_data="amount_200"),
        ],
        [InlineKeyboardButton(text="🏠 Менюи асосӣ", callback_data="main_menu")],
    ]
    await callback.message.edit_text(
        "💳 **Маблағро барои пур кардани ҳисоб интихоб кунед:**",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown",
    )


@dp.callback_query(F.data.startswith("amount_"))
async def process_amount(callback: types.CallbackQuery, state: FSMContext):
    amount = float(callback.data.split("_")[1])
    await state.update_data(amount=amount)

    kb = [
        [InlineKeyboardButton(text="✅ Пардохт кардам", callback_data="paid_confirm")]
    ]
    text = (
        "💳 **Реквизитҳо барои пардохт:**\n\n"
        f"🏛 **Душанбе Сити / Alif Mobi:** `{CARD_DUSHANBE}`\n\n"
        f"💰 Маблағ: **{amount:.2f} с.**\n\n"
        "Пас аз пардохт тугмаи «✅ Пардохт кардам»-ро пахш кунед."
    )
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown",
    )


@dp.callback_query(F.data == "paid_confirm")
async def paid_confirm(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TopUp.waiting_for_receipt)
    await callback.message.edit_text("🧾 ЛУТФАН ЧЕК Ё СКРИНШОТИ ПАРДОХТРО ФИРИСТЕД:")


@dp.message(TopUp.waiting_for_receipt, F.photo | F.document)
async def process_receipt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount", 0)

    admin_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Тасдиқ кардан",
                    callback_data=f"approve_topup_{message.from_user.id}_{amount}",
                ),
                InlineKeyboardButton(
                    text="❌ Рад кардан",
                    callback_data=f"reject_topup_{message.from_user.id}",
                ),
            ]
        ]
    )

    await message.answer("✅ Чек ба админ фиристода шуд. Лутфан сабр кунед.")
    await bot.send_message(
        ADMIN_ID,
        f"💳 **Пур кардани ҳисоб!**\n\nКорбар: ID {message.from_user.id}\nМаблағ: {amount:.2f} с.",
        reply_markup=admin_kb,
    )
    if message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id)
    await state.clear()


@dp.callback_query(F.data.startswith("approve_topup_"))
async def approve_topup(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    user_id = int(parts[2])
    amount = float(parts[3])

    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0}

    users_db[user_id]["balance"] += amount
    await callback.message.edit_text(f"✅ Баланси корбар +{amount:.2f} с. пур шуд.")
    await bot.send_message(user_id, f"🎉 Ҳисоби шумо +{amount:.2f} с. пур карда шуд!")


async def main():
    print("Бот бо FireLoot API фаъол шуд...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
