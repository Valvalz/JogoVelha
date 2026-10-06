import math
import random


def check_winner(b):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for cond in win_conditions:
        if b[cond[0]] and b[cond[0]] == b[cond[1]] == b[cond[2]]:
            return b[cond[0]]
    if "" not in b:
        return "Draw"
    return None


def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score


def should_trigger_hard_bug(round_number):
    if round_number is None:
        return False
    try:
        round_number = int(round_number)
    except (TypeError, ValueError):
        return False
    return round_number >= 50 and round_number % 12 == 0


def _blunder_move(board, legal_moves):
    scored_moves = []
    for move in legal_moves:
        board[move] = "O"
        score = minimax(board, 0, False)
        board[move] = ""
        scored_moves.append((score, move))

    scored_moves.sort(key=lambda item: item[0])
    pool_size = max(1, min(3, len(scored_moves)))
    bug_pool = [move for _, move in scored_moves[:pool_size]]
    return random.choice(bug_pool)


def _hard_tuned_move(board, legal_moves):
    scored_moves = []
    for move in legal_moves:
        board[move] = "O"
        score = minimax(board, 0, False)
        board[move] = ""
        scored_moves.append({"move": move, "score": score})

    best_score = max(item["score"] for item in scored_moves)
    best_moves = [item for item in scored_moves if item["score"] == best_score]

    preference_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    best_moves.sort(key=lambda item: preference_order.index(item["move"]))

    if len(best_moves) == 1:
        return best_moves[0]["move"]

    if random.random() < 0.82:
        return best_moves[0]["move"]

    return random.choice([item["move"] for item in best_moves])


def choose_move_by_difficulty(board, difficulty, round_number=None):
    legal_moves = [i for i, value in enumerate(board) if value == ""]
    if not legal_moves:
        return None

    if difficulty == "easy":
        return random.choice(legal_moves)

    if difficulty == "normal":
        best_move = None
        best_score = -math.inf
        for move in legal_moves:
            board[move] = "O"
            score = minimax(board, 0, False)
            board[move] = ""
            if score > best_score:
                best_score = score
                best_move = move
        if best_move is not None:
            if random.random() < 0.25:
                return random.choice(legal_moves)
            return best_move
        return legal_moves[0]

    if difficulty == "hard":
        if should_trigger_hard_bug(round_number):
            return _blunder_move(board, legal_moves)

        return _hard_tuned_move(board, legal_moves)

    return legal_moves[0]
