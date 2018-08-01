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
                #print eeg
                l = eeg.split(", ")
                l = [x.split("=") for x in l]
                l[len(l)-1][1] = l[len(l)-1][1].replace(')','')
                #print([l[i][1] for i in range(len(l))])
                masaki = [int(l[i][1]) for i in range(len(l))]
                #print([float(masaki[i])/sum(masaki) for i in range(len(masaki))])
                print([float(masaki[i])/(sum(masaki)-masaki[0]) for i in range(1,len(masaki))])

                #print([int(x) for x in l])
