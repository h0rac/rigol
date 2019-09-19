import os
import json

with open("{}/rigol/json/system/system.json".format(os.path.dirname(os.getcwd())), 'r') as f:
    system = json.load(f)

class System():
    """Class represents system config on device
        Args:
            instr (obj): vx11 instance object
        Returns:
            object: system object
    """       
    def __init__(self, instr):
        self.instr = instr

    def getOutput(self):
        """Returns:
            str: trigger ouput value -> output|pfail
        """       
        return  self.instr.ask(":SYSTem:AOUTput?")
    
    def output(self, value):
        """
        Args:
            value (str): set trigger out port to output|pfail
        """
        try:
            self.instr.write(":SYSTem:AOUTput {0}".format(system['output'][value.lower()]))
        except KeyError as err:
            print('Unsupported output value:', err)
