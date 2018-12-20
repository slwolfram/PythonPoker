from app.player_controller import player_controller
from app.game_controller import game_controller
from flask import Flask
from flask import Flask, jsonify, abort, request
import player

app = Flask(__name__)

games = []


app = Flask(__name__)
app.register_blueprint(game_controller)
app.register_blueprint(player_controller)
