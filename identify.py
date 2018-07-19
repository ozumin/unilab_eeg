# coding:utf-8
'''
人あてゲームをするためのプログラム
'''

import myfunc as mf
import numpy as np
import csv
import sys
import pandas as pd

def calc_features(tau=20):
    '''
    脳波の特徴量を計算する関数。それぞれの周波数強度の平均と標準偏差を特徴とする。
    引数
        tau ... 平均と標準偏差を計算するための窓幅
    戻り値
        平均(mu)...[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の各平均値を順にリストで返す。
        標準偏差(sigma)...上記と同様、標準偏差を返す
    '''
    print('calculating features...')
    count = 0
    df = []
    for mind in mf.get_nouha():
        if (mind['attention'] != 0) & (mind['meditation'] != 0):
            df.append(mind['eeg'])
            if count == tau:
                print('caribrating...')
                df = np.array(df[3:])
                # print df
                mu = np.mean(df, axis=0)
                sigma = np.std(df, axis=0)
                print('平均', mu, sigma)
                # 最初の数点は誤差の可能性があるので捨てる。
                return mu.tolist(), sigma.tolist()
            count += 1

def raw_nouha(tau=20):
    print('calculating features...')
    count = 0
    df = pd.DataFrame()
    for mind in mf.get_nouha():
        if (mind['attention'] != 0) & (mind['meditation'] != 0):
            df = pd.concat([df,pd.DataFrame({str(count) : mind['eeg']})], axis=1)
            if count == tau:
                print(df)
                return df
            count += 1

if __name__ == '__main__':
    name = sys.argv #誰のデータかを保存
    name = name[1]
    
#    mu, sigma = calc_features(40)
    data = raw_nouha(20)
    print(data)
    print(type(data))
    data.to_csv('./' + name + 'result.csv')
#    with open('./' + name + 'result.csv', 'a') as f:
#        writer = csv.writer(f)
#        writer.writerow(data)
