from flask import Flask, request, render_template
import os
import chess
import cv2
import tempfile
import numpy as np
from extract_image.fen_from_image import fen_from_imag
from chess_helper_functions.chess import get_best_move,display_board_with_arrow,print_game_state
from chess_helper_functions.chess import detect_board_orientation

app = Flask(__name__)

import os
import chess
from chess_helper_functions.chess import get_best_move, display_board_with_arrow, print_game_state

def analyze_chess_position(fen, play_as):
    # Append the play_as information to the FEN
    if play_as == 'white':
        fen += ' w'
    else:
        fen += ' b'

    # Get the best move and evaluation
    best_move, evaluation = get_best_move(fen)

    # Display the chessboard with the best move
    board = chess.Board(fen)
    board.push(best_move)
    board_svg = display_board_with_arrow(board, best_move.from_square, best_move.to_square)
    board_svg = board_svg.split('/')[1]

    game_state = print_game_state(board, evaluation)

    return fen, board_svg, game_state, best_move, evaluation


# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request"

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty part without a filename
        if file.filename == '':
            return "No selected file"
        if file:
            # Save the image to a temporary location
            temp_image_fd, temp_image_path = tempfile.mkstemp(suffix=".jpg")

            # Save the uploaded image to the temporary file
            file.save(temp_image_path)
            # Get the FEN from the image
            fen = fen_from_imag(temp_image_path)

            fen=detect_board_orientation(fen)

            play_as = request.form.get('play_as', '')
            fen, board_svg, game_state, best_move, evaluation = analyze_chess_position(fen, play_as)

            os.close(temp_image_fd)
            os.remove(temp_image_path)



            return render_template('results.html', fen=fen, board_svg=board_svg, game_state=game_state,best_move=best_move,evaluation=evaluation,play_as=play_as)

    return render_template('index.html')

@app.route('/new', methods=['GET'])
def flip():
    fen= request.args.get('fen')
    fen=fen[:-2][::-1]
    play_as=request.args.get('play_as')
    fen, board_svg, game_state, best_move, evaluation = analyze_chess_position(fen, play_as)
    return render_template('results.html', fen=fen, board_svg=board_svg, game_state=game_state,best_move=best_move,evaluation=evaluation,play_as=play_as)


if __name__ == '__main__':
    app.run(port=5001,debug=True)


