import pyautogui
from PIL import ImageGrab
import keyboard  # For toggling the script
import time
import threading

# Screen coordinates for detecting vines
left_coord = (682, 438)  # Coordinates to detect left vine
right_coord = (1213, 438)  # Coordinates to detect right vine

# Screen click coordinates
left_click = (301, 801)  # Coordinates to click on the left
right_click = (1624, 801)  # Coordinates to click on the right

# To store the last action
last_pressed = left_click  # Default to left
active = False  # Script toggle status

# Function to check if there's a green object at the given coordinates
def is_green(coord):
    # Capture a small region around the given coordinate (3x3 pixel area)
    x, y = coord
    screenshot = ImageGrab.grab(bbox=(x - 1, y - 1, x + 2, y + 2))
    
    # Average the color of the pixels in the region
    colors = [screenshot.getpixel((i, j)) for i in range(3) for j in range(3)]
    avg_color = tuple(sum(c) // len(c) for c in zip(*colors))  # Average RGB values

    # Check if the average color is predominantly green
    r, g, b = avg_color
    return g > r + 30 and g > b + 30  # Check if green is significantly greater than red and blue

# Click on the given position
def click_position(position):
    global last_pressed
    pyautogui.click(position)  # Click on the screen
    last_pressed = position
    print(f"Clicked at {position}")

# Toggle the script on and off
def toggle_script():
    global active
    active = not active
    if active:
        print("Script activated")
    else:
        print("Script deactivated")

# Function to perform detection and clicking in a separate thread
def detection_thread():
    global last_pressed

    while True:
        if active:
            # Check for green objects on the left and right
            left_green = is_green(left_coord)
            right_green = is_green(right_coord)

            # Immediate action on green detection
            if left_green:
                click_position(right_click)  # Click right if left is blocked
            elif right_green:
                click_position(left_click)  # Click left if right is blocked
            else:
                click_position(last_pressed)  # No green detected, repeat last action

            # Decrease sleep time for improved responsiveness
            time.sleep(0.001)  # Reduced delay for better performance

def main():
    global last_pressed
    # Use 't' to toggle the script on/off
    keyboard.add_hotkey('t', toggle_script)

    # Start the detection in a separate thread
    threading.Thread(target=detection_thread, daemon=True).start()

    # Keep the main thread running
    while True:
        time.sleep(0.1)  # Main thread can perform other tasks or just wait

if __name__ == "__main__":
    main()
