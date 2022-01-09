import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()#super give access to methods and properties of a parent or sibling class. and also for both single and ultiple inheritance
        self.image = pygame.Surface((size, size)) #draw image for the tile 
        
        self.image.fill(('grey'))
        self.rect = self.image.get_rect(topleft=pos) #positoin for the tile

    def update(self, x_shift):
        self.rect.x += x_shift #to store and manipulate rectangular areas
