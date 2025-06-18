echo Esse programa é py

import sys
from time import sleep

LED_PATH16 = "/sys/class/gpio/gpio16/"
SYSFS_DIR = "/sys/class/gpio/"
LED_NUMBER16 = "16"

LED_PATH20 = "/sys/class/gpio/gpio20/"
LED_NUMBER20 = "20"

LED_PATH21 = "/sys/class/gpio/gpio21/"
LED_NUMBER21 = "21"

def writeLED ( filename, value, path ):
	"Esta funcao escreve o valor 'value' no arquivo 'path+filename'"
	fo = open( path + filename,"w")
	fo.write(value)
	fo.close()
	return



writeLED (filename="value", value="1")
sleep(1)

writeLED (filename="value", value="0")
sleep(1)

writeLED (filename="export", value=LED_NUMBER16, path=SYSFS_DIR)
sleep(1)
writeLED (filename="direction", value="out")

writeLED (filename="unexport", value=LED_NUMBER16, path=SYSFS_DIR)
