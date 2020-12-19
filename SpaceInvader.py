import pygame
import random
import math
from pygame.locals import*
# sys gives us access to system modules

pygame.init()#initiates pygame

#creating the variable for the display screen
screen = pygame.display.set_mode((800,600))# here we created a screen with a widht of 800 pixels and a hieght of 600 pixels
# the dimensions of the screen could be anything you want
#Title and Icon
pygame.display.set_caption("Space Invader") #this changes the window title

#Background Image
background = pygame.image.load("space.png")

#setting the icon for the window
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("player.png")
#setting the x and y coordinates of the player, these are dependent on the screen size that we have initialised
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range (6):
    enemyImg.append(pygame.image.load("alien.png"))
    #setting the x and y coordinates of the enemy, these are dependent on the screen size that we have initialised
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

#Bullet
#ready state for the bullet means you cant see the bullet on the screen
#fire state for the bullet means that the bullet can be seen on the screen
bulletImg = pygame.image.load("bullet.png")
#setting the x and y coordinates of the bullets, these are dependent on the screen size that we have initialised
bulletX = 0 #the bullet will be shot from the x coordinate that the player is at, so we do not need to keep a predetermined x-coordinate for the bullet.
bulletY = 480 #the bullet will be shot from the player, and the player has a constant y coordinate, so we can predetermine the y-value of the coordinate.
bulletX_change = 0 #no change in the horizontal position of the bullet
bulletY_change = .9 #speed that the bullet will go up with
bullet_state = "ready"

#Score
score_value = 0
#will display the score using the pygame font object
font = pygame.font.Font('Schofield.ttf', 32) #pygame only has one free font, which is freesansbold.ttf. We have installed a new font off of dafont, and entered the name and size (32).
#decide the coordinates of where you want to display you text
textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font("Schofield.ttf", 64)

def showscore(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255)) #here, we have used a new method of displaying on the screen
    # We are rendering the score, and then blitting the score object that we have just created
    screen.blit(score, (textX, textY))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255)) #here, we have used a new method of displaying on the screen
    screen.blit(over_text, (250, 250))

#we are creating this function so that we can create the player on the screen when the game starts
def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

#in this function, we are telling the program, wether a bullet shot by the player is on the screen or not.
#because this function is called for shooting a bullet, it will set te state of the bullet to fire, because the bullet will be fired aftercalling this function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #the x + 16 and y + 10 make the bullet appear on the center of our spaceship

#in this function we are checking if two objects are colliding or not.
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2)) + (math.pow((enemyY-bulletY),2))) #finding the distance betweeen the bullet and the alien using the distance formula (analytic geometry)
    #we think 27 is a reasonable distance, so if the distance between the two is less than 27, we say they are hit, and return treu, else we return false
    if distance < 27:
        return True
    else:
        return False
    
#game loop
running = True # turning this into false will allow us to quit the while loop
while running:
    
    #fill screen color has to be enter in RGB format, R, G, B
    screen.fill((0,0,0))#we are setting the color of the screen

    #background image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #pressing a key is an event in pygame, so, we will put this block of code inside the event collector loop
        if event.type == pygame.KEYDOWN:#KEYDOWN means that the key has been pressed
            if event.key == pygame.K_LEFT:#left pressed
                playerX_change = -.3#when we press left, we want the x value to decrease by .3
            if event.key == pygame.K_RIGHT:#right pressed
                playerX_change = .3#when we press right, we want the x value to increase by .3
            if event.key == pygame.K_SPACE:#if the player is holding down space
                if bullet_state is "ready":#this makes it so that the fire_bullet function is only called when a bullet shot by the player is not seen on the screen
                    bulletX = playerX
                    #method call to fire a bullet
                    fire_bullet(playerX, bulletY)
                
        if event.type == pygame.KEYUP:#KEYUP means that the key has been released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:#left or right released
                playerX_change = 0#when the key is released, we dont want the x value to change
                
    playerX += playerX_change#setting the x coordinate of the playe

    #preventing the player going beyond the windows border
    if playerX < 0:#if the ship goes too left, we will place it at the left border
        playerX = 0
    elif playerX > 736:#if the ship goes too right, we will place it 64 pixels away from the right border. We have to place it 64 pixels away because we have to keep in mind the dimensions of the ship
        playerX = 736

    #Enemy Movement

    for i in range(6):
        #Game Over
        if enemyY[i] > 440:
            for j in range(6):
                enemyY[j] = 2000
            game_over_text()
            break;
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY) #to check if the collision has occured or not
        if collision: #if the collision has occured
            #return bullet to original y coordinate
            #set bullet state to ready so that it can be fired again
            #add to the hit counter
            #if the hit reaches 2, the alien dies, a new alien respawns, the score is incremented, hit is set to 0 again
            bulletY = 480 
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
            enemy(enemyX[i], enemyY[i], i)
        #calling the function to initialize the enemy at the coordinates
        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0:#this is when the bullet reaches the top of the screen
        bulletY = 480 #the bullet is sent back to the space ship
        bullet_state = "ready" #the status of the bullet is set to ready so that the bullet can be fired again. Reaching the top of the screen means that the bullet is off of the screen.
    if bullet_state is "fire": #if the bullet has already been fired
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change #gives the bullet a vertical translation

    
            
        
    #calling the function to initialize the player at the coordinates
    player(playerX, playerY)
    showscore(textX, textY) #we have to call the function that showcases the score in the while loop to update it
    
    #update the display for any changes made in the game loop
    pygame.display.update()

pygame.quit()
