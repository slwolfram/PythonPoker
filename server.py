from quart import Quart, jsonify, request, abort
from player import Player
from game import Game
import asyncio


app = Quart(__name__)

loop = None
players = []
games = []


@app.route("/players", methods=["GET"])
def get_players():
    return jsonify({'players': players})


@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = [player for player in players if player['id'] == player_id]
    if len(player) == 0:
        abort(404)
    return jsonify({'player': player[0]})


@app.route('/players', methods=['POST'])
def create_player():
    if not request.json or not 'name' in request.json:
        abort(400)
    id = 0
    if (len(players) > 0):
        id = players[-1]['id'] + 1
    player = Player(id=id, name=request.json['name'])
    print("ok")
    players.append(player)
    print("ok2")
    print(player.asdict())
    return jsonify({'player': player.asdict()}), 201


@app.route('/players/<int:player_id>', methods=['PUT'])
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


@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = [player for player in players if player['id'] == player_id]
    if len(player) == 0:
        abort(404)
    players.remove(player[0])
    return jsonify({'result': True})


@app.route("/games", methods=["GET"])
def get_games():
    games_json = []
    for game in games:
        games_json.append(game.asdict())
    return jsonify({'games': games_json})


@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = [game for game in games if game['id'] == game_id]
    if len(game) == 0:
        abort(404)
    return jsonify({'game': game[0]})


@app.route('/games', methods=['POST'])
async def create_game():
    print("here")
    req = await request.json
    if not req:
        abort(400)
    if not 'table_name' in req:
        abort(400)
    if type(req['table_name']) is not str:
        abort(400)
    if not 'max_table_size' in req or type(req['max_table_size']) is not int:
        abort(400)
    if not 'blinds' in req or type(req['blinds']) is not list:
        abort(400)
    if len(req['blinds']) is not 2:
        abort(400)
    if type(req['blinds'][0]) is not int or type(req['blinds'][1]) is not int:
        abort(400)
    id = 0
    if (len(games) > 0):
        id = games[-1]['id'] + 1
    game = Game(id=id, table_name=req['table_name'],
                max_table_size=req['max_table_size'], blinds=req['blinds'], players=[])
    loop.create_task(game.play())
    print(game.table_name)
    games.append(game)
    print(game.asdict())
    return jsonify({'game': game.asdict()}), 201


@app.route('/games/<int:game_id>', methods=['PUT'])
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(1)
    loop.run_until_complete(app.run(debug=True))
    print("complete!")
    loop.close
