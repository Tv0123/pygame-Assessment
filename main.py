"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script manages all the menus and scenes for the game
"""

import pygame
import menu
import renderfunctions as rf
import legal
import game
import settings
import pregame
import utils as u

pygame.init()

# CREATING CANVAS
canvas = pygame.display.set_mode((u.screen_width, u.screen_height))
pygame.display.set_caption('A Crazy Dream')


global clock
clock = pygame.time.Clock()
exit = False

while not exit:
    canvas.fill(u.white)

    #MANAGING EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        # Pass event and canvas to menu state
        if u.gamestate == "menu":
            menu.handle_event(event, canvas)  # Pass canvas here

        # Pass event to menu or game state
        if u.gamestate == "menu":
            menu.handle_event(event, canvas)



    #MANAGING MENUS
    if u.gamestate == "menu":
        menu.render(canvas)
    elif u.gamestate == "legal": 
        legal.render(canvas)
    elif u.gamestate == "game":
        game.run_game(canvas, clock)
    elif u.gamestate == "settings":  
        settings.render(canvas)
    elif u.gamestate == "pregame":
        pregame.render(canvas)


    # Update the display
    pygame.display.update()


pygame.quit()
