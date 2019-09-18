class System():
    def __init__(self, instr):
        self.instr = instr

    def getOutput(self):
        return  self.instr.ask(":SYSTem:AOUTput?")
    
    def output(self, value):
        outputs = {"tout":"TOUT", "pfail":"PFAil"}
        try:
            self.instr.write(":SYSTem:AOUTput {0}".format(outputs[value]))
        except KeyError as err:
                print('Unsupported output value:', err)
