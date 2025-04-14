import pygame
from math import *
from random import *

import pygame.surface

# Concept: 2048 but with Negative Blocks, Divide Blocks, allowing for different outcomes and contraptions. Try to get to -2048!
# Maybe a specific square in the grid could have diffeerent effects on whatever block passes on it, giving a whole new layer of strategy and planning.
# A funny condition like "if you get a 64, you lose (you have to work things around to not get that)"

# remove blocks from fade list or add a fade to every single grid cell
# a block like the negator could take effect only when a block collides with it, maybe other blocks could be ghost
# a block that throws a square coming across it to another direction

# fix merging more than 2 blocks at once working only on certain directions
# fix big number blocks (that don't have a texture size of 30x30) to match correct position (and blit properly, maybe just make them 30x30 too)

# mute sound feature

# Initial Setup
pygame.init()

run = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((120,150))
pygame.display.set_icon(pygame.image.load("src\images\sprites\-1.png"))



# Load Sprites and Initialize Variables
sprites = {
    "0" : pygame.Surface.convert(pygame.image.load("src\images\sprites\grid.png")),
    "solid" : pygame.Surface.convert(pygame.image.load("src\images\sprites\solid.png")),
    "logo" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\logo.png")),
    "gameover" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\GAME OVER.png")),
    "exit0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\EXIT0.png")),
    "exit1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\EXIT1.png")),
    "restart0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\RESTART0.png")),
    "restart1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\RESTART1.png")),
    "screenend" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\screenend.png")),
    "SCORE" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\SCORE.png")),
    "minus" : pygame.Surface.convert(pygame.image.load("src\images\sprites\minus.png")),
    "ps" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\PRESS SPACE.png")),
    "bh0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\BOARD HEIGHT0.png")),
    "bh1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\BOARD HEIGHT1.png")),
    "bw0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\BOARD WIDTH0.png")),
    "bw1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\BOARD WIDTH1.png")),
    "left0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\left0.png")),
    "left1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\left1.png")),
    "right0" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\right0.png")),    
    "right1" : pygame.Surface.convert(pygame.image.load(r"src\images\ui\right1.png"))


}

possible_integers = [1]
for i in range (11): # powers of 2
    possible_integers.append(2**(i+1))

print(possible_integers)

for i in range (len(possible_integers)):
    sprites[str(possible_integers[i])] = pygame.Surface.convert(pygame.image.load(f"src\images\sprites\{possible_integers[i]}.png")) # load all number sprites

for i in range (10):
    idx = r"src\images\ui\font\txt" + str(i) + ".png"
    sprites[f"txt{i}"] = pygame.Surface.convert(pygame.image.load(idx))

menu = "main"
pygame.display.set_caption("-2048")
pygame.mixer.music.load("src\music\SNES Classic Edition Menu Song.mp3") 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.set_volume(0)

sounds = {
    "merge" : pygame.mixer.Sound("src\sfx\game_merge.wav"),
    "hoverover" : pygame.mixer.Sound("src\sfx\menu_hoverover.wav"),
    "select" : pygame.mixer.Sound("src\sfx\menu_select.wav")
}

channels = {
}

for i in range (3):
    channels[i] = pygame.mixer.Channel(i)
    channels[i].set_volume(0.1)

mousec = 0
non_collidables = [0, "minus"] # blocks that can't be collided with
selected = "" # selected button on ui
selected_time = 0
board_width = 4
board_height = 4

# Define Methods

def setup(setup_menu):
    global board_width, board_height, SCREEN_HEIGHT, SCREEN_WIDTH, screen, grid, possible_integers, kbinp, new_block_pos, new_block_fade, level, game_lost, selected, mousec, score, special_grid, already_merged, todraw_size # i found out too late that this was bad practice, i will take note of that in the future :P
    if setup_menu == "main":
        selected = "bw"
    elif setup_menu == "in-game":
        selected = ""
    
    if setup_menu == "main":
        SCREEN_WIDTH = 30 * 6
        SCREEN_HEIGHT = 30 * 6
    else:
        SCREEN_WIDTH = 30 * board_width
        SCREEN_HEIGHT = 30 * (board_height + 1)
        if SCREEN_WIDTH <= 30*4:
            SCREEN_WIDTH = 30*4


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Setup Grid
    grid = [] # This is the grid used for math calculations, it's the raw grid data with every square number on it.
    # smoothpos = [] # This lists every square's animation
    special_grid = [] # second grid layer for special blocks 

    for i in range (board_width * board_height) :
        grid.append(0)
        special_grid.append(0)
    # print(setup_menu)
    # if setup_menu == "in-game":
    #     print(board_width)
    #     exit()

    # Reset Variables
    kbinp = "" # last keyboard input
    new_block_pos = []
    new_block_fade = 255
    level = 2 # this is the rng cap (when reaching higher numbers, it increases the integer cap, this way you can only get integers you've already gotten before)
    game_lost = 0
    score = 0   
    already_merged = []
    todraw_size = 1

    spawn("")
    spawn("")

