from flask import Flask, Blueprint, request, jsonify, abort

game_controller = Blueprint('game_controller', __name__)

games = []


@game_controller.route("/games", methods=["GET"])
def get_games():
    return jsonify({'games': games})


@game_controller.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = [game for game in games if game['id'] == game_id]
    if len(game) == 0:
        abort(404)
    return jsonify({'game': game[0]})


@game_controller.route('/games', methods=['POST'])
def create_game():
    if not request.json or not 'name' in request.json:
        abort(400)
    game = {
        'id': games[-1]['id'] + 1,
        'table_name': request.json['table_name'],
        'max_table_size': request.json['max_table_size'],
        'players': [],
        'deck': None,
        'round': 0,
        'active_player': None,
        'board': [],
        'pot': 0,
        'blinds': request.json['blinds']
    }
    games.append(game)
    return jsonify({'game': game}), 201


@game_controller.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    game = [game for game in games if game['id'] == game_id]
    if len(game) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'table_name' in request.json and type(request.json['table_name']) is not str:
        abort(400)
    if 'players' in request.json and type(request.json['players']) is not list:
        abort(400)
    if 'deck' in request.json and type(request.json['deck']) is not str:
        abort(400)
    if 'round' in request.json and type(request.json['round']) is not int:
        abort(400)
    if 'active_player' in request.json and type(request.json['active_player']) is not str:
        abort(400)
    if 'board' in request.json and type(request.json['board']) is not list:
        abort(400)
    if 'pot' in request.json and type(request.json['pot']) is not int:
        abort(400)
    if 'blinds' in request.json and type(request.json['blinds']) is not list:
        abort(400)
    game[0].table_name = request.json.get(
        'table_name', game[0]['table_name'])
    game[0]['players'] = request.json.get('players', game[0]['players'])
    game[0]['deck'] = request.json.get('deck', game[0]['deck'])
    game[0]['round'] = request.json.get('round', game[0]['round'])
    game[0]['active_player'] = request.json.get(
        'active_player', game[0]['active_player'])
    game[0]['board'] = request.json.get(
        'board', game[0]['board'])
    game[0]['pot'] = request.json.get(
        'pot', game[0]['pot'])
    game[0]['blinds'] = request.json.get(
        'blinds', game[0]['blinds'])
    return jsonify({'game': game[0]})
