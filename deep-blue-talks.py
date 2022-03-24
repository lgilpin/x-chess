#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
# -*- coding: utf-8 -*-

# TODO: use e.strerror for error messages

import kasparobot
import chess
import chess.uci
from chess.uci import InfoHandler
import os
import shlex
import sys

help_text = '''
available commands:
    help      : see this message
    resign    : quit the game
    fen       : set up a position with FEN
    move      : move a piece on the board
    ask       : ask about a particular move
    advice    : get advice for what to play next
    position  : get positional analysis
    board     : display the chess board
    engine    : configure backend chess engine
    clear     : clears the screen
'''

inverted = True

pieces = {
  'K':'♔',
  'Q':'♕',
  'R':'♖',
  'B':'♗',
  'N':'♘',
  'P':'♙',
  'k':'♚',
  'q':'♛',
  'r':'♜',
  'b':'♝',
  'n':'♞',
  'p':'♟'
}

board = chess.Board()
engines_dir = '{}/engines'.format(os.path.dirname(kasparobot.__file__))
engine = chess.uci.popen_engine('{}/stockfish'.format(engines_dir))
engine.uci()
info = InfoHandler()
engine.info_handlers.append(info)

def run():
  print(help_text)
  while True:
    args = None
    try:
      # TODO: consider readline module to cope with meta/control keys
      typed = raw_input("> ")
    except (EOFError, KeyboardInterrupt):
      print
      quit(0)
    args = shlex.split(typed)
    if args:
      parse(args)

def parse(args):
  cmd = args[0]
  if cmd == 'help':
    print(help_text)
  elif cmd == 'resign':
    quit(0)
  elif cmd == 'fen':
    set_fen(args)
  elif cmd == 'move':
    make_move(args)
  elif cmd == 'ask':
    ask(args)
  elif cmd == 'advice':
    advice(args)
  elif cmd == 'position':
    print('Not implemented. Planned for future release')
  elif cmd == 'board':
    show_board()
  elif cmd == 'engine':
    configure_engine(args)
  elif cmd == 'clear':
    os.system(cmd)
  else:
    print('error: unrecognized command {}'.format(cmd))
    print('enter "help" to see a list of available commands')

def set_fen(args):
  usage_text = 'usage: fen <FEN>'
  if len(args) == 1:
    print(board.fen())
    return
  if len(args) != 2:
    print('error: wrong number of arguments')
    print(usage_text)
  try:
    board.set_fen(args[1])
  except ValueError as e:
    #print repr(e)
    print('error: invalid FEN')
    print(usage_text)

def make_move(args):
  usage_text = 'usage: move <san_move>'
  if len(args) != 2:
    print('error: wrong number of arguments')
    print(usage_text)
  try:
    board.push_san(args[1])
  except ValueError as e:
    print('error: invalid or ambiguous move')
    print(usage_text)

def ask(args):
  move = None
  try:
    move = board.parse_san(args[1])
  except ValueError as e:
    print('error: invalid or ambiguous move')
  if move:
    comments = analyze(move)
    print(comments)

def advice(args):
  engine.position(board)
  engine.go(depth=8,movetime=800)
  with info:
    print('consider:')
    for pv in info.info['pv'].values():
      candidate_move = pv[0]
      print("\t{}".format(board.san(candidate_move)))
      comments = analyze(candidate_move)
      print("\t\t", comments)

def position():
  pass

def analyze(move):
  analyzer = kasparobot.MoveAnalyzer(board)
  comments = []
  if analyzer.controls_center(move):
    comments.append('controls center')
  if analyzer.develops(move):
    comments.append('develops piece')
  if analyzer.dims_knight(move):
    comments.append('a knight on the rim is dim')
  if analyzer.opens_position(move):
    comments.append('opens position')
  if analyzer.closes_position(move):
    comments.append('closes position')
  if analyzer.discovered_check(move):
    comments.append('discovered check')
  absolutely_pinned_square = analyzer.absolutely_pins(move)
  if absolutely_pinned_square:
    comments.append('absolutely pins {}'.format(\
        chess.SQUARE_NAMES[absolutely_pinned_square]))
  queen_pinned_square = analyzer.pins(move, chess.QUEEN)
  if queen_pinned_square:
    comments.append('pins {} to queen'.format(\
        chess.SQUARE_NAMES[queen_pinned_square]))
  if analyzer.checkmate(move):
    comments.append('delivers checkmate#')
  elif analyzer.check(move):
    comments.append('delivers check+')
  return comments


def show_board():
  # TODO: modularize... maybe into its own class?
  def piece(piece):
    if inverted:
      if piece.islower():
        return pieces[piece.upper()]
      else:
        return pieces[piece.lower()]
    else:
      return pieces[piece]
  def write(string):
    sys.stdout.write(string)
  def print_rank(i):
    print(str(8-i) + ' ',)
  def print_files():
    print(' ',)
    for col in range(8):
      print(chr(97 + col),)
    print()
  rows = board.fen().split()[0].split('/')
  for i in range(len(rows)):
    print_rank(i)
    for symbol in rows[i]:
      if symbol in pieces:
        write(piece(symbol) + ' ')
      elif symbol in '12345678':
        write(int(symbol) * '· ')
    print()
  print_files()

def configure_engine(args):
  # TODO: in-house options?
  usage_text = 'usage: engine <option_name> <option_value>'
  if len(args) == 1:
    print(engine.name)
    print(usage_text)
  elif len(args) == 3:
    try:
      engine.setoption({args[1]: int(args[2])})
    except ValueError as e:
      #print repr(e)
      print('error: option name or value invalid')
  else:
    print('error: wrong number of arguments')
    print(usage_text)

if __name__ == '__main__':
  run()
