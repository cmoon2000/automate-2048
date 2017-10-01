import sys, random, re, time
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LEFT  = 0
UP    = 1
RIGHT = 2
DOWN  = 3
DIRS  = [LEFT, UP, RIGHT, DOWN]
MOVES = [Keys.LEFT, Keys.UP, Keys.RIGHT, Keys.DOWN]
EMPTY = 0
def turn(dir):
  body.send_keys(MOVES[dir])


driver_path = r'C:\\Users\\haind\\Downloads\\geckodriver-v0.18.0-win64\\geckodriver.exe'
driver = webdriver.Firefox(executable_path=driver_path)
driver.get(r'https://gabrielecirulli.github.io/2048/')
driver.execute_script("window.scrollTo(0, 300)")

def terminate():
  driver.quit()
  sys.exit()

def newBoard():
  board = []
  for i in range(4):
    board.append([0] * 4)
  return board

def getboard():
  tileElems = driver.find_elements_by_css_selector('.tile-container > .tile')
  board = newBoard()
  tiles = []
  for e in tileElems:
    # each elemen has class attribute like below:
    # tile tile-2 tile-position-1-1 tile-new
    class_attr = e.get_attribute('class')

    #  indexing of col and row need to be transformed from base-1 to base-0,
    ## they should be subtracted by 1
    pos = class_attr.find('tile-position')
    col = int(class_attr[pos + 14]) -1    # column position
    row = int(class_attr[pos + 16]) -1    # row position
    match = re.search(r'tile-(\d+)', class_attr) 
    val = int(match.group(1))            # cell value
    board[row][col] = val
  return board

def showboard(board):
  for i in board:
    print(i)

def move(tile, dir):
  # move left
  if dir == LEFT:
    tile['x'] -= 1
  # move up
  if dir == UP:
    tile['y'] -= 1
  # move right
  if dir == RIGHT:
    tile['x'] += 1
  # move down
  if dir == DOWN:
    tile['y'] += 1

def moveBoardLeft(board):
  point = 0
  for row in board:
    for i in range(0, 4):
      v = 1
      while row[i] == EMPTY:
        if i + v > 3:
          break       # there are all empty cells to the right,
                      # move to next row (1)
        row[i], row[i + v] = row[i +v], row[i]
        v = v + 1

      if row[i] == EMPTY:
        break
      if i > 0 and row[i-1] == row[i]:
        row[i-1] *= 2      # merged tiles
        row[i] = EMPTY 
        point += row[i-1]
        v = 1
        while row[i] == EMPTY:
          if i + v > 3:
            break 
          row[i], row[i + v] = row[i + v], row[i]
          v = v + 1
  return point

def moveBoardUp(board):
  point = 0
  for x in range(0, 4):
    for y in range(0, 4):
      v = 1
      while board[y][x] == EMPTY:
        if y + v > 3:
          break       # there are all empty cells to the bottom,
                      # move to next column 
        board[y][x], board[y+v][x] = board[y+v][x], board[y][x]
        v = v + 1

      if board[y][x] == EMPTY:
        break
      if y > 0 and board[y-1][x] == board[y][x]:
        board[y-1][x] *= 2      # merged tiles
        board[y][x] = EMPTY 
        point += board[y-1][x]
        v = 1
        while board[y][x] == EMPTY:
          if y + v > 3:
            break       # there are all empty cells to the bottom,
                        # move to next column 
          board[y][x], board[y+v][x] = board[y+v][x], board[y][x]
          v = v + 1
  return point

def moveBoardRight(board):
  point = 0
  for row in board:
    for i in range(3, -1, -1):
      v = -1
      while row[i] == EMPTY:
        if i + v < 0:
          break       # there are all empty cells to the left,
                      # move to next row
        row[i], row[i + v] = row[i +v], row[i]
        v = v - 1

      if row[i] == EMPTY:
        break
      if i < 3 and row[i+1] == row[i]:
        row[i+1] *= 2      # merged tiles
        row[i] = EMPTY 
        point += row[i+1]
        v = -1
        while row[i] == EMPTY:
          if i + v < 0:
            break 
          row[i], row[i + v] = row[i + v], row[i]
          v = v - 1
  return point

def moveBoardDown(board):
  point = 0
  for x in range(0, 4):
    for y in range(3, -1, -1):
      v = -1
      while board[y][x] == EMPTY:
        if y + v < 0:
          break       # there are all empty cells to the top,
                      # move to next column 
        board[y][x], board[y+v][x] = board[y+v][x], board[y][x]
        v = v - 1

      if board[y][x] == EMPTY:
        break
      if y < 3 and board[y+1][x] == board[y][x]:
        board[y+1][x] *= 2      # merged tiles
        board[y][x] = EMPTY 
        point += board[y+1][x]
        v = -1
        while board[y][x] == EMPTY:
          if y + v < 0:
            break       # there are all empty cells to the top,
                        # move to next column 
          board[y][x], board[y+v][x] = board[y+v][x], board[y][x]
          v = v - 1
  return point

def test(dir):
  point = 0
  board = getboard()
  print('Before: ')
  showboard(board)
  if dir == LEFT:
    point = moveBoardLeft(board)
  if dir == UP:
    point = moveBoardUp(board)
  if dir == RIGHT:
    point = moveBoardRight(board)
  if dir == DOWN:
    point = moveBoardDown(board)
  print('After: ')
  showboard(board)
  print('Point: %s' % str(point))
  print()
  print()


# User can move 4 directions
# Try to move left, up, right, down to get points, respectively
#  Find the direction that we can obtain highest points.
## send_keys for that direction.
#  If all of 4 directions we can get same point(of course not zero point),
## random get 1-in-4 direction.
#  All we can get is zero point
## Do nothing

try:
  while True:
    # Get possible directions which we can get highest point
    max_point = 0
    board = getboard()
    possibleDIRS = []

    for d in DIRS:
      if d == LEFT:
        point = moveBoardLeft( deepcopy(board) )
      elif d == UP:
        point = moveBoardUp( deepcopy(board) )
      elif d == RIGHT:
        point = moveBoardRight( deepcopy(board) )
      else:
        point = moveBoardDown( deepcopy(board) )

      if point > max_point:
        max_point = point
        possibleDIRS = []
        possibleDIRS.append(d)
      elif point == max_point:
        possibleDIRS.append(d)
        
    random.shuffle(possibleDIRS)
    msg = ''
    for i in possibleDIRS:
      if i == 0:
        msg += 'LEFT '
      elif i == 1:
        msg += 'UP '
      elif i == 2:
        msg += 'RIGHT '
      else:
        msg += 'DOWN '
    print(msg, 'max_point: %s' % str(max_point), possibleDIRS)
    time.sleep(4)
    driver.find_element_by_css_selector('body').send_keys(MOVES[possibleDIRS[0]])
    time.sleep(2)
except KeyboardInterrupt:
  driver.quit()
  print('Done')

