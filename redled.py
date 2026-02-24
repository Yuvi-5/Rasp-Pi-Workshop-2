import time
from grove.gpio import GPIO

# --- CONFIGURATION FOR PORT D16 ---
# On the Grove LED Button connected to D16:
# Pin 16 (Yellow Wire) = The LED Light
# Pin 17 (White Wire)  = The Button Switch
LED_PIN    = 16
BUTTON_PIN = 17

def main():
    # 1. Setup the LED (Output)
    led = GPIO(LED_PIN, GPIO.OUT)
    
    # 2. Setup the Button (Input)
    btn = GPIO(BUTTON_PIN, GPIO.IN)
    
    print(f"Debug Mode: Reading Button on {BUTTON_PIN}, LED on {LED_PIN}")
    print("Press the button to see the value change...")

    while True:
        # Read the button state (0 or 1)
        button_state = btn.read()
        
        # DEBUG: Print the state so you can see if the button is working
        # If this number doesn't change when you press, check the connection!
        print(f"Button Value: {button_state}", end='\r')

        # LOGIC FIX: 
        # This button is "Active Low" (0 means Pressed, 1 means Released)
        if button_state == 0:
            # Button is pressed -> Turn LED ON
            led.write(1)
        else:
            # Button is released -> Turn LED OFF
            led.write(0)

        time.sleep(0.05)

if __name__ == '__main__':
    main()