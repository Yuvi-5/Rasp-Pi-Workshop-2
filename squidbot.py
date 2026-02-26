import time
import threading
import random
from grove.gpio import GPIO
from grove.grove_servo import GroveServo
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.display.jhd1802 import JHD1802

# ==========================================
#              CONFIGURATION
# ==========================================
# Pins
PIN_ULTRASONIC = 5
PIN_SERVO      = 12
PIN_LED        = 16   # Yellow Wire on LED Button
PIN_BUTTON     = 17   # White Wire on LED Button
PIN_BUZZER     = 18
PIN_PIR        = 22
PIN_LIGHT      = 0    # Analog A0

# Game Settings
WIN_DISTANCE_CM = 10  # If they get this close, they win (optional check)
START_DISTANCE  = 500 # 5 meters
CAUGHT_THRESHOLD = 10  # If distance changes by >5cm during Red Light -> CAUGHT
LIGHT_SAVE_THRESHOLD = 600 # How bright the flashlight needs to be to save them
GAME_TIME_LIMIT = 60 # Players have 60 seconds total to win

# ==========================================
#           HARDWARE CONTROLLER
# ==========================================
class SquidBot:
    def __init__(self):
        # Outputs
        self.lcd = JHD1802()
        self.servo = GroveServo(PIN_SERVO)
        self.led = GPIO(PIN_LED, GPIO.OUT)
        self.buzzer = GPIO(PIN_BUZZER, GPIO.OUT)
        
        # Initial State
        self.face_back()
        self.led_off()
        self.update_lcd("SQUID GAME", "Initializing...")

    def update_lcd(self, line1, line2):
        self.lcd.home()
        self.lcd.write(f"{line1:<16}") # Pad with spaces to clear old text
        self.lcd.setCursor(1, 0)
        self.lcd.write(f"{line2:<16}")

    def face_front(self):
        # Red Light Position (Looking at players)
        self.servo.setAngle(180)

    def face_back(self):
        # Green Light Position (Looking away)
        self.servo.setAngle(0)

    def face_rotate(self):
        # Yellow Light Transition
        self.servo.setAngle(90)

    def beep(self, count=1, duration=0.1):
        for _ in range(count):
            self.buzzer.write(1)
            time.sleep(duration)
            self.buzzer.write(0)
            time.sleep(0.05)
            
    def alarm(self):
        # "Beeps hard when caught"
        for _ in range(5):
            self.buzzer.write(1)
            time.sleep(0.05)
            self.buzzer.write(0)
            time.sleep(0.05)

    def led_on(self):
        self.led.write(1)

    def led_off(self):
        self.led.write(0)

# ==========================================
#           SENSOR FUSION THREAD
# ==========================================
class SensorMonitor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True # Kills thread when main program ends
        self.running = True
        
        # Hardware
        self.ultrasonic = GroveUltrasonicRanger(PIN_ULTRASONIC)
        self.pir = GPIO(PIN_PIR, GPIO.IN)
        self.light_sensor = GroveLightSensor(PIN_LIGHT)
        self.btn = GPIO(PIN_BUTTON, GPIO.IN)

        # Shared Data (The "State")
        self.distance = 0
        self.motion_detected = False
        self.button_pressed = False
        self.current_lux = 0
        
        # Difficulty Scaling
        self.last_stable_distance = 0

    def run(self):
        """Main Loop for the background thread"""
        while self.running:
            # 1. Read Distance
            raw_dist = self.ultrasonic.get_distance()
            if raw_dist < 600: # Filter out garbage values > 6m
                self.distance = raw_dist

            # 2. Read PIR (Motion)
            if self.pir.read() == 1:
                self.motion_detected = True
            else:
                self.motion_detected = False

            # 3. Read Button (Win Condition)
            # Active Low check (0 = Pressed)
            if self.btn.read() == 0:
                self.button_pressed = True
            else:
                self.button_pressed = False
                
            # 4. Read Light (For Second Chance)
            self.current_lux = self.light_sensor.light

            time.sleep(0.05) # fast refresh rate (20Hz)

    def reset_motion_flag(self):
        self.motion_detected = False
        self.last_stable_distance = self.distance

    def check_for_movement(self):
        """Returns True if player moved significantly"""
        # Criteria 1: PIR Sensor triggered
        if self.motion_detected:
            return True
        
        # Criteria 2: Ultrasonic Deviation
        # If distance changed by more than 5cm since Red Light started
        delta = abs(self.distance - self.last_stable_distance)
        if delta > CAUGHT_THRESHOLD:
            return True
            
        return False

