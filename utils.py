"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script manages random variables that need to be stored in memory
"""

import pygame

gamestate = "menu"


def changeState(newState):
    global gamestate
    print("Changing gamestate to:", newState)  # Print to debug
    gamestate = newState

screen_width, screen_height = 1280, 720

rect_color = (255,0,0) 
white = (255, 255, 255)
black = (0,0,0)
green = (0, 255, 0)
blue = (0, 0, 128)
canvas = None
clock = None

#GAME TILES AND ASSETS

playerSpriteSheet = pygame.image.load("assets/tiles/player.png")

skyTile = None
grassTile = None
CloudTile = None
rsignTile = None

pygame.font.init()
defaultFont = pygame.font.Font('freesansbold.ttf', 32)
titleFont = pygame.font.Font('assets/fonts/title.ttf', 120)
