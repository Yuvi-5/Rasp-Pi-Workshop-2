import time
from grove.grove_servo import GroveServo

# --- 1. CONFIGURATION ---
# The Servo must be in a PWM capable port (like Port 12)
SERVO_PIN = 12 

def main():
    # Initialize the Servo
    servo = GroveServo(SERVO_PIN)
    
    print("--- Servo Motor Controller ---")
    print(f"Connected on PWM Pin {SERVO_PIN}")
    print("Type an angle (0 to 180) and press Enter.")
    print("Type 'exit' to stop.")

    while True:
        # Step 1: Get input from the user
        user_input = input("\nEnter angle (0-180): ")

        # Check if the user wants to quit
        if user_input.lower() == 'exit':
            break

        # Step 2: Validate the input
        # We use a 'try-except' block to prevent the program from crashing
        # if the user types letters instead of numbers.
        try:
            angle = int(user_input)

            # Step 3: Check if the angle is safe
            if 0 <= angle <= 180:
                print(f"Moving to {angle} degrees...")
                servo.setAngle(angle)
            else:
                print("Error: Please choose a number between 0 and 180.")

        except ValueError:
            print("Error: That's not a valid number!")

    print("Program finished.")

if __name__ == '__main__':
    main()