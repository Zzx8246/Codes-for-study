# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 16:02:25 2019

@author: zzx
"""

ENV = [[1,1,1,0,0,0],
       [1,1,1,0,1,0],
       [0,0,0,0,0,0],
       [1,1,1,0,1,0],
       [0,0,1,0,1,0],
       [0,0,1,0,1,0]]
#构建一个三维的Value矩阵储存Cost值，分别为朝向、x、y。记录的是在该朝向下可能的最小cost
#cost是从该点该朝向，到达终点所需要的累积cost
value = [[[999 for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[999 for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[999 for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[999 for row in range(len(ENV[0]))] for col in range(len(ENV))]]
#policy记录了在该点该朝向下，cost最小的动作
policy = [[[' ' for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[' ' for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[' ' for row in range(len(ENV[0]))] for col in range(len(ENV))],
         [[' ' for row in range(len(ENV[0]))] for col in range(len(ENV))]]
#policy2D记录给定一个起始点一个起始朝向，如何到达终点的策略
#policy是每一个点到达终点的策略
#policy2D是特定点到终点的策略，是通过查询policy得到的
policy2D = [[' ' for row in range(len(ENV[0]))] for col in range(len(ENV))]

goal = [2,0]
#动作：右转、直行、左转
action = [-1,0,1]
#朝向：上、左、下、右
dirc = [[-1,0],[0,-1],[1,0],[0,1]]
#转向cost：右、前、左
cost = [1,0,10]
action_name = ['R','#','L']
init = [5,3,0]
               
change = True
while change:
    change = False
    for x in range(len(ENV)):
        for y in range(len(ENV[0])):
            for orientation in range(4):
                #将终点置零
                if x == goal[0] and y ==goal[1]:
                    if value[orientation][x][y] >0:
                        change = True
                        value[orientation][x][y] = 0
                        policy[orientation][x][y] = '*'
                elif ENV[x][y] == 0:
                    for i in range(3):
                        #顺时针改变朝向，如当前朝向+1=左转后朝向
                        #%4保证4次一循环
                        o2 = (orientation + action[i]) % 4
                        x2 = x + dirc[o2][0]
                        y2 = y + dirc[o2][1]
                        
                        if 0<=x2<=(len(ENV)-1) and 0<=y2<=(len(ENV[0])-1):
                            if ENV[x2][y2] ==0 :
                                #只记录最优值，即cost最小值
                                v2 = value[o2][x2][y2] + cost[i]
                                if v2 < value[orientation][x][y]:
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[i]
                                    change = True
                                    
x = init[0]
y = init[1]
orientation = init[2] 
 
#查阅policy获得policy2D
policy2D[x][y] = policy[orientation][x][y]
while policy[orientation][x][y] != '*':
    
    if policy[orientation][x][y] == 'R':
        o2  = (orientation -1) % 4
    elif policy[orientation][x][y] == '#':
        o2 = orientation
    elif policy[orientation][x][y] == 'L':
        o2 = (orientation +1 ) % 4
    
    x = x + dirc[o2][0]
    y = y + dirc[o2][1]
    orientation = o2
    policy2D[x][y] = policy[orientation][x][y]

for i in policy2D:
    print(i)
      
        













              
                    
                        
                    