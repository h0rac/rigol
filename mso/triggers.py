import json 
import os
import sys

with open("{}/rigol/json/trigger/rs232.json".format(os.path.dirname(os.getcwd())), 'r') as f:
    rs232 = json.load(f)

class TriggerFactory(object):
    """Produces trigger objects"""

    def factory(type, instr):
        """Produce object base on trigger type

        Args:
            type (str): Type of trigger
            instr (obj): vx11 instance

        Returns:
            object: Trigger object base on type
        """
        if type == "RS232":
            return RS232(instr)

    factory = staticmethod(factory)

class RS232(TriggerFactory):
    """RS232 Trigger class"""

    def __init__(self, instr):
        """
            Args:
                instr (obj): vx11 instance
            
            Returns:
            object: RS232 trigger object   
        """
        TriggerFactory.__init__(self)
        self.instr = instr

    def getSourceChannel(self):
        """Returns:
            str: source trigger channel
        """
        return  self.instr.ask(":TRIGger:RS232:SOURce?")

    def getBoud(self):
        """Returns:
            str: boud rate
        """
        return  self.instr.ask(":TRIGger:RS232:BAUD?")
    
    def getVoltageLevel(self):
        """Returns:
            str: voltage level
        """
        return  self.instr.ask(":TRIGger:RS232:LEVel?")

    def getWhen(self):
        """Returns:
            str: when trigger will happen
        """
        return self.instr.ask(":TRIGger:RS232:WHEN?")
    
    def getData(self):
        """Returns:
            str: if when is set to 'DATA' return trigger data in decimal 0-255
        """
        return  self.instr.ask(":TRIGger:RS232:DATA?")
    
    def getStopBit(self):
        """Returns:
            str: stop bit for rs232 with values 1|1,5|2
        """
        return self.instr.ask(":TRIGger:RS232:STOP?")
    
    def getParity(self):
        """Returns:
            str: parity for rs232 with values None|Odd|Even
        """
        return  self.instr.ask(":TRIGger:RS232:PARity?")
    
    def getDataBits(self):
        """Returns:
            str: data bits for rs232 with values 5|7|6|8
        """
        return  self.instr.ask(":TRIGger:RS232:WIDTh?")

    def setBoud(self, boud=9600):
        """Set boud lever for trigger

        Args:
            boud (str): baud rate for rs232
            If the baud rate is set to a value with "M", 
            then "A" should be added at the end of the value. For example, if you send 5 M, you need to send 5 MA
        """
        try:
            self.instr.write(":TRIGger:RS232:BAUD {0}".format(boud))
        except ValueError as err:
            print('Unsupported boud:', err)
    
    def setVoltageLevel(self, voltage=0.0):
        """Set voltage lever for trigger

        Args:
            voltage (str): support extension with mV|uV|nV|kV|V
        """
        try:
            self.instr.write(":TRIGger:RS232:LEVel {0}".format(voltage))
        except ValueError as err:
            print('Unsupported voltage:', err)
            sys.exit()
    
    def setSourceChannel(self, chan="chan1"):
        """Set channel source for trigger

        Args:
            chan (str): source channel for trigger
            provide as chan1, chan2... it will be convered to CHANnel1, CHANnel2 etc 
            
            available channels:
            D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D1 0|D11|D12|D13|D14|D15|CHANnel1|CHANnel2|CHANnel3|CHANnel4
        """
        try:
            self.instr.write(":TRIGger:RS232:SOURce {0}".format(rs232['source'][chan.lower()]))
        except KeyError as err:
            print('Unsupported channel source:', err)
            sys.exit()
        
    def setWhen(self, value="data"):
        """Set when trigger fire

        Args:
            when (str): start|error|cerror|data
        """
        try:
            self.instr.write(":TRIGger:RS232:WHEN {0}".format(rs232['when'][value.lower()]))
        except KeyError as err:
            print('Unsupported when source:', err)
    
    def setData(self, num=10):
        """Set on which ASCII char trigger when "data" is set as when

        Args:
            num (int): decimal 0-255
        """
        result = num in rs232['data']
        if result:
            self.instr.write(":TRIGger:RS232:DATA {0}".format(num))
        else:
            print('Unsupported data, accept value in range 0-255')
    
    def setStopBit(self, stopBit=1):
        """Set stop bit for rs232

        Args:
            stopBit (int): accepts 1|1.5|2
        """
        result = stopBit in rs232['stopBits']
        if result:
            self.instr.write(":TRIGger:RS232:STOP {0}".format(stopBit))
        else:
            print('Unsupported value, accept 1,1.5,2')
    
    def setParity(self, parity="none"):
        """Set stop bit for rs232

        Args:
            parity (str): accepts none|even|odd
        """
        try:
            self.instr.write(":TRIGger:RS232:PARity {0}".format(rs232['parity'][parity.lower()]))
        except KeyError as err:
            print('Unsupported parity, accept ODD, EVEN, NONE:', err)
    
    def setDataBits(self, bits=8):
        """Set stop bit for rs232

        Args:
            bits (int): accepts 5|6|7|8
        """
        result = bits in rs232['dataBits']
        if result:
            self.instr.write(":TRIGger:RS232:WIDTh {0}".format(bits))
        else:
            print('Unsupported value, accept 5,6,7 or 8')
         
    
    def setup(self, src = "chan1", voltage = 0.0, baud=9600, when="data",data=10, dataBits=8, stopBit=1, parity="none"):
        """Set rs232 parameters in one function

        Args:
            src (str): source channel
            voltage (str): source voltage
            boud (str): boud rate
            when (str): when to trigger
            data (str): if when is data set ASCII dec value to trigger
            dataBits (int): data bits
            stopBit (int): stop bit
            parity (str): parity for rs232
        """
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
        """Restore rs232 trigger options to default
            
        Returns:
            dict: with default key,pair values
        """
        self.setup()
        return {'src':self.getSourceChannel(), 'voltage':self.getVoltageLevel(), 'baud':self.getBoud(), "when":self.getWhen(),
        'data':self.getData(), "stopBit":self.getStopBit()
         }

    def getDefaults(self):
        """Returns:
            dict: with availble default key,pair values
        """
        return {'src':'chan1', 'voltage':0, 'baud':9600, 'when':"data","data":10, "dataBits":8, "stopBit":1, "parity":'none'}
    
    def getCurrentSetup(self):
        """Returns:
            dict: current configuration
        """
        return {'src':self.getSourceChannel(), 'voltage':self.getVoltageLevel(), 'baud':self.getBoud(), 
        'when':self.getWhen(), 'data':self.getData(), "dataBits":self.getDataBits(), "stopBit":self.getStopBit(), "parity":self.getParity()}


