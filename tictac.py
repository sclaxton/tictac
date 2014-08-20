import sys
import random
from utils import enumerate2
from copy import deepcopy

"""The Game class is the top level interface between IO and the rest of the code."""
class Game(object):

  """Init the game with a new board.

  Keywords:
  board -- object instantiating the Board class"""
  def __init__(self, board):
    self.board = board
    self.players = board.players
    self.ply = 0
    self.winner = None
    self.isOver = False

"""The Board Class abstracts away the game board."""
class Board(object):

  """Init the board for TicTacToe.

  Keywords:
  players -- a tuple of the names of the two players
  size    -- the row/col length"""
  def __init__(self, players, size, data=None):
    self.size = size
    self.data = (data if (data is not None) else
      [[None]*(size) for i in range(size)])
    self.players = players
    self.valueToSymbol = { None: ' ' }
    for player in players:
      self.valueToSymbol[player] = player

  """Method makes a move on the board for specified player.

  Arguments:
  player -- players name
  x      -- the row on the board (ranging from 0 - size-1)
  y      -- the col on the board (ranging from 0 - size-1)"""
  def move(self, player, row, col):
    self.data[row][col] = player

  """Method returns value at square at (row, col)."""
  def square(self, row, col):
    return self.data[row][col]

  """Method returns an enumerator of squares in the board with two indices."""
  def squares(self):
    data = self.data
    return enumerate2(data)

  """Method returns an enumerator of enumerated rows."""
  def rows(self):
    data = self.data
    rows = (enumerate(row) for row in data)
    return enumerate(rows)

  """Method returns an enumerator of enumerated columns"""
  def cols(self):
    board = self
    cols = (enumerate(self.data[i][j] for i in range(board.size))
      for j in range(board.size))
    return enumerate(cols)

  """Method returns an enumerator of enumerated diagonals."""
  def diags(self):
    board = self
    data = board.data
    return enumerate([enumerate(data[k][k] for k in range(board.size)),
      enumerate(data[k][board.size-1 - k] for k in range(board.size))])

  """Method returns the number of squares owned by player in specifed row."""
  def numberInRow(self, row, player):
    data = self.data
    return data[row].count(player)

  """Method returns the number of squares owned by player in specifed col."""
  def numberInCol(self, col, player):
    data = self.data
    colData = zip(*data)
    return colData[col].count(player)

  """Method returns the number of squares owned by player in specifed diag."""
  def numberInDiag(self, diag, player):
    data = self.data
    size = self.size
    elements = []
    count = 0
    if diag == 0:
      for i, row in enumerate(data):
        if row[i] == player:
          count += 1
    elif diag == 1:
      for i, row in enumerate(data):
        if row[size-1 - i] == player:
          count += 1
    return count

  """Method checks if board contains a winning configuration."""
  def isWin(self, player):
    data = self.data
    size = self.size
    rowNums = [self.numberInRow(i, player) for i, row in enumerate(data)]
    colNums = [self.numberInCol(i, player) for i, col in enumerate(zip(*data))]
    diagNum0 = self.numberInDiag(0, player)
    diagNum1 = self.numberInDiag(1, player)
    # this returns whether or not a row, column, or diagonal
    # contains more than three of a given player's tokens
    return (any(num == size for num in rowNums) or
      any(num == size for num in colNums) or
      diagNum0 == size or
      diagNum1 == size)

  """Method checks if board contains a forking configuration for a play."""
  def isFork(self, player):
    board = self
    # to check if the board currently contains a fork
    # we just check whether or not there are two ways
    # a given player can win
    count = 0
    squares = board.squares()
    for i, j, square in squares:
      if square is None:
        boardCopy = self.clone()
        boardCopy.move(player, i, j)
        if boardCopy.isWin(player):
          count += 1
    if count > 1:
      return True
    # other wise there is no fork in the current state
    return False

  """Method makes a deep copy of the current board."""
  def clone(self):
    new = Board(self.players, self.size)
    new.data = deepcopy(self.data)
    return new

  """Define low level representation for Board Class."""
  def __repr__(self):
    list.__repr__(self.data)


  """Define pretty print for Board Class."""
  def __str__(self):
    data = self.data
    size = self.size
    # the board unrolled into a list of values
    valueList = [val for row in data for val in row]
    # convert values to symbols
    symbolList = map(lambda x: self.valueToSymbol[x], valueList)
    divider = "----" * (size-1) + '---'
    string = ""
    for i in range(size):
      for j in range(size):
        if j < size-1:
          string += ' {' + str(i*size + j) + '} |'
        else:
          string += ' {' + str(i*size + j) + '}\n'
      if i < size-1:
        string += divider + '\n'
    return string.format(*symbolList)

