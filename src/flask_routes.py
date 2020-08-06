from flask import Flask
import query
import json

# TODO: return error in update and delete


app = Flask(__name__)


@app.route('/types/<pokemon>', methods=['PATCH'])
def update_type(pokemon):
    return query.pokemon_type.update(pokemon)


@app.route('/pokemon/<pokemon>', methods=['POST'])
def add_pokemon(pokemon):
    return query.pokemon.add(pokemon)


@app.route('/types/<type_>')
def get_pokemon_by_type(type_):
    return query.pokemon.find_pokemon_by_type(type_)


@app.route('/trainer/<pokemon>')
def get_trainer_of_pokemon(pokemon):
    result = query.trainer.find_owners(pokemon)

    if result == "error":
        return json.dumps({"error": "internal error"}), 500

    if len(result) == 0:
        return json.dumps({"error": "there is no trainer"}), 400

    return json.dumps({"ok": result}), 200


@app.route('/pokemon/<trainer>')
def get_pokemon_of_trainer(trainer):
    result = query.pokemon.find_roster(trainer)

    if result == "error":
        return json.dumps({"error": "internal error"}), 500

    if len(result) == 0:
        return json.dumps({"error": "there is no pokemon"}), 400

    return json.dumps({"ok": result}), 200


@app.route('/trainer/<trainer>/<pokemon>', methods=['DELETE'])
def delete_from_trainer(trainer, pokemon):
    return query.trainer.delete_from_trainer(trainer, pokemon)


@app.route('/trainer/evolve/<trainer>/<pokemon>', methods=['PATCH'])
def evolve_pokemon(trainer, pokemon):
    return query.pokemon.evolve(trainer, pokemon)


if __name__ == '__main__':
    app.run(port=3001)

