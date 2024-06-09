"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script manages the settings menu
"""

import pygame 
import sys
import random
import time
import threading
import utils as u
import renderfunctions as rf



stars = rf.generateStars(200, u.screen_width, u.screen_height)
volumeSlider = rf.Slider((u.screen_width - 600) // 2, 300, 600, 20, 0, 1, 0.5)
def render(canvas):

    # Draw stars
    canvas.fill(u.black)
    for i, star in enumerate(stars):
            # Randomly change the brightness of stars
            if random.random() < 0.01:  # Adjust this value to control the twinkling frequency
                brightness_change = random.randint(-20, 20)
                stars[i] = (star[0], star[1], star[2], max(100, min(255, star[3] + brightness_change)))
    for star in stars:
        pygame.draw.circle(canvas, (star[3], star[3], star[3]), (star[0], star[1]), star[2])


    #Setting the Title
    rf.text(canvas, u.titleFont, u.blue, 640, 90, "Settings")
    rf.text(canvas, u.defaultFont, u.blue, 640, 150, "A certified hood classic, by Thomas")

    button_width, button_height = 300, 50



    volumeSlider.draw(canvas)
    rf.text(canvas, u.defaultFont, u.white, 640, 270, f'Volume: {volumeSlider.get_value():.2f}')


    # Draw "Go Back" button
    goBack = rf.Button("Go Back", (u.screen_width - button_width) // 2, 500, button_width, button_height, u.blue, u.green, lambda: u.changeState("menu"))
    goBack.draw(canvas, u.defaultFont)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle events for the button
        goBack.handle_event(event)
        volumeSlider.handle_event(event)
