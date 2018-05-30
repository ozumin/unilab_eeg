# -*- coding: utf-8 -*-
import numpy as np
import thinkgear
import matplotlib as mpl
import matplotlib.pyplot as plt

PORT = '/dev/tty.MindWaveMobile-SerialPo'

# matplotlibのデフォルト設定の変更
font = {'family':'monospace', 'size':'9'}
mpl.rc('font', **font)

class realtime_plot(object):

    def __init__(self):
        self.fig = plt.figure(figsize=(12,8))
        self.initialize()

    def initialize(self):
        self.fig.suptitle('monitoring sample', size=12)
        self.fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.90, wspace=0.2, hspace=0.6)
        self.ax00 = plt.subplot2grid((2,2),(0,0))
#        self.ax10 = plt.subplot2grid((2,2),(1,0))
#        self.ax01 = plt.subplot2grid((2,2),(0,1))
#        self.ax11 = plt.subplot2grid((2,2),(1,1))
        self.ax00.grid(True)
#        self.ax10.grid(True)
#        self.ax01.grid(True)
#        self.ax11.grid(True)
        self.ax00.set_title('real time result')
#        self.ax10.set_title('histogram')
#        self.ax01.set_title('correlation')
#        self.ax11.set_title('optimized result')
        self.ax00.set_xlabel('x')
        self.ax00.set_ylabel('y')
#        self.ax01.set_xlabel('correct')
#        self.ax01.set_ylabel('predict')
#        self.ax11.set_xlabel('correct')
#        self.ax11.set_ylabel('predict')

        # プロットの初期化
        self.lines000, = self.ax00.plot([-1,-1],[1,1],label='y1')
        self.lines001, = self.ax00.plot([-1,-1],[1,1],label='y2')
#        self.lines100 = self.ax10.hist([-1,-1],label='res1')
#        self.lines101 = self.ax10.hist([-1,-1],label='res2')
#        self.lines01, = self.ax01.plot([-1,-1],[1,1],'.')
#        self.lines11, = self.ax11.plot([-1,-1],[1,1],'.r')

    # 値名と値を代入した辞書タイプのdataから，必要なデータをsubplotの値に代入します
    def set_data(self,data):

        self.lines000.set_data(data['x'],data['y1'])
        self.lines001.set_data(data['x'],data['y2'])
        self.ax00.set_xlim((data['x'].min(),data['x'].max()))
        self.ax00.set_ylim((0,100))
        # 凡例を固定するために必要
        self.ax00.legend(loc='upper right')

#        self.lines01.set_data(data['corr'],data['pred'])
#        self.ax01.set_xlim((-2,12))
#        self.ax01.set_ylim((-2,12))

    def pause(self,second):
        plt.pause(second)

# 使用例
RP = realtime_plot()
data = {}
x = np.arange(-np.pi,np.pi,0.1)
y1 = np.sin(x)
y2 = np.cos(x)
opt_coef = 0
attention = 5 
meditation = 0

for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for pkt in packets:
        if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
            continue

        t = str(pkt)

        if t != '':
            differencer = t[0:1]
            if int(differencer) == 1:
                attention = t[1:]
                print 'attention: %d' %int(attention)
            if int(differencer) == 2:
                meditation = t[1:]
                print 'meditation: %d' %int(meditation)
            if int(differencer) == 5:
                eeg = t[1:]
                #print eeg
                l = eeg.split(", ")
                l = [x.split("=") for x in l]
                l[len(l)-1][1] = l[len(l)-1][1].replace(')','')
                #print([l[i][1] for i in range(len(l))])
                masaki = [int(l[i][1]) for i in range(len(l))]
                #print([float(masaki[i])/sum(masaki) for i in range(len(masaki))])
            x += 0.1
            print(type(x))
            y1 = int(attention)
            y2 = int(meditation)
            data['x'] = np.pi * x
            data['y1'] = y1
            data['y2'] = y2
    #        data['corr'] = 0 
    #        data['pred'] = 0
            RP.set_data(data)
            RP.pause(0.1)
