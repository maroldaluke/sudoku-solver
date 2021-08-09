"""
Sudoku Solver: Solve any sudoku puzzle within seconds using backtracking
Written by: Luke Marolda
"""

from cmu_112_graphics import *
from boards import *
import random, copy

# MODEL

# this function initilizes the game model and important attributes
def appStarted(app):
    app.boards = [board1, board2, board3, board4, board5, 
                  board6, board7, board8, board9, board10]
    app.index = random.randint(0,9)
    # deep copy the board so we can solve the empty boards multiple times
    app.board = copy.deepcopy(app.boards[app.index])
    # some attributes for the user interface
    app.rows = 9
    app.cols = 9
    app.margin = 100
    app.buttonMargin = 25
    app.buttonWidth = 120
    app.buttonHeight = 50

# CONTROLLER

# checks if the given board is valid with a number at a given (row, col)
def is_valid_board(board, number, position):
    boardSize = 3
    (row, col) = position
    # check the current row for the number
    for j in range(len(board[0])):
        if (board[row][j] == number) and (j != col):
            return False
    # check the current col for the number
    for i in range(len(board)):
        if (board[i][col] == number) and (i != row):
            return False
    # check the current small grid for the number
    boxRow = row - row % boardSize
    boxCol = col - col % boardSize
    for i in range(boardSize):
        for j in range(boardSize):
            if (board[i + boxRow][j + boxCol] == number):
                return False
    return True

# function finds the next empty spot on board and returns it as a tuple
# if there are no empty spots, we return False
def find_empty_spot(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return False

# this function solves a sudoko board using a backtracking algorithm
def solve_board_backtrack(board):
    # find the next empty spot on the board
    position = find_empty_spot(board)
    # base case: the board is solved (no empty spots)
    if (position == False):
        return True
    # recursive case: place a number, if valid, recursively call function
    else:
        (row, col) = position
        # place numbers to find a valid board
        for num in range(1, 10):
            if (is_valid_board(board, num, position)):
                board[row][col] = num
                # now recursively call the solve function
                if (solve_board_backtrack(board)):
                    return True
                # otherwise, we backtrack by undoing our last move
                board[row][col] = 0
        return False

# this function changes the current board to a different board
def new_board(app):
    newIndex = random.randint(0,9)
    # make sure the board index is not the same as the current one
    while(newIndex == app.index):
        newIndex = random.randint(0,9)
    app.index = newIndex
    newBoard = app.boards[newIndex]
    # deepcopy so we can solve this board multiple times
    app.board = copy.deepcopy(newBoard)

# controller function changes the model based on mouse clicks
def mousePressed(app, event):
    (x1, y1) = (app.width // 2 - app.buttonMargin, app.height - app.buttonMargin)
    (x0, y0) = (x1 - app.buttonWidth, y1 - app.buttonHeight)
    (x2, y2) = (app.width // 2 + app.buttonMargin, app.height - app.buttonMargin)
    (x3, y3) = (x2 + app.buttonWidth, y2 - app.buttonHeight)
     # backtracker solve button
    if (event.x >= x0 and event.x <= x1) and (event.y >= y0 and event.y <= y1):
        solve_board_backtrack(app.board)
    # new board button
    elif (event.x >= x2 and event.x <= x3) and (event.y >= y3 and event.y <= y2):
        new_board(app)

# VIEW

# from https://www.kosbie.net/cmu/fall-20/15-112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

# this function draws the sudoku board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width= 4, fill= "light blue")
            # center numbers in each grid box
            (textX, textY) = ((x0 + x1) / 2, (y0 + y1) / 2)
            text = str(app.board[row][col])
            # if the number is 0, we want the grid box to be empty
            if (text != "0"):
                canvas.create_text(textX, textY, text= text, font= "Tahoma 26 bold")

# this function is pretty boring, just draws the larger squares in the grid
def drawBoardLines(app, canvas):
    (x0,y0) = (app.margin, app.margin)
    (x1, y1) = (app.width - app.margin, app.margin)
    dist = (app.height - 2 * app.margin) // 3
    # draw the horizontal lines
    canvas.create_line(x0, y0, x1, y1, width= 8)
    canvas.create_line(x0, y0 + dist, x1, y1 + dist, width= 8)
    canvas.create_line(x0, y0 + 2 * dist, x1, y1 + 2 * dist, width= 8)
    canvas.create_line(x0, y0 + 3 * dist, x1, y1 + 3 * dist, width= 8)
    (x2, y2) = (app.margin, app.height - app.margin)
    # draw the vertical lines
    canvas.create_line(x0, y0, x2, y2, width= 8)
    canvas.create_line(x0 + dist, y0, x2 + dist, y2, width= 8)
    canvas.create_line(x0 + 2 * dist, y0, x2 + 2 * dist, y2, width= 8)
    canvas.create_line(x0 + 3 * dist, y0, x2 + 3 * dist, y2, width= 8)

# this function draws the background of the game
def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill= "purple")

# this function draws the backtrack solving button
def drawBacktrackButton(app, canvas):
    (x1, y1) = (app.width // 2 - app.buttonMargin, app.height - app.buttonMargin)
    (x0, y0) = (x1 - app.buttonWidth, y1 - app.buttonHeight)
    canvas.create_rectangle(x0, y0, x1, y1, width= 8, fill= "light blue")
    (textX, textY) = ((x0 + x1) / 2, (y0 + y1) / 2)
    text = """
  Solve with 
Backtracking!
    """
    canvas.create_text(textX, textY, text= text, font= "Tahoma 14 bold")

# this function draws the new board button
def drawNewBoardButton(app, canvas):
    (x0, y0) = (app.width // 2 + app.buttonMargin, app.height - app.buttonMargin)
    (x1, y1) = (x0 + app.buttonWidth, y0 - app.buttonHeight)
    canvas.create_rectangle(x0, y0, x1, y1, width= 8, fill= "light blue")
    (textX, textY) = ((x0 + x1) / 2, (y0 + y1) / 2)
    text = """New Board"""
    canvas.create_text(textX, textY, text= text, font= "Tahoma 16 bold")

# this function draws the sudoku title 
def drawTitle(app, canvas):
    (x0, y0) = (app.width // 2 - app.buttonWidth, app.buttonMargin)
    (x1, y1) = (x0 + app.buttonWidth * 2, y0 + app.buttonHeight)
    canvas.create_rectangle(x0, y0, x1, y1, width= 8, fill= "light blue")
    (textX, textY) = ((x0 + x1) / 2, (y0 + y1) / 2)
    text = "SUDOKU SOLVER"
    canvas.create_text(textX, textY, text= text, font= "Tahoma 24 bold")    

# this function draws all the necessary components of the user interface
def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawBoard(app, canvas)
    drawBoardLines(app, canvas)
    drawTitle(app, canvas)
    drawNewBoardButton(app, canvas)
    drawBacktrackButton(app, canvas)

# run the app! 
runApp(width= 700, height= 700)