# ==========================================
#               GAME LOGIC
# ==========================================
def second_chance_challenge(bot, sensors):
    """The 'Flashlight' Minigame"""
    bot.update_lcd("YOU MOVED!", "FLASH LIGHT NOW!")
    bot.alarm()
    
    # Give them 3 seconds
    timeout = time.time() + 3
    saved = False
    
    while time.time() < timeout:
        lux = sensors.current_lux
        countdown = int(timeout - time.time())
        bot.update_lcd(f"LUX: {lux}", f"TIME: {countdown}s")
        
        if lux > LIGHT_SAVE_THRESHOLD:
            saved = True
            break
        time.sleep(0.1)
        
    if saved:
        bot.beep(2, 0.1) # Happy beep
        bot.update_lcd("SAFE!", "Resuming...")
        time.sleep(1)
        return True # Survived
    else:
        bot.buzzer.write(1) # Long dead tone
        bot.update_lcd("GAME OVER", "ELIMINATED")
        time.sleep(2)
        bot.buzzer.write(0)
        return False # Died

def main():
    bot = SquidBot()
    sensors = SensorMonitor()
    sensors.start() # Start the background thread

    print("--- RED LIGHT GREEN LIGHT: SYSTEM READY ---")
    print("Press the Red Button to start the game.")
    bot.update_lcd("PRESS BUTTON", "TO START")

    # Wait for start
    while not sensors.button_pressed:
        time.sleep(0.1)

    print("GAME STARTED!")
    game_active = True

    # [NEW] Capture the exact moment the game begins
    game_start_time = time.time()

    while game_active:
        # [NEW] Check Global Timer at start of every round
        elapsed = time.time() - game_start_time
        time_left = int(GAME_TIME_LIMIT - elapsed)
        
        if time_left <= 0:
            bot.buzzer.write(1) # Long continuous tone
            bot.update_lcd("TIME UP!", "EVERYONE OUT")
            time.sleep(3)
            bot.buzzer.write(0)
            break # End the game immediately

        # --- PHASE 1: GREEN LIGHT ---
        bot.face_back()
        bot.led_off()
        bot.update_lcd("GREEN LIGHT", f"Dist: {sensors.distance:.0f}cm")
        bot.beep(1, 0.5)
        
        # Random duration for Green Light
        green_duration = random.uniform(3, 6)
        start_green = time.time()
        
        while time.time() - start_green < green_duration:
            # Check Win Condition continuously
            if sensors.button_pressed:
                bot.update_lcd("VICTORY!", "YOU SURVIVED")
                bot.beep(5, 0.1)
                game_active = False
                break
            
            # Update distance on screen
            bot.update_lcd("GREEN LIGHT", f"Dist: {sensors.distance:.0f}cm")
            time.sleep(0.1)

        if not game_active: break

        # --- PHASE 2: YELLOW LIGHT (Calibration) ---
        bot.face_rotate()
        bot.update_lcd("YELLOW LIGHT", "PREPARE...")
        bot.beep(3, 0.1) # Warning beeps
        
        # Dynamic difficulty: Shorter yellow light if they are closer!
        difficulty_factor = max(1.0, sensors.distance / 100) # Closer = smaller factor
        time.sleep(2.0) 

        # --- PHASE 3: RED LIGHT ---
        bot.face_front() # DOLL HEAD TURNS
        bot.led_on()     # RED LED ON
        bot.update_lcd("RED LIGHT", "DONT MOVE")
        bot.buzzer.write(1) # Loud initial tone
        time.sleep(0.5)
        bot.buzzer.write(0)
        
        # Stabilize sensors
        sensors.reset_motion_flag()
        time.sleep(0.5) # Give players a split second to freeze
        
        red_duration = random.uniform(3, 5)
        start_red = time.time()
        
        while time.time() - start_red < red_duration:
            # CRITICAL: Check for movement
            if sensors.check_for_movement():
                print(">>> MOTION DETECTED <<<")
                
                # Trigger Second Chance
                survived = second_chance_challenge(bot, sensors)
                
                if survived:
                    # Reset sensors and continue Red Light
                    sensors.reset_motion_flag()
                    bot.face_front()
                    bot.led_on()
                else:
                    game_active = False # Game Over
                    break
            
            # Check Win Condition (Risky move!)
            if sensors.button_pressed:
                bot.update_lcd("VICTORY!", "RISKY WIN!")
                bot.beep(5, 0.1)
                game_active = False
                break
                
            time.sleep(0.1)

    # End of Game Loop
    bot.face_front()
    bot.led_off()
    print("Game Finished.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nForce Quit")
        # Clean up GPIO (turn off buzzer/led)
        GPIO(PIN_BUZZER, GPIO.OUT).write(0)
        GPIO(PIN_LED, GPIO.OUT).write(0)