def button (name, x ,y):
    global menu, mousec, selected_time, board_width, board_height, keyjp

    x_sprite, y_sprite = pygame.mouse.get_pos()
    xh = x * 0.05 # makes x hitbox 20% bigger for buttons
    yh = y * 0.05 # makes y hitbox 20% bigger for buttons
    bidx = "" # button idx (which button arrows correspond to)

    if "left" in name:
        lr = "left"
    elif "right" in name:
        lr = "right"
    else: 
        lr = ""
    
    if lr == "":
        width = pygame.Surface.get_width(sprites[f"{name}0"])
        height = pygame.Surface.get_height(sprites[f"{name}0"])
    else:
        width = pygame.Surface.get_width(sprites[f"{lr}0"])
        height = pygame.Surface.get_height(sprites[f"{lr}0"])
        if lr == "left" or lr == "right":
            if "0" in name:
                val = board_width
                bidx = "bw"
            elif "1" in name:
                val = board_height
                bidx = "bh"
    
    # Rect(x, y, pygame.Surface.get_width(sprites[f"{name}0"])), pygame.Surface.get_width(sprites[f"{name}0"])

    if x_sprite in range (round(x-xh) ,round(x+width+xh)) and y_sprite in range (round(y-yh), round(y+height+yh)):
        hovered_over = 1
        if not ("left" in name or "right" in name):
            global selected
            if selected != name:
                selected_time = 0
            selected = name

    else:
        global game_lost
        if game_lost == 1:
            if selected == name:
                hovered_over = 2
            else:
                hovered_over = 0
        else:
            hovered_over = 0
            if selected == name:
                selected = 0

    if not ("left" in name or "right" in name):
        if hovered_over > 0 and selected_time == 0:
            channels[1].play(sounds["hoverover"])
    else:
        if selected == "bw" or selected == "bh":
            if keyjp[pygame.K_DOWN] == True:
                channels[0].play(sounds["merge"])
                if selected == "bw":
                    selected = "bh"

            if lr == "left" and keyjp[pygame.K_LEFT] == True and bidx == selected: # left button with keyboard
                val = change_bsize(val, -1, 3, 20)
                if isinstance(val,str):
                    val = int(val)
                    hovered_over = 3
                    channels[0].play(sounds["merge"])
            elif lr == "right" and keyjp[pygame.K_RIGHT] == True and bidx == selected: # right button with keyboard
                val = change_bsize(val, 1, 3, 20)
                if isinstance(val,str):
                    val = int(val)
                    hovered_over = 4
                    channels[0].play(sounds["merge"])


    if ((hovered_over == 1 and mousec == 1) or (hovered_over == 2 and keyjp[pygame.K_SPACE] == 1) or (hovered_over == 3 or hovered_over == 4)) == True: # receives signal to trigger the button
        if name == "restart": # trigger restart button
            channels[0].play(sounds["select"])
            setup(menu)
        elif name == "exit": # trigger exit button
            channels[0].play(sounds["select"])
            menu = "main"
            setup(menu)
        elif lr == "left" or lr == "right": # trigger right/left increments (via keyboard)
            if hovered_over == 3 and lr == "left": # trigger left
                if lr == "left":
                    hovered_over = 1
                    channels[0].play(sounds["merge"])
                else:
                    hovered_over = 0
            elif hovered_over == 4: # trigger right
                if lr == "right":
                    hovered_over = 1
                    channels[0].play(sounds["merge"])
                else:
                    hovered_over = 0

            else: # trigger right/left increments (via mouseclick)
                val = change_bsize(val, (lr == "right" *1)-(lr == "left" *1), 2, 30)
                if isinstance(val,str):
                    hovered_over = 1
                    val = int(val)
                    channels[0].play(sounds["merge"])
                    selected = bidx
                else:
                    hovered_over = 0
    elif lr == "left" or lr == "right":
        hovered_over = 0

    if lr == "left" or lr == "right":
        if "0" in name :
            board_width = val
        else:
            board_height = val
        name = lr
    
    screen.blit(sprites[f"{name}{(hovered_over>0)*1}"], (x, y))

    # pygame.draw.rect(screen,(255,255,255), (x-xh, y-yh, width+xh, height+yh))

        #     button("restart", (x,y))
        # screen.blit(sprites["restart0"], (0, SCREEN_HEIGHT-15))
        # screen.blit(sprites["exit0"], (SCREEN_WIDTH-pyga  ²+me.Surface.get_width(sprites["exit0"]), SCREEN_HEIGHT-15))

