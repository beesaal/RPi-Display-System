import os
import sys
import numpy as np

# Add the current directory to Python path to allow local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class FileDispatcher:
    def __init__(self, file_path, display_width=320, display_height=240):
        self.file_path = file_path
        self.display_width = display_width
        self.display_height = display_height
        self.handler = None
        self.file_type = self.detect_file_type()
        self.setup_handler()
    
    def detect_file_type(self):
        """Detect file type based on extension"""
        ext = os.path.splitext(self.file_path)[1].lower()
        
        # Image formats
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
        # Video formats  
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        # GIF format
        gif_extensions = ['.gif']
        # Text formats
        text_extensions = ['.txt', '.log', '.md', '.py', '.cpp', '.c', '.h', '.html', '.css', '.js']
        
        if ext in gif_extensions:
            return 'gif'
        elif ext in image_extensions:
            return 'image'
        elif ext in video_extensions:
            return 'video'
        elif ext in text_extensions:
            return 'text'
        else:
            return 'unsupported'
    
    def setup_handler(self):
        """Setup appropriate handler based on file type"""
        try:
            if self.file_type == 'gif':
                from gif_handler import GIFHandler
                self.handler = GIFHandler(self.file_path, self.display_width, self.display_height)
                print("GIF handler initialized")
            
            elif self.file_type == 'image':
                from image_handler import ImageHandler
                self.handler = ImageHandler(self.file_path, self.display_width, self.display_height)
                print("Image handler initialized")
            
            elif self.file_type == 'video':
                from video_handler import VideoHandler
                self.handler = VideoHandler(self.file_path, self.display_width, self.display_height)
                print("Video handler initialized")
            
            elif self.file_type == 'text':
                from text_handler import TextHandler
                self.handler = TextHandler(self.file_path, self.display_width, self.display_height)
                print("Text handler initialized")
            
            else:
                print(f"Unsupported file format: {self.file_path}")
                self.handler = None
                
        except Exception as e:
            print(f"Error setting up handler: {e}")
            import traceback
            traceback.print_exc()
            self.handler = None
    
    def get_next_frame(self):
        """Get next frame/data based on file type"""
        if not self.handler:
            return None, 1000
        
        try:
            if self.file_type in ['gif', 'video']:
                return self.handler.get_next_frame()
            elif self.file_type == 'image':
                # For static images, return the image once
                if hasattr(self, 'image_displayed'):
                    return None, 1000
                self.image_displayed = True
                return self.handler.get_image_data(), self.handler.display_duration()
            elif self.file_type == 'text':
                return self.handler.get_next_page()
                
        except Exception as e:
            print(f"Error getting next frame: {e}")
            return None, 1000
    
    def is_supported(self):
        """Check if file format is supported"""
        return self.handler is not None
    
    def get_file_type(self):
        """Get detected file type"""
        return self.file_type
    
    def cleanup(self):
        """Cleanup resources"""
        if self.handler and hasattr(self.handler, 'cleanup'):
            self.handler.cleanup()