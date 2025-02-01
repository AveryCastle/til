import sqlite3
import click
from flask import current_app, g
import pickle
import logging

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

def save_user_credentials(email, credentials):
    """사용자의 credentials를 데이터베이스에 저장"""
    db = get_db()
    # credentials 객체를 바이너리로 직렬화
    pickled_credentials = pickle.dumps(credentials)
    db.execute('''
        UPDATE active_users 
        SET credentials = ? 
        WHERE email = ?
    ''', (pickled_credentials, email))
    db.commit()

def get_user_credentials(email):
    """데이터베이스에서 사용자의 credentials 조회"""
    db = get_db()
    result = db.execute(
        'SELECT credentials FROM active_users WHERE email = ?', 
        (email,)
    ).fetchone()
    if result and result[0]:
        return pickle.loads(result[0])
    return None

def get_user_last_move_date(email):
    """
    사용자의 마지막 시트 이동 날짜를 조회합니다.
    Args:
        email (str): 사용자 이메일
    Returns:
        str or None: 'YYYY-MM-DD' 형식의 날짜 문자열 또는 None
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("""
            SELECT strftime('%Y-%m-%d', last_move_date)
            FROM active_users 
            WHERE email = ?
        """, (email,))
        
        result = cursor.fetchone()
        return result[0] if result else None
        
    except Exception as e:
        logging.error(f"Error getting last move date: {str(e)}")
        return None

def update_last_move_date(email, move_date):
    """사용자의 마지막 시트 이동 날짜 업데이트"""
    db = get_db()
    db.execute(
        'UPDATE active_users SET last_move_date = ? WHERE email = ?',
        (move_date, email)
    )
    db.commit() 