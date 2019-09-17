#!/usr/bin/python3 

from rigol import RigolMSO
        
mso5000 = RigolMSO()
trigger = mso5000.setTrigger("rs232")
trigger.setup(src ="chan1", baud=38400, voltage=2.68, when="data", data=10, stopBit=1, parity="none", dataBits=8)
print(trigger.getCurrentSetup())
