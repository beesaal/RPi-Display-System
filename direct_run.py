#!/usr/bin/env python3

import os
import sys

# Add all necessary paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
config_dir = os.path.join(current_dir, 'config')

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, config_dir)

# Now import and run
try:
    from src.display_driver import ILI9341, PORTRAIT, LANDSCAPE
    from src.file_dispatcher import FileDispatcher
    from src.main import main
    
    # Pass command line arguments to main
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import approach...")
    
    # Alternative approach - run directly from src
    os.chdir('src')
    sys.path.insert(0, '.')
    
    from display_driver import ILI9341, PORTRAIT, LANDSCAPE
    from file_dispatcher import FileDispatcher
    from main import main
    
    if __name__ == "__main__":
        main()