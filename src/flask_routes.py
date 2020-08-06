from flask import Flask
from src import models
import json


app = Flask(__name__)


@app.route('/types/<pokemon>', methods=['PATCH'])
def update_type(pokemon):
    return models.pokemon_type.update(pokemon)


@app.route('/pokemon/<pokemon>', methods=['POST'])
def add_pokemon(pokemon):
    return models.pokemon.add(pokemon)


@app.route('/types/<type_>')
def get_pokemon_by_type(type_):
    return models.pokemon.find_pokemon_by_type(type_)


@app.route('/trainer/<pokemon>')
def get_trainer_of_pokemon(pokemon):
    result = models.trainer.find_owners(pokemon)

    if result == "error":
        return json.dumps({"error": "internal error"}), 500

    if len(result) == 0:
        return json.dumps({"error": "there is no trainer"}), 400

    return json.dumps({"ok": result}), 200


@app.route('/pokemon/<trainer>')
def get_pokemon_of_trainer(trainer):
    result = models.pokemon.find_roster(trainer)

    if result == "error":
        return json.dumps({"error": "internal error"}), 500

    if len(result) == 0:
        return json.dumps({"error": "there is no pokemon"}), 400

    return json.dumps({"ok": result}), 200


@app.route('/trainer/<trainer>/<pokemon>', methods=['DELETE'])
def delete_from_trainer(trainer, pokemon):
    return models.trainer.delete_from_trainer(trainer, pokemon)


@app.route('/evolve/<trainer>/<pokemon>', methods=['PATCH'])
def evolve_pokemon(trainer, pokemon):
    return models.pokemon.evolve(trainer, pokemon)


if __name__ == '__main__':
    app.run(port=3001)

