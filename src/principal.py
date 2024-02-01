import sys
import time
import pygame
from src.button import Button
from src.Game import Game
import vlc



def Menu():
    pygame.init()
    info = pygame.display.Info()
    SCREEN_HEIGHT = info.current_h
    SCREEN_WIDTH = info.current_w
    # SCREEN_HEIGHT = 800
    # SCREEN_WIDTH = 1000
    size = (SCREEN_WIDTH + SCREEN_WIDTH * 0.1, SCREEN_HEIGHT + SCREEN_HEIGHT * 0.1)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('Audio/titre.mp4')
    player.set_media(media)
    player.set_hwnd(pygame.display.get_wm_info()['window'])
    player.play()
    while player.get_state() != vlc.State.Ended:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                exit()
    player.stop()
    player.release()
    screen.fill((0, 0, 0))  # Remplit l'écran avec du noir (ou une autre couleur de fond)
    pygame.display.flip()  # Met à jour l'écran entier
    pygame.mixer.init()

    def set_timer_exit(second):
        time.sleep(second)
        pygame.quit()
        sys.exit()

    # Charger l'image de fond
    background = pygame.image.load('sprites/OIG.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH + 50, SCREEN_HEIGHT + 50))

    # Charger l'image et le son pour les btns
    start_img = pygame.image.load('sprites/start_btn.png')
    start_img_clic = pygame.image.load('sprites/start_btn_clic.png')
    exit_img = pygame.image.load('sprites/exit_btn.png')
    exit_img_clic = pygame.image.load('sprites/exit_btn_clic.png')
    clic_sound = pygame.mixer.Sound('Audio/sound2.wav')

    # Charger le son pour le menu
    pygame.mixer.music.load('Audio/open_song.mp3')
    pygame.mixer.music.play(-1)

    # Créer une instance de la classe Button
    bouton_play = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, start_img, 0.58)
    bouton_play_gris = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, start_img_clic, 0.58)
    bouton_exit = Button(SCREEN_WIDTH // 2 + ((start_img.get_width() - exit_img.get_width()) // 2) - 50, SCREEN_HEIGHT // 2, exit_img, 0.53)
    bouton_exit_gris = Button(SCREEN_WIDTH // 2 + ((start_img.get_width() - exit_img.get_width()) // 2) - 50, SCREEN_HEIGHT // 2, exit_img_clic, 0.53)

    current_state = "start"  # Initialiser l'état actuel à "start"
    current_state_exit = "exit" # Initialiser l'état actuel à "exit"
    clicked_time = 0  # Initialiser le temps de clic à 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_exit.rect.collidepoint(event.pos):
                    print("Le jeu est terminé !")
                    clic_sound.play()
                    current_state_exit = "exit_clicked"
                    set_timer_exit(0.5)
                elif bouton_play.rect.collidepoint(event.pos):
                    print('Le jeu commence!')
                    pygame.mixer.music.stop()
                    game = Game()
                    game.run()
                    clic_sound.play()
                    current_state = "start_clicked"  # Changer l'état actuel à "start_clicked"
                    clicked_time = time.time()  # Enregistrer le temps de clic

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('Le jeu commence!')
                    pygame.mixer.music.stop()
                    game = Game()
                    game.run()
                    clic_sound.play()
                    current_state = "start_clicked"  # Changer l'état actuel à "start_clicked"
                    clicked_time = time.time()  # Enregistrer le temps de clic

            # Logique pour détecter le survol et la sortie de la zone du bouton start
            if event.type == pygame.MOUSEMOTION:
                if bouton_play.rect.collidepoint(event.pos):
                    current_state = "start_survol"
                else:
                    current_state = "start"
            # Logique pour détecter le survol et la sortie de la zone du bouton exit
            if event.type == pygame.MOUSEMOTION:
                if bouton_exit.rect.collidepoint(event.pos):
                    current_state_exit = "exit_survol"
                else:
                    current_state_exit = "exit"
        # Dessiner l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le bouton start en fonction de l'état actuel
        if current_state == "start":
            bouton_play.draw(screen)
        elif current_state == "start_clicked":
            bouton_play_gris.draw(screen)
            # Prolonger la visibilité du bouton gris pendant 1.5 secondes après le clic
            if time.time() - clicked_time > 1.5:
                current_state = "start"
        elif current_state == "start_survol":
            bouton_play_gris.draw(screen)

        # Afficher le bouton exit en fonction de l'état actuel
        if current_state_exit == "exit":
            bouton_exit.draw(screen)
        elif current_state == "exit_clicked":
            bouton_exit_gris.draw(screen)
            # Prolonger la visibilité du bouton gris pendant 1.5 secondes après le clic
            if time.time() - clicked_time > 1.5:
                current_state_exit = "exit"  # Réinitialiser l'état actuel après 1.5 secondes
        elif current_state_exit == "exit_survol":
            bouton_exit_gris.draw(screen)

        pygame.display.flip()
        clock.tick(60)
