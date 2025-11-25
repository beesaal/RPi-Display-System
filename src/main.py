#!/usr/bin/env python3

import time
import sys
import os
import argparse

# Add the current directory to Python path to allow local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import our dual output system
from display_output import init_output, printf, display_print, dual_print

def main():
    # Initialize dual output system
    output = init_output(rotation='portrait')
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Display files on TFT screen')
    parser.add_argument('file_path', nargs='?', default=None, 
                       help='Path to file to display (GIF, image, video, or text)')
    
    args = parser.parse_args()
    file_path = args.file_path
    
    # Demonstrate the different print functions
    printf("=== TERMINAL ONLY ===")
    printf("This message only appears in terminal")
    printf("")
    
    display_print("=== DISPLAY ONLY ===")
    display_print("This message only appears on TFT display")
    display_print("")
    
    dual_print("=== BOTH TERMINAL & DISPLAY ===")
    dual_print("This message appears in both places!")
    dual_print("")
    
    # File loading logic
    if not file_path:
        # Look for files in assets directory
        assets_dirs = ['assets/images', 'assets/videos', 'assets/gifs']
        for assets_dir in assets_dirs:
            if os.path.exists(assets_dir):
                files = [f for f in os.listdir(assets_dir) if os.path.isfile(os.path.join(assets_dir, f))]
                if files:
                    file_path = os.path.join(assets_dir, files[0])
                    dual_print(f"Using first file found: {file_path}")
                    break
        
        if not file_path:
            dual_print("❌ No file specified and no files found in assets directories.")
            dual_print("💡 Usage: python main.py <file_path>")
            return
    
    if not os.path.exists(file_path):
        dual_print(f"❌ File not found: {file_path}")
        return
    
    try:
        from file_dispatcher import FileDispatcher
        
        dual_print(f"📁 Loading file: {file_path}")
        
        # Get display dimensions
        display_width = output.display.width if output.display else 320
        display_height = output.display.height if output.display else 240
        
        dispatcher = FileDispatcher(file_path, 
                                  display_width=display_width, 
                                  display_height=display_height)
        
        if not dispatcher.is_supported():
            error_msg = f"❌ Unsupported format: {os.path.basename(file_path)}"
            dual_print(error_msg)
            
            # Show error on display
            display_print("=" * 30)
            display_print("UNSUPPORTED FILE")
            display_print("=" * 30)
            display_print(f"File: {os.path.basename(file_path)}")
            display_print("This format cannot be")
            display_print("displayed on this system")
            
            time.sleep(5)
            return
        
        file_type = dispatcher.get_file_type()
        dual_print(f"📄 File type: {file_type}")
        dual_print("🎬 Displaying file... Press Ctrl+C to exit")
        
        # Show loading message on display
        display_print("=" * 30)
        display_print("LOADING FILE")
        display_print("=" * 30)
        display_print(f"Type: {file_type.upper()}")
        display_print(f"File: {os.path.basename(file_path)}")
        display_print("Starting playback...")
        
        time.sleep(2)  # Show loading message for 2 seconds
        
        display_count = 0
        start_time = time.time()
        
        while True:
            frame_start = time.time()
            
            frame_data, duration = dispatcher.get_next_frame()
            
            if frame_data and output.display:
                output.display.display_image(frame_data)
                display_count += 1
                
                # Calculate sleep time
                sleep_time = max(duration / 1000.0 - (time.time() - frame_start), 0.01)
                
                # Show progress in terminal only
                if display_count % 20 == 0:
                    current_time = time.time()
                    fps = display_count / (current_time - start_time)
                    printf(f"[TERMINAL] Frame {display_count} - FPS: {fps:.1f}")
                
                time.sleep(sleep_time)
            else:
                # No more data (for static images or end of text)
                if file_type == 'image':
                    dual_print("✅ Image display completed")
                    time.sleep(5)
                    break
                else:
                    time.sleep(0.1)
            
    except KeyboardInterrupt:
        dual_print("\n🛑 Exiting...")
    except Exception as e:
        dual_print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'dispatcher' in locals():
            dispatcher.cleanup()
        if output:
            output.cleanup()
        dual_print("✅ Cleanup complete")

if __name__ == "__main__":
    main()