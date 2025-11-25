#!/usr/bin/env python3

import sys
import os
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class DualOutput:
    def __init__(self, rotation='portrait', max_lines=15):
        self.display = None
        self.console_active = False
        self.max_lines = max_lines
        self.lines = []
        self.current_line = ""
        
        # Initialize display
        self.init_display(rotation)
    
    def init_display(self, rotation):
        """Initialize the TFT display"""
        try:
            from display_driver import ILI9341, PORTRAIT, LANDSCAPE
            
            rotation_val = PORTRAIT if rotation == 'portrait' else LANDSCAPE
            self.display = ILI9341(rotation=rotation_val)
            self.console_active = True
            
            # Load font
            try:
                self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
            except:
                try:
                    self.font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 12)
                except:
                    self.font = ImageFont.load_default()
            
            # Calculate character dimensions
            try:
                bbox = self.font.getbbox("A")
                self.char_width = bbox[2] - bbox[0]
                self.line_height = bbox[3] - bbox[1] + 2
            except:
                self.char_width = 8
                self.line_height = 15
            
            print("✅ TFT Display console initialized")
            
        except Exception as e:
            print(f"❌ TFT Display initialization failed: {e}")
            print("💡 Continuing with terminal output only")
            self.console_active = False
    
    def printf(self, *args, **kwargs):
        """Print to terminal only (like regular print)"""
        print(*args, **kwargs)
    
    def display_print(self, *args, **kwargs):
        """Print to TFT display only"""
        if not self.console_active:
            print("⚠️  Display not available - printing to terminal instead")
            print(*args, **kwargs)
            return
        
        text = ' '.join(str(arg) for arg in args)
        self._add_to_display(text)
    
    def dual_print(self, *args, **kwargs):
        """Print to both terminal and TFT display"""
        # Print to terminal
        print(*args, **kwargs)
        
        # Print to display
        if self.console_active:
            text = ' '.join(str(arg) for arg in args)
            self._add_to_display(text)
    
    def _add_to_display(self, text):
        """Add text to display buffer"""
        for char in text:
            if char == '\n':
                self._flush_display_line()
            else:
                self.current_line += char
        
        self._update_display()
    
    def _flush_display_line(self):
        """Add current line to display buffer"""
        if self.current_line:
            self.lines.append(self.current_line)
            self.current_line = ""
            
            # Keep only last max_lines
            if len(self.lines) > self.max_lines:
                self.lines = self.lines[-self.max_lines:]
    
    def _update_display(self):
        """Update the physical display"""
        if not self.console_active:
            return
            
        try:
            # Create image
            image = Image.new('RGB', (self.display.width, self.display.height), color=(0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw all lines
            y_pos = 5
            for line in self.lines:
                try:
                    draw.text((5, y_pos), line, fill=(255, 255, 255), font=self.font)
                except:
                    draw.text((5, y_pos), line, fill=(255, 255, 255))
                y_pos += self.line_height
            
            # Draw current line (if any)
            if self.current_line:
                try:
                    draw.text((5, y_pos), self.current_line, fill=(255, 255, 255), font=self.font)
                except:
                    draw.text((5, y_pos), self.current_line, fill=(255, 255, 255))
            
            # Convert to RGB565 and display
            rgb565_data = self._image_to_rgb565(image)
            self.display.display_image(rgb565_data)
            
        except Exception as e:
            print(f"❌ Display update error: {e}")
    
    def _image_to_rgb565(self, image):
        """Convert PIL Image to RGB565 byte array"""
        rgb_array = np.array(image, dtype=np.uint16)
        
        r = (rgb_array[:,:,0] >> 3) & 0x1F
        g = (rgb_array[:,:,1] >> 2) & 0x3F  
        b = (rgb_array[:,:,2] >> 3) & 0x1F
        
        rgb565 = ((r << 11) | (g << 5) | b)
        rgb565_bytes = rgb565.byteswap().tobytes()
        
        return rgb565_bytes
    
    def clear_display(self):
        """Clear the TFT display"""
        if self.console_active:
            self.lines = []
            self.current_line = ""
            self._update_display()
    
    def cleanup(self):
        """Clean up resources"""
        if self.display:
            self.display.cleanup()

# Global instance
output = None

def init_output(rotation='portrait'):
    """Initialize the dual output system"""
    global output
    if output is None:
        output = DualOutput(rotation)
    return output

# Convenience functions
def printf(*args, **kwargs):
    """Print to terminal only"""
    if output is None:
        init_output()
    output.printf(*args, **kwargs)

def display_print(*args, **kwargs):
    """Print to TFT display only"""
    if output is None:
        init_output()
    output.display_print(*args, **kwargs)

def dual_print(*args, **kwargs):
    """Print to both terminal and TFT display"""
    if output is None:
        init_output()
    output.dual_print(*args, **kwargs)