from PIL import Image
import numpy as np
import os

class ImageHandler:
    def __init__(self, image_path, display_width=320, display_height=240):
        self.image_path = image_path
        self.display_width = display_width
        self.display_height = display_height
        self.image_data = None
        self.load_image()
    
    def load_image(self):
        """Load and prepare image for display"""
        try:
            image = Image.open(self.image_path)
            print(f"Original image: {image.size}, Mode: {image.mode}")
            print(f"Target display: {self.display_width}x{self.display_height}")
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image_rgb = image.convert('RGB')
            else:
                image_rgb = image.copy()
            
            # Resize to fit display
            resized_image = image_rgb.resize((self.display_width, self.display_height), 
                                           Image.Resampling.LANCZOS)
            
            # Convert to RGB565
            self.image_data = self.rgb_to_rgb565(resized_image)
            
            print("Image processed successfully")
            
        except Exception as e:
            print(f"Error loading image: {e}")
            raise
    
    def rgb_to_rgb565(self, image):
        """Convert PIL Image to RGB565 byte array"""
        rgb_array = np.array(image, dtype=np.uint16)
        
        r = (rgb_array[:,:,0] >> 3) & 0x1F
        g = (rgb_array[:,:,1] >> 2) & 0x3F  
        b = (rgb_array[:,:,2] >> 3) & 0x1F
        
        rgb565 = ((r << 11) | (g << 5) | b)
        rgb565_bytes = rgb565.byteswap().tobytes()
        
        return rgb565_bytes
    
    def get_image_data(self):
        """Get the prepared image data"""
        return self.image_data
    
    def display_duration(self):
        """Return suggested display duration for static images"""
        return 5000  # 5 seconds for static images