class AI(object):

  def __init__(self, game, player):
    self.game = game
    self.board = game.board
    self.player = player
    players = self.board.players
    self.opponent = players[0] if self.player is players[1] else players[1]
    random.seed()

  """Method processes next game states with an aribtarty test.

  Keywords:
  player -- player making the move to advance the state of the game
  test   -- string corresponding to the name of the method to be
            called on the board (i.e. either 'isWin' or 'isFork') """
  def _lookAheadTest(self, player, test):
    board = self.board
    squares = board.squares()
    for i, j, square in squares:
      if square is None:
        boardCopy = board.clone()
        boardCopy.move(player, i, j)
        # return early if test passes
        if getattr(boardCopy, test)(player):
          return (i, j)
    # if test fails on all look ahead states return false
    return ()

  """"Method looks ahead to find a winning move."""
  def lookAheadWin(self, player):
    return self._lookAheadTest(player, 'isWin')

  """Method looks ahead to find a move to make a fork."""
  def lookAheadGetFork(self, player):
    return self._lookAheadTest(player, 'isFork')

  """Method looks ahead to find an optimal move to block a fork.

  First we try to get size-1 in a row. If we cannot fo this without
  the opponent playing a fork on the next turn, we simply block his
  fork. Alternatively, there might not be a fork to block, so we just
  move on."""
  def lookAheadBlockFork(self):
    me = self.player
    opponent = self.opponent
    board = self.board
    fork = None

    # check board for a chance to get size-1 in a row
    # forcing the opponent to defend, and thus blocking
    # a possible fork

    # first check all rows
    rows = board.rows()
    for i, row in rows:
      # if we have all squares but 2 in the row
      # and our opponent has none, try to move
      # in one of the two positions in the row
      # checking to see if moving their does not
      # allow the opponent to fork on the next ply
      if (board.numberInRow(i, opponent) == 0 and
        board.numberInRow(i, me) == board.size - 2):
        blanks = []
        for j, square in row:
          if square is None:
            blanks.append((i, j))
        copy1 = board.clone()
        copy2 = board.clone()
        copy1.move(me, *blanks[0])
        copy1.move(opponent, *blanks[1])
        copy2.move(me, *blanks[1])
        copy2.move(opponent, *blanks[0])
        if not copy1.isFork(opponent):
          return blanks[0]
        # else this was a fork so make a note of it
        else:
          fork = blanks[1]
        if not copy2.isFork(opponent):
          return blanks[1]
        # else this was a fork so make a note of it
        else:
          fork = blanks[0]

    # second check all columns
    cols = board.cols()
    for j, col in cols:
      if (board.numberInCol(j, opponent) is 0 and
        board.numberInCol(j, me) is board.size - 2):
        blanks = []
        for i, square in col:
          if square is None:
            blanks.append((i, j))
        copy1 = board.clone()
        copy2 = board.clone()
        copy1.move(me, *blanks[0])
        copy1.move(opponent, *blanks[1])
        copy2.move(me, *blanks[1])
        copy2.move(opponent, *blanks[0])
        if not copy1.isFork(opponent):
          return blanks[0]
        # else this was a fork so make a note of it
        else:
          fork = blanks[1]
        if not copy2.isFork(opponent):
          return blanks[1]
        # else this was a fork so make a note of it
        else:
          fork = blanks[0]

    # finally check the diagonals
    diags = board.diags()
    for k, diag in diags:
      if (board.numberInDiag(0, opponent) == 0 and
        board.numberInDiag(0, me) == board.size - 2):
        blanks = []
        for l, square in diag:
          if square is None:
            if k == 0:
              blanks.push((l, l))
            elif k == 1:
              blanks.append((l, size-l))
        copy1 = board.clone()
        copy2 = board.clone()
        copy1.move(me, *blanks[0])
        copy1.move(opponent, *blanks[1])
        copy2.move(me, *blanks[1])
        copy2.move(opponent, *blanks[0])
        if not copy1.isFork(opponent):
          return blanks[0]
        # else this was a fork so make a note of it
        else:
          fork = blanks[1]
        if not copy2.isFork(opponent):
          return blanks[1]
        # else this was a fork so make a note of it
        else:
          fork = blanks[0]

    # if we can't make a move to get size-1 in a row
    # without allowing the opponent to fork then we
    # should at least block their fork
    if fork is not None:
      return fork
    else: 
      return self.lookAheadGetFork(opponent)

  """Method returns the optimal corner move."""
  def tryCorners(self):
    board = self.board
    size = board.size
    me = self.player
    opponent = self.opponent
    corners = [(0, 0), (0, size-1), (size-1, size-1), (size-1, 0)]
    ret = ()
    # try to play opposite corner if opponent is in a corner
    if (board.square(*corners[0]) is opponent and 
      board.square(*corners[2]) is None):
      ret = corners[2]
    elif (board.square(*corners[2]) is opponent and 
      board.square(*corners[0]) is None):
      ret = corners[0]
    elif (board.square(*corners[1]) is opponent and 
      board.square(*corners[3]) is None):
      ret = corners[3]
    elif (board.square(*corners[3]) is opponent and 
      board.square(*corners[1]) is None):
      ret = corners[1]
    # else pick a random corner
    while len(corners) > 0:
      size = len(corners)
      randInd = random.randint(0, size-1)
      randCorner = corners.pop(randInd)
      if board.square(*randCorner) is None:
        ret = randCorner
        break

    # if no corners open, we can't return an optimal move
    # a this stage
    return ret

  """Move selects a random available square"""
  def moveRandom(self):
    board = self.board
    blanks = []
    for i in range(board.size):
      for j in range(board.size):
        if board.square(i, j) is None:
          blanks.push((i, j))
    size = len(blanks)
    if size > 0:
      index = random.randint(0, size-1)
      return blanks[index]
    else:
      return ()

  """Method uses a rule-based expert system to determine optimal move."""
  def move(self):
    board = self.board
    me = self.player
    opponent = self.opponent
    move = ()
    # make winning
    myWinningMove = self.lookAheadWin(self.player)
    if myWinningMove is not ():
      board.move(me, *myWinningMove)
      return True
    # block opponents winning move
    theirWinningMove = self.lookAheadWin(self.opponent)
    if theirWinningMove is not ():
      board.move(me, *theirWinningMove)
      return True
    # make a fork
    myForkingMove = self.lookAheadGetFork(me)
    if myForkingMove is not ():
      board.move(me, *myForkingMove)
      return True
    # block opponent's fork
    blockTheirFork = self.lookAheadBlockFork()
    if blockTheirFork is not ():
      board.move(me, *blockTheirFork)
      return True
    # move to the center
    center = (board.size-1)/2
    if board.square(center, center) is None:
      board.move(me, center, center)
      return True
    # move to opposite corner of opponent or move to any open corner
    cornerMove = self.tryCorners()
    if cornerMove is not ():
      board.move(me, *cornerMove)
      return True
    # move anywhere
    anyMove = self.moveRandom()
    if anyMove is not ():
      board.move(me, *anyMove)
      return True
    # there are no moves left  
    return False

