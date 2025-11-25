import cv2
import numpy as np
import time
import os

class VideoHandler:
    def __init__(self, video_path, display_width=320, display_height=240):
        self.video_path = video_path
        self.display_width = display_width
        self.display_height = display_height
        self.cap = None
        self.fps = 0
        self.frame_count = 0
        self.load_video()
    
    def load_video(self):
        """Load video file"""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise Exception(f"Cannot open video file: {self.video_path}")
            
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            print(f"Video loaded: {self.video_path}")
            print(f"Original resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
            print(f"FPS: {self.fps}, Frames: {self.frame_count}")
            print(f"Target display: {self.display_width}x{self.display_height}")
            
        except Exception as e:
            print(f"Error loading video: {e}")
            raise
    
    def get_next_frame(self):
        """Get next frame as RGB565 data"""
        if not self.cap or not self.cap.isOpened():
            return None, 100
        
        ret, frame = self.cap.read()
        if not ret:
            # Restart video when finished
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                return None, 100
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize to display dimensions
        resized_frame = cv2.resize(frame_rgb, (self.display_width, self.display_height))
        
        # Convert to RGB565
        rgb565_data = self.rgb_to_rgb565(resized_frame)
        
        # Calculate frame duration based on video FPS
        duration = int(1000 / self.fps) if self.fps > 0 else 100
        
        return rgb565_data, duration
    
    def rgb_to_rgb565(self, image):
        """Convert RGB image to RGB565 byte array"""
        r = (image[:,:,0] >> 3) & 0x1F
        g = (image[:,:,1] >> 2) & 0x3F
        b = (image[:,:,2] >> 3) & 0x1F
        
        rgb565 = ((r << 11) | (g << 5) | b).astype(np.uint16)
        rgb565_bytes = rgb565.byteswap().tobytes()
        
        return rgb565_bytes
    
    def cleanup(self):
        """Release video resources"""
        if self.cap:
            self.cap.release()