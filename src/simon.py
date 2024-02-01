"""
Fichier python contenant la classe SimonGame. Gère le jeu Simon via le module pygame. En cas de défaite, retourne au menu principal.

Auteur : Dylan Peltier
Date : 17/01/2024
Version : 1.0

fonctions A-Z:
    add_random_to_sequence() : Ajoute un bouton aléatoire à la séquence.
    bot_attack() : Attaque du bot.
    check_sequence() : Vérifie la séquence.
    create_buttons() : Crée les boutons du jeu Simon.
    define_types() : Définit les types utilisés dans le jeu Simon.
    draw_all() : Affiche tout le jeu Simon.
    draw_buttons(reverse=False) : Affiche les boutons du jeu Simon.
    draw_background() : Affiche le fond du jeu Simon.
    draw_health_bar(surface, x, y, health, max_health) : Affiche les barres de vie des pokemons actifs.
    draw_interfaces() : Affiche les interfaces du jeu Simon.
    draw_pokeballs(pokemons, team) : Affiche les pokeballs des pokemons.
    draw_pokemon_active(owner) : Affiche les pokemons actifs.
    end(resultat) : Gère la fin du jeu.
    find_next_pokemon_alive(team) : Recherche le prochain pokemon vivant.
    flash_button(index) : Flash le bouton.
    get_dominant_color(image_path) : Récupère la couleur dominante d'une image.
    handle_damage(max_stage, pokemon) : Gère les dégâts.
    handle_end_sequence() : Gère la fin de la séquence.
    handle_health(damage, pokemon, team) : Gère la vie du pokemon.
    handle_mouse_click(position) : Gère le clic de la souris.
    load_image(image_path) : Charge une image.
    load_images() : Charge les images du jeu Simon.
    load_pokemon_sprite(ennemy_active_pokemon, me_active_pokemon) : Charge les sprites des pokemons actifs.
    show_sequence() : Affiche la séquence.
    show_text(text) : Affiche le texte.
    start_game() : Démarre le jeu Simon.
    update_pokemon_status(team, pokemon_active) : Met à jour le statut du pokemon.
"""

##############################################################################################################
# Imports modules python
import math
from PIL import Image
import pygame
import random
import sys
##############################################################################################################
# Imports modules locaux
from src.api import Type, Team

##############################################################################################################
# Initialisation
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
##############################################################################################################
# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
# SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
IMAGE_CENTER = "Battleanimations/ballBurst_dazzle.png"
IMAGE_BACKGROUND = "Battlebacks/rocky_bg.png"
PLATFORM = "Battlebacks/rocky_eve_base1.png"
LIFE_BAR_ME = "Battle/databox_thin_foe.png"
LIFE_BAR_ENNEMY = "Battle/databox_thin.png"
POKEBALLS_ALIVE = "Battle/icon_ball.png"
POKEBALLS_DEAD = "Battle/icon_ball_faint.png"
MESSAGE_BOX = "Battle/overlay_message.png"
FONT = pygame.font.Font("font/PokemonGb-RAeo.ttf", 18)
BLACK_COLOR = (0, 0, 0)
SOUND_CLICK = pygame.mixer.Sound("Audio/pokemon-a-button.mp3")
# SOUND_BATTLE = pygame.mixer.Sound("Audio/1-15. Battle (Vs. Trainer).mp3")
GAME_OVER = "Battle/game_over.png"
ATTACK_EFFECT = "Battleanimations/ballBurst_diamond.png"
VELOCITY = 10
PROJECTILE = 'Battleanimations/ballBurst_diamond.png'
AUDIO_PROJECTILE = pygame.mixer.Sound('Audio/Battle_damage_normal.ogg')
# BOUTON_CHANGE = 'sprites/change_pokemon.png'
# BOUTON_CHANGE_CLIC = 'sprites/change_pokemon_clicked.png'

##############################################################################################################

