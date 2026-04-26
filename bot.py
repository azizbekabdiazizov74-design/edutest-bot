import logging
import asyncio
import os
import random
import aiohttp
import json
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
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY")
MONTHLY_PRICE = 29900
YEARLY_PRICE = 199000
FREE_TESTS_PER_DAY = 3

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()

# ===== GEMINI AI =====
async def ask_gemini(prompt: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        async with aiohttp.ClientSession() as session:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
                data = await resp.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                elif "error" in data:
                    return f"❌ API xato: {data['error'].get('message', 'Noma\'lum xato')}"
                else:
                    return "❌ Javob olishda xato yuz berdi. Qayta urinib ko'ring."
    except Exception as e:
        return f"❌ Xato yuz berdi: {str(e)}"

# ===== STATES =====
class TestState(StatesGroup):
    choosing_subject = State()
    choosing_count = State()
    answering = State()

class PaymentState(StatesGroup):
    waiting_receipt = State()

class AIState(StatesGroup):
    referat_topic = State()
    konspekt_topic = State()
    qa_question = State()
    search_query = State()

# ===== KLAVIATURALAR =====
def main_menu_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📚 Test boshlash"), KeyboardButton(text="🎯 Kunlik challenge")],
        [KeyboardButton(text="🏆 Reyting"), KeyboardButton(text="👥 Referal")],
        [KeyboardButton(text="📝 Referat yozish"), KeyboardButton(text="📖 Konspekt")],
        [KeyboardButton(text="💬 AI Yordamchi"), KeyboardButton(text="🔍 Qidiruv")],
        [KeyboardButton(text="📝 DTM Simulyatsiya"), KeyboardButton(text="⭐ Premium")],
        [KeyboardButton(text="📊 Natijalarim"), KeyboardButton(text="👤 Profil")],
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

# ===== START =====
@dp.message(CommandStart())
async def start(message: types.Message):
    user = message.from_user
    args = message.text.split()
    await db.add_user(user.id, user.username, user.full_name)
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].replace("ref_", ""))
            if referrer_id != user.id:
                added = await db.add_referral(referrer_id, user.id)
                if added:
                    ref_count = await db.get_referral_count(referrer_id)
                    days = 30 if ref_count >= 10 else 7 if ref_count >= 5 else 3 if ref_count >= 3 else 1
                    await db.set_premium(referrer_id, days)
                    await bot.send_message(referrer_id, f"🎉 Yangi do'st! Jami: {ref_count}\n🎁 +{days} kun Premium!")
        except: pass
    await message.answer(
        f"👋 Salom, <b>{user.first_name}</b>!\n\n"
        f"🎓 <b>SmartTalaba Bot</b>\n\n"
        f"📚 Test ishlash\n🎯 Kunlik challenge\n"
        f"📝 AI bilan referat yozish\n"
        f"📖 Konspekt yaratish\n"
        f"💬 AI yordamchi\n🔍 Qidiruv\n"
        f"🏆 Reyting tizimi\n\n"
        f"Bepul: kuniga {FREE_TESTS_PER_DAY} ta test",
        reply_markup=main_menu_kb(), parse_mode="HTML")

# ===== REFERAT =====
@dp.message(F.text == "📝 Referat yozish")
async def referat_start(message: types.Message, state: FSMContext):
    await message.answer(
        "📝 <b>Referat yozish</b>\n\n"
        "Qaysi mavzuda referat kerak?\n"
        "Masalan: <i>O'zbekiston tarixi, Fotosintez, Matematik analiz</i>",
        parse_mode="HTML")
    await state.set_state(AIState.referat_topic)

@dp.message(AIState.referat_topic)
async def write_referat(message: types.Message, state: FSMContext):
    topic = message.text
    await state.clear()
    wait_msg = await message.answer("⏳ Referat yozilmoqda... (30-60 soniya)")
    
    prompt = f"""O'zbek tilida '{topic}' mavzusida to'liq referat yoz.
Tuzilishi:
1. Kirish (100-150 so'z)
2. Asosiy qism (3-4 bo'lim, har biri 200-300 so'z)
3. Xulosa (100 so'z)
4. Foydalanilgan adabiyotlar (5 ta)

Ilmiy uslubda, to'liq va sifatli yoz."""

    result = await ask_gemini(prompt)
    await wait_msg.delete()
    
    # Uzun matnni bo'lib yuborish
    if len(result) > 4000:
        parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
        for i, part in enumerate(parts):
            await message.answer(f"📝 <b>Referat ({i+1}/{len(parts)}):</b>\n\n{part}", parse_mode="HTML")
            await asyncio.sleep(0.5)
    else:
        await message.answer(f"📝 <b>Referat: {topic}</b>\n\n{result}", parse_mode="HTML")
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Boshqa mavzu", callback_data="new_referat")
    await message.answer("✅ Referat tayyor!", reply_markup=builder.as_markup())

# ===== KONSPEKT =====
@dp.message(F.text == "📖 Konspekt")
async def konspekt_start(message: types.Message, state: FSMContext):
    await message.answer(
        "📖 <b>Konspekt yaratish</b>\n\n"
        "Qaysi mavzu yoki fan bo'yicha konspekt kerak?\n"
        "Masalan: <i>Termodinamika 1-qonun, SQL asoslari</i>",
        parse_mode="HTML")
    await state.set_state(AIState.konspekt_topic)

@dp.message(AIState.konspekt_topic)
async def write_konspekt(message: types.Message, state: FSMContext):
    topic = message.text
    await state.clear()
    wait_msg = await message.answer("⏳ Konspekt tayyorlanmoqda...")

    prompt = f"""O'zbek tilida '{topic}' mavzusida qisqa va aniq konspekt yoz.
Format:
📌 Asosiy tushunchalar
📋 Muhim ta'riflar  
🔑 Kalit formulalar/qoidalar
💡 Misollar
❓ Nazorat savollari (5 ta)

Strukturali, o'qishga qulay qilib yoz."""

    result = await ask_gemini(prompt)
    await wait_msg.delete()
    
    if len(result) > 4000:
        parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
        for i, part in enumerate(parts):
            await message.answer(f"📖 <b>Konspekt ({i+1}/{len(parts)}):</b>\n\n{part}", parse_mode="HTML")
            await asyncio.sleep(0.5)
    else:
        await message.answer(f"📖 <b>Konspekt: {topic}</b>\n\n{result}", parse_mode="HTML")

# ===== AI YORDAMCHI =====
@dp.message(F.text == "💬 AI Yordamchi")
async def qa_start(message: types.Message, state: FSMContext):
    await message.answer(
        "💬 <b>AI Yordamchi</b>\n\n"
        "Istalgan savolingizni bering!\n"
        "Masalan:\n"
        "• <i>Integral nima?</i>\n"
        "• <i>Essay qanday yoziladi?</i>\n"
        "• <i>Fotosintezni tushuntir</i>",
        parse_mode="HTML")
    await state.set_state(AIState.qa_question)

@dp.message(AIState.qa_question)
async def answer_qa(message: types.Message, state: FSMContext):
    question = message.text
    wait_msg = await message.answer("💭 O'ylanmoqda...")

    prompt = f"""Sen o'zbek tilida javob beruvchi aqlli o'qituvchisan.
Savol: {question}

Aniq, tushunarli va qisqa javob ber. Kerak bo'lsa misollar keltir."""

    result = await ask_gemini(prompt)
    await wait_msg.delete()
    await message.answer(f"💬 <b>Javob:</b>\n\n{result}", parse_mode="HTML")
    
    builder = InlineKeyboardBuilder()
    builder.button(text="❓ Yana savol", callback_data="new_qa")
    builder.button(text="🏠 Bosh menyu", callback_data="main_menu")
    builder.adjust(2)
    await message.answer("Yana savol berishingiz mumkin yoki boshqa xizmatdan foydalaning!", reply_markup=builder.as_markup())

# ===== QIDIRUV =====
@dp.message(F.text == "🔍 Qidiruv")
async def search_start(message: types.Message, state: FSMContext):
    await message.answer(
        "🔍 <b>Qidiruv</b>\n\n"
        "Nima haqida ma'lumot kerak?\n"
        "Masalan: <i>Albert Einstein, Kvant fizikasi, O'zbekiston</i>",
        parse_mode="HTML")
    await state.set_state(AIState.search_query)

