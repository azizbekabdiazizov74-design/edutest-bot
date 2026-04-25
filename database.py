import aiosqlite
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_path="bot.db"):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    is_premium INTEGER DEFAULT 0,
                    premium_until TEXT,
                    daily_tests INTEGER DEFAULT 0,
                    last_test_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    subject TEXT,
                    correct INTEGER,
                    total INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int, username: str, full_name: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (user_id, username, full_name)
                VALUES (?, ?, ?)
            """, (user_id, username, full_name))
            await db.commit()

    async def is_premium(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT is_premium, premium_until FROM users WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return False
                is_premium, premium_until = row
                if not is_premium:
                    return False
                if premium_until:
                    until = datetime.fromisoformat(premium_until)
                    if datetime.now() > until:
                        # Premium muddati tugagan
                        await db.execute(
                            "UPDATE users SET is_premium = 0 WHERE user_id = ?",
                            (user_id,)
                        )
                        await db.commit()
                        return False
                return True

    async def set_premium(self, user_id: int, days: int):
        until = datetime.now() + timedelta(days=days)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users SET is_premium = 1, premium_until = ?
                WHERE user_id = ?
            """, (until.isoformat(), user_id))
            await db.commit()

    async def get_daily_tests(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT daily_tests, last_test_date FROM users WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return 0
                daily_tests, last_date = row
                today = datetime.now().date().isoformat()
                if last_date != today:
                    # Yangi kun — testlar sifirlanadi
                    await db.execute(
                        "UPDATE users SET daily_tests = 0, last_test_date = ? WHERE user_id = ?",
                        (today, user_id)
                    )
                    await db.commit()
                    return 0
                return daily_tests or 0

    async def increment_daily_tests(self, user_id: int):
        today = datetime.now().date().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users SET
                    daily_tests = daily_tests + 1,
                    last_test_date = ?
                WHERE user_id = ?
            """, (today, user_id))
            await db.commit()

    async def save_test_result(self, user_id: int, subject: str, correct: int, total: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO test_results (user_id, subject, correct, total)
                VALUES (?, ?, ?, ?)
            """, (user_id, subject, correct, total))
            await db.commit()

    async def get_recent_results(self, user_id: int, limit: int = 5) -> list:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT subject, correct, total, created_at
                FROM test_results
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {"subject": r[0], "correct": r[1], "total": r[2], "date": r[3]}
                    for r in rows
                ]

    async def get_user_stats(self, user_id: int) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT
                    COUNT(*) as total,
                    AVG(CAST(correct AS FLOAT) / total * 100) as avg_score,
                    MAX(CAST(correct AS FLOAT) / total * 100) as best_score
                FROM test_results WHERE user_id = ?
            """, (user_id,)) as cursor:
                row = await cursor.fetchone()
                return {
                    "total_tests": row[0] or 0,
                    "avg_score": row[1] or 0,
                    "best_score": row[2] or 0
                }

    async def get_global_stats(self) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as c:
                users = (await c.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM users WHERE is_premium = 1") as c:
                premium = (await c.fetchone())[0]
            async with db.execute("SELECT COUNT(*) FROM test_results") as c:
                tests = (await c.fetchone())[0]
            return {"users": users, "premium": premium, "tests": tests}
