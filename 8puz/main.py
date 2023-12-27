import pygame as pg, sys, random
from pygame.locals import *

from board import Board
from solver import evaluate

pg.font.init()
my_font = pg.font.SysFont('Comic Sans MS', 20)
pg.init()
 
BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pg.time.Clock()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 580

BOARD_POS = ((WINDOW_WIDTH-WINDOW_HEIGHT)//2, 0)
BOARD_SIZE = (WINDOW_HEIGHT, WINDOW_HEIGHT)
 
WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('8 puzzle')
 
def main():
    looping = True
    board = Board(BOARD_SIZE)
    while looping :
        for event in pg.event.get() :
            if event.type == QUIT :
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                board.gen_best_move()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if BOARD_POS[0] <= pos[0] <= BOARD_POS[0] + BOARD_SIZE[0] and BOARD_POS[1] <= pos[1] <= BOARD_POS[1] + BOARD_SIZE[1]:
                    board.mouse_pressed((pos[0] - BOARD_POS[0], pos[1] - BOARD_POS[1]))


        WINDOW.fill(BACKGROUND)
        # WINDOW.blit(my_font.render('Curr Deviation: ' + str(evaluate(board.board)), False, (0, 0, 0)), (0,0))
        WINDOW.blit(board.update(), BOARD_POS)
        
        pg.display.update()
        fpsClock.tick(FPS)
        
 
main()
