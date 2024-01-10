import cv2
import numpy as np
import picamera2
from trilobot import Trilobot

tbot = Trilobot()

SPEED = 0.7
TURN_DISTANCE = 30

BGR_RANGES = {
    "red": ((0, 0, 200), (20, 255, 255)),
    "green": ((35, 0, 0), (70, 255, 255)),
    "blue": ((90, 0, 0), (120, 255, 255)),
    "yellow": ((20, 0, 0), (30, 255, 255))
}

HSV_RANGES = {
    "red": ((160, 100, 100), (180, 255, 255)),
    "green": ((60, 100, 100), (75, 255, 255)),
    "blue": ((100, 100, 100), (120, 255, 255)),
    "yellow": ((25, 100, 100), (40, 255, 255))
}

def detect_color(image):
  color = None
  
  # Convert the image to HSV color space
  hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  
  # Detect the color using HSV range
  for color_name, hsv_range in HSV_RANGES.items():
      mask = cv2.inRange(hsv_image, np.array(hsv_range[0]), np.array(hsv_range[1]))
      if np.sum(mask) > 1000:# if sum greater than 1000 then colour is present 
          color = color_name
          break
  
  return color

def process_frames():
  with picamera2.PiCamera2() as camera:
      config = camera.still_configuration()
      camera.configure(config)

      while True:
          # Capture a frame
          camera.capture_buffer()
          frame = camera.processed_array

          # Detect the color
          color = detect_color(frame)

          # Print the detected color
          if color:
              print(f"Detected color: {color}")

          # Wait for a while before capturing the next frame
          cv2.waitKey(100)

def auto_drive(tbot, speed, turn_distance):
  """
  Function to autonomously drive a trilobot
  """
  # Start moving forward
  tbot.forward(speed)

  while not tbot.read_button(BUTTON_A):
      distance = tbot.read_distance()

      # Turn if we are too closer than the turn distance
      if distance < turn_distance:
          tbot.turn_right(speed)
          time.sleep(0.5)
      elif distance < 5:
          tbot.backward(speed)
          time.sleep(1)
      else:
          tbot.forward(speed)
      # No sleep is needed, as distance sensor provides sleep

if __name__ == "__main__":
  process_frames()
  auto_drive(tbot, SPEED, TURN_DISTANCE)
