from flask import Flask, render_template, request, jsonify

# 할일(Todo) 데이터 저장소
# todos = [ 
#   {'todo': '할일1', 'date': '날짜1', 'done': True }
#   {'todo': '할일2', 'date': '날짜2', 'done': False }
# ]

todos = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('todo_basic.html')

@app.route('/todo/upload', methods=['POST'])
def upload():
    incoming_data = request.get_json()
    global todos
    todos = incoming_data
    
    return jsonify({'status': '데이터 업로드 성공!'}), 200

@app.route('/todo/download', methods=['GET'])
def download():
    global todos
    return jsonify(todos), 200

@app.route('/todo/init', methods=['GET'])
def init():
    global todos
    todos = []
    return jsonify({'status': '초기화 성공!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)