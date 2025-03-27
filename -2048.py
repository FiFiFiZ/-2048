import pygame
from math import *
from random import *

# Concept: 2048 but with Negative Blocks, Divide Blocks, allowing for different outcomes and contraptions. Try to get to -2048!
# Maybe a specific square in the grid could have diffeerent effects on whatever block passes on it, giving a whole new layer of strategy and planning.



pygame.init()

board_width = 5
board_height = 6

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
while gridlen < 16:
    possible_integers.append(gridlen)
    gridlen = gridlen * 2
# print(randint(0,len(possible_integers)))

# Load Sprites
sprites = [pygame.Surface.convert(pygame.image.load("grid.png")), pygame.Surface.convert(pygame.image.load("1.png")), pygame.Surface.convert(pygame.image.load("2.png")), pygame.Surface.convert(pygame.image.load("4.png")), pygame.Surface.convert(pygame.image.load("8.png"))]
sprites = []

sprites = {
    "0" : pygame.Surface.convert(pygame.image.load("grid.png"))

}


for i in range (len(possible_integers)):
    sprites[str(possible_integers[i])] = pygame.Surface.convert(pygame.image.load(f"{possible_integers[i]}.png"))

# print(sprites)
# exit()

# Initiatial Variable Setup
kbinp = "" # last keyboard input
idx = ""
idx_2 = ""
new_block_pos = []
new_block_fade = 255
level = 1 # this is the rng cap (when reaching higher numbers, it increases the integer cap, this way you can only get integers you've already gotten before)


# Define Methods

def spawn(type): # spawns a block
    lost = 0
    idx = randint(0,len(grid)-1) # randomly pick a position for the square
    print(f"step 1: {idx}")
    while grid[idx] != 0: # look for the next open position if needed
        idx = (idx + 1) % len(grid)
        lost += 1
        if lost > len(grid):
            idx = "lose"
            new_block_pos.append(idx)
            return idx
    new_block_pos.append(idx)
    
    # assign a number to this block:
    idx_2 = expovariate()
    if idx_2 > level:
        idx_2 = 0
    idx_2 = possible_integers[floor(idx_2)]
    print(f"step 2: {idx_2}")

    # write block to grid
    grid[idx] = idx_2 #idx_2
    print(f"step 3: {grid}")
    
spawn("")
spawn("")

print(f"position: {idx}, value: {idx_2}")

def collide(position, direction):
    newposition = position
    collided = 0
    if direction == "left":
        while (newposition % board_width != 0) and collided == 0:
            if grid[newposition-1] == 0: # open space, move there
                newposition -= 1
            else: # collide
                # if newposition-2 >= 0:
                if grid [newposition-1] == grid[position]:
                    return f"m{newposition-1}"
                collided = 1 
        return newposition 
    
    elif direction == "right":
        while (newposition % board_width != board_width-1) and collided == 0:
            if grid[newposition+1] == 0: # open space, move there
                newposition += 1
            else: # collide 
                if newposition+1 < len(grid):
                    # print(newposition+1)
                    if grid [newposition+1] == grid[position]:
                        return f"m{newposition+1}"
                collided = 1 
        return newposition
    
    elif direction == "up":
        while (newposition - board_width >= 0) and collided == 0:
            if grid[newposition - board_width] == 0: # open space, move there
                newposition -= board_width
            else: # collide 
                if newposition - board_width >= 0:
                    if grid [newposition - board_width ] == grid[position]:
                        return f"m{newposition - board_width}"
                collided = 1 
        return newposition
    
    else:
        while (newposition + board_width <= len(grid)-1) and collided == 0:
            if grid[newposition + board_width] == 0: # open space, move there
                newposition += board_width
            else: # collide 
                if newposition + board_width  < len(grid):
                    if grid [newposition + board_width] == grid[position]:
                        return f"m{newposition+board_width}"
                    collided = 1 
        return newposition


# Main Loop
while run: 
    clock.tick(30)

    
    for i in range (0, board_height): # Draw every square
        for n in range (0, board_width) : 
            # print(f"square prinited: {i*board_width+n}")
            if grid[i*board_width+n] == 0:
                sprite_n = 0
            else:
                sprite_n = possible_integers.index(grid[i*board_width+n]) + 1
                sprite_n = grid[i*board_width+n]
            print(sprite_n)
            todraw = sprites[str(sprite_n)]
            todraw.set_alpha( 255 - ((i*board_width+n in new_block_pos) * new_block_fade) )
            screen.blit(todraw, (n*30,i*30))


    

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
    



    if kbinp: # if player inputs   
    
        grid_changed = 0 # initialize grid changes

        # initialize the direction and orientation in which is scanned the grid for collision detection
        scandir_type = (kbinp == "up" or kbinp == "down") * 1 # horizontal = 0, vertical = 1
        scandir = 1 - (kbinp == "down" or kbinp == "right") * 2 # up/left = 1, down/right = -1


        position_y = 0
        if scandir_type == 1 and scandir == -1:
                position_y = board_height-1 # if you press down, collision starts scanning grid from the bottom
        for i in range (board_height):
            # reset x position every y change
            if scandir == 1:    
                position_x = 0
            else:
                position_x = board_width-1
            # horizontally scan all blocks at this y position
            for n in range (board_width):
                print(f"{n} ,{position_y}, val:{position_y*board_width+position_x}")
                if grid[position_y*board_width+position_x] != 0: # if not an empty block, check collision
                    currentpos = position_y*board_width+position_x
                    newpos = collide(currentpos, kbinp)                        

                    if newpos != currentpos: # if position updated, write position to grid
                        grid_changed = 1 # grid has been modified

                        if "m" in str(newpos):
                            newpos = newpos.replace("m","")
                            grid[int(newpos)] = grid[currentpos] * 2
                            grid_changed = 2 # there's been a merge 
                        else:
                            grid[newpos] = grid[currentpos]
                        grid[currentpos] = 0
                position_x += scandir
            position_y = position_y + 1 - ((scandir_type == 1 and scandir == -1) *2) 
        


        if grid_changed > 0 :
            
            new_block_pos = [] # reset blocks fade-in list
            new_block_fade = 255 # reset global fade-in value for blocks
            

            check_repeat = []
            for i in range (len(grid)):
                if not grid[i] in check_repeat or grid[i] == 0:
                    check_repeat.append(grid[i])                
                else: 
                    break
            
            if len(check_repeat) < len(grid):
                if randint(0,2) == 1 :
                    spawn("")
            else:
                spawn("")
                max_spawn = floor(len(grid)/30)
                if max_spawn < 1:
                    max_spawn = 1
                
                for i in range (max_spawn):
                    if randint(0,2) == 0:
                        spawn("")


    new_block_fade -= 25

    # if key[pygame.K_SPACE] == True:
    #     if block_n < 2 or randint(0,1) == 1:
    #         new_block_fade = 255
    #         spawn("")

    if key[pygame.K_SPACE] == True:
        spawn("solid") # USE A DICTIONARY TO ASSIGN A VALUE TO A SPRITE

    # print(new_block_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


