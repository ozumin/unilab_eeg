# -*- coding: utf-8 -*-
import time as tm
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
        self.ax10 = plt.subplot2grid((2,2),(1,0))
        self.ax01 = plt.subplot2grid((2,2),(0,1))
        self.ax11 = plt.subplot2grid((2,2),(1,1))
        self.ax00.grid(True)
        self.ax10.grid(True)
        self.ax01.grid(True)
        self.ax11.grid(True)
        self.ax00.set_title('attention and meditation')
        self.ax10.set_title('eeg')
        self.ax01.set_title('highalpha')
        self.ax11.set_title('lowgamma')
        self.ax00.set_xlabel('x')
        self.ax00.set_ylabel('y')
        self.ax10.set_xlabel('x')
        self.ax10.set_ylabel('y')
        self.ax01.set_xlabel('x')
        self.ax01.set_ylabel('y')
        self.ax11.set_xlabel('x')
        self.ax11.set_ylabel('y')
#        self.ax01.set_xlabel('correct')
#        self.ax01.set_ylabel('predict')
#        self.ax11.set_xlabel('correct')
#        self.ax11.set_ylabel('predict')

        # プロットの初期化
        self.lines000, = self.ax00.plot([-1,-1],[1,1],label='attention')
        self.lines001, = self.ax00.plot([-1,-1],[1,1],label='meditation')
        self.lines100, = self.ax10.plot([-1,-1],[1,1],label='delta')
        self.lines101, = self.ax10.plot([-1,-1],[1,1],label='theta')
        self.lines102, = self.ax10.plot([-1,-1],[1,1],label='lowalpha')
        self.lines103, = self.ax10.plot([-1,-1],[1,1],label='highalpha')
        self.lines104, = self.ax10.plot([-1,-1],[1,1],label='lowbeta')
        self.lines105, = self.ax10.plot([-1,-1],[1,1],label='highbeta')
        self.lines106, = self.ax10.plot([-1,-1],[1,1],label='lowgamma')
        self.lines107, = self.ax10.plot([-1,-1],[1,1],label='midgamma')
        self.lines01, = self.ax01.plot([-1,-1],[1,1],label='highalpha')
        self.lines11, = self.ax11.plot([-1,-1],[1,1],label='lowgamma')
#        self.lines01, = self.ax01.plot([-1,-1],[1,1],'.')
#        self.lines11, = self.ax11.plot([-1,-1],[1,1],'.r')

    # 値名と値を代入した辞書タイプのdataから，必要なデータをsubplotの値に代入します
    def set_data(self,data):

        self.lines000.set_data(data['x'],data['y1'])
        self.lines001.set_data(data['x'],data['y2'])
        self.ax00.set_xlim((data['x'].min(),data['x'].max()))
        self.ax00.set_ylim((-1,101)) 
        self.lines100.set_data(data['x'],data['delta'])
        self.lines101.set_data(data['x'],data['theta'])
        self.lines102.set_data(data['x'],data['lowalpha'])
        self.lines103.set_data(data['x'],data['highalpha'])
        self.lines104.set_data(data['x'],data['lowbeta'])
        self.lines105.set_data(data['x'],data['highbeta'])
        self.lines106.set_data(data['x'],data['lowgamma'])
        self.lines107.set_data(data['x'],data['midgamma'])
        self.ax10.set_xlim((data['x'].min(),data['x'].max()))
        self.ax10.set_ylim((-0.01,1))
        self.lines01.set_data(data['x'],data['highalpha_'])
        self.lines11.set_data(data['x'],data['lowgamma_'])
        self.ax01.set_xlim((data['x'].min(),data['x'].max()))
        self.ax01.set_ylim((-0.01,1677721))
        self.ax11.set_xlim((data['x'].min(),data['x'].max()))
        self.ax11.set_ylim((-0.01,1677721))
        # 凡例を固定するために必要
        self.ax00.legend(loc='upper right')
        self.ax10.legend(loc='upper left')

#        self.lines01.set_data(data['corr'],data['pred'])
#        self.ax01.set_xlim((-2,12))
#        self.ax01.set_ylim((-2,12))

    def pause(self,second):
        plt.pause(second)

# 使用例
RP = realtime_plot()
data = {}
#x = np.arange(-np.pi,np.pi,0.1)
time = 0
x = np.arange(-5, 5, 0.1)
data['y1'] = np.zeros(100)
data['y2'] = np.zeros(100)
data['delta'] = np.zeros(100)
data['theta'] = np.zeros(100)
data['lowalpha'] = np.zeros(100)
data['highalpha'] = np.zeros(100)
data['lowbeta'] = np.zeros(100)
data['highbeta'] = np.zeros(100)
data['lowgamma'] = np.zeros(100)
data['midgamma'] = np.zeros(100)
data['highalpha_'] = np.zeros(100)
data['lowgamma_'] = np.zeros(100)
#m0 = np.zeros(100)
#m1 = np.zeros(100)
#m2 = np.zeros(100)
#m3 = np.zeros(100)
#m4 = np.zeros(100)
#m = np.zeros(100)
#m = np.zeros(100)
#m = np.zeros(100)
opt_coef = 0
attention = 5 
meditation = 0
highalpha = 0 
lowgamma = 0
masaki_ = [np.zeros(100)]*8
masaki = [0]*8

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
                highalpha = masaki[3]
                lowgamma = masaki[6]
                masaki[2:] = [float(masaki[i])/sum(masaki[2:]) for i in range(2,len(masaki))]
            
            tm.sleep(0.2)
            time += 1
            x = np.arange(-5+0.1*time, 5+0.1*time, 0.1)
#            y1_new = np.append(y1[1:], np.array([int(attention)]))
#            y1 = y1_new
#            y2_new = np.append(y2[1:], np.array([int(meditation)]))
#            y2 = y2_new
            data['x'] = x
            data['y1'] = np.append(data['y1'][1:], np.array([int(attention)]))
            data['y2'] = np.append(data['y2'][1:], np.array([int(meditation)]))
            data['delta'] = np.append(data['delta'][1:], np.array([masaki[0]]))
            data['theta'] = np.append(data['theta'][1:], np.array([masaki[1]]))
            data['lowalpha'] = np.append(data['lowalpha'][1:], np.array([masaki[2]]))
            data['highalpha'] = np.append(data['highalpha'][1:], np.array([masaki[3]]))
            data['lowbeta'] = np.append(data['lowbeta'][1:], np.array([masaki[4]]))
            data['highbeta'] = np.append(data['highbeta'][1:], np.array([masaki[5]]))
            data['lowgamma'] = np.append(data['lowgamma'][1:], np.array([masaki[6]]))
            data['midgamma'] = np.append(data['midgamma'][1:], np.array([masaki[7]]))
            data['highalpha_'] = np.append(data['highalpha_'][1:], np.array([int(highalpha)]))
            data['lowgamma_'] = np.append(data['lowgamma_'][1:], np.array([int(lowgamma)]))
            RP.set_data(data)
            RP.pause(0.1)
