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
                print 'attention: %d' %int(attention)
            if int(differencer) == 2:
                meditation = t[1:]
                print 'meditation: %d' %int(meditation)
            if int(differencer) == 5:
                eeg = t[1:]
                print eeg
