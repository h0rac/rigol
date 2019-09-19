from abc import ABC, abstractmethod
import os
import json
import sys

with open("{}/rigol/bus.json".format(os.path.dirname(os.getcwd())), 'r') as f:
    bus = json.load(f)

class BusFactory(object):

    def factory(type, instr, busNum):
        if type == "RS232":
            return RS232Bus(instr, busNum)

    factory = staticmethod(factory)

class Bus():
    def __init__(self, instr):
        self.instr = instr
        self.busNum = None
    
    def getMode(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:MODE?".format(self.busNum))
    
    def getBusStatus(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:DISPlay?".format(self.busNum))
    
    def getBusDataFormat(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:FORMat?".format(self.busNum))
    
    def getBusLabelStatus(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:LABel?".format(self.busNum))
    
    def getEventTableStatus(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt?".format(self.busNum))
    
    def getEventTableFormat(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt:FORMat?".format(self.busNum))
    
    def getEventTableView(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:EVENt:VIEW?".format(self.busNum))
    
    def getPosition(self):
        if not self.busNum:
            print("First bus type and number need to be set")
            sys.exit(0)
        return self.instr.ask(":BUS{0}:POSition?".format(self.busNum))

    
    def setBus(self, busNum, busType):
        if busNum > 0 and busNum <= 4:
            self.busNum = busNum
            self.instr.write(":BUS{0}:MODE {1}".format(str(busNum), bus['mode'][busType.lower()]))
        else:
            print("Device support only 4 buses")
            sys.exit()
    
    def toggle(self, status=False):
        if status:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay ON".format(self.busNum))
        elif not status:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:DISPlay OFF".format(self.busNum))
        else:
            print("Expect 'True' or 'False' to toggle bus'")
    
    def toggleLabel(self, toggle=False):
        if toggle == True:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:LABel ON".format(self.busNum))
        elif toggle == False:
            if self.busNum > 0 and self.busNum <= 4:
                self.instr.write(":BUS{0}:LABel OFF".format(self.busNum))
        else:
            print("Expect 'True' or 'False to toggle bus label'")
    
    def setDataformat(self, format):
        try:
            self.instr.write(":BUS{0}:FORMat {1}".format(self.busNum, bus['format'][format.lower()]))
        except KeyError as err:
            print("Unsupported data format: ", err)
    
    def setPosition(self, pos):
        if self.busNum > 0 and self.busNum <= 4:
            if pos >=-167 and pos <=217:
                 self.instr.write(":BUS{0}:POSition {1}".format(self.busNum, pos))
            else:
                print("Expect pos between -167 and 217")
        else:
            print("Device support only 4 buses")
    
    def setup(self, toggle=False, labelStatus=False, format="ascii", position=0):
        self.toggle(toggle)
        self.toggleLabel(labelStatus)
        self.setDataformat(format)
        self.setPosition(position)
    
    def getCurrentSetup(self):
        return {"mode":self.getMode(), "display":self.getBusStatus(), "format":self.getBusDataFormat(), 
        "labelStatus":self.getBusLabelStatus(),
        "position":self.getPosition(),
        "eventTable":{
            "event":self.getEventTableStatus(),
            "format":self.getEventTableFormat(),
            "view":self.getEventTableView()
            }
        }
    
    def toggleEventTable(self, toggle=False, format="ascii", view="packets"):
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


class RS232Bus(Bus):
    def __init__(self, instr, busNum):
        self.instr = instr
        self.busNum = busNum
    
    def setBoud(self):
        print("Boud set", self.busNum)