import pygame
import time
import math
from pygame import mixer
import random
import os

############################ Global################################
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
# SMALL_CACTUS = pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png"))
# LARGE_CACTUS = pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png"))
frame1=pygame.transform.scale(pygame.image.load('ghoul1.png'),(150,150))
frame2=pygame.transform.scale(pygame.image.load('ghoul2.png'),(150,150))
RUNNING=[frame1,frame2]


BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

############################ Setting up the player ########################################

class Player(pygame.sprite.Sprite):
    global frame1, frame2

    def __init__(self):
        super().__init__()
        self.x_pos=100
        self.y_pos=400
        self.frame1=frame1
        self.frame2=frame2
        self.image_list=[frame1,frame2]    # Storing scaled images in a 2D list
        self.current_image=0
        self.frame_counter=0
        self.frame_speed=5
        self.image=self.image_list[self.current_image]
        self.rect=self.image.get_rect()
        self.rect.center=[self.x_pos, self.y_pos]
        self.jump_vel=8.5
        self.jump=False
    
    def GetY_Pos(self):    # returns the current y coordiate of the player
        return self.y_pos
    
    def Get_Initial_Y_Pos(self):
        return 400
    
    def SetY_Pos(self, y_pos):     # sets the new y coordinate when the character jumps
        self.y_pos = y_pos
        self.rect.center=[self.x_pos, y_pos]

    def change_image(self):   # Changes between frames 
        self.frame_counter+=1
        if self.frame_counter>=self.frame_speed:
            self.frame_counter=0
            self.current_image=(self.current_image+1) % (len(self.image_list))
            self.image=self.image_list[self.current_image]

    def jump(self):
        if self.jump:
            self.y_pos -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - 8.5:
            self.jump = False
            self.jump_vel = 8.5
        
############################ Initializing sprite group ##########################################################

pygame.init()        
timer=pygame.time.Clock()
player_group=pygame.sprite.Group()
ghoul=Player()
player_group.add(ghoul)

############################## Background intializtion #########################################################

width=1100
height=600
screen=pygame.display.set_caption('Ghoul Dash') 
screen=pygame.display.set_mode((width,height))
timer=pygame.time.Clock()
frame_rate = 60
game_clock = pygame.time.Clock()
win_width, win_height = 1100, 600
background_image = pygame.image.load("BG_C.png").convert()
bg_scaled = pygame.transform.scale(background_image,(win_width,win_height)) # Scaling the background image
bg_img_width = bg_scaled.get_width()
bg_image_rect = bg_scaled.get_rect()
scroll_speed = 100
num_tiles = math.ceil(win_width / bg_img_width) + 1

################################ Function for adding the jumping sound effect ###################################
def Sound_Effect():
    mixer.init()
    mixer.music.load('Jump_sound.mp3') 
    mixer.music.set_volume(0.5)
    mixer.music.play()

##############################Obstacles##############################################################
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            return True
        return False

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 375

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

############################## Main game loop / Runs the game ###################################################
def main():
    global points, obstacles, death_count, vel, game_speed
    vel=300
    jump=False
    game_speed=20
    jump_count=0
    # jump_height=300
    # game_time=0
    # gravity=200
    obstacles=[]
    points=0
    run=True
    clock = pygame.time.Clock()
    death_count=0
    a= -250/156.25

    def score():
        global points, vel
        points += 1
        if points % 100 == 0:
            vel += 1
        font = pygame.font.Font('freesansbold.ttf', 20)

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)
        pygame.display.update()

    def Move_BG():
        global frame_rate, game_clock, win_width, win_height, bg_scaled, bg_img_width, bg_image_rect, scroll_speed, num_tiles
        game_clock.tick(frame_rate)
        for tile in range(num_tiles):
            x_position = (tile * bg_img_width) - (scroll_speed % bg_img_width)
            screen.blit(bg_scaled, (x_position, 0))
        scroll_speed += 10

    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        screen.fill((50,100,160))
        key=pygame.key.get_pressed()  # Returns dictionary consisting of keyboard input 

        if key[pygame.K_SPACE]:
            jump=True
            jump_count=25
        
        if jump:
            if jump_count <= 1:
                jump=False
                ghoul.SetY_Pos(ghoul.Get_Initial_Y_Pos())
            else:
                ghoul.SetY_Pos(ghoul.Get_Initial_Y_Pos()-((a*jump_count*jump_count)-(25*a*jump_count)))
                jump_count-=1

        Move_BG()
        player_group.draw(screen) # Drawing the character on the screen
        # ghoul.change_image()  # Calls the function to change frames for the character
        pygame.display.update() # Updating the changes on the screen

        if len(obstacles) == 0:
            rand_num = random.randint(0, 2)
            if rand_num == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand_num == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand_num == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            # if not obstacle_active:
            obstacle.draw(screen)
            obstacle.update()
            pygame.display.update()
            if ghoul.rect.colliderect(obstacle.rect):
                # pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
            # pygame.time.delay(2000)

        # Move_BG() # Calls the function moving background 

        score()

        clock.tick(30)

        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (width // 2, height // 2 + 50)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.blit(text, textRect)
        screen.blit(RUNNING[0], (width // 2 - 20, height // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

# death_count=0
menu(0)
# main()

pygame.quit()