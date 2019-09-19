from abc import ABC, abstractmethod
import os
import json
import sys

with open("{}/rigol/json/decoder/bus.json".format(os.path.dirname(os.getcwd())), 'r') as f:
    bus = json.load(f)

class BusFactory(object):
    """Class create decoder objects base on type
    """

    def factory(type, instr, busNum):
        """Args:
            instr (obj): vx11 instance
            busNum (int): decoder bus number
        Returns:
            object: decoder object base on type
        """
        if type == "RS232":
            return RS232(instr, busNum)
    factory = staticmethod(factory)

class Bus():
    """Decoder bus class

        Args:
            instr (obj): vx11 instance

        Returns:
            object: main decoder object
    """
    def __init__(self, instr):
        self.instr = instr
        self.busNum = None
        self.ttype = "tx"
    
    def getMode(self):
        """Returns:
            str: selcted decoder bus mode
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:MODE?".format(self.busNum))
    
    def getBusStatus(self):
        """Returns:
            str: 0|1 indicate ON/OFF for decoder bus
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:DISPlay?".format(self.busNum))
    
    def getBusDataFormat(self):
        """Returns:
            str: data display format for bus
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:FORMat?".format(self.busNum))
    
    def getBusLabelStatus(self):
        """Returns:
            str: 0|1 indicate ON/OFF for decoder bus label
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:LABel?".format(self.busNum))
    
    def getEventTableStatus(self):
        """Returns:
            str: 0|1 indicate ON/OFF for decoder event table
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt?".format(self.busNum))
    
    def getEventTableFormat(self):
        """Returns:
            str: format for event table data
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt:FORMat?".format(self.busNum))
    
    def getEventTableView(self):
        """Returns:
            str: event table view
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt:VIEW?".format(self.busNum))
    
    def getPosition(self):
        """Returns:
            str: current position of decoder bus on screen
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:POSition?".format(self.busNum))
     
    def getThreshold(self, ttype="tx"):
        """
        Args:
            ttype (str): line for which threshold should be enabled
        Returns:
            str: threshold value
        """
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:THReshold? {1}".format(self.busNum, ttype))
    
    def _setBus(self, busNum=1, busType="rs232"):
        """Get bus number and type and set decoder bus
        Args:
            busNum (int): bus number 1|2|3|4
            busType (str): parallel|rs232|spi|iic|iis|lib|can|flexray|m1553
        """
        if busNum > 0 and busNum <= 4:
            self.busNum = busNum
            self.instr.write(":BUS{0}:MODE {1}".format(str(busNum), bus['mode'][busType.lower()]))
        else:
            print("Device support only 4 buses")
            sys.exit()
    
    def _toggle(self, toggle=False):
        """Enable bus decoder base on status
        Args:
            toggle (bool): True|False
        """
        if toggle:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay ON".format(self.busNum))
        elif not toggle:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay OFF".format(self.busNum))
        else:
            print("Expect 'True' or 'False' to toggle bus'")
    
    def _toggleLabel(self, toggle=False):
        """Enable bus decoder label base on toggle 
        Args:
            toggle (bool): True|False
        """
        if toggle == True:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:LABel ON".format(self.busNum))
        elif toggle == False:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:LABel OFF".format(self.busNum))
        else:
            print("Expect 'True' or 'False to toggle bus label'")
    
    def _setDataformat(self, format):
        """Enable bus decoder data format
        Args:
            format (str): ascii|hex|dec|bin
        """
        try:
            self.instr.write(":BUS{0}:FORMat {1}".format(self.busNum, bus['format'][format.lower()]))
        except KeyError as err:
            print("Unsupported data format: ", err)
    
    def _setPosition(self, pos):
        """Set bus decoder position
        Args:
            pos (int): pos >= -167 and pos <=217
        """
        if self.busNum > 0 and self.busNum <= 4:
            if pos >=-167 and pos <=217:
                 self.instr.write(":BUS{0}:POSition {1}".format(self.busNum, pos))
            else:
                print("Expect pos between -167 and 217")
        else:
            print("Device support only 4 buses")
    
    def _setThreshold(self, threshold, ttype):
        """Set bus decoder threshold value to proper line type
        Args:
            threshold (str): value that represents voltage level, accept extension kV|uV|mV|V
            ttype (str): pal|tx|rx|scl|sda|cs|clk|miso|mosi|lin|can|cansub1
        """
        if self.busNum > 0 and self.busNum <= 4:
            self.ttype = ttype
            self.instr.write(":BUS{0}:THReshold {1},{2}".format(self.busNum, threshold, bus['threshold'][ttype.lower()]))
        else:
            print("Device support only 4 buses")
    
    def setup(self, toggle=False, toggleLabel=False, format="ascii", position=0, threshold=0.0, ttype="tx"):
        """Set bus decoder in single function
        Args:
            toggle (bool): enable bus decoder -> True|False
            toggleLabel (bool): enable bus decoder label display -> True|False
            format (str): defines format data to display -> ascii|hex|dec|bin
            position (str): defines position of decoder line on screen -> pos >= -167 and pos <=217
            threshold (str): value that represents voltage level, accept extension kV|uV|mV|V
            ttype (str): type of line -> pal|tx|rx|scl|sda|cs|clk|miso|mosi|lin|can|cansub1
        """
        self._toggle(toggle)
        self._toggleLabel(toggleLabel)
        self._setDataformat(format)
        self._setPosition(position)
        self._setThreshold(threshold, ttype)
    
    def getCurrentSetup(self):
        """Returns:
            dict: dictionary of bus decoder setup represented by key,value pair
        """
        return {"mode":self.getMode(), "display":self.getBusStatus(), "format":self.getBusDataFormat(), 
        "toggleLabel":self.getBusLabelStatus(),
        "position":self.getPosition(),
        "eventTable":{
            "event":self.getEventTableStatus(),
            "format":self.getEventTableFormat(),
            "view":self.getEventTableView()
            },
        "threshold":self.getThreshold()
        }
    
    def toggleEventTable(self, toggle=False, format="ascii", view="packets"):
        """Set bus decoder event table
        Args:
            toggle (bool): enable or disable event table on screen
            format (str): data format to display for event table
            view (str): default view for event table
        """
        if self.busNum > 0 and self.busNum <= 4:
            if toggle == True:
                self.instr.write(":BUS{0}:EVENt ON".format(self.busNum))
                try:
                    self.instr.write(":BUS{0}:EVENt:FORMat {1}".format(self.busNum, bus['event']['format'][format]))
                    self.instr.write(":BUS{0}:EVENt:VIEW {1}".format(self.busNum, bus['event']['view'][view]))
                except KeyError as err:
                    print("Unsupported key: ", err)
            elif toggle == False:
                self.instr.write(":BUS{0}:EVENt OFF".format(self.busNum))
            else:
                print("Unsupported toggle value, expect True or False")


class RS232(Bus):
    """Class represents rs232 decoder

        Args:
            instr (obj): vx11 instance
            busNum (int): decoder bus number
        Returns:
            object: rs232 decoder object
    """
    def __init__(self, instr, busNum):
        self.instr = instr
        self.busNum = busNum
    
    def _setRXSource(self, src):
        pass
    
    def _setBoud(self):
        print("Boud set", self.busNum)