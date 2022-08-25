import logging
import sys
import time
import math
import smbus
import RPi.GPIO as GPIO

import os
import socket
import fcntl
import struct
from PIL import Image,ImageDraw,ImageFont
from . import SSD1306


show = SSD1306.SSD1306()
show.Init();
dir_path = os.path.dirname(os.path.abspath(__file__))


font = ImageFont.truetype(dir_path+'/Courier_New.ttf',13)

image1 = Image.new('1', (show.width, show.height), "WHITE")
draw = ImageDraw.Draw(image1)
class POE_HAT_B:
    def __init__(self,address = 0x20):
        self.i2c = smbus.SMBus(1)
        self.address = address#0x20
        self.FAN_ON()
        self.FAN_MODE = 0;
    def FAN_ON(self):
        self.i2c.write_byte(self.address, 0xFE & self.i2c.read_byte(self.address))
        
    def FAN_OFF(self):
        self.i2c.write_byte(self.address, 0x01 | self.i2c.read_byte(self.address))
        
    def GET_IP(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
        s.close()
        return ip
        
    def GET_Temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = (int)(f.read() ) / 1000.0
        return temp
    
    def POE_HAT_Display(self, FAN_TEMP):
        # show.Init()
        # show.ClearBlack()
        
        image1 = Image.new('1', (show.width, show.height), "WHITE")
        draw = ImageDraw.Draw(image1)  
        ip = self.GET_IP()
        temp = self.GET_Temp()
        draw.text((0,1), 'IP:'+str(ip), font = font, fill = 0)
        draw.text((0,15), 'Temp:'+ str(((int)(temp*10))/10.0), font = font, fill = 0)
        if(temp>=FAN_TEMP):
            self.FAN_MODE = 1
            
        elif(temp<FAN_TEMP-2):
            self.FAN_MODE = 0
        
        if(self.FAN_MODE == 1):
            draw.text((77,16), 'FAN:ON', font = ImageFont.truetype(dir_path+'/Courier_New.ttf',12), fill = 0)
            self.FAN_ON()
        else:
            draw.text((77,16), 'FAN:OFF', font = ImageFont.truetype(dir_path+'/Courier_New.ttf',12), fill = 0)
            self.FAN_OFF()
        show.ShowImage(show.getbuffer(image1))