@dp.message(AIState.search_query)
async def do_search(message: types.Message, state: FSMContext):
    query = message.text
    await state.clear()
    wait_msg = await message.answer("🔍 Qidirilmoqda...")

    prompt = f"""'{query}' haqida O'zbek tilida to'liq va aniq ma'lumot ber.
Quyidagilarni o'z ichiga ol:
📌 Asosiy ma'lumot
📅 Muhim sanalar (agar mavjud)
🌟 Qiziqarli faktlar
📚 Qo'shimcha o'rganish uchun tavsiyalar"""

    result = await ask_gemini(prompt)
    await wait_msg.delete()
    
    if len(result) > 4000:
        parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
        for part in parts:
            await message.answer(part, parse_mode="HTML")
            await asyncio.sleep(0.3)
    else:
        await message.answer(f"🔍 <b>{query}</b>\n\n{result}", parse_mode="HTML")

# ===== TEST =====
@dp.message(F.text == "📚 Test boshlash")
async def start_test(message: types.Message, state: FSMContext):
    if not await db.is_premium(message.from_user.id) and await db.get_daily_tests(message.from_user.id) >= FREE_TESTS_PER_DAY:
        await message.answer(f"⚠️ Bugungi bepul testlar tugadi!\n\n⭐ Premium — cheksiz testlar!\n<b>{MONTHLY_PRICE:,} so'm/oy</b>",
            reply_markup=premium_kb(), parse_mode="HTML")
        return
    await message.answer("📚 <b>Fan tanlang:</b>", reply_markup=subjects_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_subject)

@dp.message(F.text == "🎯 Kunlik challenge")
async def daily_challenge(message: types.Message, state: FSMContext):
    done = await db.check_daily_challenge(message.from_user.id)
    if done is not None:
        await message.answer(f"✅ Bugungi challenge bajarildi!\n🏆 Jami ball: <b>{done}</b>\n⏰ Keyingi: ertaga!", parse_mode="HTML")
        return
    questions = get_questions("aralash", 5)
    await state.update_data(questions=questions, current_q=0, correct=0, count=5, is_challenge=True, is_dtm=False)
    await message.answer("🎯 <b>Kunlik Challenge!</b>\n\n5 savol — har to'g'ri +10 ball\n5/5 → +20 bonus! 🎁", parse_mode="HTML")
    await send_question(message.chat.id, state, bot)
    await state.set_state(TestState.answering)

@dp.message(F.text == "📝 DTM Simulyatsiya")
async def dtm_mode(message: types.Message, state: FSMContext):
    if not await db.is_premium(message.from_user.id):
        await message.answer("📝 <b>DTM Simulyatsiya — Premium!</b>\n\n90 savol, haqiqiy DTM sharoiti\n\n"
            f"⭐ <b>{MONTHLY_PRICE:,} so'm/oy</b>", reply_markup=premium_kb(), parse_mode="HTML")
        return
    questions = get_questions("aralash", 90)
    await state.update_data(questions=questions, current_q=0, correct=0, count=len(questions), is_dtm=True, is_challenge=False)
    await message.answer("📝 <b>DTM Simulyatsiya!</b>\n90 ta savol\nOmad! 🍀", parse_mode="HTML")
    await send_question(message.chat.id, state, bot)
    await state.set_state(TestState.answering)

@dp.message(F.text == "🏆 Reyting")
async def leaderboard(message: types.Message):
    top = await db.get_leaderboard()
    if not top:
        await message.answer("🏆 Hozircha reyting yo'q!")
        return
    medals = ["🥇","🥈","🥉"]
    text = "🏆 <b>Top o'quvchilar</b>\n\n"
    for i, u in enumerate(top):
        medal = medals[i] if i < 3 else f"{i+1}."
        text += f"{medal} <b>{u['full_name'] or 'Noma\'lum'}</b> — {u['avg_score']:.0f}%\n"
    rank = await db.get_user_rank(message.from_user.id)
    if rank: text += f"\n📍 Sizning o'rningiz: <b>{rank}-o'rin</b>"
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == "👥 Referal")
async def referral(message: types.Message):
    uid = message.from_user.id
    ref_count = await db.get_referral_count(uid)
    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{uid}"
    await message.answer(
        f"👥 <b>Do'stlarni taklif qil!</b>\n\n"
        f"🔗 <code>{ref_link}</code>\n\n"
        f"👤 Taklif: <b>{ref_count} kishi</b>\n\n"
        f"🎁 1 do'st → 1 kun\n3 do'st → 3 kun\n5 do'st → 7 kun\n10 do'st → 30 kun Premium",
        parse_mode="HTML")

