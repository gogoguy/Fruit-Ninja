#Name: Yonah Tenenbaum
#Date: May 27, 2020
#Filename: fruitninja.py
#Description: The game "Fruit Ninja". The levels get progressively harder. To pause, press "p". 
# How to play:
# Click and drag to start slicing. Slice the fruit but NOT the bombs! If you slice a bomb, you lose. 
# Also, make sure not to miss more than three fruit!

#import library of functions called pygame
import pygame
import math
import random
import os
from pygame.constants import K_RETURN,K_p
import time
import os.path
from os import path


#initialize the game engine
pygame.init()

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
# Set the width and height of the screen [width, height]
size = [750, 500]
screen = pygame.display.set_mode(size)

#Initialize fonts
font = pygame.font.SysFont(None, 24)
level_font = pygame.font.Font('level.otf',50)
hs_font = pygame.font.SysFont(None,50)
# Set caption 
pygame.display.set_caption("Fruit Ninja")
# Load the background images
bgs = []
for i in range(11):
    background = pygame.image.load("bg"+str(i)+".jpg")
    bgs.append(background)
    
# Loop until the user clicks the close button.
done = False # this is a Boolean variable to control the while loop
# Used to manage how fast the screen updates
clock = pygame.time.Clock() # this controls how fast the game runs
# Load images
w_melon = pygame.image.load("wmelon.png")
w_melon = pygame.transform.smoothscale(w_melon,(98,85))
w_melon_l_half = pygame.image.load("wmelon_l_half.png")
w_melon_l_half = pygame.transform.smoothscale(w_melon_l_half,(98,85))
w_melon_r_half = pygame.image.load("wmelon_r_half.png")
w_melon_r_half = pygame.transform.smoothscale(w_melon_r_half,(98,85))

apple = pygame.image.load("apple.png")
apple = pygame.transform.smoothscale(apple,(66,66))
apple_l_half = pygame.image.load("apple_l_half.png")
apple_l_half = pygame.transform.smoothscale(apple_l_half,(66,66))
apple_r_half = pygame.image.load("apple_r_half.png")
apple_r_half = pygame.transform.smoothscale(apple_r_half,(66,66))

peach = pygame.image.load("peach.png")
peach = pygame.transform.smoothscale(peach,(62,59))
peach_l_half = pygame.image.load("peach_l_half.png")
peach_l_half = pygame.transform.smoothscale(peach_l_half,(62,59))
peach_r_half = pygame.image.load("peach_r_half.png")
peach_r_half = pygame.transform.smoothscale(peach_r_half,(62,59))

s_berry = pygame.image.load("s_berry.png")
s_berry = pygame.transform.smoothscale(s_berry,(68,72))
s_berry_l_half = pygame.image.load("s_berry_l_half.png")
s_berry_l_half = pygame.transform.smoothscale(s_berry_l_half,(68,72))
s_berry_r_half = pygame.image.load("s_berry_r_half.png")
s_berry_r_half = pygame.transform.smoothscale(s_berry_r_half,(68,72))

bomb = pygame.image.load("bomb.png")
bomb = pygame.transform.smoothscale(bomb,(66,68))

zero_x = pygame.image.load("0x.png")
zero_x = pygame.transform.smoothscale(zero_x,(90,40))

one_x = pygame.image.load("1x.png")
one_x = pygame.transform.smoothscale(one_x,(90,40))

two_x = pygame.image.load("2x.png")
two_x = pygame.transform.smoothscale(two_x,(90,40))

three_x = pygame.image.load("3x.png")
three_x = pygame.transform.smoothscale(three_x,(90,40))
# The slice list shows the program which slice to replace a fruit with when hit
slice_list = [w_melon,w_melon_l_half,w_melon_r_half,apple,apple_l_half,apple_r_half,peach,peach_l_half,peach_r_half,s_berry,s_berry_l_half,s_berry_r_half]
# Velocity is in pixels per 1/60 of a second
# Define starting variables for position and velocity
x_velocity = -2
y_velocity = 5
x_pos = 250
y_pos = 400
# Define the game to be not paused
paused = False

def start_pos_x():
    """
    Returns a randomly generated integer between 100 and 650, which will be used to determine the starting postition on the x-axis of every new fruit.
    """
    start_x = random.randint(100,650)
    return start_x
def start_velocity_x():
    """
    Returns a randomly generated number between -3 and 3, which will be used to determine the starting velocity on the x-axis of every new fruit.
    """
    start_vel_x = random.uniform(-3,3)
    return start_vel_x
