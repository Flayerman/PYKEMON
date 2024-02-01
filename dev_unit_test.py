import unittest
from src.api import Pokemon, Type, Team

class TestPokemonMethods(unittest.TestCase):

    def test_get_pokemon_by_name(self):
        pikachu = Pokemon.get_pokemon_by_name("Pikachu")
        self.assertIsNotNone(pikachu)
        self.assertEqual(pikachu.name, "Pikachu")

    def test_get_pokemon_by_id(self):
        pikachu = Pokemon.get_pokemon_by_id(25)
        self.assertIsNotNone(pikachu)
        self.assertEqual(pikachu.id, 25)

class TestTypeMethods(unittest.TestCase):

    def test_get_type_by_id(self):
        fire_type = Type.get_type_by_id(46)
        self.assertIsNotNone(fire_type)
        self.assertEqual(fire_type.name, "Feu")

    def test_get_type_by_name(self):
        fire_type = Type.get_type_by_name("Feu")
        self.assertIsNotNone(fire_type)
        self.assertEqual(fire_type.name, "Feu")

class TestTeamMethods(unittest.TestCase):

    def test_create_random_team(self):
        team = Team.create_random_team("Random Team")
        self.assertIsNotNone(team)
        self.assertEqual(len(team.pokemons), 6)

    def test_create_team_by_id(self):
        team = Team.create_team_by_id("Team by ID", [1, 2, 3, 4, 5, 6])
        self.assertIsNotNone(team)
        self.assertEqual(len(team.pokemons), 6)

    def test_create_team_by_name(self):
        team = Team.create_team_by_name("Team by Name", ["Pikachu", "Florizarre", "Salamèche", "Tortank", "Rattata", "Roucoups"])
        self.assertIsNotNone(team)
        self.assertEqual(len(team.pokemons), 6)

if __name__ == '__main__':
    unittest.main()
