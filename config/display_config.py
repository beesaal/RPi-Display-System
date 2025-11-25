# Display configuration for ILI9341 2.8" TFT

# GPIO Pin configuration (BCM numbering)
DC = 24
RST = 25
CS = 8

# SPI configuration
SPI_PORT = 0
SPI_DEVICE = 0
SPI_SPEED = 32000000

# Display dimensions
WIDTH = 240
HEIGHT = 320

# ILI9341 commands
ILI9341_SOFTRESET = 0x01
ILI9341_SLEEPOUT = 0x11
ILI9341_DISPLAYON = 0x29
ILI9341_COLADDRSET = 0x2A
ILI9341_PAGEADDRSET = 0x2B
ILI9341_MEMORYWRITE = 0x2C
ILI9341_MADCTL = 0x36

# Memory Access Control values
MADCTL_MY = 0x80  # Row Address Order
MADCTL_MX = 0x40  # Column Address Order  
MADCTL_MV = 0x20  # Row/Column Exchange
MADCTL_ML = 0x10  # Vertical Refresh Order
MADCTL_BGR = 0x08 # BGR Order (usually needed)
MADCTL_MH = 0x04  # Horizontal Refresh Order

# ===== ALL POSSIBLE ORIENTATIONS =====
# Try each one until you find the correct one

# Landscape modes (320x240):
LANDSCAPE_NORMAL = MADCTL_BGR                     # 0x08 - Most common
LANDSCAPE_MIRRORED = MADCTL_MX | MADCTL_BGR       # 0x48 - Horizontally mirrored
LANDSCAPE_FLIPPED = MADCTL_MY | MADCTL_BGR        # 0x88 - Vertically flipped
LANDSCAPE_BOTH = MADCTL_MX | MADCTL_MY | MADCTL_BGR # 0xC8 - Both mirrored and flipped

# Portrait modes (240x320):
PORTRAIT_NORMAL = MADCTL_MV | MADCTL_BGR          # 0x28 - Most common
PORTRAIT_MIRRORED = MADCTL_MV | MADCTL_MX | MADCTL_BGR # 0x68 - Horizontally mirrored
PORTRAIT_FLIPPED = MADCTL_MV | MADCTL_MY | MADCTL_BGR # 0xA8 - Vertically flipped  
PORTRAIT_BOTH = MADCTL_MV | MADCTL_MX | MADCTL_MY | MADCTL_BGR # 0xE8 - Both

# Default to most common ones:
LANDSCAPE = PORTRAIT_FLIPPED    # Try this first for landscape
PORTRAIT = PORTRAIT_FLIPPED      # Try this first for portrait

# Font settings
FONT_SIZE = 12
FONT_SCALE = 1
TEXT_COLOR = (255, 255, 255)  # White
BACKGROUND_COLOR = (0, 0, 0)   # Black