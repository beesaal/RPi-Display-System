from PIL import Image, ImageSequence
import numpy as np
import os
import sys

# Add this to the top of your file
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

class GIFHandler:
    def __init__(self, gif_path, display_width=320, display_height=240):
        self.gif_path = gif_path
        self.display_width = display_width
        self.display_height = display_height
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.load_gif()
    
    def load_gif(self):
        """Load GIF and convert frames to RGB565 format"""
        dual_print(f"Loading GIF from {self.gif_path}")
        try:
            gif = Image.open(self.gif_path)
            print(f"Original GIF: {gif.size}, {gif.n_frames} frames")
            print(f"Target display: {self.display_width}x{self.display_height}")
            
            # ===== ANTI-BLINKING SETTINGS =====
            MIN_FRAME_DURATION = 50  # Minimum frame duration in ms (increase if blinking)
            MAX_FRAME_DURATION = 200 # Maximum frame duration in ms
            # ==================================
            
            frame_count = 0
            for frame in ImageSequence.Iterator(gif):
                # Convert to RGB if necessary
                if frame.mode != 'RGB':
                    frame_rgb = frame.convert('RGB')
                else:
                    frame_rgb = frame.copy()
                
                # Resize to fit display - SIMPLE STRETCH
                resized_frame = frame_rgb.resize((self.display_width, self.display_height), 
                                               Image.Resampling.LANCZOS)
                
                # Convert to RGB565
                rgb565_data = self.rgb_to_rgb565(resized_frame)
                self.frames.append(rgb565_data)
                
                # Get and adjust duration to prevent blinking
                duration = frame.info.get('duration', 100)
                
                # Apply minimum and maximum duration limits
                if duration < MIN_FRAME_DURATION:
                    duration = MIN_FRAME_DURATION
                elif duration > MAX_FRAME_DURATION:
                    duration = MAX_FRAME_DURATION
                    
                self.durations.append(duration)
                frame_count += 1
                
                # Progress indicator for large GIFs
                if frame_count % 10 == 0:
                    print(f"Processed frame {frame_count}/{gif.n_frames}")
            
            print(f"Processed {len(self.frames)} frames")
            print(f"Frame duration range: {min(self.durations)}-{max(self.durations)}ms")
            
        except Exception as e:
            print(f"Error loading GIF: {e}")
            raise
    
    def rgb_to_rgb565(self, image):
        """Convert PIL Image to RGB565 byte array - OPTIMIZED"""
        rgb_array = np.array(image, dtype=np.uint16)
        
        r = (rgb_array[:,:,0] >> 3) & 0x1F
        g = (rgb_array[:,:,1] >> 2) & 0x3F  
        b = (rgb_array[:,:,2] >> 3) & 0x1F
        
        rgb565 = ((r << 11) | (g << 5) | b)
        rgb565_bytes = rgb565.byteswap().tobytes()
        
        return rgb565_bytes
    
    def get_next_frame(self):
        """Get next frame and its duration"""
        if not self.frames:
            return None, 100
            
        frame_data = self.frames[self.current_frame]
        duration = self.durations[self.current_frame]
        
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        return frame_data, duration
    
    def get_frame_count(self):
        return len(self.frames)
    
    def reset(self):
        """Reset to first frame"""
        self.current_frame = 0