def checkloss(): 
    if not 0 in grid:
        for i in range (board_height):
            for n in range (board_width):
                currentpos = i*board_width+n

                if isinstance (grid[currentpos], int): # if not special block (which can't merge), run merge detection:
                    idx = [currentpos + 1, currentpos - 1, currentpos + board_width, currentpos - board_width]
                    line = floor(currentpos/board_width)
                    line = [line, line, line+1, line-1] # to check whether the block corresponds to the line it's supposed to be on

                    tocheck = []

                    for k in range (len(idx)):
                        if idx[k] in range (0, len(grid)): # check if it's within the grid
                            if (floor(idx[k]/board_width)) == line[k]: # check whether or not it's on the intended line
                                tocheck.append(idx[k]) # add positions to check

                    for k in range (len(tocheck)):
                        checkloss = (grid[currentpos] == grid[tocheck[k]])
                        if checkloss == True:
                            return "notlost"
                        
                        
        global game_lost
        game_lost = 1
        return "lost"
    else: return "notlost"
    


def checksolid(idx): # check if spawning solid block is in immediate diagonal vicinity of another solid block (to prevent squares getting surrounded by solids)

# it also needs to check whether the immediate diagonal vicinity block is on the line it's supposed to be (a line above or below the square, not the same)
    if grid[idx] != 0:
        return True

    list_of_spots_to_check = [idx+board_width-1, idx+board_width+1, idx-board_width-1, idx-board_width+1]
    list_of_lines = [floor(idx/board_width)+1, floor(idx/board_width)+1, floor(idx/board_width)-1, floor(idx/board_width)-1]

    print(f"fijqspfjqspofjsqpf {list_of_spots_to_check}")
    for i in range(len(list_of_spots_to_check))  :
        print(f"iteration: {i}")
        try:
            test = grid[list_of_spots_to_check[i]]
        except IndexError: # if off-grid (if the square number is out of list range)
            print(i)
            print(f"OFF-GRID, SKIPPED: {list_of_spots_to_check[i]}")
            pass
        else:
            if floor(list_of_spots_to_check[i]/board_width) != list_of_lines[i] or list_of_lines[i] not in range (0,len(grid)-1): # if off-grid (here the square position actually corresponds to another one that isn't intended)
                print(i)
                print(f"OFF-GRID, SKIPPED: {list_of_spots_to_check[i]}")
                pass
            elif test == 0: # open space, continue to look for blocks within vicinity
                print(f"THIS MEANS THERE'S OPEN SPACE AT: {list_of_spots_to_check[i]}")
                pass
            elif test == "solid": # found space taken up by solid within vicinity
                print(f"CANNOT SPAWN: {list_of_spots_to_check[i]}")
                return True
    print(f"IT CAN SPAWN")
    return False

def spawn(type): # spawns a block
    global game_lost
    lost = 0
    idx = randint(0,len(grid)-1) # randomly pick a position for the square
    solid_not_spawnable = False
    if type == "solid":
        solid_not_spawnable = checksolid(idx)
    print(f"step 1: {idx}")
    print(f"if true, there is no gridpsace: {grid[idx] != 0}   if true, there is no specialspace: {((type == "solid" and solid_not_spawnable == True) or (not type == "solid" and ((type == "minus" and special_grid[idx] != 0) or not type == "minus")))}    if True, continue: {grid[idx] != 0 and ((type == "solid" and solid_not_spawnable == True) or (not type == "solid" and ((type == "minus" and special_grid[idx] != 0) or not type == "minus")))}")
    while grid[idx] != 0 or (type == "solid" and solid_not_spawnable == True) or (type == "minus" and special_grid[idx] != 0): # look for the next open position if needed
        idx = (idx + 1) % len(grid)
        lost += 1
        print(str(idx) + " " + str(lost))
        if type == "solid":
            solid_not_spawnable = checksolid(idx)
            if lost > len(grid):
                # game_lost = 1
                return
        else:
            solid_not_spawnable = 0
            if lost > len(grid):
                print(grid)
                print(special_grid)
                # exit()
                # game_lost = 1
                # new_block_pos.append(idx)
                return
    print(f"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW what there is at this spot: {special_grid[idx]} //// {not type == "solid" and (type == "minus" and special_grid[idx] != 0)} //// {grid[idx] != 0} //// {grid[idx] != 0 and ((type == "solid" and solid_not_spawnable == True) or (not type == "solid" and ((type == "minus" and special_grid[idx] != 0) or not type == "minus")))}") 

