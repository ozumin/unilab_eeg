from nanoleaf import setup
from nanoleaf import Aurora
import time as tm
import sys
import myfunc
# auroraのip addressを見つけてトークンを作成する．
# 日によってip addressは異なる場合がある
#ipAddressList = setup.find_auroras()
#token = setup.generate_auth_token("10.0.1.2")

# auroraと接続する
my_aurora = Aurora("10.0.1.2", "KtYCHJDIxuE4WEY8fuAuuiBftFZAnAL5")
my_aurora.on = True
my_aurora.brightness_raise(100)
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
    color.append('255 255 255 0 0 ')

#newcolor = '0 255 255 0 0 '
#color.insert(0, newcolor)
#color.pop()

#g = '50'
count = 0
dat = ()

# calibration
mu, sigma = myfunc.caribrate()

def rgb(wave):
    color = int(float(wave * 65 + 130))
    if color > 255: color = 255
    elif color < 0: color = 0
    return str(color)

# after calibration
while True:
    try:
        for a in myfunc.get_nouha(mu, sigma):
            count += 1
            if(count < 6):
                dat = dat + (a['eeg'],)
                ave = a['eeg']
            else:
                dat = dat[1:] + (a['eeg'],)
            ave = myfunc.moving_average(*dat)
            print(ave)
            print(a['meditation'])
            print(a['attention'])
            animdata = '9 '
            r = rgb(ave[9])
            g = rgb(ave[10])
            b = rgb(ave[8])
            newcolor = r + ' ' + g + ' ' + b + ' ' +'0 0 '
            print(newcolor)
            type(newcolor)

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
    except ValueError:
        print("ValueError") 

clientsock.close()
