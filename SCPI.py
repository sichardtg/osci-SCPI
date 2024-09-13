import usb.core
import usb.util
from matplotlib import pyplot as plt
from fftplot import plotFFT

dev = usb.core.find(idVendor=0x5345, idProduct=0x1234)

if dev is None:
    raise ValueError('Device not found')
else:
    print(dev)
    dev.set_configuration()

def send(cmd):
    # address taken from results of print(dev):   ENDPOINT 0x3: Bulk OUT
    dev.write(0x1,cmd)
    # address taken from results of print(dev):   ENDPOINT 0x81: Bulk IN
    result = (dev.read(0x81,100000,1000)) #addr, len, timeout
    return result

def get_id():
    return send('*IDN?').tobytes().decode('utf-8')

def get_data(ch):
    # first 4 bytes indicate the number of data bytes following
    rawdata = send(':DATA:WAVE:SCREen:CH{}?'.format(ch))
    data = []
    for idx in range(4,len(rawdata),2):
        # take 2 bytes and convert them to signed integer using "little-endian"
        point = int().from_bytes([rawdata[idx], rawdata[idx+1]],'little',signed=True)
        data.append(point/4096)  # data as 12 bit
    return data

def get_header():
    # first 4 bytes indicate the number of data bytes following
    header = send(':DATA:WAVE:SCREen:HEAD?')
    header = header[4:].tobytes().decode('utf-8')
    return header

def save_data(ffname,data):
    f = open(ffname,'w')
    f.write('\n'.join(map(str, data)))
    f.close()

def scpi():
    print(get_id())
    header = get_header()

#plt.figure(1)
#plt.ion()
#plt.show()
#plt.grid()
#i=0
#while (i<200):
#    i=i+1
#    print("plot...",i)
    data = get_data(1)
#save_data('Osci.dat',data)
#    plt.figure(1)
#    plt.clf()
#    plt.plot(data, 'y')
#    plt.draw()
#    plt.pause(0.001)
#    plotFFT(data)
    dev.reset()
    return data
#dev.reset()

