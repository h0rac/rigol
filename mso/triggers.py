import json 

with open('/Users/grzegorz.wypych@pl.ibm.com/tools/rigol/rs232.json', 'r') as f:
    rs232 = json.load(f)

class TriggerFactory(object):

    def factory(type, instr):
        if type == "RS232":
            return RS232(instr)

    factory = staticmethod(factory)

class RS232(TriggerFactory):

    def __init__(self, instr):
        TriggerFactory.__init__(self)
        self.instr = instr

    def getSourceChannel(self):
          return    self.instr.ask(":TRIGger:RS232:SOURce?")

    def getBoud(self):
        return  self.instr.ask(":TRIGger:RS232:BAUD?")
    
    def getVoltageLevel(self):
        return  self.instr.ask(":TRIGger:RS232:LEVel?")

    def getWhen(self):
         return self.instr.ask(":TRIGger:RS232:WHEN?")
    
    def getData(self):
        return  self.instr.ask(":TRIGger:RS232:DATA?")
    
    def getStopBit(self):
         return self.instr.ask(":TRIGger:RS232:STOP?")
    
    def getParity(self):
        return  self.instr.ask(":TRIGger:RS232:PARity?")
    
    def getDataBits(self):
        return  self.instr.ask(":TRIGger:RS232:WIDTh?")

    def setBoud(self, boud):
        try:
            self.instr.write(":TRIGger:RS232:BAUD {0}".format(boud))
        except KeyError as err:
            print('Unsupported boud:', err)
    
    def setVoltageLevel(self, voltage):
        try:
            self.instr.write(":TRIGger:RS232:LEVel {0}".format(voltage))
        except Error as err:
            print('Unsupported voltage:', err)
    
    def setSourceChannel(self, chan):
        try:
            self.instr.write(":TRIGger:RS232:SOURce {0}".format(rs232['source'][chan.lower()]))
        except KeyError as err:
            print('Unsupported channel source:', err)
    
        
    def setWhen(self, value):
        try:
            self.instr.write(":TRIGger:RS232:WHEN {0}".format(rs232['when'][value.lower()]))
        except KeyError as err:
            print('Unsupported when source:', err)
    
    def setData(self, num):
        result = num in rs232['data']
        if result:
            self.instr.write(":TRIGger:RS232:DATA {0}".format(num))
        else:
            print('Unsupported data, accept value in range 0-255')
            return False
    
    def setStopBit(self, stopBit):
        result = stopBit in rs232['stopBits']
        if result:
            self.instr.write(":TRIGger:RS232:STOP {0}".format(stopBit))
        else:
            print('Unsupported value, accept 1,1.5,2')
            return False
    
    def setParity(self, parity):
        try:
            self.instr.write(":TRIGger:RS232:PARity {0}".format(rs232['parity'][parity.lower()]))
        except KeyError as err:
            print('Unsupported parity, accept ODD, EVEN, NONE:', err)
    
    def setDataBits(self, bits):
        result = bits in rs232['dataBits']
        if result:
            self.instr.write(":TRIGger:RS232:WIDTh {0}".format(bits))
        else:
            print('Unsupported value, accept 5,6,7 or 8')
            return False
         
    
    def setup(self, src = "chan1", voltage = 0, baud=9600, when="data",data=10, dataBits=8, stopBit=1, parity="none"):
        self.setSourceChannel(src)
        self.setVoltageLevel(voltage)
        self.setBoud(baud)
        self.setWhen(when)
        if when == "data":
            self.setData(data)
        self.setStopBit(stopBit)
        self.setParity(parity)
        self.setDataBits(dataBits)
    
    def restoreDefault(self):
        self.setup()
        return {'src':self.getSourceChannel(), 'voltage':self.getVoltageLevel(), 'baud':self.getBoud(), "when":self.getWhen(),
        'data':self.getData(), "stopBit":self.getStopBit()
         }

    def getDefaults(self):
        return {'src':'chan1', 'voltage':0, 'baud':9600, 'when':"data","data":10, "dataBits":8, "stopBit":1, "parity":'none'}
    
    def getCurrentSetup(self):
        return {'src':self.getSourceChannel(), 'voltage':self.getVoltageLevel(), 'baud':self.getBoud(), 
        'when':self.getWhen(), "dataBits":self.getDataBits(), "stopBit":self.getStopBit(), "parity":self.getParity()}


