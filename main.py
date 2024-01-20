# main.py -- put your code here!
import betterESPNOW
from neo_pix_matrix_openBit import *
import time

led_matrix_MAIN = led_matrix_MAIN()
espNow = betterESPNOW.ESPN()

def testUnit():
  led_matrix_MAIN.led_matrix_fill(led_matrix_MAIN.hex_color("000000"))
  led_matrix_MAIN.led_matrix_active()
  time.sleep(2)
  led_matrix_MAIN.led_matrix_fill(led_matrix_MAIN.hex_color("1F1F1F"))
  led_matrix_MAIN.led_matrix_active()
  
  
  
  espNow.addPeer('10:97:BD:25:35:80')
  time.sleep(1)
  if espNow.isReadyToRead():
    print(espNow.readAsText())
    print(espNow.getSenderMAC())
    
  
  


def main():
  testUnit()
  






if __name__ == "main":
  main()