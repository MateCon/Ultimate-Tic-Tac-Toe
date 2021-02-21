import pygame
from pygame.locals import *

def areEquals(array):
    for i in range(len(array) - 1):
        if array[i] != array[i+1]:
            return False
    return True

def isInArray(array, target):
    for i in array:
        if i == target:
            return True
    return False

def endGame(board, state):
    if state != "yellow" and state != "white":
        return state

    for i in range(3):
        column = areEquals([board[i][0].state, board[i][1].state, board[i][2].state])
        row = areEquals([board[0][i].state, board[1][i].state, board[2][i].state])
        if column and board[i][0].state != "yellow" and board[i][0].state != "white":
            return board[i][0].state
        elif row and board[0][i].state != "yellow" and board[i][0].state != "white":
            return board[0][i].state

    if areEquals([board[0][0].state, board[1][1].state, board[2][2].state]) or areEquals([board[2][0].state, board[1][1].state, board[0][2].state]):
        return board[1][1].state

    for row in board:
        for cell in row:
            if cell.state == "yellow" or cell.state == "white":
                return "white"
    return "draw"

def resetBoards(superBoard, index, superBoardState):
    for row in superBoard:
        for board in row:
            board.update(superBoard)

    indexes = []
    if superBoard[index[-1]][index[0]].state != "yellow" and superBoard[index[-1]][index[0]].state != "white":
        for i in range(3):
            for j in range(3):
                if superBoard[j][i].state == "yellow" or superBoard[j][i].state == "white":
                    indexes.append([i, j])
    else:
        indexes = [index]

    for i in range(len(indexes)):
        indexes[i] = [indexes[i][1], indexes[i][0]]

    newState = ""
    for j in range(3):
        for i in range(3):
            if isInArray(indexes, [i, j]):
                newState = "yellow"
            else:
                newState = "white"
            for row in superBoard[i][j].cells:
                for cell in row:
                    if cell.state == "yellow" or cell.state == "white":
                        if superBoardState != "white" and superBoardState != "yellow":
                            cell.state = "white"
                        else:
                            cell.state = newState
                        



class Board:
    def createBoard(self):
        board = []
        for yIndex in range(3):
            row = []
            for xIndex in range(3):
                row.append(Cell(self.display, self.CELL_SIZE, 3 + self.xPos + (xIndex * (self.CELL_SIZE + self.GRID_GAP)), 3 + self.yPos + (yIndex * (self.CELL_SIZE + self.GRID_GAP)), self.index, [xIndex, yIndex]))
            board.append(row)
        return board

    def __init__(self, display, CELL_SIZE, GRID_GAP, xPos, yPos, index):
        self.state = "yellow"
        self.display = display
        self.CELL_SIZE = CELL_SIZE
        self.BOARD_SIZE = (CELL_SIZE + GRID_GAP) * 3 + 10
        self.GRID_GAP = GRID_GAP
        self.xPos = xPos
        self.yPos = yPos
        self.index = index
        self.cells = self.createBoard()
        self.rect = pygame.Rect(self.xPos - 2, self.yPos - 2, self.BOARD_SIZE, self.BOARD_SIZE)

    def checkState(self):
        if self.state != "yellow" and self.state != "white":
            return self.state
        for i in range(3):
            column = areEquals([self.cells[i][0].state, self.cells[i][1].state, self.cells[i][2].state])
            row = areEquals([self.cells[0][i].state, self.cells[1][i].state, self.cells[2][i].state])
            if column and self.cells[i][0].state != "yellow" and self.cells[i][0].state != "white":
                return self.cells[i][0].state
            elif row and self.cells[0][i].state != "yellow" and self.cells[i][0].state != "white":
                return self.cells[0][i].state

        if areEquals([self.cells[0][0].state, self.cells[1][1].state, self.cells[2][2].state]) or areEquals([self.cells[2][0].state, self.cells[1][1].state, self.cells[0][2].state]):
            return self.cells[1][1].state

        for row in self.cells:
            for cell in row:
                if cell.state == "yellow" or cell.state == "white":
                    return "white"
        return "draw"

    def show(self):
        if self.state == "red":
            color = (255, 0, 0)
        elif self.state == "blue":
            color = (0, 0, 255)
        elif self.state == "draw":
            color = (140, 140, 140)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(self.display, color, self.rect)
        for row in self.cells:
            for cell in row:
                cell.show()

    def update(self, superBoard):
        for row in superBoard:
            for board in row:
                board.state = board.checkState()
        

class Cell:
    def __init__(self, display, CELL_SIZE, xPos, yPos, boardIndex, index):
        self.state = "yellow"
        self.boardState = "yellow"
        self.display = display
        self.CELL_SIZE = CELL_SIZE
        self.xPos = xPos
        self.yPos = yPos
        self.index = index
        self.boardIndex = boardIndex
        self.rect = pygame.Rect(3 + self.xPos, 3 + self.yPos, self.CELL_SIZE, self.CELL_SIZE)
    
    def handleClick(self, mousePos, turn, superBoard, superBoardState):
        if self.boardState == "red" or self.boardState == "blue" or self.state == "white":
            return False
        wasClicked = mousePos[0] >= self.xPos and mousePos[0] <= self.xPos + self.CELL_SIZE and mousePos[1] >= self.yPos and  mousePos[1] <= self.yPos + self.CELL_SIZE
        if wasClicked and self.state == "yellow":
            self.state = turn
            resetBoards(superBoard, self.index, superBoardState)
            return True
        else:
            return False

    def show(self):
        if self.state == "red":
            color = (255, 0, 0)
        elif self.state == "blue":
            color = (0, 0, 255)
        elif self.state == "yellow":
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(self.display, (0, 0, 0), self.rect, 3)
        pygame.draw.rect(self.display, color, self.rect)
