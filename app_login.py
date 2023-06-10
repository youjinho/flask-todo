from flask import Flask, redirect, url_for, request, render_template, jsonify
# 로그인 관리 모듈 불러오기
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# 할일(Todo) 데이터 저장소
# todos['아이디'] = [ 
#   {'todo': '할일1', 'date': '날짜1', 'done': True }
#   {'todo': '할일2', 'date': '날짜2', 'done': False }
# ]
tododb = {}

@app.route('/home')
@login_required    # 로그인을 한 후에 호출될 수 있음
def home():
    return render_template('todo.html')

@app.route('/todo/upload', methods=['POST'])
@login_required
def upload():
    incoming_data = request.get_json()
    global tododb
    user_id = current_user.get_id()
    tododb[user_id] = incoming_data
    return jsonify({'status': '데이터 업로드 성공!'}), 200

@app.route('/todo/download', methods=['GET'])
@login_required
def download():
    global tododb
    user_id = current_user.get_id()
    todos = tododb.get(user_id, [])
    return jsonify(todos), 200

@app.route('/todo/init', methods=['GET'])
def init():
    global tododb
    tododb = {}
    return jsonify({'status': '초기화 성공!'}), 200


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
