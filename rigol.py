import vxi11
import json

from mso.triggers import TriggerFactory

rs232 = None

with open('rs232.json', 'r') as f:
    rs232 = json.load(f)

class RigolMSO():        
    def __init__(self):
        self.instr = vxi11.Instrument("192.168.1.10")
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

    def _getTriggerType(self):
        return  self.instr.ask(":TRIGger:MODE?")

    def triggerOn(self, trigger = None):
        if trigger:
            try:
                self.instr.write(":TRIGger:MODE {0}".format(self.triggers[trigger.lower()]))
            except KeyError as err:
                print('Unsupported trigger:', err)
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