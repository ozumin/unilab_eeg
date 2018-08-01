from nanoleaf import setup
from nanoleaf import Aurora
import time as tm
import sys

# auroraのip addressを見つけてトークンを作成する．
# 日によってip addressは異なる場合がある
#ipAddressList = setup.find_auroras()
#token = setup.generate_auth_token("10.0.1.2")

# auroraと接続する
my_aurora = Aurora("10.0.1.3", "ufeEL3sFsRYJB92XH6gDG6O5oXRIJPhB")
my_aurora.on = True
#for panel in my_aurora.panel_positions:
#  print(panel['panelId'])

# panel index
# 218, 113, 23, 101, 77, 87, 86, 209, 53

# effectの設定
effect_data = {
    "command" : "add",
    "animName": "Flash",
    "animType": "static",
    "animData": '1 87 1 0 0 255 0 10',
    "loop": True
}

test = '1 87 3 255 0 255 0 20' + ' 0 0 255 0 20 0 255 255 0 20'
test = '2 87 1 0 255 255 0 20 209 1 0 255 0 0'

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
my_aurora.effect_set_raw(effect_data2)
