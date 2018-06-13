# -*- coding: utf-8 -*-
import time as tm
import numpy as np
import thinkgear
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys

PORT = '/dev/tty.MindWaveMobile-SerialPo'

# matplotlibのデフォルト設定の変更
font = {'family': 'monospace', 'size': '9'}
mpl.rc('font', **font)

class realtime_plot(object):

    def __init__(self, data):
        self.number = len(data)
        self.fig = plt.figure(figsize=(12, 8))
        self.initialize()

    def initialize(self):
        self.fig.suptitle('monitoring sample', size=12)
        self.fig.subplots_adjust(
            left=0.05, bottom=0.1, right=0.95, top=0.90, wspace=0.2, hspace=0.6)
        self.plot = {}
        self.lines = {}
        for i in range(self.number-1):
            self.plot[i] = plt.subplot2grid((2,3), (i, i))
            self.plot[i].grid(True)
            self.plot[i].set_title(str(i))
            self.plot[i].set_xlabel('x')
            self.plot[i].set_ylabel('y')
            # プロットの初期化
            if i == 0:
                self.lines[i], = self.plot[i].plot([-1, -1], [1, 1], label='attention')
                self.lines[i+1], = self.plot[i].plot([-1, -1], [1, 1], label='meditation')
            else:
                self.lines[i+1], = self.plot[i].plot([-1, -1], [1, 1], label=str(i))

    # 値名と値を代入した辞書タイプのdataから，必要なデータをsubplotの値に代入します
    def set_data(self, data):
        
        for i in range(self.number-1):
            self.lines[i+1].set_data(data[0], data[i+2])
            if i == 0:
                self.lines[0].set_data(data[0], data[i+1])
                # 凡例を固定するために必要
                self.plot[i].legend(loc='upper right')
            self.plot[i].set_xlim((data[0].min(), data[0].max()))
            self.plot[i].set_ylim((-1, 101))

    def pause(self, second):
        plt.pause(second)

# timeとxの初期化
time = 0
x = np.arange(-5, 5, 0.1)

#模擬データmasaki作成
n = 3 # number of data
masaki = [0] * n

#plot用のデータを格納する
data = {}
for i in range(n):
    data[i+1] = np.zeros(100)

RP = realtime_plot(masaki)

#ここでmasaki更新する
while(True):
    try:
        time += 1
        #ここでmasaki更新する
        for i in range(n):
            masaki[i] = time + i
        
        x = np.arange(-5 + 0.1 * time, 5 + 0.1 * time, 0.1)
        data[0] = x
        for i in range(n):
            data[i+1] = np.append(data[i+1][1:], np.array([masaki[i]]))
        RP.set_data(data)
        RP.pause(0.1)
    except KeyboardInterrupt:
        sys.exit()
