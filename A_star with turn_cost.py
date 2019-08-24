# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 09:54:52 2019

@author: zzx
"""

ENV = [[1,1,1,0,0,0],
       [1,1,1,0,1,0],
       [0,0,0,0,0,0],
       [1,1,1,0,1,0],
       [0,0,1,0,1,0],
       [0,0,1,0,1,0]]
x = len(ENV)-1
y = len(ENV[0])-1

expend = [[0,0,-10,0,0,0],
          [0,-10,-10,0,0,0],
          [0,0,0,0,-10,0],
          [0,0,-10,-10,-10,0],
          [0,0,0,0,-10,0]]
path = [['$' for row in range(len(ENV[0]))] for col in range(len(ENV))]

count = 0
sign = ['↑','↓','←','→']
dirc = [[1,0],
       [-1,0],
       [0,1],
       [0,-1]]

turn_cost = [100,0,3]
start = [[0,5,3,8]]
goal = [2,0]


mark = [[0,0]]
def find_grid(now_grid,length):
    if length == 0:
        return now_grid
    else:   
        for i in range(length):
            if now_grid[i][0] > now_grid[i+1][0]:
                max = now_grid[i]
                now_grid[i] = now_grid[i+1]
                now_grid[i+1] = max
        length -= 1
        return find_grid(now_grid,length)
        
    return now_grid

def min_grid(now_grid):
    min_grid_ = []
    length = len(now_grid)
    for i in range(length):
        if now_grid[i][0] <= now_grid[0][0]:
            min_grid_.append(now_grid[i])
    return min_grid_
            



def mov(now_grid,ENV,dirc,goal,flag = False):
    if flag == True:
        return now_grid
    else:
        new_grid = []
        for each_grid in now_grid:
            x = each_grid[1]
            y = each_grid[2]
            
            for each_dirc in dirc:
                new_x = x + each_dirc[0]
                new_y = y + each_dirc[1]
                
                h_value = (goal[0]-new_x)**2 + (goal[1]-new_y)**2
                if new_x == goal[0] and new_y ==goal[1]:
                    flag = True
                if 0<=new_x<=5 and 0<=new_y<=5:
                    if ENV[new_x][new_y] != 1:
                        if new_x == x+1:
                            t_flag = 2
                        elif new_x == x-1:
                            t_flag = 8
                        elif new_y == y+1:
                            t_flag = 3
                        elif new_y == y-1:
                            t_flag = 7
                        
                        if t_flag - each_grid[3] == -1 or t_flag - each_grid[3] == 1:
                            turn_cost_ = turn_cost[0]
                        elif t_flag - each_grid[3] == -5 or t_flag - each_grid[3] == 5:
                            turn_cost_ = turn_cost[2]
                        elif  abs(t_flag - each_grid[3]) == 6 or abs(t_flag - each_grid[3])==4:
                            turn_cost_ = 9999
                        else:
                            turn_cost_=0
                        
                        new_grid.append([h_value+turn_cost_,new_x,new_y,t_flag])
                        
        order = find_grid(new_grid,len(new_grid)-1)
        min_grid_ = min_grid(order)
        print(min_grid_)
        return mov(min_grid_,ENV,dirc,goal,flag)


        
def draw(expend,dirc,x,y,path,sign):

    for i in range(len(dirc)):
        new_x = x + dirc[i][0]
        new_y = y + dirc[i][1]
        if 0 <= new_x <= 4 and 0 <= new_y <= 5:
            if expend[new_x][new_y] == expend[x][y] - 1:
                path[new_x][new_y] = sign[i]
                x,y = new_x,new_y
                if x == 0 and y == 0:
                    return path
                else:
                    
                    return draw(expend,dirc,x,y,path,sign)
                    
    

now_grid = mov(start,ENV,dirc,goal,flag = False)
print(now_grid)
