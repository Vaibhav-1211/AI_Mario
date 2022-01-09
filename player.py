import pygame,sys
from pygame.display import update
from support import import_folder
pygame.init()

screen_height = 704
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
game_font = pygame.font.Font("freesansbold.ttf", 100)

class Player(pygame.sprite.Sprite): #Simple base class for visible game objects.
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 # one of the animation
        self.animation_speed = 0.15 # animation speed update
        self.image = self.animations['idle'][self.frame_index]# list of animation
        self.rect = self.image.get_rect(topleft=pos)


        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0) #x,y
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16 # negative for jump up
        self.pos = 0

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('./graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed # speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False) #x,y
            self.image = flipped_image

        # # set the rect
        # if self.on_ground and self.on_right:
        #     self.rect = self.image.get_rect(bottomright=self.rect.bottomright) #to create a rectangle for the Surface centered at a given position.
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        # elif self.on_ground:
        #     self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # elif self.on_ceiling and self.on_right:
        #     self.rect = self.image.get_rect(topright=self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #     self.rect = self.image.get_rect(topleft=self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop=self.rect.midtop)

        

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                #spot the dust toleft becauserunning right
                #vector for displaying the dust a bit up as set by the x,y
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10) 
                self.display_surface.blit(dust_particle, pos) # draw the dust with pos
            else:
                # spot the dust to left because running right
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.pos += 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.pos -= 1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

        

    #create new fun GAT
    def ply_mov(self):
        endpoint = 459
        going = False
    
        if (self.pos//4) <= endpoint:
            going = True
            self.direction.x = 1
            self.pos += 1
            

        else:
            self.direction.x = 0
            going = False
        
        if (self.pos//4) >= endpoint or going == False:
            game_over = game_font.render(" AI WON", True, (255, 255, 255))
            #background1 = pygame.image.load('graphics/back.png')
            #screen.blit(background1,(0,0))
            screen.blit(game_over, (screen_width/2-200 ,screen_height/2-50))

            def quit(x, y):
                IntroFont = pygame.font.Font("freesansbold.ttf", 25)
                quittext = IntroFont.render("QUIT", True, (255, 255, 255))
                screen.blit(quittext, (x, y))
            quit(screen_width/2-30,screen_height/2+100)
            x, y = pygame.mouse.get_pos()
            btn = pygame.Rect(screen_width/2-60,screen_height/2+60,130,100)
            pygame.draw.rect(screen, (255, 255, 255), btn, 3)
            if btn.collidepoint(x, y):    
                pygame.draw.rect(screen, (238, 69, 52), btn, 5)

            for event in pygame.event.get():
                 if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if btn.collidepoint(x,y):
                            pygame.quit()
                            sys.exit()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
       
        print(self.pos//4, self.direction.x)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed 

    def update(self):
        #self.get_input()
        self.ply_mov()
        self.get_status()
        self.animate()
        self.run_dust_animation()


