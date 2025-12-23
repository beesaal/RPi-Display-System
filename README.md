# Raspberry Pi TFT Display GIF Player

TFT-Display-Hub
A comprehensive Python-based display system for Raspberry Pi with ILI9341 TFT display. Supports multiple media formats, real-time console output, and dual-display capabilities for both debugging and user feedback.

![Untitled video - Made with Clipchamp](https://github.com/user-attachments/assets/4e4a4b7e-21e8-4eae-abe9-faa9669a6c5d)


## 🎯 Features

- Display GIF animations on ILI9341 2.8" TFT display
- Support for multiple display orientations (Portrait/Landscape)
- Adjustable image positioning and scaling
- Optimized SPI communication for smooth playback
- Easy configuration through simple Python files

## 🚀 Hardware Requirements

- Raspberry Pi (3/4/Zero) with GPIO pins
- 2.8" ILI9341 TFT Display with SPI interface
- Jumper wires for connections
- 100Ω resistor for backlight (optional but recommended)

## Wiring Diagram
TFT Display (ILI9341) → Raspberry Pi GPIO
```text

        ┌─────────────────────┐
        │ 1: VCC  ──────► 3.3V (Pin 1)          │
        │ 2: GND  ──────► GND  (Pin 6)          │
        │ 3: CS   ──────► GPIO 8  (Pin 24)      │
        │ 4: RESET─────► GPIO 25 (Pin 22)       │
        │ 5: DC   ──────► GPIO 24 (Pin 18)      │
        │ 6: SDI  ──────► GPIO 10 (Pin 19) MOSI │
        │ 7: SCK  ──────► GPIO 11 (Pin 23) SCLK │
        │ 8: LED  ──────► 3.3V (with 100Ω)      │
        │ 9: SDO  ──────► GPIO 9  (Pin 21) MISO │
        └─────────────────────┘

```

## Software Installation

1. **Update system and install dependencies:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pil python3-numpy
```
Install Python libraries:
```bash
pip3 install RPi.GPIO spidev Pillow numpy
Enable SPI interface:
```
```bash
sudo raspi-config nonint do_spi 0
sudo reboot
```
Quick Start
Clone or copy the project files:

```bash
git clone https://github.com/beesaal/RPi-Display-System.git
```
Place your GIF file:
```bash
cd RPi-Display-System/assests/gifs/...
```
cp your_gif.gif to RPi-Display-System/assests/gifs/your_gif.gif

Run the application:
Inside RPi-Display-System/... folder run:
```bash
sudo python3 run.py
or
sudo python3 run.py assests/gifs/your_gif.gif

sudo python3 run.py assets/gifs/animation.gif
sudo python3 run.py assets/videos/demo.mp4
sudo python3 run.py image.jpg
sudo python3 run.py document.txt
```
Configuration
Display Orientation
Test the display:

```bash
sudo python3 src/find_orientation.py
```
Edit config/display_config.py to set the correct orientation:

python
# For Portrait mode (240x320)
display_orientation = PORTRAIT  # 0x48

# For Landscape mode (320x240)
display_orientation = LANDSCAPE  # 0x28
Image Positioning
Adjust src/gif_handler.py for perfect positioning:

python
# Manual position adjustments
MANUAL_X_ADJUST = 0    # Positive = move right, Negative = move left
MANUAL_Y_ADJUST = 0    # Positive = move down, Negative = move up

# GIF size on screen
GIF_WIDTH = 240
GIF_HEIGHT = 320

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

🎨 Debugging text-print Use Cases
1. IoT Project Dashboard
```python
# In your IoT project
from display_output import display_print
eg.
def update_dashboard(sensor_data):
    display_print("=== SMART HOME ===")
    display_print(f"Temp: {sensor_data['temperature']}°C")
    display_print(f"Humidity: {sensor_data['humidity']}%")
    display_print(f"Lights: {'ON' if sensor_data['lights'] else 'OFF'}")
```
2. Robotics Status Display
```python
# In robotics project
eg.
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
eg.
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



License
MIT License - See LICENSE file for details.

Acknowledgments
Raspberry Pi Foundation for hardware

PIL/Pillow for image processing

SPIdev for SPI communication
