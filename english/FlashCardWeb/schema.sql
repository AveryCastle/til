DROP TABLE IF EXISTS active_users;

CREATE TABLE IF NOT EXISTS active_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    spreadsheet_id TEXT NOT NULL,
    credentials BLOB,
    last_move_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
