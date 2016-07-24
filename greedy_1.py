import os, sys
from pprint import pprint, pformat
import logging
#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)-15s %(filename)s:%(lineno)d %(message)s')


DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1)
)

class reservi(object):
  @staticmethod
  def pp(obj):
    if isinstance(obj, basestring):
      logging.info(obj)
    else:
      from pprint import pformat
      logging.info(pformat(obj))
  
  @staticmethod
  def is_out_of_bound(x):
      return x < 0 or x > 7
  
  @staticmethod
  def is_valid_move(x, y, me, board):
      ''' (x,y) is an empty space. we have to look for the 8 direction and see if it is connected. '''
      opponent = 'W' if me == 'B' else 'B'
      for direction in DIRECTIONS:
        dx, dy = direction
        xx, yy = x + dx, y + dy
        if reservi.is_out_of_bound(xx) or reservi.is_out_of_bound(yy):
          continue
        if board[yy][xx] == opponent:
          # try following that direction
          found_buddy = False
          while found_buddy is False:
              xx += dx
              yy += dy
              if reservi.is_out_of_bound(xx) or reservi.is_out_of_bound(yy):
                  break
              if board[yy][xx] == me:
                  found_buddy = True
                  break
          if found_buddy is False:
            logging.debug(
              '({}, {}) is connected to the opponent in ({}, {}) but no buddy in that direction'.format(
                x, y, dx, dy))
            continue 
          logging.debug('({}, {}) is connected to the opponent in ({}, {}) and buddy on the same line'.format(
                  x, y, dx, dy))
          return True
      return False
  
  @staticmethod
  def find_moves(me, board):
      ret = []
      for y, line in enumerate(board):
          for x, cell in enumerate(line):
              if cell == '.' and reservi.is_valid_move(x, y, me, board):
                  ret.append((x, y))
      return ret
  
  @staticmethod
  def show_moves(moves, board):
      dummy = list(board)
      for m in moves:
          x, y = m
          line = dummy[y]
          dummy[y] = line[0:x] + 'x' + line[x+1:]
      reservi.pp(dummy)
  
  @staticmethod
  def show_board(board):
      logging.info('\n' + ''.join(board))
      
  @staticmethod
  def do_move(me, move, board):
      opponent = 'B' if me == 'W' else 'W'
      new_board = list([list(row) for row in board])
      x, y = move
      new_board[y][x] = me
      for direction in DIRECTIONS:
          dx, dy = direction
          xx = x
          yy = y
          do_flip = False
          i = 0
          while True:
              xx += dx
              yy += dy
              i += 1
              if reservi.is_out_of_bound(xx) or reservi.is_out_of_bound(yy):
                  break
              if board[yy][xx] == '.':
                  break
              if board[yy][xx] == me:
                  do_flip = True
                  break
          if do_flip and i > 1:
              xx, yy = x, y
              for j in xrange(0, i):
                  xx += dx
                  yy += dy
                  new_board[yy][xx] = me
  
      new_board = [''.join(row) for row in new_board]
      return new_board
      
  @staticmethod
  def get_score(board):
      count_w = reduce(lambda m, x: m + 1 if x=='W' else m, ''.join(board), 0)
      count_b = reduce(lambda m, x: m + 1 if x=='B' else m, ''.join(board), 0)
      return {'B': count_b, 'W': count_w}

import sys

# write your compute function
# it takes in a 8 * 8 board, your disc and your opponents' disc
# return your next move by returning an tuple of [x, y]
def compute(me, opponent, board):
  # only valid for the first move, give this AI more capability!
  reservi.pp('Me =')
  reservi.pp(me)
  reservi.pp('Opponent =')
  reservi.pp(opponent)
  
  reservi.show_board(board)
  #         print is_cell_connected_to(2, 4, board, 'W')
  moves = reservi.find_moves(me, board)
  reservi.pp('Moves:')
  reservi.pp(moves)
  reservi.show_moves(moves, board)

  def sort_fn(move):
    new_board = reservi.do_move(me, move, board)
    #reservi.show_board(new_board)
    score = reservi.get_score(new_board)
    return score[me]
  
  for move in moves:
      reservi.pp(move)
      new_board = reservi.do_move(me, move, board)
      reservi.show_board(new_board)
      score = reservi.get_score(new_board)
      reservi.pp(score)
  sorted_moves = sorted(moves, key=sort_fn)
  reservi.pp('Best move:')
  reservi.pp(sorted_moves[-1])
  bx, by = sorted_moves[-1]
  return by, bx

while True:
  # read my disc symbol and opponent's disc symbol
  s = sys.stdin.readline()
  me = s[0]
  opponent = s[2]

  # read game board
  board = [sys.stdin.readline() for i in range(8)]

  # compute my move
  (row, col) = compute(me, opponent, board)

  # output my move
  print '%d %d' % (row, col)