# begin the main program
if __name__ == "__main__":
  players = ('x', 'o')
  size = 3
  board = Board(players, size)
  game = Game(board)
  humanPlayer = 'x' 
  aiPlayer = 'o'
  ai = AI(game, aiPlayer)

  raw_input("Welcome to TicTac! Press ENTER to begin.\n")

  while game.ply < size**2 and not game.isOver:
    print "\n"
    print board
    next = raw_input("Enter your next move by typing 'i j' to move " +
      "to the square in the ith row and jth column. Remember that 0 <= i, j <= " + 
      str(size-1) + ".\n")
    i, j = next.split(' ', 1)
    # makes sure input is valid
    try:
      # make sure the input makes sense
      i = int(i)
      j = int(j)
      if i < size and j < size:
        if board.square(i, j) == None:
          # make the move indicated by the user
          board.move('x', i, j)
          # was this the winning move?
          if board.isWin(humanPlayer):
            game.isOver = True
            game.winner = humanPlayer
            break
          # let the AI make the optimal move
          ai.move()
          # was this the winning move?
          if board.isWin(aiPlayer):
            game.isOver = True
            game.winner = aiPlayer
            break
          # increment the number of plays made
          game.ply += 2
        else: 
          print "This square has already been played!"
      # if the input doesn't make sense, remind
      # the user to input data that makes sense
      else:
        print "Remember that 0 <= i, j <= " + str(size-1) + ".\n"
    # if the data isn't valid, alert them
    except ValueError:
      print ("Sorry you did not input the row and column number of the square " + 
        "you want to move in the right format\n")
  # give the user a recap of the game
  print "\n"
  print board
  if game.winner == humanPlayer:
    print "Congrats you won!\n"
  elif game.winner == aiPlayer:
    print "Oh no! The computer beat you!\n"
  else:
    print "Cat game! Good Job!\n"

  sys.exit(0)
