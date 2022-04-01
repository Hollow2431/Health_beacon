import board
import busio as io
import adafruit_mlx90614
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from smbus2 import SMBus
from mlx90614 import MLX90614
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep

'''
import socket
import sys

HOST, PORT = "192.168.0.35", 9999
'''

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx =adafruit_mlx90614.MLX90614(i2c)
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)



# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
bus = SMBus(1)
time.sleep(1)

a1=5
listAmbTemp = []
listbt= []
while 1:
    for x in range (a1):
        


        
        sensor = MLX90614(bus, address=0x5A)

        celcius = sensor.get_object_1();
        faren = (celcius*1.8)+32
        print("Body Temperature : ",(round(celcius,2)))

        ambient = sensor.get_ambient()
        limited_ambient = round(ambient, 2)
        print ("Ambient Temperature :", limited_ambient,u"\N{DEGREE SIGN}C")

        
        '''ambiantTemp ="{:.2f}".format(mlx.ambient_temperature)
        targetTemp ="{:.2f}".format(mlx.object_temperature)
        #print(type(ambiantTemp))
        print("ambiant temperature:", ambiantTemp ,"\N{DEGREE SIGN}C")
        print("body temperature:", targetTemp ,"\N{DEGREE SIGN}C")'''


        listAmbTemp.append(float(ambient))
        listbt.append(float(celcius))
        #averageAmbiantTemp = (val1+val2)
        
        sleep(2)
    averageAmbiantTemp = round((listAmbTemp[0]+listAmbTemp[1]+listAmbTemp[2]+listAmbTemp[3]+listAmbTemp[4])/5,1)
    averageBodyTemp = round((listbt[0]+listbt[1]+listbt[2]+listbt[3]+listbt[4])/5,1)
    print(listbt)
    print("average ambient temperature",averageAmbiantTemp)
    print("average Body temperature",averageBodyTemp)
    print ("20 sec timer")
    
    padding = -2
    shape_width = 20
    top = padding
    bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
    x = padding

# Load default font.
    font = ImageFont.load_default()
    draw.text((x, top),       " Ambient Temp:" + str(averageAmbiantTemp),  font=font, fill=255)
    draw.text((x, top+8),     " Body Temp:" + str(averageBodyTemp ), font=font, fill=255)
    draw.text((x, top+16),    " Oxygen %",  font=font, fill=255)
    draw.text((x, top+25),    " BPM:",  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    
    listbt.clear()
    listAmbTemp.clear()
    
    """
    data = '1-100-100-' + str(averageBodyTemp) + '-100'
    # data --> <id>-<bp>-<pulse>-<temp>-<rp>
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    # received = str(sock.recv(1024), "utf-8")

    print("Sent: {}".format(data))
    """
    sleep(5)
    #print(listAmbTemp[0])





# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:


