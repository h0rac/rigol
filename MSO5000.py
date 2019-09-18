#!/usr/bin/python3 

from rigol import RigolMSO
        
mso5000 = RigolMSO("192.168.1.10")
trigger = mso5000.setTrigger("rs232")
trigger.setup(src ="chan1", baud=38400, voltage=2.68, when="data", data=10, stopBit=1, parity="none", dataBits=8)
print(trigger.getCurrentSetup())
mso5000.sweapTrigger("auto")
mso5000.enableSystem().output("tout")
rs232Decoder = mso5000.setBus(2, "rs232")
mso5000.getLastBus().toggle(False)
spiDecoder = mso5000.setBus(3, "spi")
mso5000.getLastBus().toggle(False)