import json
import os
import random
from datetime import datetime

class Player:
    def __init__(self, firstname, lastname, birthdate, national_id, score=0):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate  # Format: "DD-MM-YYYY"
        self.national_id = national_id  # e.g., "AB12345"
        self.score = score  # Cumulative score across tournaments

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "national_id": self.national_id,
            "score": self.score  # Include score for global tracking in players.json
        }

class Match:
    def __init__(self, player1, player2):
        self.players = [
            [player1, 0],  # [player, score]
            [player2, 0]   # [player, score]
        ]
        # Randomly assign white/black (simplified as 1/0 for now)
        self.white_player = random.choice([0, 1])
        self.is_finished = False

    def set_result(self, winner_idx=None):
        if winner_idx is not None:
            self.players[winner_idx][1] = 1  # Winner gets 1 point
            self.players[1 - winner_idx][1] = 0  # Loser gets 0
        else:
            self.players[0][1] = 0.5  # Draw, both get 0.5
            self.players[1][1] = 0.5
        self.is_finished = True

    def to_dict(self):
        return {
            "players": [
                [p[0].to_dict() if isinstance(p[0], Player) else p[0].to_dict(), p[1]]
                for p in self.players
            ],
            "white_player": self.white_player,
            "is_finished": self.is_finished
        }

    @classmethod
    def from_dict(cls, data, players_by_id):
        """Reconstruct a Match from dict, using players_by_id to map national_ids to Player objects."""
        match = cls(None, None)  # Temporary initialization
        match.white_player = data["white_player"]
        match.is_finished = data["is_finished"]
        match.players = []
        for player_data, score in data["players"]:
            if isinstance(player_data, dict):
                national_id = player_data.get("national_id", "XX00000")  # Default if missing
                player = players_by_id.get(national_id)
                if player:
                    match.players.append([player, score])
                else:
                    # Fallback: create a new Player if not found (shouldn't happen)
                    match.players.append([Player(**{**player_data, "national_id": national_id}), score])
            else:
                raise ValueError("Invalid player data in Match")
        return match

class Round:
    def __init__(self, name):
        self.name = name  # e.g., "Round 1"
        self.matches = []
        self.start_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.end_time = None

    def finish(self):
        self.end_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data, players_by_id):
        """Reconstruct a Round from dict, using players_by_id to map national_ids to Player objects."""
        round_obj = cls(data["name"])
        round_obj.start_time = data["start_time"]
        round_obj.end_time = data["end_time"]
        for match_data in data["matches"]:
            round_obj.matches.append(Match.from_dict(match_data, players_by_id))
        return round_obj

