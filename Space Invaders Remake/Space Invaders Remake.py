#Louis Powis
#Space Invaders Remake

import pygame, time, random


def main():
    
    pygame.init()
    #Initialise the modules
    global clock
    clock = pygame.time.Clock()

    global bullets
    global invaders
    global invbullets
    bullets, invaders, invbullets = [], [], []

    size = width, height = 550, 400
    global BLACK
    BLACK = (0, 0, 0)

    global RED
    RED = (255, 0, 0)

    global BLUE
    BLUE = (0, 0, 255)
    #Colours and window width and height

    global screen
    screen = pygame.display.set_mode(size)
    screen.fill(BLACK)
    pygame.display.set_caption('Space Invaders Remake')
    #Caption for the window

    startbutton = pygame.Rect(150, 160, 250, 50)
    pygame.draw.rect(screen, [255, 0, 0], startbutton)

    quitbutton = pygame.Rect(150, 250, 250, 50)
    pygame.draw.rect(screen, [255, 0, 0], quitbutton)
    #The start and quit buttons for the main menu

    font = pygame.font.SysFont("Arial", 34)
    titletxt = font.render("Welcome to Space Invaders Remake", 1 ,(255,0,0))
    screen.blit(titletxt, (40,85))

    starttxt = font.render("Start", 1, (0,0,0))
    screen.blit(starttxt, (235,165))

    quittxt= font.render("Quit", 1 , (0, 0, 0,))
    screen.blit(quittxt, (240,255))

    pygame.display.update()

    global lives
    global player
    font = pygame.font.SysFont("Arial", 20)
    lives = font.render("Lives:", 1, (255,0,0))
    player = pygame.Rect(260, 350, 30, 10)  
    #Text for lives, player's starting position and size


    while True:
        pygame.event.get()
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if startbutton.collidepoint(mouse_pos):
                    print('startbutton was pressed at {0}'.format(mouse_pos))
                    gameStart() 
                    return
                    #If the player presses the start button start the game
                    
                    

                if quitbutton.collidepoint(mouse_pos):
                    print('quitbutton was pressed at {0}'.format(mouse_pos))
                    pygame.quit()
                    quit()
                    #If the player presses the quit button quit the game        


