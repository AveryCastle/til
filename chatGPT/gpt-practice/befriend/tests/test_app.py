import os
import sys
import pytest
from werkzeug.security import generate_password_hash

# 현재 디렉토리를 sys.path에 추가하여 app 모듈을 찾을 수 있도록 함
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, Post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', json={
        'email': 'test@gmail.com',
        'password': '1234'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Registered successfully'
    user = User.query.filter_by(email='test@gmail.com').first()
    assert user is not None
    assert user.email == 'test@gmail.com'

def test_login(client):
    password = '1234'
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(email='test@gmail.com', password=hashed_password)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', json={
        'email': 'test@gmail.com',
        'password': password
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Login successful'

def test_post_creation(client):
    password = '1234'
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(email='test@gmail.com', password=hashed_password)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    client.post('/login', json={
        'email': 'test@gmail.com',
        'password': password
    })

    response = client.post('/post', json={
        'title': 'Test Title',
        'content': 'Test Content'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['message'] == 'Post created'
    post = Post.query.filter_by(title='Test Title').first()
    assert post is not None
    assert post.title == 'Test Title'
    assert post.content == 'Test Content'

def test_get_posts(client):
    password = '1234'
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(email='test@gmail.com', password=hashed_password)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    client.post('/login', json={
        'email': 'test@gmail.com',
        'password': password
    })

    client.post('/post', json={
        'title': 'Test Title',
        'content': 'Test Content'
    })

    response = client.get('/posts')
    json_data = response.get_json()
    assert response.status_code == 200
    assert 'posts' in json_data
    assert len(json_data['posts']) == 1
    assert json_data['posts'][0]['title'] == 'Test Title'
    assert json_data['posts'][0]['content'] == 'Test Content'
