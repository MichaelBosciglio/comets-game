#Imports / Initializing Pygame
import pygame, sys, time
from pygame.locals import *
from pygame.constants import *
import random
import time
pygame.init()

#Sound Files
shoot_sound = pygame.mixer.Sound("shoot.wav")
death_sound = pygame.mixer.Sound("explosion.wav")
collision_sound = pygame.mixer.Sound("invaderkilled.wav")
pygame.mixer.music.load("song.wav")

#Global Variables
width = 800
height = 600
spaceship_width = 50
spaceship_height = 50
comet_width = 87
comet_height = 83
ufo_height = 276
ufo_width = 200
highscore = []
pause = False
sound = False

#Fonts
menu_text = pygame.font.SysFont('freesansbold.ttf',50)
title_text = pygame.font.Font('Hyperspace Bold.otf',110)
controls_text = pygame.font.Font('Hyperspace Bold.otf',30)
scoreboard = pygame.font.SysFont('freesansbold.ttf',25)

#Colors for Text
colorWhite = pygame.Color(255,255,255)
colorYellow = pygame.Color(200,200,0)
colorGrey = pygame.Color(128,128,128)
colorlightGrey = pygame.Color(191,191,191)
colorBlack = pygame.Color(0,0,0)
colorbrightBlack = pygame.Color(70,70,70)
colordarkGrey = pygame.Color(40,40,40)
colorRed = pygame.Color(175,0,0)
colorbrightRed = pygame.Color(255,0,0)
colorbrightBlue = pygame.Color(0,0,255)
colorBlue = pygame.Color(0,0,175)

#Initialization
fpsClock = pygame.time.Clock() 
screen  = pygame.display.set_mode((width,height)) #Sets Screen Dimensions
pygame.display.set_caption("Comets by Michael Bosciglio") #Sets Game Title on Window

#Icon and Images
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon) #Sets Icon on Game Window
background_image = pygame.image.load("Background.jpg")
spaceship_image = pygame.image.load("spaceship.png")
comet_image = pygame.image.load("comet.png")
projectile = pygame.image.load("bullet_image.png")
ufo_image = pygame.image.load("ufo.png")
ufo_image = pygame.transform.scale(ufo_image,(200,276)) #Transforms UFO image to be larger
spaceship_image.set_colorkey((255,255,255)) #Sets white background to be transparent on spaceship
   
def spaceship(x,y):
    """spaceship(x,y) - Displays a spaceship at the given parameters x and y"""
    screen.blit(spaceship_image, [x,y])  

def text_objects(text, font):
    """text_objects(text, font) - Saves a string and given font for the string"""
    textSurface = font.render(text, True, colorWhite) 
    return textSurface, textSurface.get_rect()
    
def titles(text):
    """titles(text) - Displays a screen title given the text as a string"""
    largeText = pygame.font.Font('Hyperspace Bold.otf',110)#Font
    TextSurf, TextRect = text_objects(text, largeText) #Text, Font
    TextRect.center = ((width / 2),(height / 2 - 150)) #Centers Text
    screen.blit(TextSurf, TextRect) #Displays Text to Screen 

def manual_text(text,height):
    """manual_text(text,height) - "Displays text for manual screen given the parameter \ntext as a string and height as an integer"""
    largeText = pygame.font.Font('Hyperspace Bold.otf',20)#Font
    TextSurf, TextRect = text_objects(text, largeText) #Text, Font
    TextRect.center = ((width / 2),height) #Centers Text
    screen.blit(TextSurf, TextRect) #Displays Text to Screen 

def controls_text(text,width,height):
    """controls_text(text,width,height) - Displays text for controls screen given parameter text as a string and width/height as an integer"""
    largeText = pygame.font.Font('Hyperspace Bold.otf',35) #Font
    TextSurf, TextRect = text_objects(text, largeText) #Text, Font
    TextRect = (width,height) #Position on screen
    screen.blit(TextSurf, TextRect) #Displays Text to Screen  

