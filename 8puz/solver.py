from queue import PriorityQueue
import copy

def evaluate(curr):
    pos = {1 : (0,0), 2 : (0,1), 3 : (0, 2), 4 : (1, 0), 5: (1, 1),
                6 : (1, 2), 7 : (2, 0), 8 : (2, 1), 0 : (2, 2)}
    cost = 0
    for i in range(3):
        for j in range(3):
            c = curr[i][j]
            cost += abs(pos[c][0] - i) + abs(pos[c][1] - j)
    return cost
    

def magic(curr):
    pos = []
    idx = [[i, e.index(0)] for i, e in enumerate(curr) if 0 in e][0]
    
    move = [(0, 1),(0, -1),(1, 0),(-1, 0)]
    
    for m in move:
        if 0 <= idx[0] + m[0] <= 2 and  0 <= idx[1] + m[1] <= 2:
            l = copy.deepcopy(curr)
            l[idx[0] + m[0]][idx[1]+m[1]], l[idx[0]][idx[1]] = l[idx[0]][idx[1]], l[idx[0]+m[0]][idx[1]+m[1]]
            pos.append((l, (idx[0] + m[0], idx[1] + m[1])))
    
    return pos


def solve(start = [[1, 2, 3], [4, 5, 6], [0, 7, 8]], goal=[[1,2,3],[4,5,6],[7,8,0]]):
    moves = PriorityQueue() 
    mem = {}
    moves.put((evaluate(start), start, 0))
    start = str(start)
    while not moves.empty():
        _, curr, p_cost = moves.get()
        if curr == goal:
            tmp, t_path = str(curr), []
            while(tmp != start):
                tmp, mov, _ = mem[tmp]
                t_path.append(mov)
            
            return t_path
        
        pos = magic(curr)
        for i, mov in pos:
            if str(i) not in mem:
                mem[str(i)] = (str(curr), mov, p_cost)
                moves.put((evaluate(i)+p_cost+1, i, p_cost+1))
            else:
                if mem[str(i)][2] > p_cost:
                    mem[str(i)] = (str(curr), mov, p_cost)

if __name__ == "__main__":
    print(solve())