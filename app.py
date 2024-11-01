from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Sử dụng SQLite cho đơn giản
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    # Quan hệ với User
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        username = request.form['username']
        session['current_receiver'] = username  # Lưu username vào session
        return redirect(url_for('messages', username=username))

    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Lưu mật khẩu dưới dạng văn bản thuần
        new_user = User(username=username, password=password)  # Không băm mật khẩu
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # So sánh mật khẩu trực tiếp

            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/messages/<username>', methods=['GET', 'POST'])
@login_required
def messages(username):
    if request.method == 'POST':
        content = request.form['content']
        receiver = User.query.filter_by(username=username).first()
        if receiver:
            new_message = Message(sender_id=current_user.id, receiver_id=receiver.id, content=content)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('messages', username=username))

    receiver = User.query.filter_by(username=username).first()
    if not receiver:
        return redirect(url_for('home'))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == receiver.id)) |
        ((Message.sender_id == receiver.id) & (Message.receiver_id == current_user.id))
    ).all()

    return render_template('messages.html', messages=messages, receiver=receiver)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():  # Thiết lập context ứng dụng
        db.create_all()  # Tạo các bảng trong DB
    app.run(debug=True, host='0.0.0.0')