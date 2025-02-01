CREATE TABLE IF NOT EXISTS active_users (
    email TEXT PRIMARY KEY,
    spreadsheet_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 