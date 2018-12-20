from flask import Flask, Blueprint, request, jsonify, abort
from player import Player

player_controller = Blueprint('player_controller', __name__)

players = []


@player_controller.route("/players", methods=["GET"])
def get_players():
    return jsonify({'players': players})


@player_controller.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = [player for player in players if player['id'] == player_id]
    if len(player) == 0:
        abort(404)
    return jsonify({'player': player[0]})


@player_controller.route('/players', methods=['POST'])
def create_player():
    if not request.json or not 'name' in request.json:
        abort(400)
    id = 0
    if (len(players) > 0):
        id = players[-1]['id'] + 1
    player = Player(id=id, name=request.json['name'])
    players.append(player)
    return jsonify({'player': player.asdict()}), 201


@player_controller.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    player = [player for player in players if player['id'] == player_id]
    if len(player) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'cash' in request.json and type(request.json['cash']) is not int:
        abort(400)
    if 'hand' in request.json and type(request.json['hand']) is not list:
        abort(400)
    if 'position' in request.json and type(request.json['position']) is not int:
        abort(400)
    if 'bet_amount' in request.json and type(request.json['bet_amount']) is not int:
        abort(400)
    if 'is_active' in request.json and type(request.json['is_active']) is not bool:
        abort(400)
    if 'has_folded' in request.json and type(request.json['has_folded']) is not bool:
        abort(400)
    if 'is_winner' in request.json and type(request.json['is_winner']) is not bool:
        abort(400)
    player[0].name = request.json.get('name', player[0]['name'])
    player[0].cash = request.json.get('cash', player[0]['cash'])
    player[0].hand = request.json.get('hand', player[0]['hand'])
    player[0].position = request.json.get('position', player[0]['position'])
    player[0].bet_amount = request.json.get(
        'bet_amount', player[0].bet_amount)
    player[0].is_active = request.json.get(
        'is_active', player[0].is_active)
    player[0].has_folded = request.json.get(
        'has_folded', player[0].has_folded)
    player[0].is_winner = request.json.get(
        'is_winner', player[0].is_winner)
    return jsonify({'player': player[0].asdict})


@player_controller.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = [player for player in players if player['id'] == player_id]
    if len(player) == 0:
        abort(404)
    players.remove(player[0])
    return jsonify({'result': True})
