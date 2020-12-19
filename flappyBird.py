import pygame, sys
# sys gives us access to system modules

pygame.init()#initiates pygame

#creating the variable for the display screen
screen = pygame.display.set_mode((576,1024))# here we created a screen with a widht of 576 pixels and a hieght of 1024 pixels
# the dimensions of the screen could be anything you want
clock =  pygame.time.Clock()#clock object will help us set the frame rate of the screen

bg_surface = pygame.image.load('assets\backgroud-day.png')#image that you want to load onto your surface

while True:
    for event in pygame.event.get():# for loop that catches events, these events could be key clicks, window exits, or timers
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit() #closes the program entirely, by making the program quit the while loop
    screen.blit(bg-surface,(288,512))#method to put a defined image onto the surface, .blit(nameofimage,(x,y)), the x and y coordinates are the coordianates of the top left surface of the image
    pygame.display.update()#updates a portion of the screen, whatever you draw in this loop, this method draws it on the display surface
    clock.tick(120)#setting the frame rate of the screen to 120
pygame.quit()
