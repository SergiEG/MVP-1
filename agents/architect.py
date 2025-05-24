# agents/architect.py

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "agent_data.db"

class ArchitectAgent:
    """
    AI-агент «Архитектор-Администратор»
    Хранит задачи и память в SQLite и умеет их очищать.
    """

    def __init__(self):
        # Открываем (или создаём) файл базы рядом с проектом
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        """Создаём таблицу tasks, если она ещё не существует."""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                command   TEXT    NOT NULL
            )
        """)
        self.conn.commit()

    def respond_to_command(self, command: str) -> str:
        """Сохраняем команду в БД и возвращаем подтверждение."""
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (timestamp, command) VALUES (?,?)",
            (now, command)
        )
        self.conn.commit()
        return f"Я получил команду «{command}» и запланировал её выполнение."

    def list_tasks(self) -> list[tuple]:
        """Возвращает все записи из tasks: [(id, timestamp, command), ...]."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, timestamp, command FROM tasks ORDER BY id")
        return cur.fetchall()

    def show_memory(self) -> list[tuple]:
        """
        Возвращает те же записи, что list_tasks().
        Оставлено для будущего разделения memory ↔ tasks.
        """
        return self.list_tasks()

    def run_diagnostic(self) -> str:
        """Проверяет доступность БД."""
        try:
            self.conn.execute("SELECT 1")
            return "✅ БД работает корректно"
        except Exception as e:
            return f"❌ Ошибка БД: {e}"

    def clear_tasks(self) -> str:
        """Удаляет все записи из tasks."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks")
        self.conn.commit()
        return "🗑️ Список задач очищен."

    def clear_memory(self) -> str:
        """
        Удаляет все записи памяти.
        Пока memory == tasks, дублируем удаление.
        """
        return self.clear_tasks()