class SimonGame():
    def __init__(self, team_me, team_ennemy):
        # SOUND_BATTLE.play()
        self.team_me = team_me
        self.team_ennemy = team_ennemy
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.types = self.define_types()
        self.buttons = []
        self.sequence = []
        self.active_pokemon_me = None
        self.active_pokemon_ennemy = None
        self.position_me = None
        self.position_ennemy = None
        self.create_buttons()

    def define_types(self):
        # print("Définition des types...")
        """
        Définit les types utilisés dans le jeu Simon.

        Retourne :
            types (list) : Liste des types utilisés dans le jeu Simon.
        """
        used = []
        types = []
        while len(types) < 5:
            id_type = random.randint(37, 54)
            type = Type.get_type_by_id(id_type)
            if id_type not in used:
                used.append(id_type)
                types.append(type)

        # print("Types définis.")
        return types
    
    def get_dominant_color(self, image_path):
        # print("Récupération de la couleur dominante...")
        """
        Récupère la couleur dominante d'une image.

        Paramètres :
            image_path (str) : Chemin vers l'image.

        Retourne :
            dominant_color (tuple) : Couleur dominante de l'image.
        """
        try:
            image = Image.open(image_path)
            image = image.convert('RGBA')
            non_transparent_colors = []
            for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
                if a != 0:
                    non_transparent_colors.append((count, (r, g, b)))
            non_transparent_colors.sort(reverse=True)
            dominant_color = non_transparent_colors[0][1] if non_transparent_colors else (0, 0, 0)
            # print("Couleur dominante récupérée.")
            return dominant_color
        except Exception as e:
            # print(f"Erreur lors du chargement ou de l'analyse de l'image : {e}")
            return (0, 0, 0)

    def create_buttons(self):
        # print("Création des boutons...")
        """
        Crée les boutons du jeu Simon.
        """
        angle = 0 
        radius = 200
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        button_radius = 75
        for i, type in enumerate(self.types):
            image_path = type.image
            color = self.get_dominant_color(image_path)
            image_surface = self.load_image(image_path)
            angle_rad = math.radians(angle)
            button_x = center_x + int(math.cos(angle_rad) * radius) - button_radius
            button_y = center_y + int(math.sin(angle_rad) * radius) - button_radius
            button_color = color + (128,)
            self.buttons.append((button_x, button_y, button_color, image_surface, button_radius))
            # print(f"Bouton {i} créé.")
            angle += 360 / len(self.types)

    def draw_buttons(self, reverse=False):
        # print("Affichage des boutons...")
        """
        Affiche les boutons du jeu Simon.
        """
        for button_x, button_y, button_color, image_surface, button_radius in self.buttons:
            button_surface = pygame.Surface((button_radius*2, button_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(button_surface, button_color, (button_radius, button_radius), button_radius)
            self.screen.blit(button_surface, (button_x, button_y))
            image_rect = image_surface.get_rect(center=(button_x + button_radius, button_y + button_radius))
            self.screen.blit(image_surface, image_rect)
        if reverse:
            pygame.display.flip()

    def load_image(self, image_path):
        # print("Chargement de l'image...")
        """
        Charge une image.

        Paramètres :
            image_path (str) : Chemin vers l'image.

        Retourne :
            image (pygame.Surface) : Image chargée.
        """
        try:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (100, 100))
            # print("Image chargée.")
            return image
        except Exception as e:
            # print(f"Erreur lors du chargement de l'image : {e}")
            return None

    def load_images(self):
        # print("Chargement des images...")
        """
        Charge les images du jeu Simon.
        """
        self.bg_image_full = pygame.image.load(IMAGE_BACKGROUND)
        self.bg_image_full = pygame.transform.scale(self.bg_image_full, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image_centered = pygame.image.load(IMAGE_CENTER)
        self.bg_image_centered = pygame.transform.scale(self.bg_image_centered, (600, 600))
        self.platform_me = pygame.image.load(PLATFORM)
        self.platform_me = pygame.transform.scale(self.platform_me, (512, 256))
        self.platform_ennemy = pygame.image.load(PLATFORM)
        self.platform_ennemy = pygame.transform.scale(self.platform_ennemy, (512, 256))
        self.life_bar_me = pygame.image.load(LIFE_BAR_ME)
        self.life_bar_ennemy = pygame.image.load(LIFE_BAR_ENNEMY)
        self.pokeballs_alive = pygame.image.load(POKEBALLS_ALIVE)
        self.pokeballs_dead = pygame.image.load(POKEBALLS_DEAD)
        self.message_box = pygame.image.load(MESSAGE_BOX)
        self.message_box = pygame.transform.scale(self.message_box, (700, 100))
        self.game_over_img = pygame.image.load(GAME_OVER)
        self.game_over_img = pygame.transform.scale(self.game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.bouton_change = pygame.image.load(BOUTON_CHANGE).convert_alpha()
        # self.bouton_change = pygame.transform.scale(self.bouton_change, (100, 50))
        # self.bouton_change_clic = pygame.image.load(BOUTON_CHANGE_CLIC).convert_alpha()
        # self.bouton_change_clic = pygame.transform.scale(self.bouton_change_clic, (100, 50))

    def load_pokemon_sprite(self, ennemy_active_pokemon, me_active_pokemon):
        # print("Chargement des sprites...")
        """
        Charge les sprites des pokemons actifs.

        Paramètres :
            ennemy_active_pokemon (Pokemon) : Pokemon actif de l'ennemi.
            me_active_pokemon (Pokemon) : Pokemon actif du joueur.
        """
        self.pokemon_active_me = pygame.image.load(me_active_pokemon.image)
        self.pokemon_active_me = pygame.transform.scale(self.pokemon_active_me, (self.pokemon_active_me.get_width() * 5, self.pokemon_active_me.get_height() * 5))
        self.pokemon_active_me = pygame.transform.flip(self.pokemon_active_me, True, False)
        # self.pokemon_active_me = pygame.transform.rotate(self.pokemon_active_me, 10)
        self.pokemon_active_ennemy = pygame.image.load(ennemy_active_pokemon.image)
        self.pokemon_active_ennemy = pygame.transform.scale(self.pokemon_active_ennemy, (self.pokemon_active_ennemy.get_width() * 5, self.pokemon_active_ennemy.get_height() * 5))

    def draw_pokemon_active(self, owner):
        # print("Affichage des pokemons actifs...")
        """
        Affiche les pokemons actifs.

        Paramètres :
            owner (str) : propriétaire du pokemon actif.
        """
        if owner == "me":
            self.screen.blit(self.pokemon_active_me, (self.platform_me.get_width() - self.pokemon_active_me.get_width(), SCREEN_HEIGHT - self.platform_me.get_height() - (self.pokemon_active_me.get_height() / 2) + 50))
        elif owner == "ennemy":
            self.screen.blit(self.pokemon_active_ennemy, (SCREEN_WIDTH - self.platform_ennemy.get_width(), self.platform_ennemy.get_height() - (self.pokemon_active_ennemy.get_height() / 2)))

    def draw_background(self):
        # print("Affichage du fond...")
        """
        Affiche le fond du jeu Simon.
        """
        self.screen.blit(self.bg_image_full, (0, 0))
        centered_x = (SCREEN_WIDTH - 600) // 2
        centered_y = (SCREEN_HEIGHT - 600) // 2
        self.screen.blit(self.bg_image_centered, (centered_x, centered_y))

    def draw_interfaces(self):
        # print("Affichage des interfaces...")
        """
        Affiche les interfaces du jeu Simon.
        """
        self.screen.blit(self.platform_me, (0, SCREEN_HEIGHT - self.platform_me.get_height() + 50))
        self.screen.blit(self.platform_ennemy, (SCREEN_WIDTH - self.platform_ennemy.get_width(), self.pokemon_active_ennemy.get_height() - self.platform_ennemy.get_height()))
        self.screen.blit(self.life_bar_me, (0, SCREEN_HEIGHT - self.platform_me.get_height() - (self.life_bar_me.get_height() * 3.5)))
        self.screen.blit(self.life_bar_ennemy, (SCREEN_WIDTH - (self.platform_ennemy.get_width() / 2), (self.platform_ennemy.get_height() * 1.75)))
        self.screen.blit(self.message_box, (SCREEN_WIDTH - self.message_box.get_width(), SCREEN_HEIGHT - self.message_box.get_height()))
        # self.screen.blit(self.bouton_change, (SCREEN_WIDTH - self.bouton_change.get_width(), SCREEN_HEIGHT - self.message_box.get_height() - self.bouton_change.get_height()))

    def draw_health_bar(self, surface, x, y, health, max_health):
        # print("Affichage des barres de vie...")
        """
        Affiche les barres de vie des pokemons actifs.

        Paramètres :
            surface (pygame.Surface) : Surface sur laquelle afficher la barre de vie.
            x (int) : Position x de la barre de vie.
            y (int) : Position y de la barre de vie.
            health (int) : Points de vie actuels du pokemon.
            max_health (int) : Points de vie max du pokemon.
        """
        bar_width = 96
        bar_height = 6
        fill = (health / max_health) * bar_width
        if health > max_health * 0.25:
            color = (0, 255, 0)
        elif health > max_health * 0.1 and health <= max_health * 0.25:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, color, fill_rect)

    def draw_pokeballs(self, pokemons, team):
        # print("Affichage des pokeballs...")
        """
        Affiche les pokeballs des pokemons.

        Paramètres :
            pokemons (list) : Liste des pokemons.
            team (str) : Equipe du pokemon.
        """
        if team == "me":
            for i, pokemon in enumerate(pokemons):
                if pokemon.status == "alive":
                    self.screen.blit(self.pokeballs_alive, (30 + (i * 35), SCREEN_HEIGHT - self.platform_me.get_height() - (self.life_bar_me.get_height() * 3.5) + 5))
                elif pokemon.status == "dead":
                    self.screen.blit(self.pokeballs_dead, (30 + (i * 35), SCREEN_HEIGHT - self.platform_me.get_height() - (self.life_bar_me.get_height() * 3.5) + 5))
        elif team == "ennemy":
            for i, pokemon in enumerate(pokemons):
                if pokemon.status == "alive":
                    self.screen.blit(self.pokeballs_alive, (SCREEN_WIDTH - (self.platform_ennemy.get_width() / 2) + (i * 35) + 30, (self.platform_ennemy.get_height() * 1.75) + 5))
                elif pokemon.status == "dead":
                    self.screen.blit(self.pokeballs_dead, (SCREEN_WIDTH - (self.platform_ennemy.get_width() / 2) + (i * 35) + 30, (self.platform_ennemy.get_height() * 1.75) + 5))

    def draw_all(self):
        # print("Affichage de tout...")
        """
        Affiche tout le jeu Simon.
        """
        self.draw_background()
        self.draw_interfaces()
        self.draw_buttons()
        self.draw_pokemon_active("me")
        self.draw_pokemon_active("ennemy")
        self.draw_pokeballs(self.team_me.pokemons, "me")
        self.draw_pokeballs(self.team_ennemy.pokemons, "ennemy")
        self.draw_health_bar(
                self.screen,
                118,
                431,
                self.active_pokemon_me.stats["HP"],
                self.active_pokemon_me.stats["max_hp"]
            )
        self.draw_health_bar(
                self.screen,
                SCREEN_WIDTH - 120,
                488,
                self.active_pokemon_ennemy.stats["HP"],
                self.active_pokemon_ennemy.stats["max_hp"]
            )
        pygame.display.flip()

    def start_game(self):
        # print("Démarrage du jeu...")
        """
        Démarre le jeu Simon.
        """
        self.running = True
        self.user_sequence = []
        self.current_stage = 0
        # self.draw_all()
        while self.running:
            self.screen.fill((0, 0, 0))
            self.load_images()
            self.active_pokemon_ennemy = self.find_next_pokemon_alive(self.team_ennemy)
            self.active_pokemon_me = self.find_next_pokemon_alive(self.team_me)
            if self.active_pokemon_ennemy is None:
                self.end("win")
            elif self.active_pokemon_me is None:
                self.end("lose")
            self.load_pokemon_sprite(self.active_pokemon_ennemy, self.active_pokemon_me)
            self.draw_all()
            if self.current_stage == len(self.sequence):
                self.add_random_to_sequence()
                self.show_sequence()
                self.user_sequence = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    SOUND_CLICK.play()
                    self.handle_mouse_click(event.pos)

    def add_random_to_sequence(self):
        # print("Ajout d'un bouton à la séquence...")
        """
        Ajoute un bouton aléatoire à la séquence.
        """
        self.sequence.append(random.randint(0, len(self.buttons) - 1))

    def show_sequence(self):
        # print("Affichage de la séquence...")
        """
        Affiche la séquence.
        """
        self.show_text(FONT.render("C'est à vous de jouer !", True, BLACK_COLOR))
        for index in self.sequence:
            pygame.time.wait(500)
            self.flash_button(index)
            pygame.time.wait(500)
            self.draw_all()

    def flash_button(self, index):
        # print("Flash du bouton...")
        """
        Flash le bouton.

        Paramètres :
            index (int) : Index du bouton.
        """
        button_x, button_y, button_color, image_surface, button_radius = self.buttons[index]
        bright_color = tuple(min(c + 60, 255) for c in button_color[:3]) + (255,)
        button_surface = pygame.Surface((button_radius*2, button_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(button_surface, bright_color, (button_radius, button_radius), button_radius)
        self.screen.blit(button_surface, (button_x, button_y))
        image_rect = image_surface.get_rect(center=(button_x + button_radius, button_y + button_radius))
        self.screen.blit(image_surface, image_rect)
        pygame.display.flip()

    def handle_mouse_click(self, position):
        # print("Gestion du clic de la souris...")
        """
        Gère le clic de la souris.

        Paramètres :
            position (tuple) : Position du clic.
        """
        for i, (button_x, button_y, _, _, button_radius) in enumerate(self.buttons):
            if (position[0] - button_x - button_radius) ** 2 + (position[1] - button_y - button_radius) ** 2 < button_radius ** 2:
                self.flash_button(i)
                self.user_sequence.append(i)
                if not self.check_sequence():
                    self.handle_end_sequence()
                    return
                break

    def check_sequence(self):
        # print("Vérification de la séquence...")
        """
        Vérifie la séquence.

        Retourne :
            bool : True si la séquence est correcte, False sinon.
        """
        pygame.time.wait(1000)
        if self.user_sequence != self.sequence[:len(self.user_sequence)]:
            return False
        if len(self.user_sequence) == len(self.sequence):
            self.current_stage += 1
        return True

    def handle_damage(self, max_stage, pokemon):
        # print("Gestion des dégâts...")
        """
        Gère les dégâts.

        Paramètres :
            max_stage (int) : Nombre de tours de jeu.
            pokemon (Pokemon) : Pokemon attaquant.

        Retourne :
            damage (int) : Dégâts infligés.
            effect (str) : Effet de l'attaque.
        """
        AUDIO_PROJECTILE.play()
        base_attack = round(pokemon.stats["attack"] / 10)
        attack = base_attack * max_stage
        max_defense_ennemy = round(self.active_pokemon_ennemy.stats["defense"] / 2)
        damage = round(attack * round(1 - (max_defense_ennemy / 100), 2))
        my_types = [type["name"] for type in self.active_pokemon_me.types]
        effect = ""
        for type in self.active_pokemon_ennemy.vulnerabilities:
            if type["name"] in my_types:
                if type["damage_relation"] == "twice_vulnerable":
                    effect = "L'attaque est très efficace"
                elif type["damage_relation"] == "vulnerable":
                    effect = "L'attaque est efficace"
                damage = round(damage * type["damage_multiplier"])
        for type in self.active_pokemon_ennemy.resistances:
            if type["name"] in my_types:
                if type["damage_relation"] == "twice_resistant":
                    effect = "L'attaque n'est pas très efficace"
                elif type["damage_relation"] == "resistant":
                    effect = "L'attaque n'est pas efficace"
                damage = round(damage * type["damage_multiplier"])
        return damage, effect

    def handle_health(self, damage, pokemon, team):
        # print("Gestion de la vie...")
        """
        Gère la vie du pokemon.

        Paramètres :
            damage (int) : Dégâts infligés.
            pokemon (Pokemon) : Pokemon attaqué.
            team (Team) : Equipe du pokemon attaqué.
        """
        pokemon.stats["HP"] -= damage
        if pokemon.stats["HP"] <= 0:
            pokemon.stats["HP"] = 0
            pokemon.status = "dead"
            self.update_pokemon_status(team, pokemon)
        self.draw_all()

    def bot_attack(self):
        # print("Attaque du bot...")
        """
        Attaque du bot.

        Retourne :
            damage_bot (int) : Dégâts infligés par le bot.
            effect_bot (str) : Effet de l'attaque du bot.
        """
        stage_bot = random.randint(2, 10)
        return self.handle_damage(stage_bot, self.active_pokemon_ennemy)

    def find_next_pokemon_alive(self, team):
        # print("Recherche du prochain pokemon vivant...")
        """
        Recherche le prochain pokemon vivant.

        Paramètres :
            team (Team) : Equipe du pokemon.

        Retourne :
            pokemon (Pokemon) : Pokemon vivant.
        """
        for pokemon in team.pokemons:
            if pokemon.status == "alive":
                return pokemon
        return None
    
    def update_pokemon_status(self, team, pokemon_active):
        # print("Mise à jour du statut du pokemon...")
        """
        Met à jour le statut du pokemon.

        Paramètres :
            team (Team) : Equipe du pokemon.
            pokemon_active (Pokemon) : Pokemon actif.
        """
        for pokemon in team.pokemons:
            if pokemon.id == pokemon_active.id:
                pokemon.status = pokemon_active.status
                pokemon.stats["HP"] = pokemon_active.stats["HP"]
                break

    def show_text(self, text):
        # print("Affichage du texte...")
        """
        Affiche le texte.

        Paramètres :
            text (pygame.Surface) : Texte à afficher.
        """
        self.screen.blit(text, ((SCREEN_WIDTH // 2) + 100, SCREEN_HEIGHT - 60))
        pygame.display.flip()
        pygame.time.wait(2000)

    def handle_end_sequence(self):
        # print("Game over...")
        """
        Gère la fin de la séquence.
        """
        self.sequence = []
        self.draw_all()
        self.show_text(FONT.render("Votre pokemon attaque !", True, BLACK_COLOR))
        damage, effect = self.handle_damage(self.current_stage, self.active_pokemon_me)
        self.handle_health(damage, self.active_pokemon_ennemy, self.team_ennemy)
        self.show_text(FONT.render(f"{self.active_pokemon_me.name} a infligé {damage} !!", True, BLACK_COLOR))
        self.draw_all()
        if effect != "":
            self.show_text(FONT.render(effect, True, BLACK_COLOR))
            self.draw_all()
        self.current_stage = 0
        self.show_text(FONT.render("Le Pokemon ennemi attaque !", True, BLACK_COLOR))
        damage_bot, effect_bot = self.bot_attack()
        self.handle_health(damage_bot, self.active_pokemon_me, self.team_me)
        self.show_text(FONT.render(f"{self.active_pokemon_ennemy.name} a infligé {damage_bot} !!", True, BLACK_COLOR))
        if effect_bot != "":
            self.draw_all()
            self.show_text(FONT.render(effect_bot, True, BLACK_COLOR))
        self.start_game()

    def end(self, resultat):
        # print("Fin du jeu...")
        """
        Gère la fin du jeu.

        Paramètres :
            resultat (str) : Résultat de la partie.
        """
        if resultat == "win":
            self.running = False
            pygame.quit()
            sys.exit()
        elif resultat == "lose":
            self.screen.blit(self.game_over_img, (0,0))
            pygame.display.flip()
            pygame.time.wait(7000)
            from src.principal import Menu
            menu = Menu()
            menu.run()

# if __name__ == "__main__":
#     team1 = Team.create_random_team("Joueur 1")
#     team2 = Team.create_random_team("Joueur 2")
#     game = SimonGame(team1, team2)
#     game.start_game()
    
