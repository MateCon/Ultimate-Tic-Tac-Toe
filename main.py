import pygame, sys
from board import *

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Verdana', 64)
pygame.display.set_caption('Ultimate tic tac toe')

WINDOW_SIZE = (816, 816)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface(WINDOW_SIZE)

CELL_SIZE = 80
GRID_GAP = 8
BOARD_SIZE = (CELL_SIZE + GRID_GAP) * 3 + 10

def createSuperBoard():
    superBoard = []
    for yIndex in range(3):
        row = []
        for xIndex in range(3):
            row.append(Board(display, CELL_SIZE, GRID_GAP, xIndex * BOARD_SIZE, yIndex * BOARD_SIZE, [xIndex, yIndex]))
        superBoard.append(row)
    return superBoard

def resetGame():
    superBoard = createSuperBoard()
    superBoardState = "yellow"
    turn = "red"
    return superBoard, superBoardState, turn

superBoard, superBoardState, turn = resetGame()

def createText(superBoardState):
    text = ""
    if superBoardState == "red":
        text = "Red won!"
    elif superBoardState == "blue":
        text = "Blue won!"
    elif superBoardState == "draw":
        text = "Draw!"
    elif superBoardState == "yellow" or superBoardState == "white":
        text = ""
    color = (0, 0, 0)
    return myfont.render(text, False, color)

while True:
    display.fill((255, 255, 255))

    for row in superBoard:
        for board in row:
            board.update(superBoard)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in superBoard:
                for board in row:
                    for row in board.cells:
                        for cell in row:
                            if cell.handleClick(pygame.mouse.get_pos(), turn, superBoard, superBoardState):
                                if turn == "red":
                                    turn = "blue"
                                else:
                                    turn = "red"
            superBoardState = endGame(superBoard, superBoardState)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                superBoard, superBoardState, turn = resetGame()
        
    for row in superBoard:
        for board in row:
            board.show()

    text = createText(superBoardState)
    
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    text_rect = text.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))
    screen.blit(text, text_rect)
    pygame.display.update()
    clock.tick(60)
