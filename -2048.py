import pygame
from math import *
from random import *

# Concept: 2048 but with Negative Blocks, Divide Blocks, allowing for different outcomes and contraptions. Try to get to -2048!
# Maybe a specific square in the grid could have diffeerent effects on whatever block passes on it, giving a whole new layer of strategy and planning.



pygame.init()

board_width = 5
board_height = 5

SCREEN_WIDTH = 30 * board_width
SCREEN_HEIGHT = 30 * board_height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
clock = pygame.time.Clock()

# Initial Grid Setup
grid = [] # This is the grid used for math calculations, it's the raw grid data with every square number on it.
# smoothpos = [] # This lists every square's animation
gridlen = 0 
block_n = 0

while gridlen < board_width * board_height :
    grid.append(0)
    gridlen = len(grid)

possible_integers = [1]
gridlen = 2
while gridlen < 2048:
    possible_integers.append(gridlen)
    gridlen = gridlen * 2
# print(randint(0,len(possible_integers)))

# Load Sprites
sprites = [pygame.Surface.convert(pygame.image.load("grid.png")), pygame.Surface.convert(pygame.image.load("1.png")), pygame.Surface.convert(pygame.image.load("2.png")), pygame.Surface.convert(pygame.image.load("4.png")), pygame.Surface.convert(pygame.image.load("8.png"))]

# Initiatial Variable Setup
kbinp = "" # last keyboard input4
idx = ""
idx_2 = ""
level = 1 # this is the rng cap (when reaching higher numbers, it increases the integer cap, this way you can only get integers you've already gotten before)


# Define Methods

def spawn(): # spawns a block
    lost = 0
    idx = randint(0,len(grid)-1) # randomly pick a position for the square
    print(f"step 1: {idx}")
    while grid[idx] != 0: # look for the next open position if needed
        idx = (idx + 1) % len(grid)
        lost += 1
        if lost > len(grid):
            idx = "lose"
            return idx
    
    # assign a number to this block:
    idx_2 = expovariate()
    if idx_2 > level:
        idx_2 = 0
    idx_2 = possible_integers[floor(idx_2)]
    print(f"step 2: {idx_2}")

    # write block to grid
    grid[idx] = idx_2 #idx_2
    print(f"step 3: {grid}")
    
spawn()
spawn()

print(f"position: {idx}, value: {idx_2}")

def collide(position, direction):
    collided = 0
    if direction == "left":
        while (position % board_width != 0) and collided == 0:
            if grid[position-1] == 0: # open space, move there
                position -= 1
            else: # collide 
                collided = 1 
            print(f"position: {position} - collided: {collided}")
        return position

    elif direction == "right":
        pass
    elif direction == "up":
        variation = board_width
        pass
    else:
        variaton = -board_width


print(f"FINAL POSITION AFTER COLLIDING: {collide(2,"left")}")

# Main Loop
while run: 
    clock.tick(30)
    for i in range (0, board_height): # Draw every square
        for n in range (0, board_width) : 
            print(i*board_width+n)
            if grid[i*board_width+n] == 0:
                sprite_n = 0
            else:
                sprite_n = possible_integers.index(grid[i*board_width+n]) + 1
            screen.blit(sprites[sprite_n], (n*30,i*30))


    

    kbinp = "" # reset last keyboard input
    key = pygame.key.get_just_pressed()
    if key[pygame.K_LEFT] == True:
        kbinp = "left"
    elif key[pygame.K_RIGHT] == True:
        kbinp = "right"
    elif key[pygame.K_UP] == True:
        kbinp = "up"
    elif key[pygame.K_DOWN] == True:
        kbinp = "down"
    
    if kbinp: # if player moves
        for i in range (board_height): # depends on direction: if you move left, collision detection is left to right to prevent right blocks from colliding with left blocks that haven't been yet placed)
            for n in range (board_width):
                if grid[i*board_width+n] != 0:
                    currentpos = i*board_width+n
                    newpos = collide(currentpos, kbinp)
                    if newpos != currentpos:
                        grid[newpos] = grid[currentpos]
                        grid[currentpos] = 0
                    

    print(kbinp)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


