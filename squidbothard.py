import time
import threading
import random
from grove.gpio import GPIO
from grove.grove_servo import GroveServo
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.display.jhd1802 import JHD1802

# ==========================================
#        HARD MODE CONFIGURATION
# ==========================================
# Pins
PIN_ULTRASONIC = 5
PIN_SERVO      = 12
PIN_LED        = 16   # Yellow Wire
PIN_BUTTON     = 17   # White Wire
PIN_BUZZER     = 18
PIN_PIR        = 22
PIN_LIGHT      = 0    # Analog A0

# Difficulty Settings
GAME_TIME_LIMIT  = 45   # Only 45 seconds to win
MAX_LIVES        = 1    # Only 1 Second Chance allowed
CAUGHT_THRESHOLD = 15    # Sensitivity (cm)
LIGHT_SAVE_LUX   = 600  # Flashlight brightness needed
MAX_DISTANCE     = 500  # Used for calculating difficulty (5 meters)

# ==========================================
#           HARDWARE CONTROLLER
# ==========================================
class SquidBot:
    def __init__(self):
        self.lcd = JHD1802()
        self.servo = GroveServo(PIN_SERVO)
        self.led = GPIO(PIN_LED, GPIO.OUT)
        self.buzzer = GPIO(PIN_BUZZER, GPIO.OUT)
        self.face_back()
        self.led_off()
        self.update_lcd("HARD MODE", "Initializing...")

    def update_lcd(self, line1, line2):
        # Truncate to 16 chars to prevent errors
        l1 = f"{line1:<16}"[:16]
        l2 = f"{line2:<16}"[:16]
        self.lcd.setCursor(0, 0)
        self.lcd.write(l1)
        self.lcd.setCursor(1, 0)
        self.lcd.write(l2)

    def face_front(self):
        self.servo.setAngle(180) # Red Light

    def face_back(self):
        self.servo.setAngle(0)   # Green Light

    def face_rotate(self):
        self.servo.setAngle(90)  # Yellow Light

    def beep(self, count=1, duration=0.1):
        for _ in range(count):
            self.buzzer.write(1)
            time.sleep(duration)
            self.buzzer.write(0)
            time.sleep(0.05)
            
    def kill_sound(self):
        # The sound of elimination
        self.buzzer.write(1)
        time.sleep(1.5)
        self.buzzer.write(0)

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
        self.daemon = True
        self.running = True
        
        # Hardware
        self.ultrasonic = GroveUltrasonicRanger(PIN_ULTRASONIC)
        self.pir = GPIO(PIN_PIR, GPIO.IN)
        self.light_sensor = GroveLightSensor(PIN_LIGHT)
        self.btn = GPIO(PIN_BUTTON, GPIO.IN)

        # State
        self.distance = 0
        self.motion_detected = False
        self.button_pressed = False
        self.current_lux = 0
        
        # Stability
        self.last_stable_distance = 0

    def run(self):
        while self.running:
            # 1. Ultrasonic (Filter noise > 6m)
            raw_dist = self.ultrasonic.get_distance()
            if raw_dist < 600:
                self.distance = raw_dist

            # 2. PIR Motion
            if self.pir.read() == 1:
                self.motion_detected = True
            
            # 3. Button (Active Low)
            if self.btn.read() == 0:
                self.button_pressed = True
            else:
                self.button_pressed = False
                
            # 4. Light
            self.current_lux = self.light_sensor.light
            
            time.sleep(0.05) # 20Hz Refresh Rate

    def reset_motion_flag(self):
        self.motion_detected = False
        self.last_stable_distance = self.distance

    def check_for_movement(self):
        # PIR Check
        if self.motion_detected:
            return False
        # Ultrasonic Check
        delta = abs(self.distance - self.last_stable_distance)
        if delta > CAUGHT_THRESHOLD:
            return True
        return False

# ==========================================
#               GAME LOGIC
# ==========================================
def run_flashlight_save(bot, sensors):
    """Returns True if saved, False if eliminated"""
    bot.update_lcd("DETECTED!", "FLASH LIGHT!")
    bot.beep(3, 0.05) # Panic beeps
    
    # 5 Seconds to save yourself
    # Using 5s because "Hard Mode" is already hard enough!
    end_time = time.time() + 5 
    
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        bot.update_lcd(f"LUX: {sensors.current_lux}", f"TIME: {remaining}s")
        
        if sensors.current_lux > LIGHT_SAVE_LUX:
            bot.beep(1, 0.5)
            bot.update_lcd("SAVED!", "DONT MOVE...")
            time.sleep(1)
            return True
        
        time.sleep(0.1)
        
    return False

