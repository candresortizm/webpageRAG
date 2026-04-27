import sqlite3

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db_path = "chat_history.db"
        self._init_db()
        self._initialized = True

    def _get_connection(self):
        # En SQLite, es mejor abrir la conexión por hilo o petición
        # pero centralizamos la configuración aquí.
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    human TEXT,
                    ai TEXT,
                    source TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            conn.commit()

    def save_message(self, conversation_id, human, ai):
        with self._get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO conversations (id) VALUES (?)", (conversation_id,))
            conn.execute(
                "INSERT INTO messages (conversation_id, human, ai) VALUES (?, ?, ?)",
                (conversation_id, human, ai)
            )
            conn.commit()

    def get_history(self, conversation_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT human, ai FROM messages WHERE conversation_id = ? ORDER BY id ASC",
                (conversation_id,)
            )
            return cursor.fetchall()
