"""
Author: Thomas Vrkic
Date: 6/10/24
Description: This script acts as the game aspect
"""



import pygame
import sys
import utils
import renderfunctions as rf


# Player properties
PLAYER_WIDTH = 36
PLAYER_HEIGHT = 72
PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 15

# Camera properties
camera_x = 0
camera_y = 0

# Tile properties
TILE_SIZE = 75
SMALL_TILE_SIZE = 45
global playerLives

FREEZE = False


# Define the level (0 = grass, 1 = sky, 2 = clouds)
level_data = [
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 1, 2, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 1, 1, 1, 1, 1, 2, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 1, 1, 2, 1, 1, 1, 1, 6, 6, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 2, 1, 1, 1, 1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1,],
    [6, 6, 2, 2, 1, 1, 1, 1, 1, 6, 6, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1,],
    [6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7 , 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1,],
    [6, 6, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 9, 5, 1, 1, 1, 1, 10, 1, 1, 5, 1, 1, 7, 7, 1, 0, 1, 7, 7, 1, 0, 1, 7, 7, 1, 0, 1, 1, 11, 1, 5, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 7, 1, 1, 1, 1, 1, 12, 1, 1, 1, 1,],
    [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 1, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 4, 4, 7, 4, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,],
]


def renderHUD(canvas, lives):
    canvas.blit(u['faceTile'], (55, 10))
    healthStart = 120
    for x in range(lives):
        canvas.blit(u['heartTile'], (healthStart + (45 * x), 10))


# Load and scale tile images
u = {}


u['heartTile'] = pygame.image.load("assets/tiles/heart.png")
u['heartTile'] = pygame.transform.scale(u['heartTile'], (55, 55))

u['faceTile'] = pygame.image.load("assets/tiles/playerface.png")
u['faceTile'] = pygame.transform.scale(u['faceTile'], (55, 55))

u['skyTile'] = pygame.image.load("assets/tiles/sky.png") #1
u['skyTile'] = pygame.transform.scale(u['skyTile'], (75, 75))

u['grassTile'] = pygame.image.load("assets/tiles/grass.png") #0
u['grassTile'] = pygame.transform.scale(u['grassTile'], (75, 75))

u['CloudTile'] = pygame.image.load("assets/tiles/cloud.png") #2
u['CloudTile'] = pygame.transform.scale(u['CloudTile'], (75, 75))

u['rsignTile'] = pygame.image.load("assets/tiles/esign.png") #5
u['rsignTile'] = pygame.transform.scale(u['rsignTile'], (75, 75))

u['dirtTile'] = pygame.image.load("assets/tiles/dirt.png") #4
u['dirtTile'] = pygame.transform.scale(u['dirtTile'], (75, 75))

u['stoneTile'] = pygame.image.load("assets/tiles/stone.png") #6
u['stoneTile'] = pygame.transform.scale(u['stoneTile'], (75, 75))

u['spikeTile'] = pygame.image.load("assets/tiles/spike.png") #7
u['spikeTile'] = pygame.transform.scale(u['spikeTile'], (75, 75))

u['esignTile'] = pygame.image.load("assets/tiles/esign.png") #8
u['esignTile'] = pygame.transform.scale(u['esignTile'], (75, 75))

u['lv1Tile'] = pygame.image.load("assets/tiles/lv1.png") #9
u['lv1Tile'] = pygame.transform.scale(u['lv1Tile'], (75, 75))

u['lv2Tile'] = pygame.image.load("assets/tiles/lv2.png") #10
u['lv2Tile'] = pygame.transform.scale(u['lv2Tile'], (75, 75))

u['lv3Tile'] = pygame.image.load("assets/tiles/lv3.png") #11
u['lv3Tile'] = pygame.transform.scale(u['lv3Tile'], (75, 75))

u['flagTile'] = pygame.image.load("assets/tiles/flag.png") #11
u['flagTile'] = pygame.transform.scale(u['flagTile'], (75, 75))



