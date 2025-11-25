#!/usr/bin/env python3

import time
import sys
import os

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from display_output import init_output, printf, display_print, dual_print

def main():
    # Initialize the dual output system
    output = init_output('portrait')
    
    dual_print("\n DUAL OUTPUT DEMONSTRATION\n")
    dual_print("=" * 40)
    
    # Test different output methods
    printf("\n1. TERMINAL ONLY MESSAGES:")
    printf("   - Debug information")
    printf("   - Technical details")
    printf("   - Log files")
    
    display_print("\n2. DISPLAY ONLY MESSAGES:")
    display_print("   - User instructions")
    display_print("   - Status messages")  
    display_print("   - Progress indicators")
    
    dual_print("\n3. BOTH TERMINAL & DISPLAY:")
    dual_print("   - Important alerts")
    dual_print("   - Program status")
    dual_print("   - Error messages")
    
    # Simulate a process with different types of output
    dual_print("\n🔄 STARTING SIMULATION PROCESS")
    
    printf("\n[DEBUG] Process ID: 12345")
    printf("[DEBUG] Memory allocated: 1024 KB")
    
    display_print("Initializing components...")
    time.sleep(1)
    
    for i in range(5):
        progress = (i + 1) * 20
        dual_print(f"Progress: {progress}% complete")
        
        # Terminal-only detailed info
        printf(f"[DEBUG] Step {i+1}: Processing data chunk {i*100}")
        
        # Display-only status
        if i == 2:
            display_print("✓ Halfway point reached")
        
        time.sleep(1)
    
    display_print("✅ Process completed!")
    printf("[DEBUG] Process finished, cleaning up resources")
    dual_print("🎉 Simulation finished successfully!")
    
    # Show final status
    display_print("\n" + "=" * 30)
    display_print("FINAL STATUS")
    display_print("=" * 30)
    display_print("All systems: OK")
    display_print("Memory: Good")
    display_print("Ready for next task")

if __name__ == "__main__":
    main()