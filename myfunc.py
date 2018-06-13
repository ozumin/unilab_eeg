# -*- coding: utf-8 -*-
import numpy as np
import thinkgear
import time as tm
PORT = '/dev/tty.MindWaveMobile-SerialPo'


def calc_nouha(intensities):
    '''
    各周波数の強度成分intensities(具体的にはmasaki)を受け取り、主要な強度に足し合わせる関数
    intensitiesの中身は[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgammma]である。
    返り値は、
    {alpha: 値,
    beta: 値,
    gamma: 値}の辞書型
    '''
    return {
        'alpha': sum(intensities[3:5]),
        'beta': sum(intensities[5:7]),
        'gamma': sum(intensities[7:9])
    }


def get_nouha(eeg):
    '''
    脳波の振幅強度をgetするための関数。
    引数
        eeg...str型。EEGPowerData(delta=1211157, theta=231413, lowalpha=40965, highalpha=57317, lowbeta=20250, highbeta=22608, lowgamma=1701, midgamma=442399)のような構造になったもの
    戻り値
        [delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の振幅強度を返す。
    '''
    l = eeg.split(", ")
    l = [x.split("=") for x in l]
    l[len(l) - 1][1] = l[len(l) - 1][1].replace(')', '')
    #print([l[i][1] for i in range(len(l))])
    # masakiはふざけてつけた変数名, それぞれの波の強度をint型で格納している。
    # masakiは順番にdelta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gammaみたいになっている。
    masaki = [int(l[i][1]) for i in range(len(l))]
    dat = calc_nouha(masaki)
    masaki.extend([dat['alpha'], dat['beta'], dat['gamma']])
    return masaki


def calibrate(PORT=PORT):
    '''
    キャリブレーションのための関数。人によって脳波が違いすぎるのでこれを行う。(脳波強度が正規分布に従って発生すると仮定)
    ここでは平均と標準偏差を求め、それらを返す。これによって後に平均0分散1となるような変形ができる
    引数
        とくになし。
    戻り値
        平均(mu)...[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の各平均値を順にリストで返す。
        標準偏差(sigma)...上記と同様、標準偏差を返す

    '''
    count = 0
    attention, meditation = 0, 0
    df = []
    for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
        for pkt in packets:
            if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
                continue
            t = str(pkt)
            # センサーで取得した値の格納
            if t != '':
                differencer = t[0:1]
                if int(differencer) == 1:
                    attention = int(t[1:])
                    print 'attention: %d' % attention
                if int(differencer) == 2:
                    meditation = int(t[1:])
                    print 'meditation: %d' % meditation
                if int(differencer) == 5:
                    eeg = t[1:]
                    # eggは各波長の強度を記述した文字列になっている。ので分割する。
                    masaki = get_nouha(eeg)
                    # print masaki
                    # masakiはふざけてつけた変数名, それぞれの波の強度をint型で格納している。
                    # masakiは順番にdelta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gammaみたいになっている。
                    if (attention != 0) and (meditation != 0):
                        df.append(masaki)
                        if count > 20:
                            # 条件を満たしたら平均分散の計算
                            #print df
                            df = np.array(df[3:])
                            #print df
                            mu = np.mean(df, axis=0)
                            print '平均', mu
                            sigma = np.std(df, axis=0)
                            # 最初の数点は誤差の可能性があるので捨てる。
                            return mu.tolist(), sigma.tolist()
                        count = count + 1


def transform(masaki, mu, sigma):
    '''
    masaki([delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の振幅強度)が与えられたら、それを平均0分散1になるようにmuとsigmaで調節する関数
    引数
        [delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]...それぞれの振幅強度

        mu...それぞれに対応する平均値のリスト

        sigma...それぞれに対応する標準偏差のリスト

    戻り値
        ret...平均値を引いて標準偏差でわった[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]のリスト
    '''
    if len(masaki) == len(mu):
        return [(x - m) / s for x, m, s in zip(masaki, mu, s)]
    else:
        print '!!!Maybe Error in transform()!!!'


def moving_average():
    '''
    移動平均を取るための関数。
    編集中
    '''


if __name__ == '__main__':
    print calibrate()

# 平均([677715.5263157894, 114093.63157894737, 24982.157894736843, 24046.526315789473, 19356.63157894737, 13616.842105263158, 5000.315789473684, 231846.26315789475, 43403.15789473684, 18617.157894736843, 231846.26315789475],

# 標準偏差[479656.80842094286, 125444.25667632134, 34211.296286557874, 26693.98110627074, 20394.499406020255, 19177.078566442025, 5538.17903811097, 259605.190335114, 46271.29902771168, 23882.26995572714, 259605.190335114])
