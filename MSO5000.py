#!/usr/bin/python3 

import vxi11
import json
instr = vxi11.Instrument("192.168.1.10")

rs232 = None

with open('rs232.json', 'r') as f:
    rs232 = json.load(f)

class RigolMSO():        
    def __init__(self):
        print(instr.ask("*IDN?"))
        self.triggers = {"edge":"EDGE",
        "pulse": "PULSe",
        "slope":"SLOPe",
        "video": "VIDeo",
        "pattern": "PATTern",
        "duration": "DURation", 
        "timeout": "TIMeout",
        "runt": "RUNT",
        "window": "WINDow",
        "delay":"DELay",
        "setup":"SETup",
        "nedge":"NEDGe", 
        "rs232":"RS232",
        "iic": "IIC",
        "spi":"SPI",
        "can":"CAN",
        "flexray":"FLEXray",
        "lin":"LIN",
        "iis":"IIS",
        "m1553":"M1553"}
        self.triggerType = None

    def _getTriggerType(self):
        return instr.ask(":TRIGger:MODE?")

    def triggerOn(self, trigger = None):
        if trigger:
            try:
                instr.write(":TRIGger:MODE {0}".format(self.triggers[trigger.lower()]))
            except KeyError as err:
                print('Unsupported trigger:', err)
        else:
            instr.write(":TRIGger:MODE {0}".format(self.triggerType))
        return self._getTriggerType()

    def getTrigger(self):
        return self._getTriggerType()
    
    def getAllTriggers(self):
        return [k for k in self.triggers.keys()]
    
    def setTrigger(self, trigger):
        try:
            self.triggerType = self.triggers[trigger.lower()]
            self.triggerOn(trigger)
            self.trigger =  TriggerFactory()
            return self.trigger.create_trigger(trigger)
        except KeyError as err:
            print('Unsupported trigger:', err)
        


class TriggerFactory():
   def create_trigger(self, typ):
      targetclass = typ.upper()
      return globals()[targetclass]()
    
class RS232():

    def getSourceChannel(self):
          return instr.ask(":TRIGger:RS232:SOURce?")

    def getBoud(self):
        return instr.ask(":TRIGger:RS232:BAUD?")
    
    def getVoltageLevel(self):
        return instr.ask(":TRIGger:RS232:LEVel?")

    def getWhen(self):
         return instr.ask(":TRIGger:RS232:WHEN?")
    
    def getData(self):
        return instr.ask(":TRIGger:RS232:DATA?")
    
    def getStopBit(self):
         return instr.ask(":TRIGger:RS232:STOP?")
    
    def getParity(self):
        return instr.ask(":TRIGger:RS232:PARity?")
    
    def getDataBits(self):
        return instr.ask(":TRIGger:RS232:WIDTh?")

    def setBoud(self, boud):
        try:
            instr.write(":TRIGger:RS232:BAUD {0}".format(boud))
        except KeyError as err:
            print('Unsupported boud:', err)
    
    def setVoltageLevel(self, voltage):
        try:
            instr.write(":TRIGger:RS232:LEVel {0}".format(voltage))
        except Error as err:
            print('Unsupported voltage:', err)
    
    def setSourceChannel(self, chan):
        try:
            instr.write(":TRIGger:RS232:SOURce {0}".format(rs232['source'][chan.lower()]))
        except KeyError as err:
            print('Unsupported channel source:', err)
    
        
    def setWhen(self, value):
        try:
            instr.write(":TRIGger:RS232:WHEN {0}".format(rs232['when'][value.lower()]))
        except KeyError as err:
            print('Unsupported when source:', err)
    
    def setData(self, num):
        result = num in rs232['data']
        if result:
            instr.write(":TRIGger:RS232:DATA {0}".format(num))
        else:
            print('Unsupported data, accept value in range 0-255')
            return False
    
    def setStopBit(self, stopBit):
        result = stopBit in rs232['stopBits']
        if result:
            instr.write(":TRIGger:RS232:STOP {0}".format(stopBit))
        else:
            print('Unsupported value, accept 1,1.5,2')
            return False
    
    def setParity(self, parity):
        try:
            instr.write(":TRIGger:RS232:PARity {0}".format(rs232['parity'][parity.lower()]))
        except KeyError as err:
            print('Unsupported parity, accept ODD, EVEN, NONE:', err)
    
    def setDataBits(self, bits):
        result = bits in rs232['dataBits']
        if result:
            instr.write(":TRIGger:RS232:WIDTh {0}".format(bits))
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


mso5000 = RigolMSO()
trigger = mso5000.setTrigger("rs232")
trigger.setup(src ="chan1", baud=38400, voltage=2.68, when="data", data=10, stopBit=1, parity="none", dataBits=8)
