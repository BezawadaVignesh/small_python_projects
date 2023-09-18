import pygame as pg
import pygame_gui as pg_gui

from settings import *
from board import Board


pg.init()

pg.display.set_caption('Backtracking VIZ')
window_surface = pg.display.set_mode(WINDOW_SIZE)

left_ui_win = pg.Surface(LEFT_WIN_SIZE)

l_manager = pg_gui.UIManager(LEFT_WIN_SIZE)

# manager.set_visual_debug_mode(True)

SOME_VAR = 0
pg_gui.elements.UILabel(relative_rect=pg.Rect((0, SOME_VAR), (136, 30)),
                                            text='Number of Queens:',
                                            manager=l_manager)
msg_box = pg_gui.elements.UITextBox(relative_rect=pg.Rect((0,LEFT_WIN_SIZE[1]//2), (LEFT_WIN_SIZE[0],LEFT_WIN_SIZE[1]//2)),manager=l_manager, html_text="")
rem_queen = pg_gui.elements.UIButton(relative_rect=pg.Rect((0, SOME_VAR + 30), (45, 45)),
                                            text='-',
                                            manager=l_manager)
queen_count = pg_gui.elements.UILabel(relative_rect=pg.Rect((45, SOME_VAR + 30), (45, 45)),
                                            text=str(INIT_QUEENS),
                                            manager=l_manager)

add_queen = pg_gui.elements.UIButton(relative_rect=pg.Rect((90, SOME_VAR + 30), (45, 45)),
                                            text='+',
                                            manager=l_manager)

SOME_VAR_2 = SOME_VAR + 100

start_button = pg_gui.elements.UIButton(relative_rect=pg.Rect((0, SOME_VAR_2), (100, 50)),
                                            text='Next',
                                            manager=l_manager)

solve_button = pg_gui.elements.UIButton(relative_rect=pg.Rect((0, SOME_VAR_2+50), (100, 50)),
                                            text='Solve',
                                            manager=l_manager)
stop_button = pg_gui.elements.UIButton(relative_rect=pg.Rect((110, SOME_VAR_2+50), (100, 50)),
                                            text='Stop',
                                            manager=l_manager)
stop_button.disable()
pg_gui.elements.UILabel(relative_rect=pg.Rect((0, SOME_VAR_2+120), (50, 30)),
                                            text='Speed:',
                                            manager=l_manager)
speed_bar = pg_gui.elements.UIHorizontalSlider(relative_rect=pg.Rect((0, SOME_VAR_2+150), (150, 50)), start_value=60, value_range=(1, 150),manager=l_manager)


board = Board(INIT_QUEENS)
board.msg_box = msg_box
clock = pg.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    window_surface.fill('black')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pg_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                board.next_step()
            elif event.ui_element == add_queen:
                board.set_queens(board.no_queens + 1)
                queen_count.set_text(str(board.no_queens))
            elif event.ui_element == rem_queen:
                board.set_queens(board.no_queens - 1)
                queen_count.set_text(str(board.no_queens))
            elif event.ui_element == solve_button:                    
                solve_button.disable()
                stop_button.enable()
                board.auto = True
            elif event.ui_element == stop_button:                    
                stop_button.disable()
                solve_button.enable()
                board.auto = False

        if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_bar:
                board.auto_speed = event.value

        l_manager.process_events(event)

    l_manager.update(time_delta)
    left_ui_win.fill('black')
    l_manager.draw_ui(left_ui_win)
    window_surface.blit(left_ui_win, (0, 0))
    board.draw(window_surface)

    pg.display.update()