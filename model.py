"""
model.py

A module defining the data models for the chess tournament management system.
Handles the structure and persistence of players, matches, rounds, tournaments, and database operations.

Directory Structure:
    data/
        players/ - Directory for storing player data (players.json).
        tournaments/ - Directory for storing tournament data (e.g., EUChessTour.json).

Usage:
    Import and use the classes to manage tournament data:
        $ python3 main.py

Classes:
    Player: Represents a chess player with personal details and score.
    Match: Represents a chess match between two players.
    Round: Represents a round in a chess tournament.
    Tournament: Represents a chess tournament with multiple rounds and players.
    Database: Handles file-based storage and retrieval of player and tournament data.

Author:
    Mathieu Patoz
    Updated: March 06, 2025
"""

import json
import os
import random
from datetime import datetime


class Player:
    """A class representing a chess player with personal details and score.

    Attributes:
        firstname (str): The player's first name.
        lastname (str): The player's last name.
        birthdate (str): The player's birthdate in "DD-MM-YYYY" format.
        national_id (str): The player's national chess ID (e.g., "AB12345").
        score (int): The cumulative score across all tournaments (default 0).

    Methods:
        to_dict(): Return a dictionary representation of the player.
    """

    def __init__(self, firstname, lastname, birthdate, national_id, score=0):
        """Initialize a Player with given attributes.

        Args:
            firstname (str): The player's first name.
            lastname (str): The player's last name.
            birthdate (str): The player's birthdate in "DD-MM-YYYY" format.
            national_id (str): The player's national chess ID (e.g., "AB12345").
            score (int, optional): The initial score. Defaults to 0.
        """
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate  # Format: "DD-MM-YYYY"
        self.national_id = national_id  # e.g., "AB12345"
        self.score = score  # Cumulative score across tournaments

    def to_dict(self):
        """Return a dictionary representation of the player.

        Returns:
            dict: A dictionary containing player attributes.
        """
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "national_id": self.national_id,
            "score": self.score
        }


class Match:
    """A class representing a chess match between two players.

    Attributes:
        players (list): List of [player, score] pairs for the two players.
        white_player (int): Index (0 or 1) indicating the white player.
        is_finished (bool): Whether the match has concluded.

    Methods:
        set_result(winner_idx): Set the match result based on winner index.
        to_dict(): Return a dictionary representation of the match.
        from_dict(cls, data, players_by_id): Reconstruct a Match from dictionary data.
    """

    def __init__(self, player1, player2):
        """Initialize a Match with two players and random white/black assignment.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        """
        self.players = [[player1, 0], [player2, 0]]  # [player, score]
        self.white_player = random.choice([0, 1])
        self.is_finished = False

    def set_result(self, winner_idx=None):
        """Set the match result based on winner index (0, 1, or None for draw).

        Args:
            winner_idx (int, optional): Index of the winning player (0 or 1). None for draw.
        """
        if winner_idx is not None:
            self.players[winner_idx][1] = 1  # Winner gets 1 point
            self.players[1 - winner_idx][1] = 0  # Loser gets 0
        else:
            self.players[0][1] = 0.5  # Draw, both get 0.5
            self.players[1][1] = 0.5
        self.is_finished = True

    def to_dict(self):
        """Return a dictionary representation of the match.

        Returns:
            dict: A dictionary containing match details.
        """
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
        """Reconstruct a Match from dictionary data.

        Args:
            data (dict): Dictionary containing match data.
            players_by_id (dict): Mapping of national_ids to Player objects.

        Returns:
            Match: A reconstructed Match object.

        Raises:
            ValueError: If player data is invalid.
        """
        match = cls(None, None)
        match.white_player = data["white_player"]
        match.is_finished = data["is_finished"]
        match.players = []
        for player_data, score in data["players"]:
            if isinstance(player_data, dict):
                national_id = player_data.get("national_id", "XX00000")
                player = players_by_id.get(national_id)
                if player:
                    match.players.append([player, score])
                else:
                    match.players.append([
                        Player(**{**player_data, "national_id": national_id}), score
                    ])
            else:
                raise ValueError("Invalid player data in Match")
        return match


