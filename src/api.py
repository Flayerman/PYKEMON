"""
Script permettant de récupérer des informations sur les Pokémon et les types à partir de l'API de PokeBuild.
Possibilité de créer une team soit en random soit avec des identifiants ou noms de Pokémon.

Exemple d'utilisation :
Pokemon.get_pokemon_by_name("Pikachu")
 --> Récupère les informations du Pokémon Pikachu par son nom

Pokemon.get_pokemon_by_id(25)
 --> Récupère les informations du Pokémon Pikachu par son identifiant

Type.get_type_by_name("Feu")
 --> Récupère les informations du type Feu par son nom

Type.get_type_by_id(10)
 --> Récupère les informations du type Feu par son identifiant

Team.create_random_team("Team 1")
 --> Crée une équipe de Pokémon aléatoirement

Team.create_team_by_id("Team 2", [1, 2, 3, 4, 5, 6])
 --> Crée une équipe de Pokémon à partir d'une liste d'identifiants

Team.create_team_by_name("Team 3", ["Pikachu", "Bulbizarre", "Salamèche", "Carapuce", "Rattata", "Piafabec"])
 --> Crée une équipe de Pokémon à partir d'une liste de noms
"""
##############################################################################################################
# imports
import json
import random
# constantes
FILE_POKEMONS = "data/pokemongeneration1.json"
FILE_TYPES = "data/types.json"
##############################################################################################################

class Pokemon():
    """
    Classe représentant un Pokémon, contenant ses informations détaillées.

    Attributs :
        id (int) : Identifiant unique du Pokémon.
        pokedexId (int) : Identifiant dans le Pokédex.
        name (str) : Nom du Pokémon.
        types (list) : Liste des types du Pokémon.
        stats (dict) : Statistiques du Pokémon.
        vulnerabilities (list) : Liste des vulnérabilités du Pokémon.
        resistances (list) : Liste des résistances du Pokémon.
        image (str) : URL de l'image du Pokémon.
    """

    def __init__(self, id, pokdedexId, name, types, stats, vulnerabilities, resistances, image, status):
        self.id = id
        self.pokedexId = pokdedexId
        self.name = name
        self.types = types
        self.stats = stats
        self.vulnerabilities = vulnerabilities
        self.resistances = resistances
        self.image = image
        self.status = status

    def get_pokemon_by_name(name):
        """
        Récupère un Pokémon par son nom.

        Paramètres :
            name (str) : Nom du Pokémon à récupérer.

        Retourne :
            Pokemon : Instance de la classe Pokémon, None si non trouvé.
        """
        resistances_list = []
        vulnerabilities_list = []
        types = []
        if not name[0].isupper():
            name = name.capitalize()
        with open(FILE_POKEMONS, "r") as file:
            data = json.load(file)
        for pokemon in data:
            if pokemon["name"] == name:
                for resistances in pokemon["apiResistances"]:
                    if "resistant" in resistances["damage_relation"]:
                        resistances_list.append(resistances)
                    elif "vulnerable" in resistances["damage_relation"]:
                        vulnerabilities_list.append(resistances)
                pokemon["stats"]["max_hp"] = pokemon["stats"]["HP"]
                for type in pokemon["apiTypes"]:
                    types.append(type)
                return Pokemon(pokemon["id"], pokemon["pokedexId"], pokemon["name"], types, pokemon["stats"], vulnerabilities_list, resistances_list, pokemon["sprite"], status="alive")

    def get_pokemon_by_id(id):
        """
        Récupère un Pokémon par son identifiant.

        Paramètres :
            id (int) : Identifiant du Pokémon à récupérer.

        Retourne :
            Pokemon : Instance de la classe Pokémon, None si non trouvé.
        """
        resistances_list = []
        vulnerabilities_list = []
        types = []
        with open(FILE_POKEMONS, "r") as file:
            data = json.load(file)
        for pokemon in data:
            if pokemon["id"] == id:
                for resistances in pokemon["apiResistances"]:
                    if "resistant" in resistances["damage_relation"]:
                        resistances_list.append(resistances)
                    elif "vulnerable" in resistances["damage_relation"]:
                        vulnerabilities_list.append(resistances)
                pokemon["stats"]["max_hp"] = pokemon["stats"]["HP"]
                for type in pokemon["apiTypes"]:
                    types.append(type)
                return Pokemon(pokemon["id"], pokemon["pokedexId"], pokemon["name"], types, pokemon["stats"], vulnerabilities_list, resistances_list, pokemon["sprite"], status="alive")
            
        def get_stats(self):
            """
            Récupère les statistiques du Pokémon.

            Retourne :
                dict : Dictionnaire contenant les statistiques du Pokémon.
            """
            return self.stats
        
        def get_vulnerabilities(self):
            """
            Récupère les vulnérabilités du Pokémon.

            Retourne :
                list : Liste des vulnérabilités du Pokémon.
            """
            return self.vulnerabilities
        
        def get_resistances(self):
            """
            Récupère les résistances du Pokémon.

            Retourne :
                list : Liste des résistances du Pokémon.
            """
            return self.resistances
        
        def get_types(self):
            """
            Récupère les types du Pokémon.

            Retourne :
                list : Liste des types du Pokémon.
            """
            print(self.types)
            print(self.types[0])
            return self.types[0]


