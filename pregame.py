"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script manages the pregame menu
"""

import pygame 
import sys
import random
import time
import threading
import utils as u
import renderfunctions as rf

def legal():
    print("Legal clicked!")

stars = rf.generateStars(200, u.screen_width, u.screen_height)

def render(canvas):
    
    canvas.fill(u.black)
    for i, star in enumerate(stars):
            # Randomly change the brightness of stars
            if random.random() < 0.01:  # Adjust this value to control the twinkling frequency
                brightness_change = random.randint(-20, 20)
                stars[i] = (star[0], star[1], star[2], max(100, min(255, star[3] + brightness_change)))

    # Draw stars
    for star in stars:
        pygame.draw.circle(canvas, (star[3], star[3], star[3]), (star[0], star[1]), star[2])

    rf.text(canvas, u.titleFont, u.blue, 640, 90, "PreGame")
    rf.text(canvas, u.defaultFont, u.blue, 640, 150, "A certified hood classic, by Thomas")

    button_width, button_height = 300, 50
 
    paragraph = "Here you play as Homas, a young student who is being targeted\nand harrased by an evil wizzard \nnamed Bill, for the past year bill has been casting\nevil spells on Homas called \"NWarnings\", you must\ncomplete 3 stages of parkour to break the spells!"
    lines = paragraph.split("\n")  # Split the paragraph into lines

    line_height = u.defaultFont.get_linesize()  # Get the height of a line in the default font

    # Calculate the starting y-coordinate to center the text vertically
    total_text_height = len(lines) * line_height
    start_y = (u.screen_height - total_text_height) // 2

    # Render each line of the paragraph
    for i, line in enumerate(lines):
        rf.text(canvas, u.defaultFont, u.white, 640, start_y + i * line_height, line)

    # Draw "Go Back" button
    goBack = rf.Button("Start Game!", (u.screen_width - button_width) // 2, 500, button_width, button_height, u.blue, u.green, lambda: u.changeState("game"))
    goBack.draw(canvas, u.defaultFont)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle events for the button
        goBack.handle_event(event)