# add a if grid.count(0) > 0 to check whether or not there even is an instance and find the closest one to the random number generated


    if not solid_not_spawnable == True:
        new_block_pos.append(idx)
        print(f"what we spawned: {idx}, at iteration: {i}")
    else: return "can't spawn solid"
    
    # assign a number to this block:
    if type ==  "solid" : 
        idx_2 = type
    elif type == "minus":
        idx_2 = "minus" 
    else:
        idx_2 = expovariate()
        if idx_2 > level:
            idx_2 = 0
        idx_2 = possible_integers[floor(idx_2)]
    print(f"step 2: {idx_2}")

    # write block to grid
    if type == "minus":
        special_grid[idx] = idx_2
    else:
        grid[idx] = idx_2 #idx_2
    print(f"step 3: {special_grid}")
    print(f"fade list: {new_block_pos}")


def change_bsize(value, increment, min, max):
    value += increment
    if value < min:
        value = min
    elif value > max:
        value = max
    else: 
        return str(value)
    return value

def collide(position, direction):
    newposition = position
    collided = 0
    if direction == "left":
        while (newposition % board_width != 0) and collided == 0:
            if grid[newposition-1] in non_collidables : # open space, move there
                newposition -= 1
            else: # collide
                # if newposition-2 >= 0:
                if grid[newposition-1] == grid[position]:
                    return f"m{newposition-1}"
                collided = 1 
        return newposition 
    
    elif direction == "right":
        while (newposition % board_width != board_width-1) and collided == 0:
            if grid[newposition+1] in non_collidables: # open space, move there
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
            if grid[newposition - board_width] in non_collidables: # open space, move there
                newposition -= board_width
            else: # collide 
                if newposition - board_width >= 0:
                    if grid [newposition - board_width ] == grid[position]:
                        return f"m{newposition - board_width}"
                collided = 1 
        return newposition
    
    else:
        while (newposition + board_width <= len(grid)-1) and collided == 0:
            if grid[newposition + board_width] in non_collidables: # open space, move there
                newposition += board_width
            else: # collide 
                if newposition + board_width  < len(grid):
                    if grid [newposition + board_width] == grid[position]:
                        return f"m{newposition+board_width}"
                    collided = 1 
        return newposition

def rendergrid():
    global todraw_size

    for i in range (0, board_height): # Draw every square
        for n in range (0, board_width) : 
            # print(f"square prinited: {i*board_width+n}")
            print(f"{len(grid)}  //  board_width: {board_width*board_height}")
            if grid[i*board_width+n] == 0:
                sprite_n = 0
            else:
                # sprite_n = possible_integers.index(grid[i*board_width+n]) + 1
                sprite_n = grid[i*board_width+n]
            # print(sprite_n)
            todraw = sprites[str(sprite_n)]
            if game_lost == 0:
                todraw.set_alpha(255 - ((i*board_width+n in new_block_pos) * new_block_fade))
            else:
                todraw.set_alpha(122)
            if str(i*board_width+n) in already_merged:
                print(todraw_size)
                todraw = pygame.transform.smoothscale_by(todraw, todraw_size)
            offset_board = (SCREEN_WIDTH != board_width*30) * (SCREEN_WIDTH - board_width*30)/2
            offset_square = (pygame.Surface.get_width(todraw) - 30)/2
            screen.blit(todraw, (n*30+offset_board-offset_square,i*30-offset_square))

            todraw2 = special_grid[i*board_width+n]
            if todraw2 != 0:
                todraw2 = sprites[todraw2]
                if sprite_n != 0:
                    todraw2.set_alpha(170)
                else:
                    todraw2.set_alpha(240)
                screen.blit(todraw2, (n*30+offset_board,i*30))
    
    for i in range (board_width):
        screen.blit(sprites["screenend"], (i*30+offset_board, SCREEN_HEIGHT-30))

def centertext(texture): # generate offset to center a texture
    w = texture.get_width()
    return (w/2)


