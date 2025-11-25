#!/bin/bash
echo "Installing dependencies for Universal Display on TFT..."

# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-pil python3-numpy

# Install OpenCV for video support
sudo apt install -y python3-opencv

# Install Python libraries
pip3 install RPi.GPIO spidev Pillow numpy opencv-python

# Enable SPI interface
sudo raspi-config nonint do_spi 0

echo "Installation complete! Please reboot your Raspberry Pi."
echo "sudo reboot"