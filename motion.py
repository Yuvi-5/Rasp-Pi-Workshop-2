import time
from grove.gpio import GPIO

# --- 1. CONFIGURATION ---
# Connect the Mini PIR Motion Sensor to Port D22
PIR_PIN = 22

def main():
    # Initialize the Sensor as an INPUT
    # (The Pi 'reads' data coming FROM the sensor)
    motion_sensor = GPIO(PIR_PIN, GPIO.IN)
    
    print(f"Security System Active on Pin D{PIR_PIN}...")
    print("Wave your hand in front of the sensor.")

    while True:
        # Step 1: Read the sensor state
        # 1 = Motion Detected
        # 0 = No Motion
        motion_state = motion_sensor.read()

        if motion_state == 1:
            print(">>> MOTION DETECTED! <<<")
            
            # Customization:
            # We sleep for 2 seconds here because PIR sensors usually
            # stay 'High' for a few seconds after triggering.
            # This prevents the screen from scrolling too fast.
            time.sleep(2) 
            
            print("System resetting...")
        
        else:
            # Print a dot to show the system is alive and scanning
            print(".", end='', flush=True)
            time.sleep(0.5)

if __name__ == '__main__':
    main()