def crash():
    """crash() - Creates a crash screen when the spaceship has collided with an object"""
    global highscore #Makes all changes within the function global
    highscore.sort() #Sorts the highscore list from least to greatest
    controls_text("Highest Score - "+str(highscore[-1]),210,500) #Displays the highest score from the end of the list which is the greatest score
    pygame.mixer.music.stop() #Once the game ends, music stops
    pygame.mixer.Sound.play(death_sound) #Plays the death sound once the player gets hit by an object
    pygame.mouse.set_visible(True) 
    titles("You Crashed")
    while True:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #If the escape key is pressed, game closes
                    pygame.quit()
                    quit()
        #Buttons and Updates                    
        button("1 Player",150,275,150,75,colorRed,colorbrightRed,"1 Player")
        button("2 Player",325,275,150,75,colorRed,colorbrightRed,"2 Player")
        button("Back to Menu",500,275,150,75,colorBlue,colorbrightBlue,'mainmenu')       
        pygame.display.update()
        fpsClock.tick(60)

def button(message,x,y,w,h,ic,ac,action=None):
    """button(message,x,y,w,h,ic,ac,action=None) - Creates a button given the message as a string,\nx and y coordinates as an integer\n width and height as an integer\nthe inactive and active colour of the button\n and the action that the button performs."""
    mouse = pygame.mouse.get_pos() #Checks for Mouse Position
    click = pygame.mouse.get_pressed() #Checks if Mouse is pressed
    global sound #Makes all changes within the function global
    if x < mouse[0] and x + w > mouse[0] and y < mouse[1] and y + h > mouse[1]: #if the mouse is on the button, the active colour is displayed
        pygame.draw.rect(screen, ac,(x,y,w,h))
        #Logic for Button Actions
        if click[0] == 1 and action != None: #If they click on the button, the following action is performed
            if action == "1 Player": 
                game_loop(True,False) #Runs the 1 Player Game
            if action == "2 Player":
                game_loop(False,True) #Runs the 2 Player Game
            if action == 'unpause': #Unpauses the game and unpauses the music
                global pause #Makes all changes within the function global
                pygame.mixer.music.unpause()
                pause = False
            if action == 'controls': #Runs the controls screen
                controls()
            if action == 'mainmenu': #Runs the main menu screen and stops the pause menu if it is active
                pause = False
                menu_loop()
            if action == 'soundtrue': #Allows music to be played
                sound = True
            if action == 'soundfalse': #Turns off the music
                sound = False
            if action == 'manual': #Runs the manual screen
                manual()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h)) #If the mouse is not on the button, the inactive colour of the button is displayed
    #Displays Text Centered on a Button
    smallText = pygame.font.Font('Hyperspace Bold.otf',20) #Chooses the font
    TextSurf, TextRect = text_objects(message, smallText) #Displays the text chosen in the button parameters with the text 
    TextRect.center = ((x+(w/2)),(y+(h/2))) #Centers the text on the button
    screen.blit(TextSurf, TextRect) #Displays the text   

def points(count,x,y):
    """points(count,x,y,num) - Displays the score given the x and y coordinates of the scoreboard"""
    score_total = scoreboard.render("Score "+str(count),True, colorWhite) #Text for Player Score
    screen.blit(score_total,[x,y]) #Displays Score

def controls():
    """controls() - Creates a screen with game controls"""
    screen.fill(colorBlack) #Updates Background
    #Displays Text
    titles("Controls") #Displays title
    controls_text("Player 1",325,240)
    controls_text("Player 2",575,240)
    controls_text("Move Left",50,300)
    controls_text("Move Right",50,350)
    controls_text("Fire",50,400)
    controls_text("Pause",50,450)
    controls_text("Quit",50,500)
    controls_text("A",395,300)
    controls_text("D",395,350)
    controls_text("Space",350,400)
    controls_text("Left",620,300)
    controls_text("Right",610,350)
    controls_text("L",650,400)
    controls_text("P",395,450)
    controls_text("P",650,450)
    controls_text("ESC",373,500)
    controls_text("ESC",627,500)
    while True:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #If the Escape Key is Pressed, Game Closes
                    pygame.quit()
                    quit()
        #Back Button and Update            
        button("Back",10,10,85,85,colordarkGrey,colorbrightBlack,'mainmenu')      
        pygame.display.update()