def start_velocity_y():
    """
    Returns a randomly generated number between 12 and 14, which will be used to determine the starting velocity on the y-axis of every new fruit.
    """
    start_vel_y = random.uniform(12,14)
    return start_vel_y
def border_gravity(fruit,x_pos,y_pos,x_velocity,y_velocity):
    """
    This function calculates the updated positioning every 1/60 of a second for every element in the game that uses gravity. It includes calculating bounces off the sides.
    fruit: The name of the fruit who's position is being calculated.
    x_pos: The fruit's current position on the x-axis.
    y_pos: The fruit's current position on the y-axis.
    x_velocity: The fruit's current velocity on the x-axis.
    y_velocity: The fruit's current velocity on the y-axis.
    Returns the updated values for the x_pos, y_pos, x_velocity, and y_velocity.
    """
    # If the fruit is x, then it's width and height will be y...
    if fruit == w_melon:
        fruit_w = 98
        fruit_h = 95
    elif fruit == s_berry:
        fruit_w = 68
        fruit_h = 72
    elif fruit == peach:
        fruit_w = 62
        fruit_h = 59
    elif fruit == apple:
        fruit_w = 66
        fruit_h = 66
    elif fruit == bomb:
        fruit_w = 66
        fruit_h = 68
    else:
        # If it's not any of the things above, then the fruit is actually a fruit slice, so assign it 0 for width and height. 
        # The game uses this specific width to identify fruit slices later on, which is why this is necessary.
        fruit_w = 0
        fruit_h = 0
    # Update the y-axis position by subtracting the y velocity from the current y position
    y_pos -= y_velocity
    # Update the x-axis position by adding the x velocity to the current x position
    x_pos += x_velocity
    # If the fruit touches the left border, at (0,y)
    if round(x_pos) < 1:
        # Set the x velocity equal to negative 0.9 times what it was, to simulate energy losses
        x_velocity = (x_velocity * -0.9)
        # move the fruit a pixel to the right so it doesn't touch the border again.
        x_pos = 1
    # Calculate if the fruit has touched the right border. Take into account its specific width.
    if round(x_pos > 750 - fruit_w):
        x_velocity = (x_velocity * -0.9)
        x_pos = 750 - fruit_w
    # Mimick gravity by increasing the negative y-velocity by 0.15 every time this function runs, or every 1/60 of a second.
    y_velocity -= 0.15
    
    return x_pos, y_pos, x_velocity, y_velocity, fruit_w, fruit_h
    
def random_fruit():
    """
    Randomly picks a fruit or bomb from a list.
    Returns new_fruit, the fruit that it picked.
    """
    # Randomly generate an integer between 0 and 4.
    fruit_pick = random.randint(0,4)
    # Assign the new fruit to be from the list of fruit, using the random integer as an index
    new_fruit = fruit_list[fruit_pick]
    return new_fruit

def hit_check(f_x,f_y,fruit_w,fruit_h,m_x,m_y):
    """
    This function calculates whether an inputted fruit has come into contant with the cursor.
    f_x: location of the fruit on the x-axis
    f_y: Location of the fruit on the y-axis
    fruit_w: Width of the fruit
    fruit_h: Height of the fruit
    m_x: Location of the cursor on the x-axis
    m_y: Location of the cursor on the y-axis
    Returns:
            True if the fruit has come into contact with the cursor
            False if it hasn't, or if it is a fruit slice
    """
    # If the width of the fruit is zero, then ignore it because it is a fruit slice
    if fruit_w == 0:
#         print("slice hit, ignored")
        return False
    # Check if the cursor lines up with the fruit in the x axis
    # Take into account the specific width of the fruit
    if m_x >= f_x and m_x <= (f_x+fruit_w):
        # Check if the cursor lines up with the fruit in the y axis
        # Take into account the specific height of the fruit
        if m_y >= f_y and m_y <= (f_y+fruit_h):
            return True
    else:
        return False
    
def show_strikes(strikes):
    """
    This function updates the Xs image to reflect the number of strikese.
    strikes: The inputted current number of strikes.
    returns: The value of the updated image.
    """
    # If there are 'a' strikes, set it to 'b' image
    if strikes == 0:
        strike_image = zero_x
    elif strikes == 1:
        strike_image = one_x
    elif strikes == 2:
        strike_image = two_x
    else:
        strike_image = three_x
    return strike_image

