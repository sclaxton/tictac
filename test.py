from tictac import Game, Board, AI

players = ['x', 'o']
size = 3

class TestBoard(object):

  def setup(self):
    self.boardId = Board(players, size, 
      [['x', None, None], [None, 'x', None], [None, None, 'x']])
    self.boardAnti = Board(players, size, 
      [[None, None, 'x'], [None, 'x', None], ['x', None, None]])
    self.boardCat = Board(players, size, 
      [['x', 'x', 'o'], ['o', 'o', 'x'], ['x', 'o', 'x']])
    self.boardEmpty = Board(players, size)
    self.boardWinRow = Board(players, size, 
      [['x', 'x', 'x'],['o', 'x', 'o'], ['o', None, 'o']])
    self.boardWinCol = Board(players, size, 
      [['x', 'x', 'o'],['o', 'x', 'o'], ['x', None, 'o']])
    self.boardFork1 = Board(players, size, 
      [['x', None, 'x'], [None, 'o', None], ['o', None, 'x']])
    self.boardFork2 = Board(players, size, 
      [['x', 'o', None], [None, 'x', None], ['x', None, 'o']])

  def test_diag(self):
    diagsId = [[x for k, x in diag] for m, diag in self.boardId.diags()]
    diagsAnti = [[x for k, x in diag] for m, diag in self.boardAnti.diags()]
    assert diagsId[0] == ['x', 'x', 'x']
    assert diagsId[1] == [None, 'x', None]
    assert diagsAnti[0] == [None, 'x', None]
    assert diagsAnti[1] == ['x', 'x', 'x']

  def test_numberInRow(self):
    for i in range(size):
      assert self.boardId.numberInRow(i, 'x') == 1 

  def test_numberInCol(self):
    for j in range(size):
      assert self.boardId.numberInCol(j, 'x') == 1 

  def test_numberInDiag(self):
    assert self.boardId.numberInDiag(0, 'x') == 3
    assert self.boardId.numberInDiag(1, 'x') == 1
    assert self.boardAnti.numberInDiag(0, 'x') == 1
    assert self.boardAnti.numberInDiag(1, 'x') == 3

  def test_isWin(self):
    assert self.boardId.isWin('x') == True
    assert self.boardAnti.isWin('x') == True
    assert self.boardWinRow.isWin('x') == True
    assert self.boardWinCol.isWin('o') == True
    assert self.boardCat.isWin('x') == False
    assert self.boardCat.isWin('o') == False
    assert self.boardEmpty.isWin('x') == False

  def test_isFork(self):
    assert self.boardFork1.isFork('x') == True
    assert self.boardFork2.isFork('x') == True
    assert self.boardEmpty.isFork('x') == False

class TestAI(object):

  def setupAI(self, board, player):
    return AI(Game(board), player)

  def setup(self):

    boardAlmostWin1 = Board(players, size, 
      [['x', 'x', None],['o', 'x', 'o'], ['o', None, 'o']])
    self.AIalmostWin1 = self.setupAI(boardAlmostWin1, 'o')

    boardAlmostWin2 = Board(players, size, 
      [['x', 'x', 'o'],['o', 'x', None], ['x', None, 'o']])
    self.AIalmostWin2 = self.setupAI(boardAlmostWin2, 'o')

    boardEmpty = Board(players, size)
    self.AIempty = self.setupAI(boardEmpty, 'o')

    boardAlmostFork1 = Board(players, size, 
      [['x', None, None], [None, 'o', None], ['o', None, 'x']])
    self.AIalmostFork1 = self.setupAI(boardAlmostFork1, 'x')

    boardAlmostFork2 = Board(players, size, 
      [['x', 'o', None], [None, 'x', None], [None, None, 'o']])
    self.AIalmostFork2 = self.setupAI(boardAlmostFork2, 'x')

    boardAlmostFork3 = Board(players, size, 
      [[None, 'x', None], [None, None, None], ['o', None, 'x']])
    self.AIalmostFork3 = self.setupAI(boardAlmostFork3, 'o')

    boardAlmostFork4 = Board(players, size, 
      [['x', 'o', None], [None, 'o', 'x'], [None, 'x', None]])
    self.AIalmostFork4 = self.setupAI(boardAlmostFork4, 'o')

    boardAlmostFork5 = Board(players, size, 
      [['x', 'o', None], [None, None, None], [None, 'x', None]])
    self.AIalmostFork5 = self.setupAI(boardAlmostFork5, 'o')

    boardAlmostFork6 = Board(players, size, 
      [['x', None, None], [None, 'x', None], [None, None, 'o']])
    self.AIalmostFork6 = self.setupAI(boardAlmostFork6, 'o')

  def test_lookAheadWin(self):
    assert self.AIalmostWin1.lookAheadWin('x') == (0, 2)
    assert self.AIalmostWin2.lookAheadWin('o') == (1, 2)
    assert self.AIempty.lookAheadWin('x') == ()

  def test_lookAheadMakeFork(self):
    assert self.AIalmostFork1.lookAheadGetFork('x') == (0, 2)
    almostFork2 = self.AIalmostFork2.lookAheadGetFork('x')
    assert (almostFork2 == (2, 0) or almostFork2 == (1, 0))
    assert self.AIempty.lookAheadGetFork('x') == ()

  def test_lookAheadBlockFork(self):
    assert self.AIalmostFork3.lookAheadBlockFork() == (0, 0)
    assert self.AIalmostFork4.lookAheadBlockFork() == (2, 0)
    almostFork5 = self.AIalmostFork5.lookAheadBlockFork()
    assert (almostFork5 == (2, 0) or almostFork5 == (2, 2))
    assert self.AIalmostFork6.lookAheadBlockFork() == (2, 0)
    assert self.AIempty.lookAheadBlockFork() == ()
