from nanoleaf import setup
from nanoleaf import Aurora
import time as tm
import sys

# auroraのip addressを見つけてトークンを作成する．
# 日によってip addressは異なる場合がある
#ipAddressList = setup.find_auroras()
#token = setup.generate_auth_token("10.0.1.2")

# auroraと接続する
my_aurora = Aurora("10.0.1.3", "b2UeRO2H2aImB4uHYbDKtYCHJDIxuE4W")
my_aurora.on = True
#for panel in my_aurora.panel_positions:
#  print(panel['panelId'])

# panel index
# 218, 113, 23, 101, 77, 87, 86, 209, 53

# 色の指定を行う
# animDataに入れるのは，'(panel数) (panel index) (frame数) (R) (G) (B) (W) (遷移時間)'
# (panel数)だけ最初に一つ指定
# list[0]はpanel index
# index[1]はindex + frame数
index = [['23', '53', '77', '86', '87', '101', '113', '209', '218'], 
        ['23 1 ', '53 1 ', '77 1 ', '86 1 ', '87 1 ', '101 1 ', '113 1 ', '209 1 ', '218 1 ']]

color = []
for i in range(len(index[1])):
    color.append('255 0 0 0 10 ')

newcolor = '0 255 255 0 10 '
color.insert(0, newcolor)
color.pop()
while(True):
    try:
        tm.sleep(0.7)
        animdata = '9 '

        newcolor = '255 0 255 0 10 '

        color.insert(0, newcolor)
        color.pop()

        for i in range(len(color)):
            animdata += index[1][i] + color[i]

        effect_data = {
            "command" : "add",
            "animName": "Flash",
            "animType": "custom",
            "animData": animdata,
            "loop": True
        }

        my_aurora.effect_set_raw(effect_data)

    except KeyboardInterrupt:
        sys.exit()

# effectの設定
effect_data = {
    "command" : "add",
    "animName": "Flash",
    "animType": "static",
    "animData": '1 87 1 0 0 255 0 10',
    "loop": True
}

test = '1 87 3 255 0 255 0 20' + ' 0 0 255 0 20 0 255 255 0 20'

effect_data2 = {
    "command" : "add",
    "animName": "Flash",
    "animType": "custom",
    "animData": test,
    "loop": True
}

# effectをauroraに設定する
#my_aurora.effect_set_raw(effect_data)
#tm.sleep(2)
#my_aurora.effect_set_raw(effect_data2)
