# coding:utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
# 基本参数2：潜伏期传播能力
# I代表出现症状的病人
# 基本参数1：传播范围
# R代表被政府发现已经隔离的人
# 基本参数1：多少天隔离，检测能力
# 进阶参数1：对密切接触者的排查能力


class Person:
    infectiousRate = 0.1
    boundary = np.array([-1, 1])

    def __init__(self, pos, state=0):
        self.pos = pos
        self.delta = np.zeros(2)
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
    remove = outOfBound * np.ones(2)
    colors = ["b", "g", "r", "c", "m", "y", "k", "w"]

    def __init__(self, axis, num, variety):
        self.fig, self.ax = plt.subplots()
        self.ax = plt.axis(axis)
        self.variety = variety
        self.num = num
        self.pos = [self.outOfBound * np.ones((2, num)) for _ in range(self.variety)]
        self.people = [
            Person(np.random.uniform(low=-1, size=2)) for _ in range(self.num)
        ]
        self.people[0].getVirus()
        self.patients = 1
        self.plots = [
            plt.plot(self.pos[i][0], self.pos[i][1], self.colors[i] + "o")[0]
            for i in range(self.variety)
        ]
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
