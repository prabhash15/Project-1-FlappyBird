import pygame 
import math
import sys
import random

pygame.init()
flap_sound = pygame.mixer.Sound('sounds/flap.mp3')
point_sound = pygame.mixer.Sound('sounds/point.mp3')
hit_sound = pygame.mixer.Sound('sounds/hit.mp3')
die_sound = pygame.mixer.Sound('sounds/die.mp3')


#Getting images , sound , background , objects 

win = pygame.display.set_mode((680,480))
bird = pygame.image.load("images/bird.png").convert_alpha()
background = pygame.image.load("images/cc.png").convert_alpha()
clock = pygame.time.Clock()
clouds = pygame.image.load("images/object1.png").convert_alpha()
pipe = pygame.image.load("images/longpipe2.png").convert_alpha()
pipe2 = pygame.image.load("images/longpipeopp.png").convert_alpha()
game_over_img = pygame.image.load("images/game-over.png").convert_alpha()
all_pipes = [pipe , pipe2]


score = 0
scorex = 10
scorey = 10
PP = False
font = pygame.font.Font('freesansbold.ttf', 32)
 
#Functions of the game 
bird_mask = pygame.mask.from_surface(bird)
pipe_mask = pygame.mask.from_surface(pipe)

def collision(bx, by, px, py, bird_mask, pipe_mask):
    offset = (px - bx, py - by)
    return bird_mask.overlap(pipe_mask, offset)

def flappy_bird_movement(x , y):
    win.blit(bird , (x,y))
    
def cloud(i ,x, y=100): 
    win.blit(i ,(x,y))
    
def object_movement(i ,x, y ,):
    win.blit(i, (x,y)) 
    
def gameover(score):
    while True:
        win.fill((0, 0, 0))
        win.blit(game_over_img , (150 , 75 ))
        final_score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        restart = font.render("'R' to Restart" , True , (255 , 0 , 0))
        win.blit(final_score_text, (270, 250))
        win.blit(restart , (225 , 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                 
def score1(score ,x,y): 
    text = font.render('Score: ' + str(score), True, (0,0,0))
    win.blit(text,(x, y))

# GAME LOOP 
def gameloop():

    # Movement of bird
    bird_x  = 300 
    bird_y =  200
    bird_ychangedefault  = 3
    bird_ychange = 3.5
    x= 0 
    y = 0

    #MOvement of clouds
    cloudx = 500 
    cloudy = 0 
    cloudchange = -0.9  

    #OBJECT movement meaning pipes

    obj2x = 750
    obj2y =  random.randint(-400,269 - 480)
    obj2change = -4

    objx = 750
    objy = obj2y + 575
    objchange = -4

    all_objects = [[objx , objy],[obj2x, obj2y]]

    score = 0
    scorex = 10
    scorey = 10
    PP = False
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    #Functions of the game 
    bird_mask = pygame.mask.from_surface(bird)
    pipe_mask = pygame.mask.from_surface(pipe)


    
    state = False
    RUN = True
    while RUN:
        state = False
        win.fill((0,0,0 ))
        win.blit(background , (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    flap_sound.play()
                    x = bird_y - 40
                    state = True
                    bird_ychange = -4
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        if x>bird_y:
                            bird_ychange = 4
        
            
        if x<bird_y or state == True:
            bird_y += bird_ychange
        else:
            x = 1000 
            bird_y += bird_ychangedefault


        if bird_y >= 450: 
            die_sound.play()
            r = gameover(score)
            if not r: 
                break
            else:
                bird_x  = 300 
                bird_y =  200
                bird_ychangedefault  = 3
                bird_ychange = 3.5
                x= 0 
                y = 0

                    #MOvement of clouds
                cloudx = 500 
                cloudy = 0 
                cloudchange = -0.9  

                    #OBJECT movement meaning pipes

                obj2x = 750
                obj2y =  random.randint(-300,269 - 480)
                obj2change = -4

                objx = 750
                objy = obj2y + 575
                objchange = -4

                all_objects = [[objx , objy],[obj2x, obj2y]]

                score = 0
                scorex = 10
                scorey = 10
                PP = False
                font = pygame.font.Font('freesansbold.ttf', 32)
                    
                    #Functions of the game 
                bird_mask = pygame.mask.from_surface(bird)
                pipe_mask = pygame.mask.from_surface(pipe)


        elif bird_y < -15: 
            bird_y = -15
            bird_ychange = 3.5
            
        # cloud movement change
        cloudx += cloudchange
        if cloudx < -150:
            cloudx = 850


        cloud(clouds , cloudx)
        flappy_bird_movement(bird_x , bird_y)
        
            
        all_objects[1][0] += obj2change
        all_objects[0][0] += objchange
        

        if all_objects[1][0] < -50:
            all_objects[1][0] = 750
            all_objects[1][1] = random.randint(-400, -150)  

        if all_objects[0][0] < -50:
            all_objects[0][0] = 750
            all_objects[0][1] = all_objects[1][1] + 575

            
        for i in range(2):
            object_movement(all_pipes[i], all_objects[i][0], all_objects[i][1])
            bird_rect = bird.get_rect(topleft=(bird_x, bird_y))
            pipe_rect = all_pipes[i].get_rect(topleft=(all_objects[i][0], all_objects[i][1]))
            if collision(bird_rect.left, bird_rect.top, pipe_rect.left, pipe_rect.top, bird_mask, pipe_mask):
                hit_sound.play()
                y = gameover(score)

                RUN = y

                if not RUN:
                    break
                else:
                    # Movement of bird
                    bird_x  = 300 
                    bird_y =  200
                    bird_ychangedefault  = 3
                    bird_ychange = 3.5
                    x= 0 
                    y = 0

                    #MOvement of clouds
                    cloudx = 500 
                    cloudy = 0 
                    cloudchange = -0.9  

                    #OBJECT movement meaning pipes

                    obj2x = 750
                    obj2y =  random.randint(-300,269 - 480)
                    obj2change = -4

                    objx = 750
                    objy = obj2y + 575
                    objchange = -4

                    all_objects = [[objx , objy],[obj2x, obj2y]]

                    score = 0
                    scorex = 10
                    scorey = 10
                    PP = False
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    
                    #Functions of the game 
                    bird_mask = pygame.mask.from_surface(bird)
                    pipe_mask = pygame.mask.from_surface(pipe)
                    break           
                
        if all_objects[0][0] > bird_x - 20:
            PP = True
        else: 
            PP = False 
            
        if all_objects[0][0] < bird_x - 15 and PP == True: 
            score += 1
            point_sound.play()
            
        score1(score ,scorex,scorey)
        pygame.display.flip()
        clock.tick(60)


gameloop()
 
