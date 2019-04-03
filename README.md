# Current status

Basic output for adruino is set and we are recieving data from kRPC.  

* Add TFT support and 16x2 lcd as well and 7219 module.
* Add inputs from arduino to KSP.

Might need to rope in the UNO centrally controlled by the PI.
That would essentially give a lot of FPS for us to stuff.

So PI to process and Arduinos to read and display.

Use get_and_send_data.py to add stuff and CmdMessenger/test2/test1 for arduino

SPI pin names can be confusing. These are the alternative names for the SPI pins:

* MOSI = DIN = R/W = SDO = DI = SI = MTSR = SDA = D1  
* CS = CE = RS = SS  
* DC = A0 = SDI = DO = DOUT = SO = MRST = MISO ( = RS??)
* RESET = RST  
* SCLK = CLK = E = SCK = SCL = D0  
