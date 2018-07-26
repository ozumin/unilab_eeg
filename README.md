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

#### 当てゲームのしかた
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
4. 1,2,3を2~3人に2回ずつ(根拠なし)やらせる。
5. dend.Rでデンドログラムのpdfファイルを制作する
```
Rscript dend.R
```
6. pdfのクラスター構造を見て、誰の脳波かを判断する


