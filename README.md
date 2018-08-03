Project: https://github.com/ozumin/unilab_eeg/tree/master
or
https://www.murata.eb.waseda.ac.jp/gitlab/masaki/mindwave


## ユニラブ用のプロジェクト

* タスクはIssuesで管理します。
* 締切は**7月末**

#### 技術的なtips
* pyserialを使え、ただしserialと競合する
```
pip uninstall serial
pip install pyserial
```

### 参考
Issues情報集めたうち、なんども参考にする記事はここにまとめましょう

* MindWaveからPythonを使って脳波の値を取得し、好きなプログラムで利用する方法
http://mikenerian.hatenablog.com/entry/2017/12/18/222633

* 公式ユーザーガイド
http://developer.neurosky.com/docs/lib/exe/fetch.php?media=mwmplus_qsg_print_8122016d_jp.pdf


### 使い方
プログラムの実行の仕方はここに書いて他の人も実行できるようにしておこう。

#### 脳波が他人と違うことの確かめかた
1. identify.pyを起動する

```
python3 identify.py hcl somebody(name)
```
2. 別のターミナルでmindwaveからデータを受信し、identify.pyに受け渡すプログラムを立ち上げる
```
cd ./send_eeg
python2 eeg_send.py
```
3. しばらくすると、データから特徴量の計算が終わりdata/の中に保存される。
4. ある人に2回ずつやらせる。
5. デンドログラムのpdfファイルを制作する
```
sh concat_result.sh
```
6. 結果のpdfが開くのでそれを見せる(クラスタリングに失敗することもある)

* 子どもたちのデータが溜まってきたら(元+更に3人はきついかもしれない)過去の測定データを削除する
```
sh clean.sh
```

#### オーロラで可視化するやり方
1. MurataMobile wifiをつけてパソコンを接続する．
    Auroraとmindwaveを起動しておく．
2. python3を立ち上げて以下のコマンドを打つ．
```
from nanoleaf import setup
from nanoleaf import Aurora
ipAddressList = setup.find_auroras()
```
3. AuroraのIPアドレスが出てくるのでトークンを作成する（IPアドレスは手動で打つ）
```
token = setup.generate_auth_token("IPアドレス")
```
4. トークンが作成されるのでこれをaurora_flow.pyの中にIPアドレスと共に書き込む．
```
my_aurora = Aurora("IPアドレス", "token")
```
    これで準備は整った．
5. 以下のコマンドを実行する．
```
python3 aurora_flow.py
```
別ウィンドウでsend_eeg/内で以下のコマンドを実行する．
```
python send_eeg.py
```
