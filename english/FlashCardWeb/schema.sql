DROP TABLE IF EXISTS active_users;
CREATE TABLE active_users (
    email TEXT PRIMARY KEY,
    spreadsheet_id TEXT NOT NULL
); 