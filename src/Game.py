import pygame
from src.Player import Player
from src.map import MapManager

pygame.init()
pygame.mixer.init()  # Initialiser le module mixer
pygame.mixer.music.load('Audio/Title.ogg')  # Charger la musique de fond

class Game:
    def __init__(self):
        # Creer la fenetre du jeu
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Pygamon - Aventure")

        # Jouer la musique en boucle indéfinie
        pygame.mixer.init()  # Initialiser le module mixer
        pygame.mixer.music.load('Audio/Title.ogg')  # Charger la musique de fond
        pygame.mixer.music.play(-1)

        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()
        # Boucle du jeu
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.mixer.music.stop()
        pygame.quit()