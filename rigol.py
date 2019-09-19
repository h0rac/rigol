import vxi11
import json
import sys

from mso.triggers import TriggerFactory
from mso.system import System
from mso.bus import Bus, BusFactory

sweap = None

with open('trigger.json', 'r') as f:
    sweap = json.load(f)

class RigolMSO():        
    def __init__(self, addr):
        self.instr = vxi11.Instrument(addr)
        print(self.instr.ask("*IDN?"))
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
        self.system = None
        self.mainBus = None
        self.bus = None

    def _getTriggerType(self):
        return  self.instr.ask(":TRIGger:MODE?")

    def triggerOn(self, trigger = None):
        if trigger:
            try:
                self.instr.write(":TRIGger:MODE {0}".format(self.triggers[trigger.lower()]))
            except KeyError as err:
                print('Unsupported trigger:', err)
                sys.exit()
        else:
            self.instr.write(":TRIGger:MODE {0}".format(self.triggerType))
        return self._getTriggerType()

    def getTrigger(self):
        return self._getTriggerType()
    
    def getAllTriggers(self):
        return [k for k in self.triggers.keys()]
    
    def setTrigger(self, trigger):
        try:
            self.triggerType = self.triggers[trigger.lower()]
            self.triggerOn(trigger)
            self.trigger = TriggerFactory.factory(trigger.upper(), self.instr )
            return self.trigger
        except KeyError as err:
            print('Unsupported trigger:', err)
            sys.exit()
    
    def sweepTrigger(self, state):
        try:
            self.instr.write(":TRIGger:SWEep {0}".format(sweap['trigger'][state.lower()]))
        except KeyError as err:
            print('Unsupported trigger sweap:', err)
            sys.exit()

    def getSweep(self):
        return self.instr.ask(":TRIGger:SWEep?")
    
    def enableSystem(self):
        self.system = System(self.instr)
        return self.system
    
    def getLastBus(self):
        return self.mainBus
    
    def setBus(self, busNum, busType):
        self.mainBus = Bus(self.instr)
        try:
            self.mainBus.setBus(int(busNum), busType)
            self.bus = BusFactory.factory(busType.upper(), self.instr, busNum)
        except ValueError as err:
             print('Unsupported busNum:', err)
             sys.exit()
        return self.bus

