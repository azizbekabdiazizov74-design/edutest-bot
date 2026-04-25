import aiosqlite
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path="bot.db"):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY, username TEXT, full_name TEXT,
                is_premium INTEGER DEFAULT 0, premium_until TEXT,
                daily_tests INTEGER DEFAULT 0, last_test_date TEXT,
                challenge_score INTEGER DEFAULT 0, last_challenge TEXT,
                notify INTEGER DEFAULT 1, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
            await db.execute("""CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
                subject TEXT, correct INTEGER, total INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
            await db.execute("""CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER, referred_id INTEGER UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
            await db.commit()

    async def add_user(self, user_id, username, full_name):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?,?,?)",
                (user_id, username, full_name))
            await db.commit()

    async def is_premium(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT is_premium, premium_until FROM users WHERE user_id=?", (user_id,)) as c:
                row = await c.fetchone()
                if not row or not row[0]: return False
                if row[1] and datetime.now() > datetime.fromisoformat(row[1]):
                    await db.execute("UPDATE users SET is_premium=0 WHERE user_id=?", (user_id,))
                    await db.commit()
                    return False
                return True

    async def set_premium(self, user_id, days):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT premium_until FROM users WHERE user_id=?", (user_id,)) as c:
                row = await c.fetchone()
            base = datetime.now()
            if row and row[0]:
                try:
                    existing = datetime.fromisoformat(row[0])
                    if existing > base: base = existing
                except: pass
            until = base + timedelta(days=days)
            await db.execute("UPDATE users SET is_premium=1, premium_until=? WHERE user_id=?",
                (until.isoformat(), user_id))
            await db.commit()

    async def get_daily_tests(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT daily_tests, last_test_date FROM users WHERE user_id=?", (user_id,)) as c:
                row = await c.fetchone()
                if not row: return 0
                today = datetime.now().date().isoformat()
                if row[1] != today:
                    await db.execute("UPDATE users SET daily_tests=0, last_test_date=? WHERE user_id=?", (today, user_id))
                    await db.commit()
                    return 0
                return row[0] or 0

    async def increment_daily_tests(self, user_id):
        today = datetime.now().date().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET daily_tests=daily_tests+1, last_test_date=? WHERE user_id=?",
                (today, user_id))
            await db.commit()

    async def save_test_result(self, user_id, subject, correct, total):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT INTO test_results (user_id,subject,correct,total) VALUES (?,?,?,?)",
                (user_id, subject, correct, total))
            await db.commit()

    async def get_recent_results(self, user_id, limit=5):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT subject,correct,total FROM test_results WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)) as c:
                return [{"subject":r[0],"correct":r[1],"total":r[2]} for r in await c.fetchall()]

    async def get_user_stats(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*), AVG(CAST(correct AS FLOAT)/total*100), MAX(CAST(correct AS FLOAT)/total*100) FROM test_results WHERE user_id=?",
                (user_id,)) as c:
                r = await c.fetchone()
                return {"total_tests":r[0] or 0,"avg_score":r[1] or 0,"best_score":r[2] or 0}

    async def check_daily_challenge(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT last_challenge, challenge_score FROM users WHERE user_id=?", (user_id,)) as c:
                row = await c.fetchone()
                if not row: return None
                today = datetime.now().date().isoformat()
                if row[0] == today: return row[1]
                return None

    async def save_challenge(self, user_id, score):
        today = datetime.now().date().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET last_challenge=?, challenge_score=challenge_score+? WHERE user_id=?",
                (today, score, user_id))
            await db.commit()

    async def get_leaderboard(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT u.user_id, u.full_name,
                    COUNT(t.id) as total_tests,
                    AVG(CAST(t.correct AS FLOAT)/t.total*100) as avg_score,
                    u.challenge_score
                FROM users u LEFT JOIN test_results t ON u.user_id=t.user_id
                GROUP BY u.user_id HAVING total_tests > 0
                ORDER BY avg_score DESC, challenge_score DESC LIMIT 10""") as c:
                return [{"user_id":r[0],"full_name":r[1],"total_tests":r[2],"avg_score":r[3] or 0,"challenge_score":r[4] or 0}
                    for r in await c.fetchall()]

    async def get_user_rank(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT rank FROM (
                    SELECT user_id, ROW_NUMBER() OVER (ORDER BY AVG(CAST(correct AS FLOAT)/total*100) DESC) as rank
                    FROM test_results GROUP BY user_id
                ) WHERE user_id=?""", (user_id,)) as c:
                row = await c.fetchone()
                return row[0] if row else None

    async def add_referral(self, referrer_id, referred_id):
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("INSERT INTO referrals (referrer_id, referred_id) VALUES (?,?)",
                    (referrer_id, referred_id))
                await db.commit()
                return True
            except: return False

    async def get_referral_count(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (user_id,)) as c:
                return (await c.fetchone())[0]

    async def get_all_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id FROM users WHERE notify=1") as c:
                return [r[0] for r in await c.fetchall()]

    async def set_notify(self, user_id, val):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET notify=? WHERE user_id=?", (val, user_id))
            await db.commit()

    async def get_global_stats(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as c: users = (await c.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM users WHERE is_premium=1") as c: premium = (await c.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM test_results") as c: tests = (await c.fetchone())[0]
            return {"users":users,"premium":premium,"tests":tests}
