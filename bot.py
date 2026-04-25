import logging
import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database
from questions import QUESTIONS

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))
CARD_NUMBER = os.environ.get("CARD_NUMBER", "8600 1234 5678 9012")
MONTHLY_PRICE = 29900
YEARLY_PRICE = 199000
FREE_TESTS_PER_DAY = 3

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()

class TestState(StatesGroup):
    choosing_subject = State()
    choosing_count = State()
    answering = State()

class PaymentState(StatesGroup):
    waiting_receipt = State()

def main_menu_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📚 Test boshlash")],
        [KeyboardButton(text="📊 Mening natijalarim"), KeyboardButton(text="⭐ Premium")],
        [KeyboardButton(text="ℹ️ Yordam"), KeyboardButton(text="👤 Profil")]
    ], resize_keyboard=True)

def subjects_kb():
    subjects = [
        ("🔢 Matematika","matematika"),("🌍 Ingliz tili","ingliz"),
        ("📖 O'zbek tili","ozbek"),("⚗️ Kimyo","kimyo"),
        ("🔬 Biologiya","biologiya"),("⚡ Fizika","fizika"),
        ("🌐 Geografiya","geografiya"),("📜 Tarix","tarix"),
        ("💻 Informatika","informatika"),("🎲 Aralash","aralash"),
    ]
    builder = InlineKeyboardBuilder()
    for name, data in subjects:
        builder.button(text=name, callback_data=f"subject_{data}")
    builder.adjust(2)
    return builder.as_markup()

def question_count_kb():
    builder = InlineKeyboardBuilder()
    for c in [5, 10, 20, 30]:
        builder.button(text=f"📝 {c} ta savol", callback_data=f"count_{c}")
    builder.adjust(2)
    return builder.as_markup()

def answer_kb(options, qid):
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(options):
        builder.button(text=f"{chr(65+i)}) {opt}", callback_data=f"ans_{qid}_{i}")
    builder.adjust(1)
    return builder.as_markup()

def premium_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"💳 Oylik — {MONTHLY_PRICE:,} so'm", callback_data="buy_monthly")
    builder.button(text=f"🎁 Yillik — {YEARLY_PRICE:,} so'm", callback_data="buy_yearly")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(CommandStart())
async def start(message: types.Message):
    await db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(
        f"👋 Salom, <b>{message.from_user.first_name}</b>!\n\n"
        f"🎓 <b>EduTest Bot</b> ga xush kelibsiz!\n\n"
        f"✅ Barcha fanlardan test ishlang\n"
        f"✅ Imtihonlarga tayyorlaning\n\n"
        f"📊 Bepul: Kuniga {FREE_TESTS_PER_DAY} ta test\n"
        f"⭐ Premium: Cheksiz testlar",
        reply_markup=main_menu_kb(), parse_mode="HTML"
    )

@dp.message(F.text == "📚 Test boshlash")
async def start_test(message: types.Message, state: FSMContext):
    if not await db.is_premium(message.from_user.id) and await db.get_daily_tests(message.from_user.id) >= FREE_TESTS_PER_DAY:
        await message.answer(f"⚠️ Bugungi bepul testlar tugadi!\n\n⭐ Premium oling — cheksiz testlar!\nNarx: <b>{MONTHLY_PRICE:,} so'm/oy</b>", reply_markup=premium_kb(), parse_mode="HTML")
        return
    await message.answer("📚 <b>Qaysi fandan test ishlaysiz?</b>", reply_markup=subjects_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_subject)

@dp.callback_query(F.data.startswith("subject_"))
async def choose_subject(callback: types.CallbackQuery, state: FSMContext):
    subject = callback.data.replace("subject_", "")
    await state.update_data(subject=subject)
    await callback.message.edit_text("📝 <b>Nechta savol ishlaysiz?</b>", reply_markup=question_count_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_count)

