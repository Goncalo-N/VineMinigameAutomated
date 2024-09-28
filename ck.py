import pyautogui
from PIL import ImageGrab
import keyboard  # For toggling the script
import time
import threading

# Screen coordinates and the RGB color for green vines
left_coord = (943, 465)  # Coordinates to detect left vine
right_coord = (1208, 465)  # Coordinates to detect right vine
green_threshold = (0, 156, 34)  # Adjust to match the green color of vines

# Screen click coordinates
left_click = (595, 801)  # Coordinates to click on the left
right_click = (1571, 801)  # Coordinates to click on the right

# To store the last action
last_pressed = left_click  # Default to left
active = False  # Script toggle status
is_clicking = False  # State to check if a click is in progress
last_action_time = 0  # Track time of last action

# Define a function to check if there's a vine at the given coordinates
def is_vine(coord):
    # Capture a small region around the given coordinate
    x, y = coord
    region = (x - 5, y - 5, x + 5, y + 5)  # Capture a 10x10 pixel region
    screenshot = ImageGrab.grab(bbox=region)
    
    # Average the color of the pixels in the region
    colors = [screenshot.getpixel((i, j)) for i in range(10) for j in range(10)]
    avg_color = tuple(sum(c) // len(c) for c in zip(*colors))  # Average RGB values
    
    # Check if the average color is close to green (using a threshold)
    return all(abs(avg_color[i] - green_threshold[i]) < 30 for i in range(3))  # Adjusted threshold

# Click on the given position
def click_position(position):
    global last_pressed, is_clicking, last_action_time
    is_clicking = True  # Set the clicking state
    pyautogui.click(position)  # Click on the screen
    last_pressed = position
    last_action_time = time.time()  # Update last action time
    print(f"Clicked at {position}")
    is_clicking = False  # Reset clicking state after action

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
            # Check for vines
            left_vine = is_vine(left_coord)
            right_vine = is_vine(right_coord)

            if left_vine and not right_vine:
                click_position(right_click)  # Click right if left is blocked
            elif right_vine and not left_vine:
                click_position(left_click)  # Click left if right is blocked
            else:
                click_position(last_pressed)  # No vine, repeat the last click

            # Adjust sleep time based on vine detection
            if left_vine or right_vine:
                time.sleep(0.05)  # Slow down when a vine is detected
            else:
                time.sleep(0.01)  # Normal speed when no vines detected

        else:
            time.sleep(0.1)  # Wait longer if the script is inactive

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
