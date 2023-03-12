from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
import pdb 

boggle_game = Boggle()
BOARD = 'board'
NUM_PLAYS = 'num_plays'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrets_dont_make_friends'

debug = DebugToolbarExtension(app)

@app.route('/')
def show_index():
    """ Shows game page"""

    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 1)
    session[BOARD] = boggle_game.make_board()
    return render_template('index.html', board = session[BOARD], highscore = highscore, num_plays = num_plays)

@app.route('/check', methods=['POST'])
def check_word():
    """ 
        Recieves submited word, 
        excutes function to check validity 
        and returns result
    """

    data = request.get_json()
    word = data['params']['word']
    # word = request.form.get('word')
    board = session[BOARD]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result' : result})

@app.route('/score', methods=['POST'])
def scores():
    """
        Recieves just completed game's score;
        Evalutes highscore;
        Increments number of games played;
        Returns highscore and number of games played
    """

    data = request.get_json()
    new_score = data['params']['new_score']

    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 1)

    session['highscore'] = max(new_score, highscore)
    session['num_plays'] = num_plays + 1

    return jsonify({'high_score' : session['highscore'], 'num_plays' : session['num_plays']})
