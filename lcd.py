import time
# The library for the Grove LCD RGB Backlight (JHD1802)
from grove.display.jhd1802 import JHD1802

# --- 1. CONFIGURATION (Customize this!) ---
# What message do you want to print? (Max 16 characters per line)
TOP_LINE_TEXT    = "Hello, World!"
BOTTOM_LINE_TEXT = "My First Pi Project"

# How long should the text stay on screen? (in seconds)
DISPLAY_TIME = 5

def main():
    # Initialize the LCD device
    # Note: We don't need a pin number because it uses the I2C port
    lcd = JHD1802()
    
    print("LCD Initialized. Writing text...")

    # Step 1: Clear any existing text
    lcd.clear()

    # Step 2: Set cursor to Row 0, Column 0 (Top Left)
    lcd.home()
    lcd.write(TOP_LINE_TEXT)

    # Step 3: Set cursor to Row 1, Column 0 (Bottom Left)
    lcd.setCursor(1, 0)
    lcd.write(BOTTOM_LINE_TEXT)

    # Step 4: Wait for the configured time
    time.sleep(DISPLAY_TIME)

    # Step 5: Clean up by clearing the screen
    lcd.clear()
    print("Program finished.")

if __name__ == '__main__':
    main()