@dp.callback_query(F.data.startswith("subject_"))
async def choose_subject(callback: types.CallbackQuery, state: FSMContext):
    subject = callback.data.replace("subject_", "")
    await state.update_data(subject=subject, is_challenge=False, is_dtm=False)
    await callback.message.edit_text("📝 <b>Nechta savol?</b>", reply_markup=question_count_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_count)

@dp.callback_query(F.data.startswith("count_"))
async def choose_count(callback: types.CallbackQuery, state: FSMContext):
    count = int(callback.data.replace("count_", ""))
    data = await state.get_data()
    questions = get_questions(data.get("subject"), count)
    if not questions:
        await callback.message.edit_text("❌ Savollar yo'q!")
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
    is_challenge = data.get("is_challenge", False)
    is_dtm = data.get("is_dtm", False)
    progress = "▓" * current + "░" * (total - current)
    prefix = "🎯" if is_challenge else "📝 DTM" if is_dtm else "📚"
    await bot.send_message(chat_id,
        f"{prefix} <b>{current+1}/{total}</b>  {progress}\n\n❓ <b>{q['question']}</b>",
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
    correct, total = data["correct"], data["count"]
    subject = data.get("subject", "aralash")
    is_challenge = data.get("is_challenge", False)
    pct = (correct / total) * 100
    if pct >= 90: grade, msg = "🏆 A'lo!", "Ajoyib! 🌟"
    elif pct >= 70: grade, msg = "👍 Yaxshi", "Davom eting!"
    elif pct >= 50: grade, msg = "😐 Qoniqarli", "Mashq qiling!"
    else: grade, msg = "📚 Qoniqarsiz", "Ko'proq o'qing!"
    await db.save_test_result(chat_id, subject, correct, total)
    if not is_challenge: await db.increment_daily_tests(chat_id)
    extra = ""
    if is_challenge:
        ball = correct * 10 + (20 if correct == total else 0)
        await db.save_challenge(chat_id, ball)
        extra = f"\n🎯 Ball: <b>+{ball}</b>"
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Qayta", callback_data="restart_test")
    builder.button(text="🏆 Reyting", callback_data="show_leaderboard")
    builder.adjust(2)
    await bot.send_message(chat_id,
        f"🎯 <b>Yakunlandi!</b>\n📊 <b>{correct}/{total}</b> — {pct:.0f}%{extra}\n\n{grade} {msg}",
        reply_markup=builder.as_markup(), parse_mode="HTML")
    await state.clear()

@dp.message(F.text == "👤 Profil")
async def profile(message: types.Message):
    uid = message.from_user.id
    stats = await db.get_user_stats(uid)
    is_premium = await db.is_premium(uid)
    ref_count = await db.get_referral_count(uid)
    rank = await db.get_user_rank(uid)
    await message.answer(
        f"👤 <b>{message.from_user.full_name}</b>\n\n"
        f"💎 {'⭐ Premium' if is_premium else '🆓 Bepul'}\n"
        f"📊 Testlar: {stats['total_tests']}\n"
        f"🎯 O'rtacha: {stats['avg_score']:.1f}%\n"
        f"🏆 Reyting: {rank or '-'}-o'rin\n"
        f"👥 Referal: {ref_count} kishi", parse_mode="HTML")

@dp.message(F.text == "📊 Natijalarim")
async def results(message: types.Message):
    res = await db.get_recent_results(message.from_user.id)
    if not res:
        await message.answer("📊 Hozircha natijalar yo'q!")
        return
    emojis = {"matematika":"🔢","ingliz":"🌍","ozbek":"📖","kimyo":"⚗️","biologiya":"🔬","fizika":"⚡","geografiya":"🌐","tarix":"📜","informatika":"💻","aralash":"🎲"}
    text = "📊 <b>So'nggi natijalar:</b>\n\n"
    for r in res:
        pct = (r['correct']/r['total'])*100
        text += f"{emojis.get(r['subject'],'📚')} {r['subject'].title()}: <b>{r['correct']}/{r['total']}</b> ({pct:.0f}%)\n"
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == "⭐ Premium")
async def premium(message: types.Message):
    await message.answer(
        f"⭐ <b>SmartTalaba Premium</b>\n\n"
        f"✅ Cheksiz testlar\n✅ DTM simulyatsiya\n"
        f"✅ AI referat & konspekt\n✅ Statistika\n\n"
        f"📅 Oylik: <b>{MONTHLY_PRICE:,} so'm</b>\n"
        f"🎁 Yillik: <b>{YEARLY_PRICE:,} so'm</b>",
        reply_markup=premium_kb(), parse_mode="HTML")

