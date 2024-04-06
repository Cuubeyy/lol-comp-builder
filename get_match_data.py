import os
import requests
import json
import networkx as nx


class MatchData:
    def __init__(self, match_id):
        self.match_id = match_id
        self.data = None
        self.participants = []

    def send_request(self):
        request_data = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/" + self.match_id +
                                    "?api_key=" + os.environ["api_key"])
        js = json.loads(request_data.content)
        self.data = js

    def parse_champion_data(self):
        for player in self.data["info"]["participants"]:
            self.participants.append((player["championName"], player["championId"]))

    def print_data(self):
        print(self.data)
        print(self.participants)


if __name__ == "__main__":
    match_data = MatchData("EUW1_6887440777")
    match_data.send_request()
    match_data.parse_champion_data()
    match_data.print_data()