def manual():
    """manual() - Creates a screen with the game manual"""
    screen.fill(colorBlack) #Updates Background
    #Displays Text
    titles("Manual") #Displays the title 
    manual_text("The name of the game is simple, survive at all costs",250)
    manual_text("You will be able to play two types of gamemodes",300)
    manual_text("1 Player: You are alone in space",350)
    manual_text("2 Player: You and a friend work together to survive in space",400)
    manual_text("Be sure not to get hit by comets or 'random objects'",450)
    manual_text("Have Fun!",500)
    while True:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #If the Escape Key is Pressed, Game Closes
                    pygame.quit()
                    quit()
        #Back Button and Update
        button("Back",10,10,85,85,colordarkGrey,colorbrightBlack,'mainmenu')      
        pygame.display.update()

def paused():
    """paused() - Pauses gameplay at any instant"""
    pygame.mixer.music.pause() #Pauses music when in paused screen
    pygame.mouse.set_visible(True) #Cursor is visible
    titles("Paused") #Creates title for Paused Menu
    while pause == True:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #If the Escape Key is Pressed, Game Closes
                    pygame.quit()
                    quit()
        #Back / Continue Buttons and Update                             
        button("Continue",200,275,150,75,colorRed,colorbrightRed,'unpause')
        button("Back to Menu",450,275,150,75,colorBlue,colorbrightBlue,'mainmenu')        
        pygame.display.update()
    
def menu_loop():
    """menu_loop() - Creates a main menu page where the user can play, read the controls and the manual or turn on and off music"""
    #Ensures that all of the global screens are off
    global pause
    global p1_mode
    global p2_mode
    p1_mode = False 
    p2_mode = False
    pause = False
    
    pygame.mouse.set_visible(True)
    screen.fill(colorBlack) #Creates Black Background
    titles("Comets") #Displays Title
    done = False
    while not done:
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #If the Escape Key is Pressed, Game Closes
                    done = True
        #Buttons, Update and Exit           
        button("1 Player",240,350,150,75,colorRed,colorbrightRed,"1 Player")
        button("2 Player",410,350,150,75,colorRed,colorbrightRed,"2 Player")
        button("Controls",240,450,150,75,colorBlue,colorbrightBlue,'controls')
        button("Manual",410,450,150,75,colorBlue,colorbrightBlue,'manual')
        button("Music On",675,490,125,50,colorGrey,colorlightGrey,'soundtrue')
        button("Music Off",675,550,125,50,colorGrey,colorlightGrey,'soundfalse')                       
        pygame.display.update()
        fpsClock.tick(60)            
    pygame.quit()
    sys.exit(0)
                                    