@dp.callback_query(F.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery, state: FSMContext):
    plan = callback.data.replace("buy_", "")
    price = MONTHLY_PRICE if plan == "monthly" else YEARLY_PRICE
    await callback.message.edit_text(
        f"💳 <b>{'Oylik' if plan=='monthly' else 'Yillik'} — {price:,} so'm</b>\n\n"
        f"Karta: <code>{CARD_NUMBER}</code>\n\nChek rasmini yuboring.\nIzoh: <code>Premium {callback.from_user.id}</code>",
        parse_mode="HTML")
    await state.set_state(PaymentState.waiting_receipt)
    await state.update_data(plan=plan)

@dp.message(PaymentState.waiting_receipt, F.photo)
async def receipt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_ID,
        f"💳 To'lov!\n👤 {message.from_user.full_name}\n🆔 {message.from_user.id}\n"
        f"📦 {data.get('plan')}\n\n/approve {message.from_user.id} {data.get('plan')}")
    await message.answer("✅ Chek qabul qilindi!")
    await state.clear()

@dp.callback_query(F.data == "new_referat")
async def new_referat(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Yangi mavzuni yozing:")
    await state.set_state(AIState.referat_topic)

@dp.callback_query(F.data == "new_qa")
async def new_qa(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("❓ Savolingizni yozing:")
    await state.set_state(AIState.qa_question)

@dp.callback_query(F.data == "restart_test")
async def restart(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("📚 <b>Fan tanlang:</b>", reply_markup=subjects_kb(), parse_mode="HTML")
    await state.set_state(TestState.choosing_subject)

@dp.callback_query(F.data == "show_leaderboard")
async def cb_lb(callback: types.CallbackQuery):
    top = await db.get_leaderboard()
    if not top:
        await callback.answer("Reyting yo'q!", show_alert=True)
        return
    medals = ["🥇","🥈","🥉"]
    text = "🏆 <b>Top o'quvchilar</b>\n\n"
    for i, u in enumerate(top):
        medal = medals[i] if i < 3 else f"{i+1}."
        text += f"{medal} <b>{u['full_name'] or 'Noma\'lum'}</b> — {u['avg_score']:.0f}%\n"
    await callback.message.answer(text, parse_mode="HTML")

@dp.message(Command("approve"))
async def approve(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    parts = message.text.split()
    if len(parts) < 3: return
    uid, plan = int(parts[1]), parts[2]
    days = 30 if plan == "monthly" else 365
    await db.set_premium(uid, days)
    await message.answer(f"✅ {uid} ga {days} kun Premium!")
    await bot.send_message(uid, "🎉 <b>Premium faollashtirildi! 🚀</b>", parse_mode="HTML")

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    text = message.text.replace("/broadcast ", "")
    users = await db.get_all_users()
    sent = 0
    for uid in users:
        try:
            await bot.send_message(uid, text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05)
        except: pass
    await message.answer(f"📢 Yuborildi: {sent} ta")

@dp.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    s = await db.get_global_stats()
    await message.answer(f"📊 {s['users']} user | {s['premium']} premium | {s['tests']} test")

def get_questions(subject, count):
    all_q = [q for qs in QUESTIONS.values() for q in qs] if subject == "aralash" else QUESTIONS.get(subject, [])
    if not all_q: return []
    return random.sample(all_q, min(count, len(all_q)))

async def main():
    await db.init()
    logging.info("Bot ishga tushdi! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
