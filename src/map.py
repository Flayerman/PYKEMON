import time
from dataclasses import dataclass
import pygame, pytmx, pyscroll
from src.api import Team
from src.simon import SimonGame
from src.Player import NPC
SOUND_BATTLE = pygame.mixer.Sound("Audio/1-15. Battle (Vs. Trainer).mp3")



@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2",
                   teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house3", target_world="house3",
                   teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house4", target_world="house4", teleport_point="spawn_house")
        ])
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="world",
                   teleport_point="enter_house_exit")
        ], npcs=[
            NPC("rival", nb_points=4)
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ], npcs=[
            NPC("professor", nb_points=2)
        ])
        self.register_map("house3", portals=[
            Portal(from_world="house3", origin_point="exit_house", target_world="world",
                   teleport_point="exit_house3")
        ], npcs=[
            NPC("girl", nb_points=2)
        ])
        self.register_map("house4", portals=[
            Portal(from_world="house4", origin_point="exit_house", target_world="world",
                   teleport_point="exit_house4")
        ], npcs=[
            NPC("gambler", nb_points=2)
        ])
        self.teleport_player("player")
        self.teleport_npcs()


    def check_collisions(self):
        # Portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # vérification collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                    info = pygame.display.Info()
                    image = pygame.image.load(f"sprites/Transition_{sprite.name}.png")
                    image = pygame.transform.scale(image, (info.current_w, 300))
                    pygame.mixer.music.stop()
                    self.screen.blit(image, (0,300))
                    pygame.display.flip()
                    SOUND_BATTLE.play()
                    time.sleep(5)

                    team_me = Team.create_random_team("Joueur 1")
                    team_ennemy = Team.create_random_team("Joueur 2")
                    # print(team_ennemy.pokemons[:2])
                    game = SimonGame(team_me=team_me, team_ennemy=team_ennemy)
                    game.start_game()
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger map
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        # Définir une liste stock rectangles de collision
        walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        # Recuperer NPC
        for npc in npcs:
            group.add(npc)

        # Creer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        # Boucle de verification
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
