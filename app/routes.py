from flask import request, jsonify
from app import app
from app import mongo
from app import s3_client
from app.utility import Utility

@app.route('/fixture', methods = ['GET'])
def fixture():
    if request.method == 'GET':
        match_data = Utility.get_fixture()
        return jsonify(match_data),200

@app.route('/team/<regno>', methods =['GET'])
def team_detail(team):
    if request.method == 'GET':
        player_data,team_data = Utility.get_details_by_team(team)
        return jsonify(team_data, player_data), 200
