# -*- coding: utf-8 -*-
'''
このプログラムはpython2系
https://qiita.com/nadechin/items/28fc8970d93dbf16e81b
'''
import socket
import time

host = "127.0.0.1"  # ローカルホストを指定
port = 50007  # 適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # オブジェクトの作成をします
client.connect((host, port))  # これでサーバーに接続します


if __name__ == '__main__':
    test = 1
    while (1):
        print 'sent ->', test
        client.send(str(test))
        test = test + 1
        time.sleep(0.5)
