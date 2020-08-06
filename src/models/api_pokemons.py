
import requests


def get_pokemon_details(pokemon):
    return requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{pokemon}", verify=False).json()


def get_species(pokemon):
    return requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{pokemon}", verify=False).json()["species"]["url"]


def get_evolution_chain(url):
    return requests.get(url=url, verify=False).json()["evolution_chain"]["url"]


def get_evolved_pokemon(url, pokemon_name):
    evolved_pokemon = requests.get(url=url, verify=False).json()["chain"]

    if pokemon_name == evolved_pokemon["species"]["name"]:
        return evolved_pokemon["evolves_to"][0]["species"]["name"]

    evolved_pokemon = evolved_pokemon["evolves_to"][0]

    if pokemon_name == evolved_pokemon["species"]["name"]:
        return evolved_pokemon["evolves_to"][0]["species"]["name"]

    return None