@dp.callback_query(F.data.startswith("count_"))
async def choose_count(callback: types.CallbackQuery, state: FSMContext):
    count = int(callback.data.replace("count_", ""))
    data = await state.get_data()
    questions = get_questions(data.get("subject"), count)
    if not questions:
        await callback.message.edit_text("❌ Bu fan uchun savollar yo'q!")
        return
    await state.update_data(questions=questions, current_q=0, correct=0, count=len(questions))
    await callback.message.delete()
    await send_question(callback.message.chat.id, state, callback.bot)
    await state.set_state(TestState.answering)

async def send_question(chat_id, state, bot):
    data = await state.get_data()
    questions, current, total = data["questions"], data["current_q"], data["count"]
    if current >= len(questions):
        await finish_test(chat_id, state, bot)
        return
    q = questions[current]
    progress = "▓" * current + "░" * (total - current)
    await bot.send_message(chat_id,
        f"📊 <b>{current+1}/{total}</b>  {progress}\n\n❓ <b>{q['question']}</b>",
        reply_markup=answer_kb(q["options"], current), parse_mode="HTML")

@dp.callback_query(F.data.startswith("ans_"))
async def answer_question(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    q_index, chosen = int(parts[1]), int(parts[2])
    data = await state.get_data()
    if q_index != data["current_q"]:
        await callback.answer("Allaqachon javob berilgan!", show_alert=True)
        return
    q = data["questions"][q_index]
    correct = data["correct"]
    if chosen == q["correct"]:
        correct += 1
        result = "✅ <b>To'g'ri!</b>"
    else:
        result = f"❌ <b>Noto'g'ri!</b>\nTo'g'ri: <b>{q['options'][q['correct']]}</b>"
    if q.get("explanation"):
        result += f"\n\n💡 <i>{q['explanation']}</i>"
    await callback.message.edit_text(callback.message.text + f"\n\n{result}", parse_mode="HTML")
    await state.update_data(current_q=q_index+1, correct=correct)
    await asyncio.sleep(1.5)
    await send_question(callback.message.chat.id, state, callback.bot)

async def finish_test(chat_id, state, bot):
    data = await state.get_data()
    correct, total, subject = data["correct"], data["count"], data["subject"]
    pct = (correct / total) * 100
    if pct >= 90: grade, msg = "🏆 A'lo!", "Ajoyib! 🌟"
    elif pct >= 70: grade, msg = "👍 Yaxshi", "Davom eting!"
    elif pct >= 50: grade, msg = "😐 Qoniqarli", "Mashq qiling!"
    else: grade, msg = "📚 Qoniqarsiz", "Ko'proq o'qing!"
    await db.save_test_result(chat_id, subject, correct, total)
    await db.increment_daily_tests(chat_id)
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Qayta test", callback_data="restart_test")
    builder.adjust(1)
    await bot.send_message(chat_id,
        f"🎯 <b>Test yakunlandi!</b>\n\n📊 Natija: <b>{correct}/{total}</b>\n💯 Foiz: <b>{pct:.0f}%</b>\n\n{grade} {msg}",
        reply_markup=builder.as_markup(), parse_mode="HTML")
    await state.clear()

@dp.message(F.text == "👤 Profil")
async def show_profile(message: types.Message):
    stats = await db.get_user_stats(message.from_user.id)
    is_premium = await db.is_premium(message.from_user.id)
    await message.answer(
        f"👤 <b>Profil</b>\n\n📛 {message.from_user.full_name}\n"
        f"💎 {'⭐ Premium' if is_premium else '🆓 Bepul'}\n\n"
        f"✅ Testlar: {stats.get('total_tests',0)}\n"
        f"🎯 O'rtacha: {stats.get('avg_score',0):.1f}%\n"
        f"🏆 Eng yaxshi: {stats.get('best_score',0):.0f}%", parse_mode="HTML")

@dp.message(F.text == "📊 Mening natijalarim")
async def show_results(message: types.Message):
    results = await db.get_recent_results(message.from_user.id)
    if not results:
        await message.answer("📊 Hozircha natijalar yo'q. Test ishlang!")
        return
    emojis = {"matematika":"🔢","ingliz":"🌍","ozbek":"📖","kimyo":"⚗️","biologiya":"🔬","fizika":"⚡","geografiya":"🌐","tarix":"📜","informatika":"💻","aralash":"🎲"}
    text = "📊 <b>So'nggi natijalar:</b>\n\n"
    for r in results:
        pct = (r['correct']/r['total'])*100
        text += f"{emojis.get(r['subject'],'📚')} {r['subject'].title()}: <b>{r['correct']}/{r['total']}</b> ({pct:.0f}%)\n"
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == "⭐ Premium")
async def show_premium(message: types.Message):
    await message.answer(
        f"⭐ <b>EduTest Premium</b>\n\n✅ Cheksiz testlar\n✅ Batafsil statistika\n✅ DTM simulyatsiyasi\n\n"
        f"📅 Oylik: <b>{MONTHLY_PRICE:,} so'm</b>\n🎁 Yillik: <b>{YEARLY_PRICE:,} so'm</b>",
        reply_markup=premium_kb(), parse_mode="HTML")

