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

dirc = [[1,0],
       [-1,0],
       [0,1],
       [0,-1]]
start = [[0,0,0]]
now_grid = [[1,0,0],[3,5,6],[0,0,0],[0,5,6]]
length = len(now_grid)-1
mark = [[0,0,0]]
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
            
def mov(now_grid,mark,dirc,ENV):
    goal = False
    for each in now_grid:
        if each[1] == 4 and each[2] ==5:
            goal = True
    if goal:
        return now_grid
    else:
        A = []
        for each_grid in now_grid:
            for each_dir in dirc:
                new_grid = [each_grid[0]+1,each_grid[1]+each_dir[0],each_grid[2]+each_dir[1]]
                if 0<=new_grid[1]<=4 and 0<=new_grid[2]<=5:
                    if ENV[new_grid[1]][new_grid[2]] != 1:
                        if [new_grid[1],new_grid[2]] not in mark:
                            A.append(new_grid)
                            mark.append([new_grid[1],new_grid[2]])
        order = find_grid(A,len(A)-1)
        min_grid_ = min_grid(order)
        print(min_grid_)
        return mov(min_grid_,mark,dirc,ENV)
        


A = find_grid(now_grid,length)
B = min_grid(A)
mov(start,mark,dirc,ENV)
