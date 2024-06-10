from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed'})
    login_user(user)
    return jsonify({'message': 'Login successful'})

@app.route('/post', methods=['POST'])
@login_required
def post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], author=current_user)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created'})

@app.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = Post.query.all()
    output = []
    for post in posts:
        post_data = {'title': post.title, 'content': post.content}
        output.append(post_data)
    return jsonify({'posts': output})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
