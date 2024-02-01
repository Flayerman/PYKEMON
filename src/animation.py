import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"sprites/{name}.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(12),
            'left': self.get_images(60),
            'right': self.get_images(108),
            'up': self.get_images(156)
        }
        self.speed = 2

    def change_animation(self, name):

        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(0,0)
        self.clock += self.speed * 8

        if self.clock >= 100:
            self.animation_index += 1
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0

    def get_images(self, y):
        images = []
        for i in range(0,4):
            x= i*32
            image = self.get_image(x,y)
            images.append(image)
        return images

    def get_image(self, x, y):
        # Permet de récupérer le bon morceau de l'image
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

