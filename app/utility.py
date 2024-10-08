from app import mongo

class Utility:

    @staticmethod
    def get_fixture():
        match_data = []
        try:
            match_collections  = list(mongo.db.matches.find({},{"_id":0}).sort({"MatchID":1}))
            for match in match_collections:
                teamA = match.get("TeamA")
                teamB = match.get("TeamB")
                teamAlogo = mongo.db.registration.find_one({"TeamName": teamA}, {"_id":0, "TeamLogo":1})
                teamBlogo = mongo.db.registration.find_one({"TeamName": teamB}, {"_id":0, "TeamLogo":1})
                match_dict = {
                    "match_id": match.get("MatchID"),
                    "teamA": teamA,
                    "teamAlogo": teamAlogo,
                    "teamB": teamB,
                    "teamBlogo": teamBlogo,
                    "match_date": match.get("Date"),
                    "time": match.get("Time")
                    }
                match_data.append(match_dict)
            return match_data

        except Exception as e:
            return(str(e))
            # match_data = []

    @staticmethod
    def get_details_by_team(team):
        player_data = []
        try:
            team_data = list(mongo.db.registration.find_one({"TeamName": team},
                                {"_id":0, "TeamName":1, "TeamLogo":1, "ManagerName":1, "CaptainName":1}))
             # Correct aggregation pipeline
            pipeline = [
            {
                "$match": {"team": team}  # Match players from the specified team
            },
            {
                "$group": {
                    "_id": "$player",
                    "player": { "$first": "$player" },
                    "type": { "$first": "$type" },
                    "photo": { "$first": "$photo" },
                    "score": { "$sum": "$score" },
                    "wicket": { "$sum": "$wicket" },
                    "catch": { "$sum": "$catch" }
                }
            }
        ]
            player_details = list(mongo.db.players.aggregate(pipeline))
            for player in player_details:
                player_dict = {
                    "player": player.get("player"),
                    "photo": player.get("photo"),
                    "type": player.get("type"),
                    "score": player.get("score"),
                    "wicket": player.get("wicket"),
                    "catch": player.get("catch"),
                }
                player_data.append(player_dict)
            return player_data,team_data
        except Exception as e:
            return str(e), "error"