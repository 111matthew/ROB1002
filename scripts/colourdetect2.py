import cv2
import numpy as np
import picamera2
from trilobot import Trilobot
import time
import keyboard

SPEED = 0.2
TURN_DISTANCE = 30

BUTTON_A = 0
tbot = Trilobot()


class ColourDetector:
    def __init__(self):
        self.BGR_RANGES = {
            "red": ((0, 0, 200), (20, 255, 255)),
            "green": ((35, 0, 0), (70, 255, 255)),
            "blue": ((90, 0, 0), (120, 255, 255)),
            "yellow": ((20, 0, 0), (30, 255, 255))
        }

        self.HSV_RANGES = {
            "red": ((160, 100, 100), (180, 255, 255)),
            "green": ((60, 100, 100), (75, 255, 255)),
            "blue": ((100, 100, 100), (120, 255, 255)),
            "yellow": ((25, 100, 100), (40, 255, 255))
        }

    def detect_color(self, image):
        color = None
        
        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detect the color using HSV range
        for color_name, hsv_range in self.HSV_RANGES.items():
            mask = cv2.inRange(hsv_image, np.array(hsv_range[0]), np.array(hsv_range[1]))
            if np.sum(mask) > 1000:# if sum greater than 1000 then colour is present
                color = color_name
                break
        
        return color

class FrameProcessor:
    def __init__(self, color_detector):
        self.color_detector = color_detector

    def process_frames(self):
        with picamera2.PiCamera2() as camera:
            config = camera.still_configuration()
            camera.configure(config)

            while True:
                # Capture a frame
                camera.capture_buffer()
                frame = camera.processed_array

                # Detect the color
                color = self.color_detector.detect_color(frame)

                # Print the detected color
                if color:
                    print(f"Detected color: {color}")
                    tbot.fill_underlighting(color)

                # Wait for a while before capturing the next frame
                cv2.waitKey(100)

class AutoDriver:
    def __init__(self, trilobot, speed, turn_distance):
        self.trilobot = trilobot
        self.speed = speed
        self.turn_distance = turn_distance

    def auto_drive(self):
        """
        Function to autonomously drive a trilobot
        """
        # Start moving forward
        self.trilobot.forward(self.speed)

        while not self.trilobot.read_button(BUTTON_A):
            distance = self.trilobot.read_distance()

            # Turn if we are too closer than the turn distance
            if distance < self.turn_distance:
                self.trilobot.turn_right(self.speed)
                time.sleep(0.5)
            elif distance < 5:
                self.trilobot.backward(self.speed)
                time.sleep(1)
            else:
                self.trilobot.forward(self.speed)
            # No sleep is needed, as distance sensor provides sleep

GREEN = (0, 255, 0)
RED = (255, 0, 0)

LOOPS = 10 # How many times to play the LED animation
INTERVAL = 0.3 # Control the speed of the LED animation


if __name__ == "__main__":
    if keyboard.is_pressed('a'):
            print("Flashing green underlights")
            tbot.fill_underlighting(GREEN)
            time.sleep(INTERVAL)
            tbot.clear_underlighting()
            while True:
                color_detector = ColourDetector()
                frame_processor = FrameProcessor(color_detector)
                auto_driver = AutoDriver(tbot, SPEED, TURN_DISTANCE)
                time.sleep(1)
                if keyboard.is_pressed('s'):
                    print("Flashing red underlights")
                    tbot.fill_underlighting(RED)
                    time.sleep(INTERVAL)
                    tbot.clear_underlighting() 