# Pre-Start 
setup("main")

# spawn("")
# spawn("")
# print(f"position: {idx}, value: {idx_2}")

# Main Loop
while run: 
    clock.tick(30)
    screen.fill((0,0,0))

    mouse = pygame.mouse.get_pressed()
    if mouse[0] == True:
        mousec += 1
    else:
        mousec = 0

    keyjp = pygame.key.get_just_pressed()


    if menu == "in-game":

        rendergrid()

        if game_lost == 0:
            

            kbinp = "" # reset last keyboard input
            if keyjp[pygame.K_LEFT] == True:
                kbinp = "left"
            elif keyjp[pygame.K_RIGHT] == True:
                kbinp = "right"
            elif keyjp[pygame.K_UP] == True:
                kbinp = "up"
            elif keyjp[pygame.K_DOWN] == True:
                kbinp = "down"
            



            if kbinp: # if player inputs   
            
                grid_changed = 0 # initialize grid changes

                # initialize the direction and orientation in which is scanned the grid for collision detection
                scandir_type = (kbinp == "up" or kbinp == "down") * 1 # horizontal = 0, vertical = 1
                scandir = 1 - (kbinp == "down" or kbinp == "right") * 2 # up/left = 1, down/right = -1

                already_merged = []

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

                        if grid[position_y*board_width+position_x] == "solid" or grid[position_y*board_width+position_x] == "minus" : # if solid or minus, don't move
                            pass

                        elif grid[position_y*board_width+position_x] != 0: # else (if block is movable) if not an empty block, check collision
                            currentpos = position_y*board_width+position_x
                            newpos = collide(currentpos, kbinp)

                            if newpos != currentpos: # if position updated, write position to grid
                                grid_changed = 1 # grid has been modified

                                if "m" in str(newpos) and not newpos in already_merged:
                                    newpos = newpos.replace("m","")
                                    grid[int(newpos)] = grid[currentpos] * 2 
                                    already_merged.append(newpos)
                                    grid_changed = 2 # there's been a merge 
                                    score += grid[int(newpos)]
                                    channels[2].play(sounds["merge"])
                                else:
                                    grid[newpos] = grid[currentpos]
                                grid[currentpos] = 0
                        position_x += scandir
                    position_y = position_y + 1 - ((scandir_type == 1 and scandir == -1) *2) 
                


                if grid_changed > 0 :
                    
                    new_block_pos = [] # reset blocks fade-in list
                    new_block_fade = 255 # reset global fade-in value for blocks
                    todraw_size = 1.6
                
                    spawn("")  # spawns a new number
                    max_spawn = floor(len(grid)/30)
                    
                    # for i in range (max_spawn): 
                    #     if randint(0,4) == 0:
                    #         spawn("")

                game_lost = (checkloss() == "lost") * 1
                if game_lost == 1:
                    if selected == "":
                        selected = "restart"


            new_block_fade -= 45
            selected_time += 1
            todraw_size += (1-todraw_size)/3

            # if keyjp[pygame.K_SPACE] == True:
            #     if block_n < 2 or randint(0,1) == 1:
            #         new_block_fade = 255
            #         spawn("")

            if keyjp[pygame.K_KP0] == True:
                spawn("solid") # USE A DICTIONARY TO ASSIGN A VALUE TO A SPRITE + MAKE SFX AND PARTICLES AND ANIMATIONS AND TRAILS + UI AND COMMENT EVERYTHING OUT + DEFINE DIFFERENT SETUP METHODS (main menu setup, game setup) + SCORE COUNTER
            if keyjp[pygame.K_i] == True:
                game_lost = (checkloss() == "lost") * 1
                print(f"wha: {game_lost}")
            if keyjp[pygame.K_p] == True:
                spawn("minus")
                print(special_grid)
            # print(new_block_pos)

        else: 
            screen.blit(sprites["gameover"], ((SCREEN_WIDTH-pygame.Surface.get_width(sprites["gameover"]))/2, (SCREEN_HEIGHT-pygame.Surface.get_height(sprites["gameover"]))/2))

            if keyjp[pygame.K_LEFT] == True:
                selected = "restart"
            if keyjp[pygame.K_RIGHT] == True:
                selected = "exit"
                
                                
            # menu = "main"
    
        # moused, mousedy = pygame.mouse.get_rel()
        # moused = moused**2 + mousedy**2

        # if moused > 0:
        #     selected = ""
            
        button("restart", 0, SCREEN_HEIGHT-15)
        button("exit", SCREEN_WIDTH-pygame.Surface.get_width(sprites["exit0"]), SCREEN_HEIGHT-15)

        screen.blit(sprites["SCORE"], (((SCREEN_WIDTH)-(len(f"SCORE: {score}")*8))/2, SCREEN_HEIGHT-30))

        # screen.blit(sprites["SCORE"], (0, SCREEN_HEIGHT-30))

        score = str(score)
        for i in range (len(score)):
            screen.blit(sprites[f"txt{score[i]}"], (((SCREEN_WIDTH)-(len(f"SCORE: {score}")*8))/2+(7+i)*8, SCREEN_HEIGHT-30))

            # print((board_width*30)-(len(f"SCORE: {score}")*8)/2+(7+i)*8)
            # print((board_width*30)-(len(f"SCORE: {score}")*8)/2)
            # print((board_width*30)-(len(f"SCORE: {score}")*8))
        score = int(score)

        # screen.blit(sprites["restart0"], (0, SCREEN_HEIGHT-15))
        # screen.blit(sprites["exit0"], (SCREEN_WIDTH-pygame.Surface.get_width(sprites["exit0"]), SCREEN_HEIGHT-15))



    elif menu == "main":
        screen.fill((0,0,0)) # refresh screen
        print(pygame.time.get_ticks())
        # pygame.Surface.set_colorkey(sprites["logo"], (255,255,255))
        screen.blit(pygame.transform.scale_by(sprites["logo"], 1.5), ((SCREEN_WIDTH/2-centertext(sprites["logo"])*1.5),17.5+sin(pygame.time.get_ticks()/200)*3.5))
        # screen.blit(pygame.transform.scale_by(sprites["logo"], 1), ((SCREEN_WIDTH/2-centertext(sprites["logo"])*1),17.5+sin(pygame.time.get_ticks()/200)*3.5))
        screen.blit(sprites["ps"], ((SCREEN_WIDTH/2-centertext(sprites["ps"])),SCREEN_HEIGHT-30))
        if keyjp[pygame.K_SPACE] == True:
            menu = "in-game"
            setup(menu)
            # SCREEN_WIDTH = randint(0,17*30)
            # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            # (len(str(board_width))+2)*4
        
        if selected == "bh":
            if keyjp[pygame.K_UP] == True:
                selected = "bw"
                channels[0].play(sounds["merge"])
        elif selected == "bw":
            if keyjp[pygame.K_DOWN] == True:
                selected = "bh"
                channels[0].play(sounds["merge"])

        offset = (len(str(board_width))+3.5)*4
        offs = 18
        print(offset)

        screen.blit(sprites[f"bw{(selected=="bw")*1}"], ((SCREEN_WIDTH/2-centertext(sprites["bw0"])-offset),SCREEN_HEIGHT/2-25))
        button("left_0", floor(SCREEN_WIDTH/2-centertext(sprites["left0"])-offset+4*(offs)), floor(SCREEN_HEIGHT/2-25))
        button("right_0", floor(SCREEN_WIDTH/2-centertext(sprites["right0"])-offset+4*(offs+4+len(str(board_width))*2)), floor(SCREEN_HEIGHT/2-25))
        for i in range (len(str(board_width))):
            screen.blit(sprites[f"txt{str(board_width)[i]}"], ((SCREEN_WIDTH/2-centertext(sprites["txt1"])-offset+4*((offs+3)+i*2)) ,SCREEN_HEIGHT/2-25))

        offset = (len(str(board_height))+3.5)*4
        offs = 19
        screen.blit(sprites[f"bh{(selected=="bh")*1}"], ((SCREEN_WIDTH/2-centertext(sprites["bh0"])-offset),SCREEN_HEIGHT/2-0))
        button("left_1", floor(SCREEN_WIDTH/2-centertext(sprites["left0"])-offset+4*offs), floor(SCREEN_HEIGHT/2-0))
        button("right_1", floor(SCREEN_WIDTH/2-centertext(sprites["right0"])-offset+4*((offs+4)+len(str(board_height))*2)), floor(SCREEN_HEIGHT/2-0))
        for i in range (len(str(board_height))):
            screen.blit(sprites[f"txt{str(board_height)[i]}"], ((SCREEN_WIDTH/2-centertext(sprites["txt1"])-offset+4*((offs+3)+i*2)) ,SCREEN_HEIGHT/2-0))

        button("mutev", floor(SCREEN_WIDTH/2-centertext(sprites["left0"])), floor(SCREEN_HEIGHT/2+25))


        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


