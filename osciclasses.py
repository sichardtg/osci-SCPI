import SCPI

def calcScalPrefactor(letter):

    match letter:
        case 'n':
            return 1e-9
        case 'u':
            return 1e-6
        case 'm':
            return 1e-3
        case _:
            
            
            return 1

class verticalScale:
    numeric=1
    string="1"

    def __init__(self):
        return

    def getNumeric(self):
        return self.numeric

    def getStr(self):
        return self.string

    def updateFromSCPI(self,conn):
        conn.reset()
        try:
            scalV=conn.send(':CH1:SCALe?')
            scalV=scalV.tobytes().decode('utf-8')

            vunit=calcScalPrefactor(scalV[-3])

            if(vunit==1):
                vperdiv=float(scalV[:-2])
            else:
                vperdiv=float(scalV[:-3])*vunit

        except:
            print("error reading vert scale.")
            vperdiv=1
        self.numeric=vperdiv
        self.string=scalV.strip()



class osciChannel:
    chId=1
    vertScale=verticalScale()
    vertOffset=0
    coupling="DC"
    data=[]
    offset=0
    active=1

    def getOffsetFromSCPI(self,conn):
        try:
            res=conn.send(':CH{}:OFFSet?'.format(self.chId))
            off=res.tobytes().decode('utf-8')
            #print(off)
            self.offset=float(off)*self.vertScale.getNumeric()
        except:
            self.offset=0
    
    def getCouplingFromSCPI(self, conn):
        res=conn.send(':CH{}:COUPling?'.format(self.chId))
        self.coupling=res.tobytes().decode('utf-8').strip()

    def updateSettingsFromSCPI(self,conn):
        try:
            self.vertScale.updateFromSCPI(conn)
        except:
            print("could not update vertical scale for channel ", self.chId)
        try:
            self.getOffsetFromSCPI(conn)
        except:
            print("could not update offset for channel ", self.chId)
        try:
            self.getCouplingFromSCPI(conn)
        except:
            print("could not update coupling for channel ", self.chId)


    def writeSettingsToSCPI(self):
        return


    def __init__(self,ChId=1,vertScale=verticalScale(),vertOffset=0, coupling="DC"):
        self.chId=ChId
        self.vertScale=vertScale
        self.vertOffset=vertOffset
        self.coupling=coupling
        self.active=1

    def getDataFromSCPI(self,conn):
        # first 4 bytes indicate the number of data bytes following
        rawdata = conn.send(':DATA:WAVE:SCREen:CH{}?'.format(self.chId))
        self.data = []
        for idx in range(4,len(rawdata),2):
            # take 2 bytes and convert them to signed integer using "little-endian"
            point = int().from_bytes([rawdata[idx], rawdata[idx+1]],'little',signed=True)
            self.data.append(point/4096)  # data as 12 bit
        #print(self.chId)
        #print(self.data)



class osciTrigger:
    mode="AUTO"
    level=1
    source="CH1"
    coupling="DC"
    edge="RISE"

    def __init__(self):
        self.mode="AUTO"
        self.level=1
        self.source="CH1"
        self.coupling="DC"
        self.edge="RISE"

    def updateFromSCPI(self, conn):
        return


class timeScale:
    numeric=1
    string="1 s"

    def __init__(self):
        return

    def getNumeric(self):
        return self.numeric

    def getStr(self):
        return self.string

    def updateFromSCPI(self,conn):
        conn.reset()
        res=conn.send(':HORizontal:SCALe?')
        scalStr=res.tobytes().decode('utf-8')
        unit=calcScalPrefactor(scalStr[-3])
        if(unit==1):
            self.numeric=float(scalStr[:-2])
        else:
            self.numeric=float(scalStr[:-3])*unit
        self.string=scalStr.strip()

class osciDevice:
    channels=list()
    idVendor=0x5345
    idProduct=0x1234
    endPointOut=0x01
    endPointIn=0x81
    trigger=osciTrigger()
    availableScales = list()
    timescale=1
    conn=0


    def __init__(self):
        self.channels.append(osciChannel())
        #self.channels.append(osciChannel(ChId=2))
        self.conn=SCPI.SCPIconnector(self.idVendor, self.idProduct,self.endPointOut, self.endPointIn)
        self.timescale=timeScale()

    def addChannel(self):
        self.channels.append(osciChannel())
    
    def getScalesFromSCPI(self):
        self.availableScales=list()
        return


    def updateSettings(self):
        for ch in self.channels:
            ch.updateSettingsFromSCPI(self.conn)
        self.trigger.updateFromSCPI(self.conn)
        self.getScalesFromSCPI()
        self.timescale.updateFromSCPI(self.conn)        

    def updateData(self):
        #print("fetching data...")
        for ch in self.channels:
            if(ch.active==1):
                ch.getDataFromSCPI(self.conn)
        #print("done fetching data.")

    def getData(self):
        res=list()
        for ch in self.channels:
            if (ch.active==1):
                res.append(ch.data)
            return res
