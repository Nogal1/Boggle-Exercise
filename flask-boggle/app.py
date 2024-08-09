from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecret"

boggle_game = Boggle()

def get_session_data():
    """Retrieve highscore and nplays from session."""
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return highscore, nplays

@app.route("/")
def homepage():
    """Show board."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore, nplays = get_session_data()

    return render_template("board.html", board=board,
                           highscore=highscore,
                           nplays=nplays)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""
    word = request.args.get("word")
    board = session.get("board")
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json.get("score", 0)
    highscore, nplays = get_session_data()

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)