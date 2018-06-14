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
    """
    リアルタイムでグラフ描画するクラス
    メソッドにはinitialize, set_data, pauseが入ってる
    呼び出されたら__init__でデータ数をself.numberに入れ，initializeを呼び出す
    """
    def __init__(self, masaki):
        # 最初にmasakiを渡してデータがいくつあるかをself.numberに入れる initializeを呼び出す
        self.number = len(masaki)
        self.fig = plt.figure(figsize=(12, 8))
        self.initialize()
        
    def position(self):
        ## 各プロットの位置を決める
        # plt.subplot2gridで3x4で分割するとしている
        self.pos = {}
        for i in range(self.number):
            self.pos[i,0] = i / 4 
            self.pos[i,1] = (i - self.pos[i,0]) % 4

    def initialize(self):
        ## 最初のプロットの設定
        self.fig.suptitle('monitoring sample', size=12)
        self.fig.subplots_adjust( left=0.05, bottom=0.1, right=0.95, top=0.90, wspace=0.2, hspace=0.6)
        self.position()
        # self.plotに軸やタイトルなどの設定をする
        # self.linesにプロットする線の情報を入れる
        self.plot = {}
        self.lines = {}
        for i in range(self.number):
            self.plot[i] = plt.subplot2grid((3,4), (self.pos[i,0], self.pos[i,1]))
            self.plot[i].grid(True)
            self.plot[i].set_title(str(i)) # ここにmasakiでの名前入れたい
            self.plot[i].set_xlabel('x')
            self.plot[i].set_ylabel('y')
            # プロットの初期化
            self.lines[i], = self.plot[i].plot([-1, -1], [1, 1], label=str(i))

    def set_data(self, data):
    # 値名と値を代入した辞書タイプのdataから，必要なデータをsubplotの値に代入します
        for i in range(self.number):
            self.lines[i].set_data(data[0], data[i+1])
            self.plot[i].set_xlim((data[0].min(), data[0].max()))
            self.plot[i].set_ylim((-1, 101))

    def pause(self, second):
        plt.pause(second)

# timeとxの初期化
time = 0
x = np.arange(-5, 5, 0.1)

#模擬データmasaki作成
n = 12 # number of data
masaki = [0] * n

#plot用のデータを格納するdata
data = {}
for i in range(n):
    data[i+1] = np.zeros(100)

RP = realtime_plot(masaki)

while(True):
    try:
        time += 1
        #ここでmasaki更新する
        for i in range(n):
            masaki[i] = time + i
        
        x = np.arange(-5 + 0.1 * time, 5 + 0.1 * time, 0.1)
        # data[0]にx軸のデータを格納
        data[0] = x
        for i in range(n):
            data[i+1] = np.append(data[i+1][1:], np.array([masaki[i]]))
        RP.set_data(data)
        RP.pause(0.1)
    except KeyboardInterrupt:
        sys.exit()
