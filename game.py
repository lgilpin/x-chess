__author__ = "Leilani H. Gilpin"
__copyright__ = "Copyright 2019, Creative Commons"
__license__ = "GPL"
__maintainer__ = "Leilani H. Gilpin"
__email__ = "lhg@mit.edu"
__status__ = "Proof of concept"

# Important for chess 

import chess
import random
import time
import os
from IPython.display import display, HTML, clear_output

def get_piece_name(piece):
    letter = piece.symbol.lower()
    if letter == 'r': return "rook"
    elif letter == 'n': return "knight"
    elif letter == 'b': return "bishop"
    elif letter == 'q': return "queen"

def example():
    board = chess.Board()
    board.legal_moves
    chess.Move.from_uci("a8a1") in board.legal_moves
    scholars_mate(board)

def scholars_mate(board):
    board.push_san("e4")
    board.push_san("e5") 
    board.push_san("Qh5") 
    board.push_san("Nc6")
    board.push_san("Bc4")
    board.push_san("Nf6")
    board.push_san("Qxf7")
    if board.is_checkmate():
        return True

# Random choice player 
def random_player(board):
    move = random.choice(list(board.legal_moves))
    return move.uci()
    
def show_ascii(board):
    print(chess.BaseBoard.unicode(board))

""" 
A useful function for displaying the color of a player
"""    
def who(player):
    return "White" if player == chess.WHITE else "Black"

""" 
A useful function for displaying the color of a piece

Constants for the side to move or the color of a piece.
chess.WHITE = 0
chess.BLACK = 1
"""    
def which(piece):
    return "white" if piece.color else "black"

"""
A function for displaying the board as text
or as an SVG image
"""
def display_board(board, use_svg):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"


def play_game(player1, player2, TURN_MAX=10, visual="svg", pause=0.1):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    """
    use_svg = (visual == "svg")
    board = chess.Board()
    turns = 0
    try:
        while not board.is_game_over(claim_draw=True) and turns <= TURN_MAX:
            if board.turn == chess.WHITE:
                uci = player1(board)
            else:
                uci = player2(board)
            name = who(board.turn)

            # Put monitor here, before the move....
            monitor_move(board, uci)
            board.push_uci(uci)
            turns+=1 
            board_stop = display_board(board, use_svg)
            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                os.system('clear')  # Trying to add for interactive
                show_ascii(board)
                print("\n")
                #display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    if visual is not None:
        print(msg)  # This cases an error in the break 
    return (result, msg, board)

"""
Basic reasonableness monitor for chess
"""
def monitor_move(board, move):
    start = move[0:2]
    board_index = chess.SQUARE_NAMES.index(start)
    current_piece = board.piece_at(board_index)
    print_piece_summary(current_piece)
    #    print(chess.UNICODE_PIECE_SYMBOLS[current_piece])
    to = move[2::]
    qual_description(start, to, current_piece)
    #print(to)


def print_piece_summary(piece):
    symbol = chess.UNICODE_PIECE_SYMBOLS[piece.symbol()]

    print("Piece summary for",symbol)
    # Moving from ...
    #print(piece)
    #print(which(piece))

"""
Produces a qualitative description of the move 
Right now, it's just up and down 
"""
def qual_description(start, finish, piece):
    # Set the operator for black or white.  
    print("Summary, moved from", start, "to", finish)
    [start_vert, start_side] = list(start)
    [finish_vert, finish_side] = list(finish)
    
    # First case, up and down
    if start_vert == finish_vert:
        if (start_side < finish_side):
            print("Moved up")
        else:
            print("Moved down")

    # Second case, side to side
    if start_vert == finish_side:
        return 

    if start_vert != finish_vert and start_side != finish_side:
        check_laterals(start, finish, piece)

"""
This really isn't doing anything special.

"""        
def check_laterals(start, finish, piece):
    return "Lateral movemements"


def get_qual(start,finish,piece):
    # Check if black or white
    get_piece_name(piece)
    
if __name__ == "__main__":
    
    moves = 10
    play_game(random_player, random_player, moves)


