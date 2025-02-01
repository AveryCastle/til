import sqlite3
import click
from flask import current_app, g

DATABASE = 'flashcard.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    """데이터베이스 초기화"""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def add_active_user(email, spreadsheet_id):
    """사용자를 active_users 테이블에 추가/업데이트"""
    db = get_db()
    db.execute(
        'INSERT OR REPLACE INTO active_users (email, spreadsheet_id) VALUES (?, ?)',
        (email, spreadsheet_id)
    )
    db.commit() 