import pygame


class Projectile(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.velocity = 10
        self.image = pygame.image.load('Battleanimations/ballBurst_diamond.png')
        self.image = pygame.transform.scale(self.image,(300,300))
        self.rect = self.image.get_rect()
        self.rect.x = 400 #position de tes projectiles
        self.rect.y = 400
       
    def move(self):

        self.rect.y -=self.velocity#depalcement de tes projectiles
        self.rect.x += self.velocity
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.all_projectiles=pygame.sprite.Group()
    def launch_projectile(self):# chargement des projectiles
     self.all_projectiles.add(Projectile())
