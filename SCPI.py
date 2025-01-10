import usb.core
import usb.util
#from matplotlib import pyplot as plt
#from fftplot import plotFFT

class SCPIconnector:
    dev=0
    endPointOut=0x01
    endPointIn=0x81
    def __init__(self,vendor, product, epOut, epIn):
        self.endPointOut=epOut
        self.endPointIn=epIn
        self.dev = usb.core.find(idVendor=0x5345, idProduct=0x1234)
        #self.dev = usb.core.find(idVendor=vendor, idProduct=product)
        if self.dev is None:
            raise ValueError('Device not found')
        else:
            print(self.dev)
            self.dev.set_configuration()

    def send(self,cmd):
        # address taken from results of print(dev):   ENDPOINT 0x3: Bulk OUT
        self.dev.write(self.endPointOut,cmd)
        # address taken from results of print(dev):   ENDPOINT 0x81: Bulk IN
        result = (self.dev.read(self.endPointIn,100000,10000)) #addr, len, timeout
        return result

 #   def get_id():
 #       return send('*IDN?').tobytes().decode('utf-8')

#def get_data(ch):
#    # first 4 bytes indicate the number of data bytes following
#    rawdata = send(':DATA:WAVE:SCREen:CH{}?'.format(ch))
#    data = []
#    for idx in range(4,len(rawdata),2):
#        # take 2 bytes and convert them to signed integer using "little-endian"
#        point = int().from_bytes([rawdata[idx], rawdata[idx+1]],'little',signed=True)
#        data.append(point/4096)  # data as 12 bit
#    return data

#def get_header():
#    # first 4 bytes indicate the number of data bytes following
#    header = send(':DATA:WAVE:SCREen:HEAD?')
#    header = header[4:].tobytes().decode('utf-8')
#    return header

#def save_data(ffname,data):
#    f = open(ffname,'w')
#    f.write('\n'.join(map(str, data)))
#    f.close()

    
    def reset(self):
        self.dev.reset()
    



#def scpi():
#    dev.reset()
#    print(get_id())
#    header = get_header()

#    data = get_data(1)
#save_data('Osci.dat',data)
    #dev.reset()
#    return data

