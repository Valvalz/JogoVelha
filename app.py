from flask import Flask, send_file, request, jsonify
from IA import choose_move_by_difficulty

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('home.html')

@app.route('/home')
def home_page():
    return send_file('home.html')

@app.route('/index')
def index_page():
    return send_file('index.html')

@app.route('/index.html')
def index_html_page():
    return send_file('index.html')

@app.route('/home.html')
def home_html_page():
    return send_file('home.html')

@app.route('/game')
def game():
    return send_file('index.html')

@app.route('/ai-move', methods=['POST'])
def ai_move():
    data = request.get_json(silent=True) or {}
    board = data.get('board')
    difficulty = data.get('difficulty', 'normal')
    round_number = data.get('round')

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"move": None, "error": "tabuleiro inválido"}), 400

    board_copy = [cell for cell in board]
    move = choose_move_by_difficulty(board_copy, difficulty, round_number)
    return jsonify({"move": move})

if __name__ == '__main__':
    app.run(debug=True)