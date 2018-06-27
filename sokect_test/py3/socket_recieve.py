'''
このプログラムはpython3系
https://qiita.com/nadechin/items/28fc8970d93dbf16e81b
'''
import socket

host = "127.0.0.1"  # ローカルホストを指定
port = 50007  # 適当なPORTを指定してあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host, port))  # IPとPORTを指定してバインドします
serversock.listen(10)  # 接続の待ち受けをします（キューの最大数を指定）

if __name__ == '__main__':
    print ('Waiting for connections...')
    clientsock, client_address = serversock.accept()  # 接続されればデータを格納

    while True:
        rcvmsg = clientsock.recv(1024)
        if rcvmsg == b'':
            break
        else:
            rcv = int(rcvmsg)
            print('Received ->', rcv)

    clientsock.close()
