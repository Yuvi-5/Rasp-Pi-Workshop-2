import time
from grove.gpio import GPIO

# --- 1. CONFIGURATION ---
# Connect the Buzzer to Digital Port D18
BUZZER_PIN = 18

def main():
    # Initialize the Buzzer as an Output
    buzzer = GPIO(BUZZER_PIN, GPIO.OUT)
    
    print(f"Buzzer ready on Pin D{BUZZER_PIN}")

    # --- Helper Function to make a Beep ---
    def beep(duration):
        buzzer.write(1) # Sound ON
        time.sleep(duration)
        buzzer.write(0) # Sound OFF
        time.sleep(0.1) # Small gap between beeps

    # --- PART A: Simple Alarm ---
    print("Testing Alarm Pattern...")
    for i in range(3):
        beep(0.5) # Long beep (0.5 seconds)
    
    time.sleep(1) # Wait a second

    # --- PART B: The 'SOS' Pattern ---
    # SOS is: 3 Short, 3 Long, 3 Short
    print("Sending SOS Signal...")
    
    # 3 Short
    for i in range(3):
        beep(0.1) 
        
    # 3 Long
    for i in range(3):
        beep(0.5)
        
    # 3 Short
    for i in range(3):
        beep(0.1)

    print("Program finished.")

if __name__ == '__main__':
    main()