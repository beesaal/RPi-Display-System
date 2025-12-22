#ILI9341 TFT display with Raspberry Pi (Python Based)
##Pin Connection
```text
        2.8" TFT Display (ILI9341)
        ┌─────────────────────┐
        │ 1: VCC  ──────► 3.3V (Pin 1)          │
        │ 2: GND  ──────► GND  (Pin 6)          │
        │ 3: CS   ──────► GPIO 8  (Pin 24)      │
        │ 4: RESET─────► GPIO 25 (Pin 22)      │
        │ 5: DC   ──────► GPIO 24 (Pin 18)      │
        │ 6: SDI  ──────► GPIO 10 (Pin 19) MOSI │
        │ 7: SCK  ──────► GPIO 11 (Pin 23) SCLK │
        │ 8: LED  ──────► 3.3V (with 100Ω)      │
        │ 9: SDO  ──────► GPIO 9  (Pin 21) MISO │
        └─────────────────────┘
```



TFT-Display-Hub
A comprehensive Python-based display system for Raspberry Pi with ILI9341 TFT display. Supports multiple media formats, real-time console output, and dual-display capabilities for both debugging and user feedback.
```link
https://img.shields.io/badge/Raspberry-Pi-red?logo=raspberrypi
https://img.shields.io/badge/Python-3.6%252B-blue?logo=python
https://img.shields.io/badge/License-MIT-green
```
🎯 Features
Multi-Format Support: Display GIFs, videos (MP4, AVI), images (JPEG, PNG, BMP), and text files

Real-time Console Output: Use as a debugging display with printf(), display_print(), and dual_print() functions

Dual Output System: Choose between terminal-only, display-only, or both outputs

ILI9341 TFT Support: Optimized for 2.8" ILI9341 SPI displays

Flexible Rotation: Portrait and landscape modes

Easy Integration: Simple API for use in other projects

Error Handling: Graceful fallbacks and clear error messages

🚀 Quick Start
Hardware Requirements
Raspberry Pi (3/4/Zero)

ILI9341 2.8" TFT Display

SPI-enabled connection

Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/tft-display-hub.git
cd tft-display-hub
```
Run installation script:

```bash
sudo chmod +x install_dependencies.sh
sudo ./install_dependencies.sh
```
Reboot your Raspberry Pi:

```bash
sudo reboot
```
Basic Usage
Display a media file:

```bash
sudo python3 run.py assets/gifs/animation.gif
sudo python3 run.py assets/videos/demo.mp4
sudo python3 run.py image.jpg
sudo python3 run.py document.txt
```
Test the display:

```bash
sudo python3 src/find_orientation.py
```
💡 How to Use in Your Projects
Method 1: Direct Integration
Add this to your Python project:

```python
import sys
import os

# Add TFT-Display-Hub to path
tft_path = "/path/to/tft-display-hub/src"
sys.path.insert(0, tft_path)

from display_output import printf, display_print, dual_print

# Use in your code
def my_function():
    printf("Debug info - terminal only")           # Terminal only
    display_print("User message - display only")   # TFT display only  
    dual_print("Important info - both places!")    # Both terminal and display
    
    # Example with sensor data
    temperature = read_temperature()
    display_print(f"Temperature: {temperature}°C")
    printf(f"[SENSOR] Raw temp reading: {temperature}")
```
Method 2: As a Debugging Console
Create a debugging module for your project:

```python
# debug_console.py
import sys
import os
tft_path = "/path/to/tft-display-hub/src"
sys.path.insert(0, tft_path)

from display_output import init_output, printf, display_print, dual_print

class ProjectDebugger:
    def __init__(self):
        self.output = init_output('portrait')
        
    def log_sensor(self, sensor_name, value):
        printf(f"[SENSOR] {sensor_name}: {value}")
        
    def show_status(self, message):
        display_print(f"Status: {message}")
        
    def critical_error(self, error):
        dual_print(f"❌ CRITICAL: {error}")
        
    def progress_update(self, step, total):
        progress = (step / total) * 100
        dual_print(f"Progress: {progress:.1f}% ({step}/{total})")
```
# Global instance
debug = ProjectDebugger()
Method 3: System Monitoring Dashboard
python
# system_monitor.py
```python
import time
import psutil
import subprocess
from display_output import init_output, display_print

