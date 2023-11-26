
import pygame
import time
import math
from pygame import mixer


############################ Setting up the player ########################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos=100
        self.y_pos=400
        frame1=pygame.transform.scale(pygame.image.load('ghoul1.png'),(150,150))
        frame2=pygame.transform.scale(pygame.image.load('ghoul2.png'),(150,150))
        self.image_lst=[frame1,frame2]    # Storing scaled images in a 2D list
        self.current_image=0
        self.frame_counter=0
        self.frame_speed=5
        self.image=self.image_lst[self.current_image]
        self.rect=self.image.get_rect()
        self.rect.center=[self.x_pos,self.y_pos]
    
    def GetY_Pos(self):    # returns the current y coordiate of the player
        return self.y_pos
    
    def Get_Initial_Y_Pos(self):
        return 400
    
    def SetY_Pos(self,give_y_pos):     # sets the new y coordinate when the character jumps
        self.rect.center=[self.x_pos,give_y_pos]


    def change_image(self):   # Changes between frames 
        self.frame_counter+=1
        if self.frame_counter>=self.frame_speed:
            self.frame_counter=0
            self.current_image=(self.current_image+1) % (len(self.image_lst))
            self.image=self.image_lst[self.current_image]
        
############################ Initializing sprite group ##########################################################

pygame.init()        
timer=pygame.time.Clock()
player_group=pygame.sprite.Group()
ghoul=Player()
player_group.add(ghoul)

############################## Background intializtion #########################################################

width=600
height=600
screen=pygame.display.set_caption('Ghoul Dash') 
screen=pygame.display.set_mode((width,height))
timer=pygame.time.Clock()
frame_rate = 60
game_clock = pygame.time.Clock()
win_width, win_height = 600, 600
background_image = pygame.image.load("BG_C.png").convert()
bg_scaled = pygame.transform.scale(background_image,(win_width,win_height)) # Scaling the background image
bg_img_width = bg_scaled.get_width()
bg_image_rect = bg_scaled.get_rect()
scroll_speed = 100
num_tiles = math.ceil(win_width / bg_img_width) + 1

##################################### Function for moving the background ########################################

def Move_BG():
    global frame_rate, game_clock,win_width,win_height,bg_scaled,bg_img_width,bg_image_rect,scroll_speed,num_tiles
    game_clock.tick(frame_rate)   
    for tile in range(num_tiles):
        x_position = tile * bg_img_width - scroll_speed
        screen.blit(bg_scaled, (x_position, 0))
        bg_image_rect.x = x_position
        pygame.draw.rect(screen, (0, 0, 0), bg_image_rect, 1)
    scroll_speed += 5
    if scroll_speed > bg_img_width:
        scroll_speed = 0

################################ Function for adding the jumping sound effect ###################################

def Sound_Effect():
    mixer.init()
    mixer.music.load('Jump_sound.mp3') 
    mixer.music.set_volume(0.5)
    mixer.music.play()

############################## Main game loop / Runs the game ###################################################

vel=300
jump=True
game_time=0
gravity=0.5

run=True
while run:
    screen.fill((50,100,160))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    key=pygame.key.get_pressed()  # Returns dictionary consisting of keyboard input 
    if jump:
        if key[pygame.K_SPACE]:
            Sound_Effect()  # Calls the sound effect function when "space" is pressed and activates jump
            jump=False     
    else:
        if jump_count>=-10:
            neg=1
            if jump_count<0:
                neg=-1
            ghoul_y=ghoul.GetY_Pos()
            jump_height=jump_height*0.5
            ghoul_y+=400-(vel*game_time)+(0.5*gravity*game_time**2)
            ghoul.SetY_Pos(ghoul_y)
            jump_count-=1
        else:
            ghoul_y=ghoul.Get_Initial_Y_Pos()
            jump=True 
            jump_count=10


    Move_BG() # Calls the function moving background 
    ghoul.change_image()  # Calls the function to change frames for the character
    player_group.draw(screen) # Drawing the character on the screen
    pygame.display.update() # Updating the changes on the screen

pygame.quit()