class Round:
    """A class representing a round in a chess tournament.

    Attributes:
        name (str): The name of the round (e.g., "Round 1").
        matches (list): List of Match objects in the round.
        start_time (str): Start time in "DD-MM-YYYY HH:MM:SS" format.
        end_time (str): End time in "DD-MM-YYYY HH:MM:SS" format, or None if ongoing.

    Methods:
        finish(): Set the end time when the round is finished.
        to_dict(): Return a dictionary representation of the round.
        from_dict(cls, data, players_by_id): Reconstruct a Round from dictionary data.
    """

    def __init__(self, name):
        """Initialize a Round with a name and timestamps.

        Args:
            name (str): The name of the round (e.g., "Round 1").
        """
        self.name = name  # e.g., "Round 1"
        self.matches = []
        self.start_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.end_time = None

    def finish(self):
        """Set the end time when the round is finished."""
        self.end_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        """Return a dictionary representation of the round.

        Returns:
            dict: A dictionary containing round details.
        """
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data, players_by_id):
        """Reconstruct a Round from dictionary data.

        Args:
            data (dict): Dictionary containing round data.
            players_by_id (dict): Mapping of national_ids to Player objects.

        Returns:
            Round: A reconstructed Round object.
        """
        round_obj = cls(data["name"])
        round_obj.start_time = data["start_time"]
        round_obj.end_time = data["end_time"]
        for match_data in data["matches"]:
            round_obj.matches.append(Match.from_dict(match_data, players_by_id))
        return round_obj


class Tournament:
    """A class representing a chess tournament with multiple rounds and players.

    Attributes:
        name (str): The name of the tournament.
        location (str): The location of the tournament.
        start_date (str): The start date in "DD-MM-YYYY" format.
        end_date (str): The end date in "DD-MM-YYYY" format, or None if ongoing.
        number_of_rounds (int): The total number of rounds (default 4).
        current_round (int): The current round number.
        rounds (list): List of Round objects.
        players (list): List of Player objects participating.
        description (str): Optional description of the tournament.
        all_possible_pairs (list): List of all possible player pairings.

    Methods:
        to_dict(): Return a dictionary representation of the tournament.
        add_players_from_database(available_players): Add players from the database.
        generate_pairs(): Generate pairs for the current round based on scores.
        start_round(): Start a new round if conditions are met.
        finish_round(): Finish the current round if conditions are met.
        end_tournament(): End the tournament if all rounds are completed.
    """

    def __init__(self, name, location, start_date, description=""):
        """Initialize a Tournament with given attributes.

        Args:
            name (str): The name of the tournament.
            location (str): The location of the tournament.
            start_date (str): The start date in "DD-MM-YYYY" format.
            description (str, optional): Optional description. Defaults to "".
        """
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
        """Return a dictionary representation of the tournament.

        Returns:
            dict: A dictionary containing tournament details.
        """
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
        """Add players from the database to the tournament.

        Args:
            available_players (list): List of Player objects from the database.

        Returns:
            None
        """
        self.players = [Player(**player.to_dict()) for player in available_players]
        self.all_possible_pairs = []
        if len(self.players) >= 2:
            for i in range(len(self.players)):
                for j in range(i + 1, len(self.players)):
                    pair = tuple(sorted([
                        self.players[i].national_id, self.players[j].national_id
                    ]))
                    self.all_possible_pairs.append(pair)

    def generate_pairs(self):
        """Generate pairs for the current round based on scores.

        Returns:
            list: List of (player1, player2) tuples for the round.
        """
        if not self.players or len(self.players) < 2:
            return []
        if self.current_round == 0:
            used_pairs = set()
            pairs = []
            remaining_pairs = self.all_possible_pairs.copy()
            random.shuffle(remaining_pairs)
            for pair in remaining_pairs:
                if len(pairs) >= (len(self.players) + 1) // 2:
                    break
                p1_id, p2_id = pair
                p1 = next((p for p in self.players if p.national_id == p1_id), None)
                p2 = next((p for p in self.players if p.national_id == p2_id), None)
                if p1 and p2:
                    pair_key = tuple(sorted([p1.national_id, p2.national_id]))
                    if pair_key not in used_pairs:
                        pairs.append((p1, p2))
                        used_pairs.add(pair_key)
            return pairs
        else:
            self.players.sort(key=lambda p: p.score, reverse=True)
            pairs = []
            used_pairs = set()
            for round_obj in self.rounds:
                for match in round_obj.matches:
                    p1, p2 = match.players
                    if isinstance(p1[0], dict):
                        p1 = [Player(**{k: v for k, v in p1[0].items() if k in [
                            "firstname", "lastname", "birthdate", "national_id", "score"
                        ]}), p1[1]]
                    if isinstance(p2[0], dict):
                        p2 = [Player(**{k: v for k, v in p2[0].items() if k in [
                            "firstname", "lastname", "birthdate", "national_id", "score"
                        ]}), p2[1]]
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
                    for j in range(i + 2, len(self.players), 2):
                        if j + 1 >= len(self.players):
                            break
                        alt_player2 = self.players[j]
                        alt_pair_key = tuple(sorted([
                            player1.national_id, alt_player2.national_id
                        ]))
                        if alt_pair_key not in used_pairs:
                            pairs.append((player1, alt_player2))
                            break
            return pairs

    def start_round(self):
        """Start a new round if conditions are met.

        Returns:
            bool: True if round started, False otherwise.
        """
        if self.current_round >= self.number_of_rounds:
            return False
        if self.end_date:
            return False
        round_name = f"Round {self.current_round + 1}"
        new_round = Round(round_name)
        pairs = self.generate_pairs()
        if not pairs:
            return False
        for player1, player2 in pairs:
            new_round.matches.append(Match(player1, player2))
        self.rounds.append(new_round)
        self.current_round += 1
        return True

    def finish_round(self):
        """Finish the current round if conditions are met.

        Returns:
            bool: True if round finished, False otherwise.
        """
        if not self.rounds or self.current_round == 0:
            return False
        if self.end_date:
            return False
        current_round = self.rounds[-1]
        current_round.finish()
        return True

    def end_tournament(self):
        """End the tournament if all rounds are completed.

        Returns:
            bool: True if tournament ended, False otherwise.
        """
        if not self.end_date and self.current_round >= self.number_of_rounds:
            self.end_date = datetime.now().strftime("%d-%m-%Y")
            return True
        return False


