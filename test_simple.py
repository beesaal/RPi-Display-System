#!/usr/bin/env python3

import os
import sys

print("Testing basic display functionality...")

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
config_dir = os.path.join(current_dir, 'config')

sys.path.insert(0, src_dir)
sys.path.insert(0, config_dir)

try:
    # Test display_driver import
    from display_driver import ILI9341, PORTRAIT
    print("✓ display_driver imports work")
    
    # Test creating display instance
    display = ILI9341(rotation=PORTRAIT)
    print("✓ Display initialized successfully")
    
    # Test clearing screen
    display.clear_screen()
    print("✓ Screen cleared")
    
    # Cleanup
    display.cleanup()
    print("✓ Cleanup successful")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()