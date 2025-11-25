#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now run the main function directly
if __name__ == "__main__":
    # Import and run main directly
    from src.main import main
    main()