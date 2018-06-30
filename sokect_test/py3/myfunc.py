'''
python3系で動かすこと。
eeg_sendからのデータを受け取り。様々な処理をする。またmainで呼び出すための関数群を整備している。
'''
import socket
import time
import numpy as np

host = "127.0.0.1"  # ローカルホストを指定
port = 50007  # 適当なPORTを指定してあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host, port))  # IPとPORTを指定してバインドします
serversock.listen(64)  # 接続の待ち受けをします（キューの最大数を指定）

print('Waiting for connections...')
clientsock, client_address = serversock.accept()  # 接続されればデータを格納


def recieve_eeg():
    '''
    eegを受け取る関数。イテラブルオブジェクトである。
    使用例
    for a in recieve_eeg():
        print(a)
    '''

    while True:
        rcvmsg = clientsock.recv(4096)
        if rcvmsg == b'':
            break
        else:
            yield rcvmsg


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


def eeg_decoder(eeg):
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


def get_nouha(mu=[0] * 11, sigma=[1] * 11):
    '''
    イテラボーオブジェクト
    使用例
        for a in get_nouha():
        print(a)

    引数
    平均(mu)...[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の各平均値を順にリストで引き渡す
    標準偏差(sigma)...上記と同様、標準偏差を引き渡す。

    機能...脳波(次の戻り値)を次々と返す関数。なお、引数が指定されている場合は、それぞれの要素に対してmuとsigmaで正規化すて、返り値を返す。

    戻り値 {'eeg': [305563, 1231665, 300434, 807876, 146049, 349547, 95012, 1184955, 953925, 444559, 1184955], 'attention': 0, 'meditation': 0}のような辞書型。
    '''
    ret = {}
    for t in recieve_eeg():
        t = t.decode()
        differencer = t[0:1]
        if int(differencer) == 1:
            attention = int(t[1:])
            ret['attention'] = attention
            # print('attention: %d' % attention)
        if int(differencer) == 2:
            meditation = int(t[1:])
            ret['meditation'] = meditation
            # print('meditation: %d' % meditation)
        if int(differencer) == 5:
            eeg = t[1:]
            ret['eeg'] = eeg_decoder(eeg)
            ret['eeg'] = [(pwr - m) / s
                          for pwr, m, s
                          in zip(ret['eeg'], mu, sigma)]
        if len(ret) == 3:
            yield ret
            ret = {}

def caribrate():
    '''
    キャリブレーションのための関数。人によって脳波が違いすぎるのでこれを行う。(脳波強度が正規分布に従って発生すると仮定)
    ここでは平均と標準偏差を求め、それらを返す。これによって後に平均0分散1となるような変形ができる
    引数
        とくになし。
    戻り値
        平均(mu)...[delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, alpha, beta, gamma]の各平均値を順にリストで返す。
        標準偏差(sigma)...上記と同様、標準偏差を返す
    '''
    print('caribrating stand by...')
    count = 0
    df = []
    for mind in get_nouha():
        if (mind['attention'] != 0) & (mind['meditation'] != 0):
            df.append(mind['eeg'])
            if count == 20:
                print('caribrating...')
                df = np.array(df[3:])
                # print df
                mu = np.mean(df, axis=0)
                print('平均', mu)
                sigma = np.std(df, axis=0)
                # 最初の数点は誤差の可能性があるので捨てる。
                return mu.tolist(), sigma.tolist()
            count += 1


if __name__ == '__main__':
    mu, sigma = caribrate()
    for a in get_nouha(mu, sigma):
        print(a)
        print()

    # これをつけ忘れるな
    clientsock.close()
