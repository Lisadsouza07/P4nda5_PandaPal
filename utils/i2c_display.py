# I2C OLED Display Driver Wrapper

from config import I2C_SDA_PIN, I2C_SCL_PIN, I2C_FREQ, DISPLAY_I2C_ADDR
from machine import I2C, Pin
import drivers.ssd1306 as ssd1306

class Display:
    def __init__(self):
        """Initialize SSD1306 display over I2C"""
        i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
        self.display = ssd1306.SSD1306_I2C(128, 64, i2c, DISPLAY_I2C_ADDR)
    
    def fill(self, color):
        """Fill entire display with color"""
        self.display.fill(color)
    
    def pixel(self, x, y, color):
        """Set individual pixel"""
        self.display.pixel(x, y, color)
    
    def text(self, text, x, y, color):
        """Draw text"""
        self.display.text(text, x, y, color)
    
    def show(self):
        """Update display"""
        self.display.show()
    
    def clear(self):
        """Clear display"""
        self.display.fill(0)
        self.display.show()