def calculate_green_duration(current_distance):
    """
    ADAPTIVE DIFFICULTY:
    Far away (500cm) -> Long time (5.0s)
    Close up (50cm)  -> Short time (1.5s)
    """
    # Percentage of distance remaining (0.0 to 1.0)
    factor = min(1.0, current_distance / MAX_DISTANCE)
    
    # Map to time range 1.5s to 5.0s
    duration =  (factor/3)
    return duration

def main():
    bot = SquidBot()
    sensors = SensorMonitor()
    sensors.start()

    # --- LOBBY PHASE ---
    print("HARD MODE LOADED.")
    bot.update_lcd("HARD MODE", "PRESS BTN START")
    while not sensors.button_pressed:
        time.sleep(0.1)

    # --- GAME START ---
    bot.beep(1, 1)
    game_start_time = time.time()
    player_lives = MAX_LIVES
    game_active = True
    
    print("GAME ON! 45 SECONDS!")

    while game_active:
        # 1. CHECK GLOBAL TIMER
        elapsed = time.time() - game_start_time
        time_left = int(GAME_TIME_LIMIT - elapsed)
        
        if time_left <= 0:
            bot.kill_sound()
            bot.update_lcd("TIME UP", "GAME OVER")
            break

        # 2. GREEN LIGHT (Adaptive)
        bot.face_back()
        bot.led_off()
        
        # Calculate dynamic duration
        green_time = calculate_green_duration(sensors.distance)
        green_end = time.time() + green_time
        
        while time.time() < green_end:
            # Update LCD with Time Left and Distance
            t_left = int(GAME_TIME_LIMIT - (time.time() - game_start_time))
            bot.update_lcd("GREEN LIGHT", f"T-{t_left}s | {sensors.distance:.0f}cm")
            
            if sensors.button_pressed:
                bot.update_lcd("VICTORY", f"Left: {t_left}s")
                bot.beep(5, 0.2)
                game_active = False
                break
            
            if t_left <= 0: # Timer expired mid-green
                game_active = False
                break
                
            time.sleep(0.1)

        if not game_active: break

        # 3. YELLOW LIGHT (Fast!)
        #bot.face_rotate()
        #bot.update_lcd("YELLOW...", "FREEZE!")
        #bot.beep(2, 0.1)
        # Fixed short duration for panic
        #time.sleep(0) 

        # 4. RED LIGHT (Long!)
        bot.face_front()
        bot.led_on()
        bot.buzzer.write(1)
        time.sleep(0.3)
        bot.buzzer.write(0)
        
        # Reset sensors for the freeze check
        sensors.reset_motion_flag()
        time.sleep(0.5) # Grace period
        
        # Long Red Light (4 to 7 seconds)
        red_end = time.time() + random.uniform(1, 3)
        
        while time.time() < red_end:
            # Update LCD
            t_left = int(GAME_TIME_LIMIT - (time.time() - game_start_time))
            bot.update_lcd("RED LIGHT", f"T-{t_left}s | {player_lives} Life")
            
            # Check for Kill
            if sensors.check_for_movement():
                print(">>> MOTION DETECTED <<<")
                
                if player_lives > 0:
                    player_lives -= 1
                    survived = run_flashlight_save(bot, sensors)
                    if survived:
                        sensors.reset_motion_flag() # Reset triggers
                        bot.face_front() # Re-intimidate
                        bot.led_on()
                    else:
                        bot.kill_sound()
                        bot.update_lcd("ELIMINATED", "GAME OVER")
                        game_active = False
                        break
                else:
                    # No lives left
                    bot.kill_sound()
                    bot.update_lcd("ELIMINATED", "NO LIVES LEFT")
                    game_active = False
                    break
            
            # Risky Win Check
            if sensors.button_pressed:
                bot.update_lcd("VICTORY", "RISKY WIN")
                bot.beep(5, 0.2)
                game_active = False
                break

            if t_left <= 0:
                game_active = False
                break
                
            time.sleep(0.1)

    # Cleanup
    bot.led_off()
    bot.face_front()
    print("Game Finished.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Safe exit
        GPIO(PIN_BUZZER, GPIO.OUT).write(0)
        GPIO(PIN_LED, GPIO.OUT).write(0)