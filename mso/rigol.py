import vxi11
import json
import sys
import os

from mso.triggers import TriggerFactory
from mso.system import System
from mso.bus import Bus, BusFactory

main = None

with open('{}/rigol/json/main/main.json'.format(os.path.dirname(os.getcwd())), 'r') as f:
    main = json.load(f)

class RigolMSO():
    """Class represents main rigol device

        Args:
            addr (str): IP address of rigol device
        Returns:
            object: rigol object
    """       
    def __init__(self, addr="192.168.1.10"):
        self.instr = vxi11.Instrument(addr)
        print(self.instr.ask("*IDN?"))
        self.triggerType = None
        self.system = None
        self.mainBus = None
        self.bus = None

    def getTriggerType(self):
        """Returns:
            str: selected trigger type
        """
        return  self.instr.ask(":TRIGger:MODE?")

    def _triggerOn(self, trigger="rs232"):
        """Set trigger type
        Args:
            trigger (str): pulse|slope|video|pattern|duration|timeout|runt|window|delay|setup
            |nedge|rs232|iic|spi|can|flexray|lin|iis|m1553
        Returns:
            str: trigger type after set
        """
        if trigger:
            try:
                self.instr.write(":TRIGger:MODE {0}".format(main['triggers'][trigger.lower()]))
            except KeyError as err:
                print('Unsupported trigger:', err)
                sys.exit()
        else:
            self.instr.write(":TRIGger:MODE {0}".format(self.triggerType))
        return self.getTriggerType()

    
    def getAllTriggers(self):
        """Returns:
            dict: all possible triggers
        """
        return main['triggers']
    
    def setTriggerType(self, trigger):
        """Set trigger type
        Args:
            trigger (str): pulse|slope|video|pattern|duration|timeout|runt|window|delay|setup
            |nedge|rs232|iic|spi|can|flexray|lin|iis|m1553
        Returns:
            str: trigger type after set
        """
        try:
            self.triggerType = main['triggers'][trigger.lower()]
            self._triggerOn(trigger)
            self.trigger = TriggerFactory.factory(trigger.upper(), self.instr )
            return self.trigger
        except KeyError as err:
            print('Unsupported trigger:', err)
            sys.exit()
    
    def sweepTrigger(self, mode="auto"):
        """Set trigger mode
        Args:
            mode (str): auto|single|normal
        """
        try:
            self.instr.write(":TRIGger:SWEep {0}".format(main['trigger'][mode.lower()]))
        except KeyError as err:
            print('Unsupported trigger sweep:', err)
            sys.exit()

    def getSweep(self):
        """Returns:
            str: trigger mode auto|single|normal
        """
        return self.instr.ask(":TRIGger:SWEep?")
    
    def getSystem(self):
        """Returns:
            obj: return system object
        """
        self.system = System(self.instr)
        return self.system
    
    def getLastBus(self):
        """Returns:
            str: decoder bus object
        """
        return self.mainBus
    
    def setBus(self, busNum, busType):
        """Set bus decoder line
        Args:
            busNum (int): line 1|2|3|4
            busType (str): parallel|rs232|spi|iic|iis|lin|can|flexray|m1553
        Returns:
            obj: bus subclass object
        """
        self.mainBus = Bus(self.instr)
        try:
            self.mainBus.setBus(int(busNum), busType)
            self.bus = BusFactory.factory(busType.upper(), self.instr, busNum)
        except ValueError as err:
             print('Unsupported busNum:', err)
             sys.exit()
        return self.bus

