# /*****************************************************************************
# * | File        :	  SSD1306.py
# * | Author      :   Waveshare team
# * | Function    :   SSD1306
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-11-14
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from smbus import SMBus
import time
import numpy as np

class SSD1306(object):
    def __init__(self, width=128, height=32, addr=0x3c):
        self.width = width
        self.height = height
        self.Column = width
        self.Page = int(height/8)
        self.addr = addr
        self.bus = SMBus(1)

    def SendCommand(self, cmd):# write command
        self.bus.write_byte_data(self.addr, 0x00, cmd)

    def SendData(self, cmd):# write ram
        self.bus.write_byte_data(self.addr, 0x40, cmd)

    def Closebus(self):
        self.bus.close()

    def Init(self):
        self.SendCommand(0xAE)

        self.SendCommand(0x40) # set low column address
        self.SendCommand(0xB0) # set high column address

        self.SendCommand(0xC8) # not offset

        self.SendCommand(0x81)
        self.SendCommand(0xff)

        self.SendCommand(0xa1)

        self.SendCommand(0xa6)

        self.SendCommand(0xa8)
        self.SendCommand(0x1f)

        self.SendCommand(0xd3)
        self.SendCommand(0x00)

        self.SendCommand(0xd5)
        self.SendCommand(0xf0)

        self.SendCommand(0xd9)
        self.SendCommand(0x22)

        self.SendCommand(0xda)
        self.SendCommand(0x02)

        self.SendCommand(0xdb)
        self.SendCommand(0x49)

        self.SendCommand(0x8d)
        self.SendCommand(0x14)

        self.SendCommand(0xaf)

    def ClearBlack(self):
        for i in range(0, self.Page):
            self.SendCommand(0xb0 + i)
            self.SendCommand(0x00)
            self.SendCommand(0x10) 
            for j in range(0, self.Column):
                self.SendData(0x00)

    def ClearWhite(self):
        for i in range(0, self.Page):
            self.SendCommand(0xb0 + i)
            self.SendCommand(0x00)
            self.SendCommand(0x10) 
            for j in range(0, self.Column):
                self.SendData(0xff)

    def getbuffer(self, image):
        buf = [0xff] * (self.Page * self.Column)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if(imwidth == self.width and imheight == self.height):
            # print ("Horizontal screen")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[x + int(y / 8) * self.width] &= ~(1 << (y % 8))
        elif(imwidth == self.height and imheight == self.width):
            # print ("Vertical screen")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[(newx + int(newy / 8 )*self.width) ] &= ~(1 << (y % 8))
        for x in range(self.Page * self.Column):
            buf[x] = ~buf[x]
        return buf
            
    def ShowImage(self, pBuf):
        for i in range(0, self.Page):            
            self.SendCommand(0xB0 + i) # set page address
            self.SendCommand(0x00) # set low column address
            self.SendCommand(0x10) # set high column address
            # write data #
            for j in range(0, self.Column):
                self.SendData(pBuf[j+self.width*i])


    
    
    
    
    
    