class Tournament:
    def __init__(self, name, location, start_date, description=""):
        self.name = name
        self.location = location
        self.start_date = start_date  # Format: "DD-MM-YYYY"
        self.end_date = None
        self.number_of_rounds = 4  # Default to 4 rounds
        self.current_round = 0
        self.rounds = []
        self.players = []  # Will be populated from the database
        self.description = description
        self.all_possible_pairs = []  # Track all possible player pairings

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [round.to_dict() for round in self.rounds],
            "players": [player.to_dict() for player in self.players],
            "description": self.description
        }

    def add_players_from_database(self, available_players):
        # Add all players from the database to the tournament, copying scores
        self.players = [Player(**player.to_dict()) for player in available_players]
        # Generate all possible unique pairings (ensuring every player faces each other)
        self.all_possible_pairs = []
        if len(self.players) >= 2:  # Ensure at least 2 players for pairing
            for i in range(len(self.players)):
                for j in range(i + 1, len(self.players)):
                    pair = tuple(sorted([self.players[i].national_id, self.players[j].national_id]))
                    self.all_possible_pairs.append(pair)

    def generate_pairs(self):
        if not self.players or len(self.players) < 2:
            return []  # Return empty list if not enough players
        if self.current_round == 0:
            # For the first round, ensure every player faces each other over 4 rounds
            used_pairs = set()
            pairs = []
            remaining_pairs = self.all_possible_pairs.copy()
            random.shuffle(remaining_pairs)
            
            # Generate pairs for this round, avoiding duplicates within the tournament
            for pair in remaining_pairs:
                if len(pairs) >= (len(self.players) + 1) // 2:  # Handle odd number of players (e.g., 9 players -> 5 pairs)
                    break
                p1_id, p2_id = pair
                p1 = next((p for p in self.players if p.national_id == p1_id), None)
                p2 = next((p for p in self.players if p.national_id == p2_id), None)
                if p1 and p2:  # Ensure both players exist
                    pair_key = tuple(sorted([p1.national_id, p2.national_id]))
                    if pair_key not in used_pairs:
                        pairs.append((p1, p2))
                        used_pairs.add(pair_key)
            return pairs
        else:
            # For subsequent rounds, sort by score and pair sequentially
            self.players.sort(key=lambda p: p.score, reverse=True)
            pairs = []
            used_pairs = set()
            for round in self.rounds:
                for match in round.matches:
                    p1, p2 = match.players
                    # Ensure p1 and p2 are Player objects
                    if isinstance(p1[0], dict):
                        p1 = [Player(**{k: v for k, v in p1[0].items() if k in ["firstname", "lastname", "birthdate", "national_id", "score"]}), p1[1]]
                    if isinstance(p2[0], dict):
                        p2 = [Player(**{k: v for k, v in p2[0].items() if k in ["firstname", "lastname", "birthdate", "national_id", "score"]}), p2[1]]
                    pair_key = tuple(sorted([p1[0].national_id, p2[0].national_id]))
                    used_pairs.add(pair_key)
            for i in range(0, len(self.players), 2):
                if i + 1 >= len(self.players):
                    break
                player1, player2 = self.players[i], self.players[i + 1]
                pair_key = tuple(sorted([player1.national_id, player2.national_id]))
                if pair_key not in used_pairs:
                    pairs.append((player1, player2))
                else:
                    # Find another pairing (simplified: pair with next available player)
                    for j in range(i + 2, len(self.players), 2):
                        if j + 1 >= len(self.players):
                            break
                        alt_player2 = self.players[j]
                        alt_pair_key = tuple(sorted([player1.national_id, alt_player2.national_id]))
                        if alt_pair_key not in used_pairs:
                            pairs.append((player1, alt_player2))
                            break
            return pairs

    def start_round(self):
        if self.current_round >= self.number_of_rounds:
            return False
        if self.end_date:
            return False  # Cannot start a round if tournament is ended
        round_name = f"Round {self.current_round + 1}"
        new_round = Round(round_name)
        pairs = self.generate_pairs()
        if not pairs:
            return False  # Indicate no pairs were generated
        for player1, player2 in pairs:
            new_round.matches.append(Match(player1, player2))
        self.rounds.append(new_round)
        self.current_round += 1
        return True

    def finish_round(self):
        if not self.rounds or self.current_round == 0:
            return False
        if self.end_date:
            return False  # Cannot finish a round if tournament is ended
        current_round = self.rounds[-1]
        current_round.finish()
        # Do not set default results here—let the controller handle user input
        return True

    def end_tournament(self):
        if not self.end_date and self.current_round >= self.number_of_rounds:
            self.end_date = datetime.now().strftime("%d-%m-%Y")
            return True
        return False

class Database:
    def __init__(self):
        self.players_dir = "data/players"
        self.tournaments_dir = "data/tournaments"

    def ensure_directories(self):
        os.makedirs(self.players_dir, exist_ok=True)
        os.makedirs(self.tournaments_dir, exist_ok=True)

    def load_players(self):
        players_file = os.path.join(self.players_dir, "players.json")
        if os.path.exists(players_file):
            with open(players_file, "r") as file:
                data = json.load(file)
                return [Player(**player) for player in data]
        return []

    def save_players(self, players):
        self.ensure_directories()
        players_file = os.path.join(self.players_dir, "players.json")
        with open(players_file, "w") as file:
            json.dump([player.to_dict() for player in players], file, indent=4)

    def load_tournament(self, tournament_name):
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament_name}.json")
        if os.path.exists(tournament_file):
            with open(tournament_file, "r") as file:
                data = json.load(file)
                tournament = Tournament(data["name"], data["location"], data["start_date"], data["description"])
                tournament.end_date = data["end_date"]
                tournament.number_of_rounds = data["number_of_rounds"]
                tournament.current_round = data["current_round"]
                # Create a mapping of national_id to Player objects for reconstruction
                players_by_id = {p.national_id: p for p in [Player(**player) for player in data["players"]]}
                tournament.rounds = [Round.from_dict(r, players_by_id) for r in data["rounds"]]
                tournament.players = [Player(**player) for player in data["players"]]
                return tournament
        return None

    def save_tournament(self, tournament):
        self.ensure_directories()
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament.name}.json")
        with open(tournament_file, "w") as file:
            json.dump(tournament.to_dict(), file, indent=4)