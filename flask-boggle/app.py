from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"

boggle_game = Boggle()

@app.route("/")
def display_board():
    """Generate and display the Boggle board."""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("board.html", board=board)

@app.route("/check-word", methods=["POST"])
def check_word():
    """Check if a word is valid and exists on the board."""
    word = request.json["word"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, word)

    return jsonify({"result": result})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Update the number of games played and the highest score."""
    score = request.json["score"]
    high_score = session.get("high_score", 0)
    games_played = session.get("games_played", 0)

    session["high_score"] = max(score, high_score)
    session["games_played"] = games_played + 1

    return jsonify({"high_score": session["high_score"], "games_played": session["games_played"]})


