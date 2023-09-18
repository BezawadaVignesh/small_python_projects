import pygame as pg

from settings import *

img = pg.image.load("wq.png")


class Board:
    def __init__(self, no_queens):
        self.board = pg.Surface((WINDOW_SIZE[1], WINDOW_SIZE[1]))
        self.board.fill('white')
        self.set_queens(no_queens)
        self.msg = 'INFO box is diabled since it effects performance if ran for long time'
        self.msg_box = None # this will be init explicitly
        self.auto_speed = 60
        
        
    @classmethod
    def place(cls, x, k, i):
        for j in range(k):
            if x[j] == i or abs(j - k) == abs(x[j] - i):
                return False
        return True

    @classmethod
    def solve(cls, no_queens):
        x = [-1 for _ in range(no_queens)]
        
        k = 0
        while k < no_queens:
            start = x[k]+1
            x[k] = -1
            for i in range(start, no_queens):
                if cls.place(x, k, i):
                    x[k] = i
                    yield x, k, i, (0, 255, 0)
                    break
                else:
                    yield x, k, i,(255, 0, 0)
            else:
                yield x, f"No Possible square for {k}, So backtrack ^", i,(0,0,0,0)
                x[k] = -1
                k -= 1
                if k < 0:
                    # raise StopIteration
                    return [-1 for _ in range(no_queens)], "No Solution."
                continue
            k += 1
        yield x, -1, -1, (0,0,0,0)
            

    def next_step(self):
        if self.solution == None:
            self.solution = Board.solve(self.no_queens)
        else:
            try:
                self.x, k, i, color = next(self.solution)
                self.current_square = [k, i, color]
                if self.x[-1] != -1:
                    self.auto = False
                #self.msg += f"{k}\n"
                if k == "No Solution.":
                    self.current_square = [-1, -1, color]
                    self.auto = False
                    self.solution = None
            except StopIteration:
                self.msg += "Done\n"
                self.auto = False
                self.current_square = [-1, -1, (0,0,0,0)]
                self.solution = None
                self.x = [-1 for _ in range(self.no_queens)]
            self.msg_box.set_text(self.msg)

    def set_queens(self, no_queens):
        self.x = [-1 for _ in range(no_queens)]
        self.solution = None
        self.current_square = [-1,-1]
        self.auto = False
        self.count = 0
        self.no_queens = no_queens
        self.square_width = self.board.get_width()//no_queens
        self.square_height = self.board.get_height()//no_queens
        self.img_cpy = pg.transform.scale(img.convert_alpha(), (self.square_width, self.square_width))
        

    def draw_squares(self):
        for i in range(self.no_queens):
            for j in range(self.no_queens):
                pg.draw.rect(self.board, (150, 150, 75) if i%2 + j%2 == 1 else (255,255,255), (i*self.square_width, j*self.square_height, self.square_width, self.square_height))
                if self.current_square[0] == j and self.current_square[1] == i:
                    pg.draw.rect(self.board, self.current_square[2], (i*self.square_width, j*self.square_height, self.square_width, self.square_height))

                if self.x[j] == i:
                    self.board.blit(self.img_cpy, (i*self.square_width, j*self.square_height))
                    #pg.draw.rect(self.board, (255, 0, 0), (i*self.square_width, j*self.square_height, self.square_width, self.square_height))
                
                
    def draw(self, window):
        if self.auto:
            if self.count >= self.auto_speed:
                self.next_step()
                self.count  = 0
            else:
                self.count += 1

        self.board.fill('black')
        self.draw_squares()
        window.blit(self.board, (LEFT_WIN_SIZE[0], 0))
