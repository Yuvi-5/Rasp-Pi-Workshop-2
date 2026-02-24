import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.display.jhd1802 import JHD1802

# --- 1. CONFIGURATION (Customize this!) ---
# Which Digital Port is the sensor connected to?
SENSOR_PIN = 5 

# How often should we update the distance? (in seconds)
UPDATE_DELAY = 0.5 

def main():
    # Initialize the LCD and the Sensor
    lcd = JHD1802()
    sensor = GroveUltrasonicRanger(SENSOR_PIN)
    
    print(f"Reading distance from Pin D{SENSOR_PIN}...")

    while True:
        # Step 1: Read the distance (result is in centimeters)
        distance_cm = sensor.get_distance()
        
        # Step 2: Format the text for the LCD
        # We use '{:.1f}' to round the number to 1 decimal place (e.g., 12.5 cm)
        top_line = "Target Found:"
        bottom_line = "{:.1f} cm".format(distance_cm)
        
        # Step 3: Print to Console (for the teacher/student debugging)
        print(f"Distance: {distance_cm} cm")

        # Step 4: Update the LCD
        lcd.home()
        lcd.write(top_line)
        
        lcd.setCursor(1, 0)
        lcd.write(bottom_line)

        # Step 5: Wait before the next measurement
        time.sleep(UPDATE_DELAY)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # This block runs when you press Ctrl+C to stop the code
        lcd = JHD1802()
        lcd.clear()
        print("\nProgram stopped.")