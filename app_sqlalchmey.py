from flask import Flask, redirect, url_for, request, render_template, jsonify
# 로그인 관리 모듈 불러오기
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# pip install flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#  데이터베이스 초기화

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ScE1234**@localhost:3306/tododb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/tododb_sqlalchemy'

# create database tododb_sqlalchemy;
# drop database if exists tododb_sqlalchemy;

# Database connection
db = SQLAlchemy(app)

# Todos model
class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    todo = db.Column(db.String(100))
    date = db.Column(db.Date)
    done = db.Column(db.Boolean)

@app.route('/home')
@login_required    # 로그인을 한 후에 호출될 수 있음
def home():
    return render_template('todo.html')

@app.route('/todo/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    return jsonify({'status': '초기화 성공!'}), 200


@app.route('/todo/upload', methods=['POST'])
@login_required
def upload():
    # get the incoming data
    incoming_data = request.get_json()
    user_id=current_user.get_id()
    
    # Todos에서 현재 user_id의 todo 레코드들을 삭제
    Todos.query.filter_by(user_id=user_id).delete()

    # todo 레코드 추가
    for todo_item in incoming_data:
        todo = Todos(user_id=user_id, todo=todo_item['todo'], date=todo_item['date'], done=todo_item['done'])
        db.session.add(todo)

    db.session.commit()

    return jsonify({'status': '데이터 업로드 성공!'}), 200


@app.route('/todo/download', methods=['GET'])
@login_required
def download():
    todos = Todos.query.filter_by(user_id=current_user.get_id()).order_by(Todos.date).all()
    return jsonify([{'todo': t.todo, 'date': t.date.strftime("%Y-%m-%d"), 'done': t.done} for t in todos]), 200

########################  로그인 관리 #################################
# Flask-login setup
app.secret_key = 'super secret key'  # 이 부분을 실제로 사용할 때는 안전한 랜덤 키를 사용해야 합니다.

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        user = User(user_id)
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out.'

@app.route('/user_id')
@login_required
def user_id():
    return jsonify({'user_id' : current_user.get_id()})

########################  로그인 관리: end ##############################

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