@dp.callback_query(F.data.startswith("buy_"))
async def buy_premium(callback: types.CallbackQuery, state: FSMContext):
    plan = callback.data.replace("buy_", "")
    price = MONTHLY_PRICE if plan == "monthly" else YEARLY_PRICE
    plan_name = "Oylik" if plan == "monthly" else "Yillik"
    await callback.message.edit_text(
        f"💳 <b>{plan_name} — {price:,} so'm</b>\n\nKarta: <code>{CARD_NUMBER}</code>\n\n"
        f"To'lovdan so'ng chek rasmini yuboring.\n⚠️ Izoh: <code>Premium {callback.from_user.id}</code>", parse_mode="HTML")
    await state.set_state(PaymentState.waiting_receipt)
    await state.update_data(plan=plan, price=price)

@dp.message(PaymentState.waiting_receipt, F.photo)
async def receive_receipt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_ID,
        f"💳 Yangi to'lov!\n👤 {message.from_user.full_name} (@{message.from_user.username})\n"
        f"🆔 {message.from_user.id}\n📦 {data.get('plan')}\n\n/approve {message.from_user.id} {data.get('plan')}")
    await message.answer("✅ Chek qabul qilindi! Admin tez orada faollashtiradi. 🙏")
    await state.clear()

@dp.message(Command("approve"))
async def approve_premium(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    parts = message.text.split()
    if len(parts) < 3: await message.answer("Format: /approve USER_ID monthly|yearly"); return
    user_id, plan = int(parts[1]), parts[2]
    days = 30 if plan == "monthly" else 365
    await db.set_premium(user_id, days)
    await message.answer(f"✅ User {user_id} ga {days} kunlik Premium berildi!")
    await bot.send_message(user_id, "🎉 <b>Premium faollashtirildi! Cheksiz testlardan bahramand bo'ling! 🚀</b>", parse_mode="HTML")

@dp.message(Command("stats"))
async def admin_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    s = await db.get_global_stats()
    await message.answer(f"📊 Statistika:\n👥 Foydalanuvchilar: {s['users']}\n⭐ Premium: {s['premium']}\n📝 Testlar: {s['tests']}")

@dp.callback_query(F.data == "restart_test")
async def restart_test(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("📚 <b>Qaysi fandan test?</b>", reply_markup=subjects_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_subject)

@dp.message(F.text == "ℹ️ Yordam")
async def help_cmd(message: types.Message):
    await message.answer("ℹ️ <b>Yordam</b>\n\n📚 Test boshlash — fan tanlang\n📊 Natijalar — so'nggi testlar\n⭐ Premium — cheksiz testlar\n👤 Profil — statistika", parse_mode="HTML")

def get_questions(subject, count):
    if subject == "aralash":
        all_q = [q for qs in QUESTIONS.values() for q in qs]
    else:
        all_q = QUESTIONS.get(subject, [])
    if not all_q: return []
    return random.sample(all_q, min(count, len(all_q)))

async def main():
    await db.init()
    logging.info("Bot ishga tushdi! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
