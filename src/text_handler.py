from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

class TextHandler:
    def __init__(self, text_path, display_width=320, display_height=240):
        self.text_path = text_path
        self.display_width = display_width
        self.display_height = display_height
        self.lines = []
        self.current_page = 0
        self.lines_per_page = 0
        self.load_text()
    
    def load_text(self):
        """Load and prepare text for display"""
        try:
            with open(self.text_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            # Split into lines that fit the display
            self.lines = self.wrap_text(content, self.display_width - 20)  # 20px margin
            self.lines_per_page = self.display_height // 15  # Approximate lines per page
            
            print(f"Text loaded: {len(self.lines)} lines, {self.lines_per_page} lines per page")
            
        except Exception as e:
            print(f"Error loading text file: {e}")
            raise
    
    def wrap_text(self, text, max_width):
        """Wrap text to fit display width"""
        # Simple character-based wrapping (font width approximation)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Approximate line length (rough estimation)
            test_line = ' '.join(current_line + [word])
            if len(test_line) * 8 <= max_width:  # Rough char width estimation
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def get_next_page(self):
        """Get next page of text as image data"""
        if not self.lines:
            return None, 5000  # 5 seconds per page
        
        start_idx = self.current_page * self.lines_per_page
        end_idx = start_idx + self.lines_per_page
        
        if start_idx >= len(self.lines):
            self.current_page = 0  # Loop back to beginning
            start_idx = 0
            end_idx = self.lines_per_page
        
        page_lines = self.lines[start_idx:end_idx]
        
        # Create image with text
        image = Image.new('RGB', (self.display_width, self.display_height), color='black')
        draw = ImageDraw.Draw(image)
        
        # Try to use default font, fallback to basic font
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw lines
        y_position = 10
        for line in page_lines:
            draw.text((10, y_position), line, fill='white', font=font)
            y_position += 15  # Line height
        
        # Add page indicator
        total_pages = (len(self.lines) + self.lines_per_page - 1) // self.lines_per_page
        page_info = f"Page {self.current_page + 1}/{total_pages}"
        draw.text((10, self.display_height - 20), page_info, fill='gray', font=font)
        
        # Convert to RGB565
        rgb565_data = self.rgb_to_rgb565(image)
        
        # Move to next page
        self.current_page += 1
        
        return rgb565_data, 5000  # 5 seconds per page
    
    def rgb_to_rgb565(self, image):
        """Convert PIL Image to RGB565 byte array"""
        rgb_array = np.array(image, dtype=np.uint16)
        
        r = (rgb_array[:,:,0] >> 3) & 0x1F
        g = (rgb_array[:,:,1] >> 2) & 0x3F  
        b = (rgb_array[:,:,2] >> 3) & 0x1F
        
        rgb565 = ((r << 11) | (g << 5) | b)
        rgb565_bytes = rgb565.byteswap().tobytes()
        
        return rgb565_bytes