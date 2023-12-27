import pygame as pg
import solver
img = []


class Board:
    def __init__(self, area, tiles=(3,3)):
        self.area = area
        self.piece = (area[0]//tiles[0], area[1]//tiles[1])
        self.surface = pg.Surface(area)
        self.tiles = tiles
        for i in range(1, 9):
            img.append(pg.image.load("sample/img3/image_part_00" + str(i) + ".jpg"))
            img[-1] = pg.transform.scale(img[-1], (self.piece[0]-1, self.piece[1]-1))
        # if tiles != (3, 3):
        #     raise Exception("Var tiles feature is not implemented")
        
        # init the board
        self.board = []
        n = 1
        for i in range(tiles[0]):
            self.board.append([])
            for j in range(tiles[1]):
                self.board[-1].append(n)
                n += 1
        self.board[-1][-1] = 0
        self.curr_mov = [(-1, -1), (0, 0), (-1,-1), (-1,-1), 0]
        self.is_moving = False
        self.ai_is_on = False
        self.update(forced=True)


    def gen_best_move(self):
        self.sol_mov = []
        self.sol_mov = solver.solve(self.board)
        self.ai_is_on = True

        
    def move(self, pos, vel, start, end):
        self.curr_mov[0] = pos
        self.curr_mov[1] = vel
        self.curr_mov[2] = start
        self.curr_mov[3] = end
        self.curr_mov[4] = 24
        self.is_moving = True
                
    def mouse_pressed(self, pos):
        if(self.is_moving): return
        pos = (pos[0]// self.piece[0], pos[1] // self.piece[1])
        for i in (-1, 1):
            if 0 <= pos[0] + i <= 2 and self.board[pos[1]][pos[0] + i] == 0:
                self.move(pos, [1*i, 0], (pos[0] * self.piece[0], pos[1] * self.piece[1]), ((self.piece[1] * (pos[0]+i), self.piece[0] * pos[1])))
                break
            
            if 0 <= pos[1] + i <= 2 and self.board[pos[1]+ i][pos[0]] == 0:
                self.move(pos, [0, 1*i], (pos[0] * self.piece[0], pos[1] * self.piece[1]), ((self.piece[1] * (pos[0]), self.piece[0] * (pos[1]+i))))
                break
            

        
    def update(self, forced=False):
        # if not self.is_moving and not forced: return self.surface
        if not self.is_moving and self.ai_is_on:
            if self.sol_mov:
                pos = self.sol_mov.pop()
                self.mouse_pressed((pos[1]*self.piece[1]+20, pos[0]*self.piece[0]+20))
            else:
                self.ai_is_on = False
        self.surface.fill((0,0,0))
        for i in range(self.tiles[0]):
            for j in range(self.tiles[1]):
                if self.board[i][j] == 0: continue
                if self.is_moving and self.curr_mov[0] == (j, i):
                    # print(self.curr_mov)
                    
                    to_pos = [0, 0]
                    if self.curr_mov[1][0] < 0:
                        self.curr_mov[1][0] -= max(1, self.curr_mov[4])
                        to_pos[0] = -1
                    elif self.curr_mov[1][0] > 0:
                        self.curr_mov[1][0] += max(1, self.curr_mov[4])
                        to_pos[0] = 1
                    elif self.curr_mov[1][1] < 0:
                        self.curr_mov[1][1] -= max(1, self.curr_mov[4])
                        to_pos[1] = -1
                    elif self.curr_mov[1][1] > 0:
                        self.curr_mov[1][1] += max(1, self.curr_mov[4])
                        to_pos[1] = 1
                    self.curr_mov[4] -= 1
                    if abs(self.curr_mov[1][0]) > abs(self.curr_mov[2][0] - self.curr_mov[3][0]) or \
                        abs(self.curr_mov[1][1]) > abs(self.curr_mov[2][1] - self.curr_mov[3][1]):
                        
                        from_pos = (self.curr_mov[0][1], self.curr_mov[0][0])
                        self.board[from_pos[0]][from_pos[1]], self.board[from_pos[0]+to_pos[1]][from_pos[1]+to_pos[0]] = \
                        self.board[from_pos[0]+to_pos[1]][from_pos[1]+to_pos[0]], self.board[from_pos[0]][from_pos[1]]
                        self.is_moving = False
                    self.surface.blit(img[(self.board[i][j])%9-1], (self.curr_mov[2][0]+self.curr_mov[1][0],self.curr_mov[2][1]+self.curr_mov[1][1]))
                        

                else:
                    self.surface.blit(img[(self.board[i][j])%9-1], (self.piece[1] * j, self.piece[0] * i))

        return self.surface
    