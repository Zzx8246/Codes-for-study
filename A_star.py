# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:28:38 2019

@author: zzx
"""
ENV = [[0,0,1,0,0,0],
       [0,0,1,0,0,0],
       [0,0,0,0,1,0],
       [0,0,1,1,1,0],
       [0,0,0,0,1,0]]
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
start = [[0,0,0]]
now_grid = [[1,0,0],[3,5,6],[0,0,0],[0,5,6]]
length = len(now_grid)-1
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
            
def mov(now_grid,mark,dirc,ENV,count,expend):
    goal = False
    for each_grid in now_grid:
        if each_grid[1] == 4 and each_grid[2] == 5:
            goal = True
    if goal:
        return now_grid,expend
    else:
        count += 1
        A = []
        for each_grid in now_grid:
            for each_dir in dirc:
                new_grid = [each_grid[0]+1,each_grid[1]+each_dir[0],each_grid[2]+each_dir[1]]
                new_grid[0] += (new_grid[1]-4)**2+(new_grid[2]-5)**2
                if 0<=new_grid[1]<=4 and 0<=new_grid[2]<=5:
                    if ENV[new_grid[1]][new_grid[2]] != 1:
                        if [new_grid[1],new_grid[2]] not in mark:
                            A.append(new_grid)
                            mark.append([new_grid[1],new_grid[2]])
        order = find_grid(A,len(A)-1)
        min_grid_ = min_grid(order)
        for each_min in min_grid_:
            expend[each_min[1]][each_min[2]] = count
        
        
        return mov(min_grid_,mark,dirc,ENV,count,expend)
        
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
                    
    

A = find_grid(now_grid,length)
B = min_grid(A)
now_grid,expend = mov(start,mark,dirc,ENV,count,expend)

path = draw(expend,dirc,x,y,path,sign)
print(expend)
print(path)