# Load player sprite sheet and extract frames
player_sprite_sheet = pygame.image.load("assets/tiles/player.png")
player_frames_left = [player_sprite_sheet.subsurface(pygame.Rect(i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(4)]
player_frames_right = [pygame.transform.flip(frame, True, False) for frame in player_frames_left]


# HelpBox class
class HelpBox(pygame.sprite.Sprite):
    def __init__(self, x, y, text, show=False):
        super().__init__()
        self.visible = show
        self.font = pygame.font.Font(None, 24)  # Define font
        self.text = text
        self.text_surface = self.font.render(text, True, (0,0,0))  # Render text
        text_width, text_height = self.text_surface.get_size()
        box_width = text_width + 20  # Add some padding
        box_height = text_height + 20  # Add some padding
        self.image = pygame.Surface((box_width, box_height))  # Create surface for the box
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.update_image()

    def update_image(self):
        if self.visible:
            self.image.fill((255,255,255))  # Fill with white color
            self.image.blit(self.text_surface, (10, 10))  # Blit text onto the box surface
        else:
            self.image.fill((0, 0, 0, 0))  # Transparent

    def toggle_visibility(self):
        self.visible = not self.visible
        self.update_image()


# Red box properties
RED_BOX_SIZE = 7500




helpBoxes = pygame.sprite.Group()
spikes = pygame.sprite.Group()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames_left = player_frames_left
        self.frames_right = player_frames_right
        self.current_frame = 0
        self.image = self.frames_right[self.current_frame]
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(utils.screen_width / 2, utils.screen_height / 1.2)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.anim_counter = 0
        self.facing_right = True

    def update(self):
        self.vel.y += GRAVITY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
            self.facing_right = True
        else:
            self.vel.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = -JUMP_HEIGHT

        self.move_and_check_collisions()
        self.animate()

    def move_and_check_collisions(self):
        # Separate x and y movements for better collision handling
        self.pos.x += self.vel.x
        self.resolve_collisions('x')

        self.pos.y += self.vel.y
        self.on_ground = False
        self.resolve_collisions('y')

        self.rect.topleft = self.pos  # Update the rect position

    def resolve_collisions(self, direction):
        self.rect.topleft = self.pos
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if direction == 'x':
                    if self.vel.x > 0:
                        self.rect.right = platform.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = platform.rect.right
                    self.pos.x = self.rect.x
                    self.vel.x = 0
                elif direction == 'y':
                    if self.vel.y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = platform.rect.bottom
                    self.pos.y = self.rect.y
                    self.vel.y = 0

    def animate(self):
        if self.vel.x != 0:  # Only animate when moving
            self.anim_counter += 1
            if self.anim_counter >= 10:  # Change frames every 10 ticks
                self.anim_counter = 0
                self.current_frame = (self.current_frame + 1) % 4
                if self.facing_right:
                    self.image = self.frames_right[self.current_frame]
                else:
                    self.image = self.frames_left[self.current_frame]
        else:
            self.current_frame = 0
            if self.facing_right:
                self.image = self.frames_right[self.current_frame]
            else:
                self.image = self.frames_left[self.current_frame]


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        print(f"Creating Platform at ({x}, {y}) with tile type {tile_type}")  # Debug statement
        if tile_type == 0 or tile_type == 3:
            self.image = u['grassTile']
        elif tile_type == 1:
            self.image = u['skyTile']
        elif tile_type == 2:
            self.image = u['CloudTile']
        elif tile_type == 4:
            self.image = u['dirtTile']
        elif tile_type == 5:
            self.image = u['rsignTile']
        elif tile_type == 6:
            self.image = u['stoneTile']
        elif tile_type == 7:
            self.image = u['spikeTile']
        elif tile_type == 9:
            self.image = u['lv1Tile']
        elif tile_type == 10:
            self.image = u['lv2Tile']
        elif tile_type == 11:
            self.image = u['lv3Tile']
        elif tile_type == 12:
            self.image = u['flagTile']
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class Sign(pygame.sprite.Sprite):
    def __init__(self, x, y, message, show_by_default=False, tile='esignTile'):
        super().__init__()
        self.image = u[f'{tile}']
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.message = message
        self.show_by_default = show_by_default
        if show_by_default:
            helpBox = HelpBox(self.rect.x - TILE_SIZE / 2, self.rect.y - 20, message, True)
            helpBoxes.add(helpBox)
            all_sprites.add(helpBox)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()

        self.image = u['spikeTile']
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()

        self.image = u['flagTile']
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

# Sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
signs = pygame.sprite.Group()
spikes = pygame.sprite.Group()
flags = pygame.sprite.Group()

# Creating platforms
for y in range(len(level_data)):
    for x in range(len(level_data[y])):
        platform_type = level_data[y][x]
        if platform_type in [0, 3, 4, 6]:
            platform = Platform(x, y, platform_type)
            platforms.add(platform)
            all_sprites.add(platform)

rsign_messages = [
    ("Press E on signs for help!", True),
    ("Press SPACE to jump.", False), 
    ("Avoid the spikes!", False),
    ("You're Almost there, evil Bill is over there!", False)
]

message_index = 0  # To keep track of the next message to assign

for y in range(len(level_data)):
    for x in range(len(level_data[y])):
        platform_type = level_data[y][x]
        if platform_type == 5:
            if message_index < len(rsign_messages):
                message, show_by_default = rsign_messages[message_index]
                sign = Sign(x, y, message, show_by_default, tile='rsignTile')
                signs.add(sign)
                all_sprites.add(sign)
                message_index += 1

for y in range(len(level_data)):
    for x in range(len(level_data[y])):
        platform_type = level_data[y][x]
        if platform_type == 7:
                spike = Spike(x, y, platform_type)
                spikes.add(spike)
                all_sprites.add(spike)

for y in range(len(level_data)):
    for x in range(len(level_data[y])):
        platform_type = level_data[y][x]
        if platform_type == 12:
                flag = Flag(x, y, platform_type)
                flags.add(flag)
                all_sprites.add(flag)

# Creating player
player = Player()
all_sprites.add(player)

global win


def run_game(canvas, clock):
    running = True
    win = False
    playerLives = 3
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player_rect = player.rect

            for spike in spikes:
                if player.rect.colliderect(spike.rect):
                    print("Player collided with a spike")
                    player.pos = pygame.Vector2(utils.screen_width / 2, utils.screen_height / 1.2)
                    playerLives -= 1
                    break

            for flag in flags:
                if player.rect.colliderect(flag.rect):
                    print("Player collided with a flag")
                    win = True

                    break

            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # Check if the player is colliding with the rsignTile
                # Get the rectangle of the player
                for sign in signs:  # Iterate through signs
                    if player_rect.colliderect(sign.rect):  # Check collision with player's rectangle
                        print("Player is touching rsignTile!")
                        # Check if a help box already exists at the sign's position
                        existing_box = None
                        for helpBox in helpBoxes:
                            if helpBox.rect.colliderect(sign.rect):
                                existing_box = helpBox
                                break
                        if existing_box:
                            existing_box.toggle_visibility()
                        else:
                            # Create help box at sign's position if it doesn't exist
                            helpBox = HelpBox(sign.rect.x, sign.rect.y, sign.message, True)
                            helpBoxes.add(helpBox)
                            all_sprites.add(helpBox)



        # Update
        all_sprites.update()

        # Adjust camera position to keep the player centered
        camera_x = player.rect.centerx - utils.screen_width / 2
        camera_y = player.rect.centery - utils.screen_height / 1.2

        # Draw / Render
        canvas.fill((52, 154, 255))
        for y in range(len(level_data)):
            for x in range(len(level_data[y])):
                if level_data[y][x] == 0:
                    canvas.blit(u['grassTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 1:
                    canvas.blit(u['skyTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 2:
                    canvas.blit(u['CloudTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 3:
                    canvas.blit(u['grassTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 4:
                    canvas.blit(u['dirtTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 5:
                    canvas.blit(u['rsignTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 6:
                    canvas.blit(u['stoneTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 7:
                    canvas.blit(u['spikeTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 9:
                    canvas.blit(u['lv1Tile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 10:
                    canvas.blit(u['lv2Tile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 11:
                    canvas.blit(u['lv3Tile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))
                elif level_data[y][x] == 12:
                    canvas.blit(u['flagTile'], (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))


        for sprite in all_sprites:
            if not isinstance(sprite, HelpBox) or sprite.visible:
                canvas.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

        renderHUD(canvas, playerLives)
        for helpBox in helpBoxes:
            if helpBox.visible:
                canvas.blit(helpBox.image, (helpBox.rect.x - camera_x, helpBox.rect.y - camera_y))


        if playerLives <= 0:
            sys.exit()

        if win == True:
            canvas.fill(utils.white)
            rf.text(canvas, utils.titleFont, utils.green, utils.screen_width / 2, utils.screen_height / 2, "YOU WIN!")


        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