#Main Loop
def game_loop(p1_mode,p2_mode):
    """gameloop(p1_mode,p2_mode) - Runs the game given a True value from either p1_mode or p2_mode"""
    global sound #Ensures that sound within function is changed globally when changed in game
    global highscore #Ensures that highscore list is changed globally when changed in game
    global pause #Ensures that pause is global when pressed in game
    if sound == True: #Plays music if sound is True
        pygame.mixer.music.play(-1)        
    pygame.mouse.set_visible(False) #Mouse is not visible in game
    if p1_mode == True: #Starts the Spaceship in the middle when p1_mode is True, if p2_mode is True, starts to the left
        x1 = 375
    else:
        x1 = 300
    y1 = 550 #y value for the first spaceship
    dir_x1 = 0 #x value of spaceship 1 increases by amount when button is pressed
    x2 = 500 #x value for the second spaceship
    y2 = 550 #y value for the second spaceship
    dir_x2 = 0 #x value of spaceship 2 increases by amount when button is pressed
    comet_startx1 = random.randint(0,width - comet_width) #comet 1 Starting x position
    comet_starty1 = -300 #comet 1 Starting y position
    comet_startx2 = random.randint(0,width - comet_width) #comet 2 Starting x position
    comet_starty2 = -250 #comet 1 Starting y position
    ufo_startx1 = random.randint(0,width - ufo_width) #UFO 1 Starting x position
    ufo_starty1 = -5000 #UFO 1 Starting y position
    ufo_startx2 = random.randint(0,width - ufo_width) #UFO 2 Starting x position
    ufo_starty2 = -4000 #UFO 2 Starting y position
    score1 = 0 #Score
    bullets = [] #List with Bullet position 
    done = False
    while not done:
        x1 += dir_x1 #P1 Position Change when Key Pressed
        x2 += dir_x2 #P2 Position Change when Key Pressed
        comet_speed = 2 #Beginning Speed for comet
        ufo_speed = 10 #Speed for Both UFO's
        comet_speed += (score1 * 0.10) #comet Speed Increase
        ufo_speed += (score1 * 0.03) #UFO Speed Increase       
        for event in pygame.event.get():
            if (event.type == KEYUP) or (event.type == KEYDOWN):
                if (event.key == K_ESCAPE): #When Escape Key is pressed, Game Closes
                    done = True 
            if (event.type == KEYDOWN): #Events that take place when key is pressed down
                if event.key == K_a: #P1 Move Left 5 pixels
                    dir_x1 -= 5
                elif event.key == K_d: #P1 Move Right 5 pixels
                    dir_x1 += 5
                elif event.key == K_LEFT: #P2 Move Left 5 pixels
                    dir_x2 -= 5
                elif event.key == K_RIGHT: #P2 Move Right 5 pixels
                    dir_x2 += 5
                elif event.key == K_p: #Pause Game
                    pause = True
                    paused()
                elif (event.key == K_SPACE): #Player 1 Shoot
                    bullets.append([x1+(spaceship_width / 2),y1]) #Appends bullet position
                    pygame.mixer.Sound.play(shoot_sound) #Plays shooting sound
                elif (event.key == K_l):#Player 2 Shoot
                    bullets.append([x2+(spaceship_width / 2),y2]) #Appends bullet position
                    pygame.mixer.Sound.play(shoot_sound) #Plays shooting sound
                    
            if (event.type == KEYUP): #Events that take place when key is released
                if event.key == K_a: #P1 Stop Moving Left
                    dir_x1 = 0
                elif event.key == K_d: #P1 Stop Moving Right
                    dir_x1 = 0
                elif event.key == K_LEFT: #P2 Stop Moving Left
                    dir_x2 = 0
                elif event.key == K_RIGHT: #P2 Stop Moving Right
                    dir_x2 = 0

        for b in range(len(bullets)): #After shot, bullet moves upwards
            bullets[b][1] -= 10 #Bullet moves in the y direction by -10 pixels (Upwards)
                        
        for bullet in bullets: #Once bullet is off the screen, removes bullet
            if bullet[1] < 0: #Checks to see if bullet is above 0 in the y direction
                bullets.remove(bullet) #Removes bullet from list
                
        #Displays Background, Comets, UFO's                                
        screen.blit(background_image, [0,0])
        screen.blit(comet_image,[comet_startx1,comet_starty1])
        screen.blit(comet_image,[comet_startx2,comet_starty2])
        screen.blit(ufo_image,[ufo_startx1,ufo_starty1])
        screen.blit(ufo_image,[ufo_startx2,ufo_starty2])
        
        #Once Displayed, Comets and UFOS y value increases by respective speed
        comet_starty1 += comet_speed
        comet_starty2 += comet_speed
        ufo_starty1 += ufo_speed
        ufo_starty2 += ufo_speed

        #Draws Bullet, Produces Sound, Resets when Collides with comets, Increases Score
        for bullet in bullets:
            screen.blit(projectile,(bullet[0],bullet[1])) #Draws Bullet
            if bullet[1] < comet_starty1 + comet_height: #Checks to see if the y value of the bullet is equal to the y value of comet 1
                if bullet[0] > comet_startx1 and bullet[0] < comet_startx1 + comet_width: #Checks to see if the x value of the bullet is between the x values of comet 1
                    bullets.remove(bullet) #Removes the bullet
                    pygame.mixer.Sound.play(collision_sound) #Plays sound of comet 1 being hit
                    comet_startx1 = random.randint(0,width - comet_width) #Comet 1 position Resets at a random x position
                    comet_starty1 = 0 - comet_height #Comet 1 Resets at the top of the screen
                    score1 += 1 #Score is increased by one point
            if bullet[1] < comet_starty2 + comet_height: #Checks to see if the y value of the bullet is equal to the y value of comet 2             
                if bullet[0] > comet_startx2 and bullet[0] < comet_startx2 + comet_width: #Checks to see if the x value of the bullet is between the x values of comet 1
                    bullets.remove(bullet) #Removes the bullet
                    pygame.mixer.Sound.play(collision_sound) #Plays sound of comet 2 being hit
                    comet_startx2 = random.randint(0,width - comet_width) #Comet 2 position Resets at a random x value
                    comet_starty2 = 0 - comet_height #Comet 2 Resets at the top of the screen
                    score1 += 1 #Score is increased by one point
        #Logic for Single Player Mode                              
        if p1_mode == True:
            spaceship(x1,y1) #Draws Spaceship
            points(score1,675,5) #Draws Scoreboard
            if x1 == width - spaceship_width: #Collision Detection Wall
                highscore.append(score1) #Appends score to highscore list
                crash() #Runs Crash Screen  
            if x1 == 0: #Collision Detection Wall
                highscore.append(score1)#Appends score to highscore list
                crash() #Runs Crash Screen  
            if comet_starty1 > height: #Resets comet 1 Once Off the Screen
                comet_starty1 = 0 - comet_height
                comet_startx1 = random.randint(0,width - comet_width)
            if comet_starty2 > height: #Resets comet 2 Once Off the Screen
                comet_starty2 = 0 - comet_height
                comet_startx2 = random.randint(0,width - comet_width)
            if y1 < comet_starty1 + comet_height: #Collision Detection for comet 1 on Player
                if x1 > comet_startx1 and x1 < comet_startx1 + comet_width or x1 + spaceship_width > comet_startx1 and x1 + spaceship_width < comet_startx1 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if y1 < comet_starty2 + comet_height: #Collision Detection for comet 2 on Player
                if x1 > comet_startx2 and x1 < comet_startx2 + comet_width or x1 + spaceship_width > comet_startx2 and x1 + spaceship_width < comet_startx2 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if ufo_starty1 >= height: #Rests UFO 1 Once Off the Screen
                ufo_starty1 = -5000 #Resets y value
                ufo_startx1 = random.randint(0,width - ufo_width) #Resets x value
            if ufo_starty2 >= height: #Rests UFO 2 Once Off the Screen
                ufo_starty2 = -4000 #Resets y value
                ufo_startx2 = random.randint(0,width - ufo_width) #Resets x value
            if y1 < ufo_starty1 + ufo_height: #Collision Detection for UFO 1 on Player
                if x1 > ufo_startx1 and x1 < ufo_startx1 + ufo_width or x1 + spaceship_width > ufo_startx1 and x1 + spaceship_width < ufo_startx1 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if y1 < ufo_starty2 + ufo_height: #Collision Detection for UFO 2 on Player
                if x1 > ufo_startx2 and x1 < ufo_startx2 + ufo_width or x1 + spaceship_width > ufo_startx2 and x1 + spaceship_width < ufo_startx2 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
        #Logic For 2 Player Mode                                    
        if p2_mode == True:
            spaceship(x1,y1) #Draws Spaceship 1
            spaceship(x2,y2) #Draws Spaceship 2
            points(score1,675,5) #Draws Scoreboard 1 
            if x1 == width - spaceship_width: #Collision Detection with Wall
                highscore.append(score1)#Appends score to highscore list
                crash() #Runs Crash Screen  
            if x1 == 0: #Collision Detection with Wall
                highscore.append(score1)#Appends score to highscore list
                crash() #Runs Crash Screen  
            if x2 == width + spaceship_width: #Collision Detection with Wall
                highscore.append(score1)#Appends score to highscore list
                crash() #Runs Crash Screen  
            if x2 == 0: #Collision Detection with Wall
                highscore.append(score1)#Appends score to highscore list
                crash() #Runs Crash Screen            
            if comet_starty1 > height: #Resets comet 1 Once Off the Screen
                comet_starty1 = 0 - comet_height #Resets y value
                comet_startx1 = random.randint(0,width - comet_width) #Resets x value
            if comet_starty2 > height: #Resets comet 2 Once Off the Screen
                comet_starty2 = 0 - comet_height #Resets y value
                comet_startx2 = random.randint(0,width - comet_width) #Resets x value
                
            if y1 < comet_starty1 + comet_height: #Collision Detection for comet 1 on Player 1
                if x1 > comet_startx1 and x1 < comet_startx1 + comet_width or x1 + spaceship_width > comet_startx1 and x1 + spaceship_width < comet_startx1 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if y1 < comet_starty2 + comet_height: #Collision Detection for comet 2 on Player 1
                if x1 > comet_startx2 and x1 < comet_startx2 + comet_width or x1 + spaceship_width > comet_startx2 and x1 + spaceship_width < comet_startx2 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if y2 < comet_starty1 + comet_height: #Collision Detection for comet 1 on Player 2
                if x2 > comet_startx1 and x2 < comet_startx1 + comet_width or x2 + spaceship_width > comet_startx1 and x2 + spaceship_width < comet_startx1 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            if y2 < comet_starty2 + comet_height: #Collision Detection for comet 2 on Player 2
                if x2 > comet_startx2 and x2 < comet_startx2 + comet_width or x2 + spaceship_width > comet_startx2 and x2 + spaceship_width < comet_startx2 + comet_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
            
            if ufo_starty1 >= height: #Resets UFO 1 once off the screen
                ufo_starty1 = -5000 #Resets y value
                ufo_startx1 = random.randint(0,width - ufo_width) #Resets x value
            if ufo_starty2 >= height: #Resets UFO 2 once off the screen
                ufo_starty2 = -4000 #Resets y value
                ufo_startx2 = random.randint(0,width - ufo_width) #Resets x value
                
            if y1 < ufo_starty1 + ufo_height: #Collision Detection for UFO 1 on Player 1
                if x1 > ufo_startx1 and x1 < ufo_startx1 + ufo_width or x1 + spaceship_width > ufo_startx1 and x1 + spaceship_width < ufo_startx1 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen
            if y1 < ufo_starty2 + ufo_height: #Collision Detection for UFO 2 on Player 1
                if x1 > ufo_startx2 and x1 < ufo_startx2 + ufo_width or x1 + spaceship_width > ufo_startx2 and x1 + spaceship_width < ufo_startx2 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen                
            if y2 < ufo_starty1 + ufo_height: #Collision Detection for UFO 1 on Player 2
                if x2 > ufo_startx1 and x2 < ufo_startx1 + ufo_width or x2 + spaceship_width > ufo_startx1 and x2 + spaceship_width < ufo_startx1 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen
            if y2 < ufo_starty2 + ufo_height: #Collision Detection for UFO 2 on Player 2 
                if x2 > ufo_startx2 and x2 < ufo_startx2 + ufo_width or x2 + spaceship_width > ufo_startx2 and x2 + spaceship_width < ufo_startx2 + ufo_width:
                    highscore.append(score1)#Appends score to highscore list
                    crash() #Runs Crash Screen  
        #FPS Counter
        myfont = pygame.font.SysFont("monospace", 20) #Font for fps counter
        label = myfont.render("FPS", True, (255,255,0)) #Renders Text
        screen.blit(label, (0,0)) #Displays the text
        fps = myfont.render(str(int(fpsClock.get_fps())), True, colorYellow) #Renders FPS Counter
        screen.blit(fps,(45,0)) #Displays the FPS Counter to thne screen
            
#Main Loop, Exit and Update Commands
        pygame.display.update()
        fpsClock.tick(60)
    pygame.quit()
    sys.exit()
menu_loop()