def gameStart():
    
    forward = False
    backward = False

    pbulletcooldown = time.time()
    #Player's bullet cool down time
    ibulletcooldown = time.time()
    #Invader's bullet cool down time

    invx = time.time()
    invy = time.time() + 0.5
    conx = -5
    #Consecutive x movements

    global score
    score = 0

    global scoretxt

    difficulty = 975
    #1 is hard
    #1000 is easy
    #This variable is used at the start of the function so as that the player does not have to scroll down and look through the while loop each time

    global lifecount
    lifecount = 3
    #The player starts with 3 lives
    
    for x in range (100, 450, 20):
        for y in range (100, 200, 15):
            invaders.append(pygame.Rect(x, y, 15, 10))
            #Sets the range for the invaders
            #Sets the width, height, and distance between each invader
            
    while True:
        clock.tick(100)
        #Wait 100ms before running the loop again
        for event in pygame.event.get():
            
            keypress = pygame.key.get_pressed()
            if keypress[pygame.K_ESCAPE]:
                    pygame.quit()
                    quit()
                    #This is so the user can quit the program during the game by pressing the escape key
            
            if event.type == pygame.KEYDOWN:
                #Runs this part of the loop as long as a key is being held down

                if keypress[pygame.K_SPACE] and (time.time() - pbulletcooldown > 0.5):
                    pbulletcooldown = time.time()
                    #This is used to prevent spamming the bullets
                    bullets.append(player.copy())
        
                if event.key == pygame.K_LEFT:
                    backward = True
                    print(player.x)
                    #Left arrow key
                if event.key == pygame.K_RIGHT:
                    forward = True
                    print(player.x)
                    #Right arrow key

                    

            if event.type == pygame.KEYUP:
                #Runs this part of the loop if keys are no longer being pressed
                if event.key == pygame.K_LEFT:
                    backward = False
                    print('the left key works')
                    #Left arrow key
                if event.key == pygame.K_RIGHT:
                    forward = False
                    print('the right key works')
                    #Right arrow key

            
        if backward == True and player.x >=0:
            player.move_ip(-2, 0)

            
        if forward == True and player.x <=520:
            player.move_ip(2, 0)


        #These are used so as that the player is not moved once per keypress but will continue to move until the boolean is false
        #This also keeps the player within the screen

        for invader in invaders:
            if invader.colliderect(player):
                del invaders[:]
                del invbullets[:]
                del bullets[:]
                gameOver()
                return

        for bullet in bullets:
            bullet.move_ip((0, -4))
            #The speed at which the bullet moves
            if not screen.get_rect().contains(bullet):
                bullets.remove(bullet)
                print('removed')
                #If the bullet is no longer inside the screen then remove the bullet from the list
            else:
                hit = False
                for invader in invaders:
                    if invader.colliderect(bullet):
                        score += 20
                        print("score is acknowledged")
                        #Each invader hit is worth 20 points
                        i = invaders.index(invader)
                        del invaders [i]
                        #Delete the specific invader that was hit from the list
                        hit = True
                if hit:
                    bullets.remove(bullet)
                    if not invaders:
                        scoretxt = font.render("Score: "+str(score), 1, (RED))
                        del invaders[:]
                        del invbullets[:]
                        del bullets[:]
                        gameOver()
                        print("gameOver")
                        return
                        #If there are no more invaders in the list then display the game over screen and stop the loop

        if (time.time() - invx > 0.5):
            invx = time.time()
            #Runs this part of the loop if the time passed has been 1 second
            
                
            if (conx > 0 and conx < 5) or conx == -5:
                    for invader in invaders:
                        invader.move_ip(4, 0)
                    if conx < 0:
                        conx = 1
                    else:
                        conx += 1
                        
            elif (conx < 0 and conx > -5) or conx == 5:
                    for invader in invaders:
                        invader.move_ip(-4, 0)
                    if conx > 0:
                        conx = -1
                    else:
                        conx -= 1

            #conx starts on -5
            #It runs the first if statement because conx is -5 but then it gets set to 1 as it is less than 0 and it then has 1 added to it until it equals 5
            #It now meets the requirements of the second if statement as it is now equal to 5 but then it gets set to -1 as it is greater than 0 and and it then has 1 subtracted from it until it equals -5
            #The first part of the if statement for each makes sure when adding/subtracting that the conx value is still within 0 and 5/ 0 and -5

        if (time.time() - invy > 2.5):
            invy = time.time()
        #Runs this part of the loop if the time passed has been 5 seconds
            
            for invader in invaders:
                invader.move_ip(0, 4)

        if (time.time() - ibulletcooldown > 1):
            #Wait 1 second before the invaders can fire again
            for invader in invaders:
              if random.randint(1, 1000) > difficulty:
                  #All of the invaders in the list run this loop, therefore the higher the difficulty value fewer will fire at once, whereas the lower the difficulty value more will fire at once
                  ibulletcooldown = time.time()
                  invbullets.append(invader.copy())
                  print('invbullets')
                
        for invbullet in invbullets:
            invbullet.move_ip((0, 3))
            if not screen.get_rect().contains(invbullet):
                invbullets.remove(invbullet)
                #removes the invader's bullet if it is no longer inside the screen
                print('invbullet removed')
            if player.colliderect(invbullet):
                lifecount -= 1
                i = invbullets.index(invbullet)
                del invbullets [i]
                #If the player is hit by a invader's bullet then they lose a life
                
        font = pygame.font.SysFont("Arial", 34)
        scoretxt = font.render("Score: "+str(score), 1, (RED))
 
        screen.fill(BLACK)
        screen.blit(scoretxt, (50, 20))
        pygame.draw.rect(screen, RED, player)
        
        screen.blit(lives, (375, 30))
        

        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)

        for invader in invaders:
            pygame.draw.rect(screen, BLUE, invader)

        for invbullet in invbullets:
            pygame.draw.rect(screen, BLUE, invbullet)
            

        if lifecount == 3:
            triangle1 = pygame.draw.polygon(screen, (255, 0, 0), [[520, 50], [510,25], [500,50]],  0)
            triangle2 = pygame.draw.polygon(screen, (255, 0, 0), [[490, 50], [480,25], [470,50]],  0)
            triangle3 = pygame.draw.polygon(screen, (255, 0, 0), [[460, 50], [450,25], [440,50]],  0)
            #The triangle 1, 2, 3 represent the lives the player has

        if lifecount == 2:
            triangle2 = pygame.draw.polygon(screen, (255, 0, 0), [[460, 50], [450,25], [440,50]],  0)
            triangle3 = pygame.draw.polygon(screen, (255, 0, 0), [[490, 50], [480,25], [470,50]],  0)

        if lifecount == 1:
            triangle3 = pygame.draw.polygon(screen, (255, 0, 0), [[460, 50], [450,25], [440,50]],  0)

        if lifecount == 0:
            del invaders[:]
            del invbullets[:]
            del bullets[:]
            #If i did not delete the invaders then two instances of them would be drawn at once making each invader merge and the drawing to be wrong
            gameOver()
            return
            
        
        pygame.display.update()
        #updates the surface

def gameOver():
    
    screen.fill(BLACK)

    restartbutton = pygame.Rect(150, 180, 250, 50)
    pygame.draw.rect(screen, RED, restartbutton) 

    quitbutton = pygame.Rect(150, 250, 250, 50)
    pygame.draw.rect(screen, RED, quitbutton)
    #The restart and quit buttons for the game over screen
    
    font = pygame.font.SysFont("Arial", 34)

    gameOvertxt = font.render("Game Over", 1, (RED))
    screen.blit(gameOvertxt, (200, 40))

    screen.blit(scoretxt, (197, 100))

    restarttxt = font.render("Restart", 1, (BLACK))
    screen.blit(restarttxt, (225, 185))
    
    quittxt = font.render("Quit", 1, (BLACK))
    screen.blit(quittxt, (240, 255))

    pygame.display.update()    

    
    while True:
        pygame.event.get()
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if restartbutton.collidepoint(mouse_pos):
                    gameStart()
                    return
                #If the player presses the restart button, restart the game
                    

                if quitbutton.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()
                #If the player presses the quit button, quit the game
        

if __name__=='__main__':
    main()
