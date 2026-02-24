import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor

# --- 1. CONFIGURATION ---
# The Light Sensor must be in an Analog Port (A0)
LIGHT_SENSOR_PIN = 0 

# Threshold to decide if it is "Dark" or "Bright"
# Students can adjust this number based on the room lighting!
DARK_THRESHOLD = 300

def main():
    # Initialize the Light Sensor
    sensor = GroveLightSensor(LIGHT_SENSOR_PIN)
    
    print(f"Reading Light Sensor on Pin A{LIGHT_SENSOR_PIN}...")
    print("Cover the sensor to see the value drop!")

    while True:
        # Step 1: Read the light level
        # The value is usually between 0 (pitch black) and roughly 1023 (very bright)
        light_value = sensor.light
        
        # Step 2: Determine status based on the Threshold
        if light_value < DARK_THRESHOLD:
            status = "Dark - Night Mode"
        else:
            status = "Bright - Day Mode"

        # Step 3: Display the data
        # We use \r and end='' to overwrite the same line in the terminal
        # This keeps the output clean instead of scrolling endlessly
        print(f"Light Level: {light_value} | Status: {status}   ", end='\r')

        # Short pause to prevent the CPU from working too hard
        time.sleep(0.2)

if __name__ == '__main__':
    main()