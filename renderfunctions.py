"""
Author: Thomas Vrkic
Date: 6/10/24
Description: My in house render wrapper for pygame
"""

import pygame
import random
import utils as u

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
purple = (128, 0, 128)
pink = (255, 192, 203)
orange = (255, 165, 0)


def text(canvas, font, color, x, y, text):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    canvas.blit(text_surface, text_rect.topleft)

def generateStars(num_stars, screen_width, screen_height):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)  # Initial brightness
        stars.append((x, y, size, brightness))
    return stars

def textGlow(canvas, font, color, x, y, text, alpha=255, feather = 1):

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    canvas.blit(text_surface, text_rect.topleft)

    opacity = alpha / feather

    for z in range(feather):

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x - z, y - z))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x + z, y + z))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x + z, y))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x - z, y))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x, y + z))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x, y - z))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x - z, y + z))
        canvas.blit(text_surface, text_rect.topleft)

        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity * (feather - z))
        text_rect = text_surface.get_rect(center=(x + z, y - z))
        canvas.blit(text_surface, text_rect.topleft)

class ToggleButton:
    def __init__(self, text_on, text_off, x, y, width, height, color_on, color_off, hover_color_on, hover_color_off, action=None):
        self.text_on = text_on
        self.text_off = text_off
        self.rect = pygame.Rect(x, y, width, height)
        self.color_on = color_on
        self.color_off = color_off
        self.hover_color_on = hover_color_on
        self.hover_color_off = hover_color_off
        self.action = action  # Store the button action
        self.state = False  # False means off, True means on

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.state:
                pygame.draw.rect(surface, self.hover_color_on, self.rect)
            else:
                pygame.draw.rect(surface, self.hover_color_off, self.rect)
        else:
            if self.state:
                pygame.draw.rect(surface, self.color_on, self.rect)
            else:
                pygame.draw.rect(surface, self.color_off, self.rect)
        
        text = self.text_on if self.state else self.text_off
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                if self.action:
                    self.action(self.state)



class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        
        text_surface = font.render(self.text, True, (0,0,0)) #change for text colour
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.knob_rect = pygame.Rect(x, y, h, h)
        self.knob_rect.centerx = x + (initial_val - min_val) / (max_val - min_val) * w
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect) #Change for slider background colour
        pygame.draw.ellipse(screen, (120,201,201) if self.dragging else (0,0,0), self.knob_rect) #slider drag colour

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.knob_rect.centerx = min(max(event.pos[0], self.rect.left), self.rect.right)
                self.value = self.min_val + (self.knob_rect.centerx - self.rect.left) / self.rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.value