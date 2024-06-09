"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script manages the main menu
"""

import pygame
import sys
import random
import time
import threading
import utils as u
import renderfunctions as rf

def start_game():
    u.gamestate = "pregame"

def settings():
    u.gamestate = "settings"

def quit_game():
    pygame.quit()
    sys.exit()

def legal():
    u.gamestate = "legal"

def slider_action(value):
    print(f"Slider value: {value}")



button_width, button_height = 400, 50
button_spacing = 20
title_y = 90
direction = 1  # 1 for moving down, -1 for moving up

def animate_title():
    global title_y, direction
    while True:
        # Update the title text position
        title_y += direction * 0.5  # Adjusted speed
        
        # Reverse the direction if the text reaches the top or bottom
        if title_y <= 80 or title_y >= 95:
            direction *= -1
        
        time.sleep(0.1)  # Add a delay of 0.1 seconds

# Start the animation thread
animation_thread = threading.Thread(target=animate_title)
animation_thread.daemon = True
animation_thread.start()
stars = rf.generateStars(200, u.screen_width, u.screen_height)

toggle_button = rf.ToggleButton('On', 'Off', 100, 100, 100, 50, (0, 255, 0), (255, 0, 0), (0, 200, 0), (200, 0, 0), lambda state: print(f"Button is now {'On' if state else 'Off'}"))

buttons = [
    rf.Button("Start Game", (u.screen_width - button_width) // 2, (u.screen_height - button_height) // 2, button_width, button_height, u.blue, u.green, start_game),
    rf.Button("Settings", (u.screen_width - button_width) // 2, (u.screen_height - button_height) // 2 + button_spacing + button_height, button_width, button_height, u.blue, u.green, settings),
    rf.Button("legal Disclaimer", (u.screen_width - button_width) // 2, (u.screen_height - button_height) // 2 + 2 * (button_spacing + button_height), button_width, button_height, u.blue, u.green, legal),
    rf.Button("Quit", (u.screen_width - button_width) // 2, (u.screen_height - button_height) // 2 + 3 * (button_spacing + button_height), button_width, button_height, u.blue, u.green, quit_game)
]



def handle_event(event, canvas):
    for button in buttons:
        button.handle_event(event)
    toggle_button.handle_event(event)



def render(canvas):
    canvas.fill(u.black)
    for i, star in enumerate(stars):
        # Randomly change the brightness of stars
        if random.random() < 0.1:  # Adjust this value to control the twinkling frequency
            brightness_change = random.randint(-50, 50)
            stars[i] = (star[0], star[1], star[2], max(100, min(255, star[3] + brightness_change)))

    # Draw stars
    for star in stars:
        pygame.draw.circle(canvas, (star[3], star[3], star[3]), (star[0], star[1]), star[2])
    
    rf.textGlow(canvas, u.titleFont, u.white, 640, int(title_y), "A Crazy Dream", 100, 15)  # Cast title_y to int
    rf.text(canvas, u.titleFont, u.blue, 640, int(title_y), "A Crazy Dream")
    rf.text(canvas, u.defaultFont, u.blue, 640, 150, "a certified hood classic, by Thomas")

    for button in buttons:
        button.draw(canvas, u.defaultFont)