class SystemMonitor:
    def __init__(self):
        self.output = init_output('portrait')
        
    def get_cpu_temp(self):
        try:
            output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
            return float(output.split('=')[1].split("'")[0])
        except:
            return 0.0
            
    def update_display(self):
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        cpu_temp = self.get_cpu_temp()
        
        display_print("=== SYSTEM STATUS ===")
        display_print(f"CPU: {cpu_percent:.1f}%")
        display_print(f"Temp: {cpu_temp:.1f}°C")
        display_print(f"RAM: {memory.percent:.1f}%")
        display_print("====================")
        
    def run(self):
        while True:
            self.update_display()
            time.sleep(5)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run()
```
🛠 API Reference
Core Functions
Function	Description	Output
printf(*args)	Print to terminal only	Terminal
display_print(*args)	Print to TFT display only	Display
dual_print(*args)	Print to both terminal and display	Both
Display Control
```python
from display_driver import ILI9341, PORTRAIT, LANDSCAPE

# Initialize display
display = ILI9341(rotation=PORTRAIT)  # or LANDSCAPE

# Display raw image data (RGB565)
display.display_image(image_data)

# Clear screen
display.clear_screen()

# Cleanup
display.cleanup()
```
File Display
```python
from file_dispatcher import FileDispatcher

# Display any supported file
dispatcher = FileDispatcher("path/to/file", width=320, height=240)
if dispatcher.is_supported():
    frame_data, duration = dispatcher.get_next_frame()
    display.display_image(frame_data)
```
📁 Project Structure
```text
tft-display-hub/
├── assets/                 # Sample media files
│   ├── gifs/
│   ├── images/
│   └── videos/
├── config/
│   └── display_config.py   # Display settings
├── src/
│   ├── display_driver.py   # ILI9341 driver
│   ├── display_output.py   # Dual output system
│   ├── file_dispatcher.py  # Multi-format handler
│   ├── gif_handler.py      # GIF processing
│   ├── video_handler.py    # Video processing
│   ├── image_handler.py    # Image processing
│   ├── text_handler.py     # Text display
│   └── main.py            # Main application
├── install_dependencies.sh
├── requirements.txt
└── run.py
```
🎨 Use Cases
1. IoT Project Dashboard
```python
# In your IoT project
from display_output import display_print

def update_dashboard(sensor_data):
    display_print("=== SMART HOME ===")
    display_print(f"Temp: {sensor_data['temperature']}°C")
    display_print(f"Humidity: {sensor_data['humidity']}%")
    display_print(f"Lights: {'ON' if sensor_data['lights'] else 'OFF'}")
```
2. Robotics Status Display
```python
# In robotics project
from display_output import dual_print, display_print

class RobotController:
    def on_movement_start(self):
        dual_print("🤖 Robot moving...")
        
    def on_sensor_reading(self, distance):
        display_print(f"Distance: {distance}cm")
        
    def on_error(self, error):
        dual_print(f"❌ Robot error: {error}")
```
3. Scientific Instrument Readout
```python
# Laboratory equipment
from display_output import printf, display_print

class Instrument:
    def take_measurement(self):
        data = self.capture_data()
        printf(f"[RAW_DATA] {data}")  # For logging
        display_print(f"Result: {data['value']} {data['units']}")
```
🔧 Configuration
Edit config/display_config.py for your setup:

```python
# GPIO Pin configuration (BCM numbering)
DC = 24
RST = 25
CS = 8

# SPI configuration
SPI_PORT = 0
SPI_DEVICE = 0

# Display orientation
PORTRAIT = 0xA8   # 240x320
LANDSCAPE = 0x08  # 320x240
```
🐛 Troubleshooting
Display not working?

Run orientation finder: sudo python3 src/find_orientation.py

Check SPI is enabled: lsmod | grep spi

Verify wiring connections

Import errors?

Ensure you've run the installation script

Check Python path includes the src directory

Performance issues?

Reduce video resolution for smoother playback

Use smaller GIFs or lower frame rates

🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit your changes: git commit -m 'Add amazing feature'

Push to the branch: git push origin feature/amazing-feature

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Raspberry Pi Foundation for hardware support

PIL/Pillow for image processing

OpenCV for video support

SPIDev for SPI communication

⭐ Star this repo if you find it useful!