def high_score(score):
    """
    This function determines whether or not to update the highscore in "hs.txt"
    score: The score at the time the function is called, which would be when the user loses a game
    returns: True if it is higher than the previous high score, otherwise False.
    """
    # If the highscore file does not exist, create it and write the current score to it.
    if not path.exists("hs.txt"):
        f = open("hs.txt","x")
        f.close()
        f = open("hs.txt","w")
        f.write(str(score))
        f.close()
        new_best = True
    # Otherwise open and read it
    else:
        f = open("hs.txt","r")
        hs = int(f.read())
        # If the previous high score is smaller than the current score, rewrite the file with the current score
        if score > hs:
            f = open("hs.txt","w")
            f.write(str(score))
            f.close()
            new_best = True
        else:
            new_best = False
    return new_best

def pause_game():
    """
    This function pauses the game until the user types "P".
    """
    print("Paused... Press \"P\" to resume")
    paused = True
    # While the game is paused, keep checking to see if the letter "p" has been pressed
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If it has, change paused to False to exit the loop.
                if event.key == K_p:
                        paused = False
                        print("Resumed")
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                quit()
        clock.tick(60)
    return

def delay(cycles):
    """
    This function creates a delay of time whenever called. This is better than using time.sleep(x) because time.sleep() freezes the cursor. 
    The function is called between each level to give the player a short break.
    cycles: The inputted amount of time the delay is going to be. The unit is in 1/60th of a second.
    returns: A random integer between 1 and 12, to be used to set the background after level 12
    """
    delay_count = 0
    delayed = True
    # While delayed is True, loop until it isn't; adding 1 to the delay count each time so it gets closer to making "delayed" False, exiting the loop.
    while delayed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                quit()
        if delay_count == cycles:
            delayed = False
        else:
            delay_count += 1
            # Show the new level on screen.
            level_img = level_font.render("Level "+str(level), True, WHITE)
            
            screen.blit(bgs[0],[0,0])
            screen.blit(level_img, (300, 200))
            pygame.display.flip()
        clock.tick(60)
    rand_bg = random.randint(1,12)
    return rand_bg


new_slice_props = []
new_screen_slice_list = []

# List that holds the fruit that are currently on screen.
screen_fruit_list = []
# List that holds the properties of the fruit that are on screen: positions and velocties
screen_prop_list = []
# List that contains all possible objects
fruit_list = [w_melon,s_berry,apple,peach,bomb]
# List that holds the fruit slices that are currently on screen
screen_slice_list = []
# List that holds the properties of the fruit slices that are on screen: positions and velocties
slice_props = []
# When level increases, make the send delay trend down, increase the max amount of items allowed on screen
level  = 1
# generate_fruit_delay_count is responsible for creating a small minimum delay between sending fruit or bombs
generate_fruit_delay_count = 0
# variable to keep track of the number of fruit on screen
num_fruit = 0
# Set the default max number of fruit allowed on screen at first
max_fruit = 3
# List of all the physical properties a fruit can have
props = [x_pos,y_pos,x_velocity,y_velocity]
# Sets the amount of time between starting the game and when the first fruit is sent (in 1/60s of a second)
send_delay =  50
# Trail_pos keeps track of the multiple positions of the lines that create the trailing effect behind the cursor.
trail_pos = []
# List to keep track of the positions of the cursor
mouse_pos = []
# A count to time when to create a new node of the mouse trail
# This variable allows the game to have a tiny delay between drawing new nodes of the mouse trail.
mouse_trail_count = 0
# Do not show the mouse trail until this is true
trail_show = False
# Define the starting score to be 0
score = 0
# Define the starting high score to be 0, or whatever it is
if not path.exists("hs.txt"):
    hs = 0
else:
    f = open("hs.txt","r")
    hs = int(f.read()) 
    f.close()
# Define the starting strikes to 0, and the appropriate corresponding strikes image
strikes = 0
strike_image = zero_x
# Pause the game if the following is false
playing = False
# Fruit_per_level controls the number of fruit required to slice in order to advance levels
fruit_per_level = 14
# Reset_count controls the delay between losing and restarting the game with reset variables. 
# It exists so that when the user loses, the fruit on screen can still fall to the bottom, but afterwards, everything is still reset properly.
reset_count = 0
remain = 14
max_delay = 50
blit_fade = 0
delayed = False
new_best = False

cheats = False

print("Press \"P\" during a game to pause or resume it")

