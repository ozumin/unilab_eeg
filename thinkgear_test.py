import thinkgear

PORT = '/dev/tty.MindWaveMobile-SerialPo'
for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for i, p in enumerate(packets):
        if isinstance(p, thinkgear.ThinkGearRawWaveData):
            continue
        if i == 0:
            print
        print(p)

'''
30
5EEGPowerData(delta=1211157, theta=231413, lowalpha=40965, highalpha=57317, lowbeta=20250, highbeta=22608, lowgamma=1701, midgamma=442399)
148
264

みたいなデータ構造になっていて、先頭の文字が測っているものの種類を表している。
'''
