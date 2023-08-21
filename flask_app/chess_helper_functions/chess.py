import chess 
import tempfile
import chess.svg
import chess.engine

def get_best_move(fen):
    # Create a chess.Board from the FEN string
    board = chess.Board(fen)

    # Initialize Stockfish engine
    stockfish_path = "essentials\stockfish-windows-x86-64-modern.exe"  # Replace with the path to your Stockfish executable
    stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Get the best move from Stockfish
    analysis = stockfish.analyse(board, chess.engine.Limit(time=4.0))

        # Get the evaluation score from the analysis info
    evaluation = analysis["score"].white().score(mate_score=10000) / 100.0  # Convert to centipawns

        # Get the best move from the analysis info
    best_move = analysis["pv"][0]
    # Close the Stockfish engine
    stockfish.quit()

    return best_move,evaluation

def display_board_with_arrow(board, from_square, to_square,path='static/chessboard.svg'):
    arrow = chess.svg.Arrow(from_square, to_square, color="red")
    svg_content = chess.svg.board(board=board, arrows=[arrow])
    with open(path, 'w') as f:
        f.write(svg_content)
    return path
    

def print_game_state(board, evaluation):


    if board.is_checkmate():
        return("Checkmate! The game is over.")
    elif board.is_check():
        return("Check! The opponent is in check.")
    elif board.is_stalemate():
        return("Stalemate! The game is a draw due to stalemate.")
    elif board.is_insufficient_material():
        return("Insufficient material! The game is a draw due to insufficient material.")
    elif board.is_seventyfive_moves():
        return("Draw! The game is a draw due to the 75-move rule.")
    elif board.is_fivefold_repetition():
        return("Draw! The game is a draw due to fivefold repetition.")
    

    if evaluation<=2 and evaluation>0.5:
        return('White is slightly better')
    elif evaluation>2:
        return('White is winning')
    elif evaluation>=-0.5 and evaluation<=0.5:
        return('Position is almost equal')
    elif evaluation>-2 and evaluation<-0.5:
        return('Black is slightly better')
    else:
        return('Black is winning')
    
def detect_board_orientation(f):
    fen=f
    fen=''.join(fen.split())
    pos_of_wk=fen.find('K')//8
    pos_of_bk=fen.find('k')//8
    if pos_of_wk<pos_of_bk:
        return f[::-1]
    return f