# -------- Main Program Loop -----------
while not done:
    # If the game has just ended
    if not playing:
        # Stop showing the mouse trail
        trail_show = False        
        if reset_count != 0:
            # Wait 180 cycles, and then reset a bunch of stuff
            if reset_count == 180:
                print("Reset count reached:",reset_count)
                reset_count=0
                
                strikes = 0
                screen_fruit_list = []
                screen_prop_list = []
                screen_slice_list = []
                slice_props = []
                num_fruit = 0
            else:
                reset_count += 1


        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                done = True
            if event.type == pygame.KEYDOWN:
                # If the user presses Enter, start the game
                if event.key == K_RETURN:
                    if playing == False:
                        if reset_count == 0:
                            # Reset scores 
                            playing = True
                            score = 0 
                            strikes = 0
                            level = 1
                            strike_image = zero_x

                            remain = fruit_per_level
                            rand_bg = delay(90)
                            max_fruit = 3
                            new_best = False
                    else:
                        playing = False


    # Resets the lists to blank every cycle. The lists fill up with any on-screen elements that need to get deleted by the game.
    to_be_del = []          # Fills up with fruit that need to be deleted.               
    if playing:        
        for event in pygame.event.get(): # go through every event in game (mouse etc)
            if event.type == pygame.QUIT: # if the user clicks the x on the window it will close
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_p:
                    pause_game()
                    trail_show = False
            # If the mouse button has been clicked, allow the mouse trail to be shown
            if event.type == pygame.MOUSEBUTTONDOWN:
                trail_show = True
            # Otherwise, turn off the mouse trail
            if event.type == pygame.MOUSEBUTTONUP:
                trail_show = False
        # If the score is equal to fruit_per_level times the current level, plus the current level, advance to the next level
        if score == (fruit_per_level*level)+level:
            # Increase the maximum number of fruit allowed on screen at once by one
            max_fruit += 1
            # Increase the maximum number of fruit allowed on screen at once by one (It actually double what the number says - so it's plus 2 every time)          
            fruit_per_level += 1
            print("*** Level",level+1,"***")
            print("Max # of fruit on-screen: ",max_fruit-1,"->",max_fruit)
            # Calculate the number of fruit that need to be sliced 
            remain = fruit_per_level + level
            level += 1
            # Generate a random background. This is only used after level 12
            rand_bg = delay(90)
            # Turn off the trail
            trail_show = False
            # Reset the lists of fruit and slices, and the ones containing their positions and velocities
            screen_fruit_list = []
            screen_prop_list = []
            screen_slice_list = []
            slice_props = []

            
            # Reset the number of fruit
            num_fruit = 0
        
        generate_fruit_delay_count += 1

        
        # If there are fewer fruit on screen than the maximum number allowed, and the number of fruit remaining in the level
        if num_fruit < max_fruit and num_fruit < remain+1: 
            # If the fruit sending delay (for sends between fruit) is greater that fruit sending delay (for delaying when the user runs the game)
            if generate_fruit_delay_count >= send_delay:
                # 20% of the time, give the game a random chance to increase the fruit sending delay by up to three times the normal delay. (If the level is under level 8)
                if level < 8:
                    if random.random() > 0.8:
                        send_delay = random.randint(10,150)
                    # The other 80% of the time, choose a random delay between 0 and 50 cycles.
                    else:
                        send_delay = random.randint(5,max_delay)
                else:
                    # If the level is below level 16, subtract the current level number from the maximum possible delay between sending fruit
                    if level < 16:
                        max_delay = 50 - level
                        send_delay = random.randint(0,max_delay)
                    # If we're above level 16, make the maximum send delay 18.
                    else:
                        send_delay = 18
                # Generate a new random fruit/bomb
                new_fruit = random_fruit()
                # Reset the delay count
                generate_fruit_delay_count = 0
                # Add the fruit to the list of fruit that are on screen
                screen_fruit_list.append(new_fruit)
                # Using multiple functions, randomly generate the following properties for the new fruit: x_position, x_velocity, and y_velocity.
                # The starting y_position for all objects is 600, which is slightly off screen.
                properties_list = [start_pos_x(),600,start_velocity_x(),start_velocity_y()]
                # Add the properties of the fruit to the list that is responsible for keeping track of positions and velocities.
                screen_prop_list.append(properties_list)
                # Record that a new fruit has been created
                num_fruit += 1
        # If there are the max number of fruit on screen, the game will wait until there aren't.
        else:
            pass
            #print("Too many items, waiting...")
    
    # Set background
    # If we're below level 12, use the backgrounds in order
    if level < 12:
        screen.blit(bgs[level-1],[0,0])
    else:
        # Otherwise, randomly choose one. 
        screen.blit(bgs[rand_bg],[0,0])
    # Blit the score
    score_img = font.render("Score: "+str(score), True, WHITE)
    screen.blit(score_img, (20, 20))
    # Blit the number of fruit remaining text
    remain_img = font.render("Fruit remaining: "+str(remain+1),True,WHITE)
    screen.blit(remain_img,(110,20))
    # Blit the current level
    level_img = font.render("Level: "+str(level),True,WHITE)
    screen.blit(level_img,(280,20))
    # Blit the high score
    hs_img = font.render("High Score: "+str(hs),True,WHITE)
    screen.blit(hs_img,(370,20))
    # Blit the strikes
    screen.blit(strike_image,(650,10))
    # Creating the mouse trail
    # The mouse trail works by drawing connected lines behind the cursor. The lines get increasingly smaller sideways, until they disappear.
    # I found that this gives the illusion of a mouse "trail".
    
    # Get the position of the cursor, assign it to two vars
    pos = pygame.mouse.get_pos()
    m_x = pos[0]
    m_y = pos[1]
    # Append  the mouse position to a list
    mouse_pos.append([m_x,m_y])
    # If the length of the mouse position list is three, 
    if len(mouse_pos) == 3:
        # Delete the first element of the list
        mouse_pos.pop(0)
        mouse_trail_count += 1
        # If the mouse_trail count has reached 2,
        if mouse_trail_count == 2:
            # Append the last and second last positions of the mouse to the list "trail_pos".
            trail_pos.append(mouse_pos[-2])
            trail_pos.append(mouse_pos[-1])
            mouse_trail_count = 0
    # If the trail position list has 16 entries,
    if len(trail_pos) == 16:
        # Delete the first two entries
        trail_pos.pop(0)
        trail_pos.pop(1)
    # If the trail position list has more than 10 entries,
    if len(trail_pos) > 10:
        # For the length of the backwards range of the trail positions list,
        for i in range(len(trail_pos)-1,-1,-1):
            # Set the first line's beginning and endpoint to the "last/most recent" two entries in the trail positions list
            trail_begin = trail_pos[i]
            trail_end = trail_pos[i-1]
            # Have the width grow increasingly smaller with every cycle of the for loop
            width = (i-1)
            # If the user is clicking the mouse, show the trail
            if trail_show:
                pygame.draw.line(screen,WHITE,trail_begin,trail_end,width)
    
    # Set the var equal to the length of the list containing the names of the fruit that are on screen
    draw_loop_range = len(screen_fruit_list)
    # This loop is responsible for drawing all the fruit objects on screen. It iterates through a list of every fruit, 
    # calculates where they should go, and draws them on screen.
    for i in range(draw_loop_range):       
    # Remember: Don't mess with the lists until after this loop finishes!!
        # This_prop_list will contain the properties of every element, seperately and one at a time. 
        # Every cycle, it gets redefined to have the properties of another iterated fruit that is on screen.
        this_prop_list = screen_prop_list[i]    
        # Use the border_gravity function to calculate the updated position and velocities, as well as the width and height of the fruit.
        x_pos, y_pos, x_velocity, y_velocity, fruit_w, fruit_h = border_gravity(screen_fruit_list[i],this_prop_list[0],this_prop_list[1],this_prop_list[2],this_prop_list[3])    
        # Apply the updated positions and velocities to the properties of the current iterated fruit.
        screen_prop_list[i] = [x_pos,y_pos,x_velocity,y_velocity]
        # Draw the current interated fruit on screen. Round the position because the positions are not whole integers, but pixels need to be.
        screen.blit(screen_fruit_list[i],[round(x_pos),round(y_pos)])
        
        # If the fruit has fallen past the bottom of the screen (600 pixels),
        if y_pos > 600:
            if reset_count == 0:
                # Add the fruit's index to a list. The list will be cycled through after this loop, and the fruit and its properties will be deleted.
                to_be_del.append(i)
                if screen_fruit_list[i] != bomb:
                    if cheats == False:
                        strikes += 1
                # Show the number of strikes
                strike_image = show_strikes(strikes)
                if strikes == 3:
                    playing = False
                    print("Three strikes and you're out!")
                    if high_score(score) == True:
                        hs = score
                        new_best = True
                    reset_count += 1
        # Checking if there have been any collisions with the cursor:
        # If the mouse trail is showing, meaning the user has clicked,
        elif trail_show:
            # Use the hit_check function to determine whether the user has sliced the fruit
            if hit_check(round(x_pos),round(y_pos),fruit_w,fruit_h,m_x,m_y):
                if reset_count == 0:    
                    #print("Hit! (",round(x_pos),",",round(y_pos),")",screen_fruit_list[i])
                    # If the player has sliced a bomb, end the current game
                    if screen_fruit_list[i] == bomb:
                        playing = False
                        # If the score is higher than the high score, set the high score to be the current score
                        if high_score(score) == True:
                            hs = score
                            new_best = True
                        print("Uh oh! Bombs are bad.")
                        # Set the strikes image to the one with three red exes.
                        strike_image = three_x
                        reset_count +=1
                    else:
                        # Add 1 to the score
                        score += 1
                        # Subtract one from the remaining # of fruit
                        remain -= 1
                        # Save the sliced fruit to a var
                        sliced_fruit = screen_fruit_list[i]
                        # Get the index of the fruit in the slice list
                        slice_index = slice_list.index(sliced_fruit)
                        # Send the fruit to be deleted (after this loop)
                        to_be_del.append(i)
                        # Add two slices to the slice list. The slices are the corresponding left and right slices for the fruit that was just sliced
                        screen_slice_list.append(slice_list[slice_index+1])
                        screen_slice_list.append(slice_list[slice_index+2])
                        # Add the properties of the new slices to the slice list
                        slice_properties_list = [x_pos,y_pos,-1,4]
                        slice_props.append(slice_properties_list)
                        slice_properties_list = [x_pos,y_pos,1,4]
                        slice_props.append(slice_properties_list)
                        slice_draw_loop_range = len(screen_slice_list)
    slice_draw_loop_range = len(screen_slice_list)
    # For the range of the length of the on screen slice list,
    for s in range(slice_draw_loop_range):
        # This_slice_list will contain the properties of every element, seperately and one at a time. 
        # Every cycle, it gets redefined to have the properties of another iterated slice that is on screen.
        this_slice_list = slice_props[s]
        # Use the border_gravity function to calculate the updated position and velocities, as well as the width and height of the slice.
        sx_pos, sy_pos, sx_velocity, sy_velocity, fruit_w, fruit_h = border_gravity(screen_slice_list[s],this_slice_list[0],this_slice_list[1],this_slice_list[2],this_slice_list[3])
        # Apply the updated positions and velocities to the properties of the current iterated slice.
        slice_props[s] = [sx_pos,sy_pos,sx_velocity,sy_velocity]
        # Draw the current interated slice on screen. Round the position because the positions are not whole integers, but pixels need to be.
        screen.blit(screen_slice_list[s],[round(sx_pos),round(sy_pos)])
        
    # For every entry on the to be deleted fruit list, delete the corresponding fruit and its properties.
    for k in to_be_del:
        try:
            screen_prop_list.pop(k)
            screen_fruit_list.pop(k)
        except:
            
            pass
        num_fruit -= 1

    
    
    # Remove all slices that have fallen off screen from the screen list and the properties list 
    for s in range(len(slice_props)):
        if slice_props[s][1] <= 600:
            new_slice_props.append(slice_props[s])
            new_screen_slice_list.append(screen_slice_list[s])
    slice_props = new_slice_props
    screen_slice_list = new_screen_slice_list
    new_slice_props = []
    new_screen_slice_list = []

  
    # Reset values when the game finishes
    # Make the "Press enter" text fade in and out, corresponding to a counter
    if not playing:
        fruit_per_level = 14
        if blit_fade <= 1:
            fade_rate = 3
        elif blit_fade >= 254:
            fade_rate = -3
        blit_fade += fade_rate
        
        # I used this website to make the text transparent: https://stackoverflow.com/questions/49594895/render-anti-aliased-transparent-text-in-pygame
        # Render the text surface.
        txt_surf = level_font.render("Press ENTER to start", True, WHITE)
        # Create a transparent surface.
        alpha_img = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        # Fill it with white and the desired alpha value.
        alpha_img.fill((255, 255, 255, blit_fade))
        # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
        txt_surf.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(txt_surf, (190, 200))
        # If the player got a new high score
        if new_best:
            # Render the text "high score" on the screen, with the new high score
            nb_img = hs_font.render("HIGH SCORE",True,WHITE)
            screen.blit(nb_img,(275,100))
            hs_img2 = hs_font.render(str(score),True,WHITE)
            screen.blit(hs_img2,(355,150))
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


    # --- Limit to 60 frames per second

    clock.tick(60) 


# Close the window and quit.
pygame.quit()
