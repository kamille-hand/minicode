# coding:utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# 这里是全局变量
# 感染率分别为无法感染，低风险，中风险，高风险
InfectiousRate = [0, 0.1, 0.2, 0.3]
# 经过多少时间转换状态，指E->I->R环节，S->E需要感染这个行为触发
DurationThreshold = [0, 7, 3]

# 戴口罩：正方形
# 不戴口罩：圆形
# 传染病四个阶段：Suspective -> Exposed -> Infective -> Recovered
# 对于covid19而言，可以假设所有人都是易感者。
# covid19全局参数
# 基本参数1：低/中/高风险传播率
# S代表易感者
# 基本参数1：是否注意社交距离
# E代表潜伏期病人
# 基本参数1：潜伏期长度
# 基本参数2：潜伏期是否具备传播能力
# I代表出现症状的病人
# 基本参数1：传播范围
# R代表被政府发现已经隔离的人
# 基本参数1：多少天隔离，检测能力
# 进阶参数1：对密切接触者的排查能力

# Person的基本参数
# state：0->1->2->3 状态：S->E->I->R
# pos: (x,y) 显示坐标，主要用于可视化
# roughPos: (i,j) 逻辑坐标，用于逻辑判断
# delta: (v_x, v_y) 相当于离散化的速度
# momentum: 惯性常量
# duration: 记录每个阶段的经过时间，用于状态变更
# masked: 是否佩戴口罩


class Person:
    infectiousRate = 0.1
    boundary = np.array([-1, 1])

    def __init__(self, masked, state=0):
        self.pos = np.random.uniform(low=-1, size=2)
        self.delta = np.zeros(2)
        self.masked = masked
        self.state = state
        self.step = 0.02
        self.momentum = 0.95
        self.duration = 0
        self.immune = False

    def getVirus(self):
        if self.state == 0 and self.immune == False:
            self.state = 1
            self.duration = 100
            self.immune = True

    def recover(self):
        if self.duration != 0:
            self.duration -= 1
            if self.duration == 0:
                self.state = 0

    def randomMovement(self):
        self.delta = self.momentum * self.delta + self.step * np.random.uniform(
            low=-1, size=2
        )
        self.pos += self.delta
        for i in range(2):
            if self.pos[i] < self.boundary[0]:
                self.pos[i] = 2 * self.boundary[0] - self.pos[i]
                self.delta[i] = -self.delta[i]
            elif self.pos[i] > self.boundary[1]:
                self.pos[i] = 2 * self.boundary[1] - self.pos[i]
                self.delta[i] = -self.delta[i]


class Crowd:
    outOfBound = 100
    
    grid_num = 100
    
    remove = outOfBound * np.ones(2)
    axis = [-1, 1, -1, 1]
    colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
    shapes = ["o", "s"]

    def __init__(self, masked, unmasked, variety=8):
        # 新建图层
        self.fig, self.ax = plt.subplots()
        self.ax = plt.axis(self.axis)
        # 基本参数
        self.variety = variety
        self.num = masked + unmasked
        self.masked = masked
        self.unmasked = unmasked

        self.pos_grid = [[] for i in range(self.grid_num)]
        for i in range(self.grid_num):
            for j in range(self.grid_num):
                self.pos_grid[i].append(set())

        # 实际坐标*图案总数，outofbound代表不画
        self.pos = [
            self.outOfBound * np.ones((2, self.num)) for _ in range(self.variety)
        ]
        # 以给定人群比例构建对象
        self.people = [Person(i < self.masked) for i in range(self.num)]
        # 构建variety个图层，以不同图案与颜色区分
        self.plots = [
            plt.plot(
                self.pos[i][0], self.pos[i][1], self.colors[i % 4] + self.shapes[i % 2]
            )[0]
            for i in range(self.variety)
        ]
        # 动画展示
        self.ani = FuncAnimation(self.fig, self.animate, interval=50)

    def covid(self):
        for i in range(self.num - 1):
            for j in range(i + 1, self.num):
                dist = np.linalg.norm(self.people[i].pos - self.people[j].pos)
                if dist < 0.25:
                    if (
                        self.people[i].state != self.people[j].state
                        and self.people[i].immune != self.people[j].immune
                    ):
                        if random.uniform(0, 1) < self.people[j].infectiousRate:
                            self.people[i].getVirus()
                            self.people[j].getVirus()

    def covidone(self):
        for k in range(self.num):
            if self.people[k].state == 2:
                x, y =self.people[k].
                resone = [] 
                for i in self.pos_grid[x][y]:
                    resone.append(i)
                if(y+1 < self.grid_num):
                    for i in self.pos_grid[x][y+1]:
                        resone.append(i)
                if(x+1 < self.grid_num):
                    for i in self.pos_grid[x+1][y]:
                        resone.append(i)
                if(x > 0):
                    for i in self.pos_grid[x-1][y]:
                        resone.append(i)
                if(y > 0):
                    for i in self.pos_grid[x][y-1]:
                        resone.append(i)
                for num in resone:
                    self.people[num].getVirus()

    def covidtwo(self):
        for k in range(self.num):
            if self.people[k].state == 2:
                x, y =self.people[k].
                resone = [[],[],[]]
                for i in self.pos_grid[x][y]:
                    resone[0].append(i)
                if(y+1 < self.grid_num):
                    for i in self.pos_grid[x][y+1]:
                        resone[1].append(i)
                if(x+1 < self.grid_num):
                    for i in self.pos_grid[x+1][y]:
                        resone[1].append(i)
                if(x > 0):
                    for i in self.pos_grid[x-1][y]:
                        resone[1].append(i)
                if(y > 0):
                    for i in self.pos_grid[x][y-1]:
                        resone[1].append(i)
                if(y+1 < self.grid_num and x+1 < self.grid_num):
                        for i in self.pos_grid[x+1][y+1]:
                        resone[2].append(i)
                if(y+1 < self.grid_num and x > 0):
                        for i in self.pos_grid[x-1][y+1]:
                        resone[2].append(i)
                if(y > 0 and x > 0):
                        for i in self.pos_grid[x-1][y-1]:
                        resone[2].append(i)      
                if(y > 0 and x+1 < self.grid_num):
                        for i in self.pos_grid[x+1][y-1]:
                        resone[2].append(i)                          
                if(y+2 < self.grid_num):
                    for i in self.pos_grid[x][y+2]:
                        resone[2].append(i)
                if(x+2 < self.grid_num):
                    for i in self.pos_grid[x+2][y]:
                        resone[2].append(i)
                if(x > 1):
                    for i in self.pos_grid[x-2][y]:
                        resone[2].append(i)
                if(y > 1):
                    for i in self.pos_grid[x][y-2]:
                        resone[2].append(i)                        
                for num in resone[0]:
                    self.people[num].getVirus()


    def update(self):
        for i in range(self.num):
            self.people[i].randomMovement()
            self.people[i].recover()
        self.covid()
        self.patients = 0
        for i in range(self.num):
            for j in range(self.variety):
                self.pos[j][:, i] = self.remove
            self.pos[self.people[i].state][:, i] = self.people[i].pos
            self.patients += self.people[i].state

    def animate(self, _):
        self.update()
        if self.patients == 0:
            print("happy ending!")
            plt.close()
        elif self.patients == self.num:
            print("bad ending~")
            plt.close()
        for i in range(self.variety):
            self.plots[i].set_data(self.pos[i])
        return self.plots

    def show(self):
        plt.show()


if __name__ == "__main__":
    C = Crowd([-1, 1, -1, 1], 100, 2)
    C.show()
