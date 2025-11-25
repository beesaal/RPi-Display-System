import spidev
import RPi.GPIO as GPIO
import time
import os
import sys

# Add config directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
config_path = os.path.join(parent_dir, 'config')
sys.path.insert(0, config_path)

from display_config import *

class ILI9341:
    def __init__(self, rotation=PORTRAIT):
        self.rotation = rotation
        self.update_dimensions()
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DC, GPIO.OUT)
        GPIO.setup(RST, GPIO.OUT)
        GPIO.setup(CS, GPIO.OUT)
        
        # Set CS high initially
        GPIO.output(CS, GPIO.HIGH)
        
        # Initialize SPI with optimized settings
        self.spi = spidev.SpiDev()
        try:
            self.spi.open(SPI_PORT, SPI_DEVICE)
            self.spi.max_speed_hz = 32000000
            self.spi.mode = 0b00
            self.spi.lsbfirst = False
        except Exception as e:
            print(f"SPI initialization failed: {e}")
            raise
        
        self.init_display()
    
    def update_dimensions(self):
        """Update width and height based on rotation"""
        if self.rotation == PORTRAIT or self.rotation == PORTRAIT_FLIPPED:
            self.width = 320
            self.height = 240
        else:
            self.width = 240
            self.height = 320
        print(f"Display dimensions: {self.width}x{self.height}")
    
    def write_command(self, cmd):
        GPIO.output(DC, GPIO.LOW)
        GPIO.output(CS, GPIO.LOW)
        self.spi.writebytes([cmd])
        GPIO.output(CS, GPIO.HIGH)
    
    def write_data(self, data):
        GPIO.output(DC, GPIO.HIGH)
        GPIO.output(CS, GPIO.LOW)
        if isinstance(data, list):
            self.spi.writebytes(data)
        else:
            self.spi.writebytes([data])
        GPIO.output(CS, GPIO.HIGH)
    
    def reset(self):
        GPIO.output(RST, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(RST, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(RST, GPIO.HIGH)
        time.sleep(0.15)
    
    def set_rotation(self, rotation):
        """Set display rotation"""
        self.rotation = rotation
        self.update_dimensions()
        self.write_command(ILI9341_MADCTL)
        self.write_data([rotation])
        print(f"Rotation set: {self.width}x{self.height}")
    
    def init_display(self):
        print("Initializing ILI9341 display...")
        self.reset()
        
        # Optimized initialization sequence
        commands = [
            (0xEF, [0x03, 0x80, 0x02]),
            (0xCF, [0x00, 0xC1, 0x30]),
            (0xED, [0x64, 0x03, 0x12, 0x81]),
            (0xE8, [0x85, 0x00, 0x78]),
            (0xCB, [0x39, 0x2C, 0x00, 0x34, 0x02]),
            (0xF7, [0x20]),
            (0xEA, [0x00, 0x00]),
            (0xC0, [0x1B]),
            (0xC1, [0x01]),
            (0xC5, [0x30, 0x30]),
            (0xC7, [0xB7]),
            (0x36, [self.rotation]),
            (0x3A, [0x55]),
            (0xB1, [0x00, 0x1A]),
            (0xB6, [0x0A, 0xA2]),
            (0xF6, [0x01, 0x30]),
            (0xF2, [0x00]),
            (0x26, [0x01]),
            (0xE0, [0x0F, 0x2A, 0x28, 0x08, 0x0E, 0x08, 0x54, 0xA9, 0x43, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00]),
            (0xE1, [0x00, 0x15, 0x17, 0x07, 0x11, 0x06, 0x2B, 0x56, 0x3C, 0x05, 0x10, 0x0F, 0x3F, 0x3F, 0x0F]),
            (0x11, None),
        ]
        
        for cmd, data in commands:
            self.write_command(cmd)
            if data is not None:
                self.write_data(data)
        
        time.sleep(0.12)
        self.write_command(0x29)
        time.sleep(0.05)
        
        print(f"Display initialized: {self.width}x{self.height}")
    
    def set_window(self, x0, y0, x1, y1):
        """Set the address window for drawing"""
        self.write_command(ILI9341_COLADDRSET)
        self.write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])
        self.write_command(ILI9341_PAGEADDRSET)
        self.write_data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])
        self.write_command(ILI9341_MEMORYWRITE)
    
    def display_image(self, image_data):
        """Display RGB565 image data - FIXED chunk size"""
        if image_data is None:
            return
            
        # Set address window to full screen
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Send image data with smaller chunks to avoid overflow
        GPIO.output(DC, GPIO.HIGH)
        GPIO.output(CS, GPIO.LOW)
        
        # Use smaller chunk size to avoid SPI buffer overflow
        chunk_size = 1024  # Reduced from 8192 to avoid "Argument list size exceeds 4096 bytes"
        data_length = len(image_data)
        
        for i in range(0, data_length, chunk_size):
            end = min(i + chunk_size, data_length)
            # Convert slice to list for SPI transfer
            chunk = list(image_data[i:end])
            self.spi.writebytes(chunk)
        
        GPIO.output(CS, GPIO.HIGH)
    
    def fill_screen(self, color_high, color_low):
        """Fill entire screen with a solid color - OPTIMIZED"""
        # Create color data more efficiently
        pixel_data = [color_high, color_low]
        color_data = bytearray(pixel_data * (self.width * self.height))
        self.display_image(color_data)
    
    def clear_screen(self):
        """Clear screen to black"""
        self.fill_screen(0x00, 0x00)
    
    def cleanup(self):
        try:
            self.spi.close()
        except:
            pass
        GPIO.cleanup()