class Database:
    """A class handling database operations for players and tournaments.

    Attributes:
        players_dir (str): Path to the directory storing player data.
        tournaments_dir (str): Path to the directory storing tournament data.

    Methods:
        ensure_directories(): Ensure data directories exist.
        load_players(): Load players from players.json.
        save_players(players): Save players to players.json.
        load_tournament(tournament_name): Load a tournament from its JSON file.
        save_tournament(tournament): Save a tournament to its JSON file.
    """

    def __init__(self):
        """Initialize the Database with directory paths."""
        self.players_dir = "data/players"
        self.tournaments_dir = "data/tournaments"

    def ensure_directories(self):
        """Ensure data directories exist."""
        os.makedirs(self.players_dir, exist_ok=True)
        os.makedirs(self.tournaments_dir, exist_ok=True)

    def load_players(self):
        """Load players from players.json.

        Returns:
            list: List of Player objects.
        """
        players_file = os.path.join(self.players_dir, "players.json")
        if os.path.exists(players_file):
            with open(players_file, "r") as file:
                data = json.load(file)
                return [Player(**player) for player in data]
        return []

    def save_players(self, players):
        """Save players to players.json.

        Args:
            players (list): List of Player objects to save.

        Returns:
            None
        """
        self.ensure_directories()
        players_file = os.path.join(self.players_dir, "players.json")
        with open(players_file, "w") as file:
            json.dump([player.to_dict() for player in players], file, indent=4)

    def load_tournament(self, tournament_name):
        """Load a tournament from its JSON file.

        Args:
            tournament_name (str): Name of the tournament file (without .json).

        Returns:
            Tournament: A reconstructed Tournament object, or None if not found.
        """
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament_name}.json")
        if os.path.exists(tournament_file):
            with open(tournament_file, "r") as file:
                data = json.load(file)
                tournament = Tournament(
                    data["name"],
                    data["location"],
                    data["start_date"],
                    data["description"]
                )
                tournament.end_date = data["end_date"]
                tournament.number_of_rounds = data["number_of_rounds"]
                tournament.current_round = data["current_round"]
                players_by_id = {
                    p.national_id: p
                    for p in [Player(**player) for player in data["players"]]
                }
                tournament.rounds = [Round.from_dict(r, players_by_id) for r in data["rounds"]]
                tournament.players = [Player(**player) for player in data["players"]]
                return tournament
        return None

    def save_tournament(self, tournament):
        """Save a tournament to its JSON file.

        Args:
            tournament (Tournament): The Tournament object to save.

        Returns:
            None
        """
        self.ensure_directories()
        tournament_file = os.path.join(self.tournaments_dir, f"{tournament.name}.json")
        with open(tournament_file, "w") as file:
            json.dump(tournament.to_dict(), file, indent=4)
