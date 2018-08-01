import thinkgear

PORT = '/dev/tty.MindWaveMobile-SerialPo'

for packets in thinkgear.ThinkGearProtocol(PORT).get_packets():
    for pkt in packets:
        if isinstance(pkt, thinkgear.ThinkGearRawWaveData):
            continue

        t = str(pkt)

        if t != '':
            differencer = t[0:1]
            if int(differencer) == 1:
                attention = t[1:]
                print int(attention)