class Type():
    """
    Classe représentant un type de Pokémon.

    Attributs :
        id (int) : Identifiant unique du type.
        name (str) : Nom du type.
        image (str) : URL de l'image représentant le type.
    """
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image
        
    def get_type_by_id(id):
        """
        Récupère un type de Pokémon par son identifiant.

        Paramètres :
            id (int) : Identifiant du type à récupérer.

        Retourne :
            Type : Instance de la classe Type, None si non trouvé.
        """
        with open(FILE_TYPES, "r") as file:
            data = json.load(file)
        for type in data:
            if type["id"] == id:
                return Type(type["id"], type["name"], type["image"])
    
    def get_type_by_name(name):
        """
        Récupère un type de Pokémon par son nom.

        Paramètres :
            name (str) : Nom du type à récupérer.

        Retourne :
            Type : Instance de la classe Type, None si non trouvé.
        """
        if not name[0].isupper():
            name = name.capitalize()
        with open(FILE_TYPES, "r") as file:
            data = json.load(file)
        for type in data:
            if type["name"] == name:
                return Type(type["id"], type["name"], type["image"])

class Team:
    """
    Classe représentant une équipe de Pokémon.

    Attributs :
        name (str) : Nom de l'équipe.
        pokemons (list) : Liste des Pokémon dans l'équipe.
    """
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons

    def create_random_team(name):
        """
        Crée une équipe de Pokémon aléatoirement.

        Paramètres :
            name (str) : Nom de l'équipe à créer.

        Retourne :
            Team : Instance de la classe Team, None si erreur.
        """
        pokemons = []
        while len(pokemons) < 6:
            pokemons.append(Pokemon.get_pokemon_by_id(random.randint(1, 151)))
        return Team(name, pokemons)

    def create_team_by_id(name, ids_pokemons):
        """
        Crée une équipe de Pokémon à partir d'une liste d'identifiants.

        Paramètres :
            name (str) : Nom de l'équipe.
            ids_pokemons (list) : Liste des identifiants des Pokémon à inclure dans l'équipe.

        Retourne :
            Team : Nouvelle instance de la classe Team contenant les Pokémon spécifiés.
        """
        pokemons = []
        for id in ids_pokemons:
            pokemons.append(Pokemon.get_pokemon_by_id(id))
        return Team(name, pokemons)

    def create_team_by_name(name, names_pokemons):
        """
        Crée une équipe de Pokémon à partir d'une liste de noms.

        Paramètres :
            name (str) : Nom de l'équipe.
            names_pokemons (list) : Liste des noms des Pokémon à inclure dans l'équipe.

        Retourne :
            Team : Nouvelle instance de la classe Team contenant les Pokémon spécifiés.
        """
        pokemons = []
        for name in names_pokemons:
            pokemons.append(Pokemon.get_pokemon_by_name(name))
        return Team(name, pokemons)
    
