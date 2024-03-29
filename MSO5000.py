#!/usr/bin/python3 

from mso.rigol import RigolMSO
        
mso5000 = RigolMSO(addr="192.168.1.10")
trigger = mso5000.setTriggerType("rs232")
trigger.setup(src ="chan1", baud=38400, voltage="2.68", when="data", data=10, stopBit=1, parity="none", dataBits=8)
print(trigger.getCurrentSetup())
mso5000.sweepTrigger("normal")
mso5000.getSystem().output("tout")
rs232Decoder = mso5000.setBus(1, "rs232")
decoder = mso5000.getLastBus()
decoder.setup(toggle=True, toggleLabel=True, format="ascii", position=0, threshold="2.68", ttype="tx")
decoder.toggleEventTable(toggle=False, format="ascii", view="packets")
print(decoder.getCurrentSetup())
rs232Decoder.setup(rxSrc="off", txSrc="chan1", baud=38400)
print(rs232Decoder.getCurrentSetup())