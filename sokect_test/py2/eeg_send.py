# -*- coding: utf-8 -*-
import thinkgear
import socket
PORT = '/dev/tty.MindWaveMobile-SerialPo'


host = "127.0.0.1"  # ローカルホストを指定
port = 50007  # 適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # オブジェクトの作成をします
client.connect((host, port))  # これでサーバーに接続します

if __name__ == '__main__':
    print starting...

    # ここでmindwaveと接続する。
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
                    # eeegを直接送信する。
                    print 'sent ->', eeg
                    client.send(str(eeg))
