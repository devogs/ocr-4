"""
controller.py

A module controlling the flow and logic of the chess tournament management system.
Manages user interactions, tournament creation, round management, and report generation.

Directory Structure:
    data/
        players/ - Directory for storing player data (players.json).
        tournaments/ - Directory for storing tournament data (e.g., EUChessTour.json).

Usage:
    Run the script to start the interactive menu:
        $ python3 main.py

Classes:
    Controller: Manages the application logic and user interface interactions.

Functions:
    run(): Entry point to start the application loop.

Author:
    Mathieu Patoz
    Updated: March 06, 2025
"""

from model import Player, Tournament, Database
from view import View
import os


class Controller:
    """A class managing the flow and logic of the chess tournament application.

    Attributes:
        db (Database): The database handler for player and tournament data.
        tournament (Tournament): The current tournament being managed.
        players (list): List of all Player objects.
        view (View): The view handler for user interface operations.

    Methods:
        create_tournament(): Create a new tournament and save it.
        add_players(): Add a new player to the database.
        update_global_scores(): Update global player scores from the current tournament.
        manage_rounds(): Manage the rounds of the current tournament.
        manage_existing_tournament(): Manage an existing unfinished tournament.
        generate_reports(): Generate and display reports.
        run(): Run the main application loop.
    """

    def __init__(self):
        """Initialize the Controller with database and view.

        Initializes the database, loads existing players, and sets up the view.
        """
        self.db = Database()
        self.tournament = None
        self.players = self.db.load_players()
        self.view = View()

    def create_tournament(self):
        """Create a new tournament and save it.

        Prompts the user for tournament details and initializes it with players from the
        database.

        Returns:
            None
        """
        name, location, start_date, description = self.view.get_tournament_info()
        self.tournament = Tournament(name, location, start_date, description)
        self.tournament.add_players_from_database(self.players)
        self.db.save_tournament(self.tournament)
        self.view.display_message(
            f"Tournament '{name}' created successfully with "
            f"{len(self.tournament.players)} players!"
            )

    def add_players(self):
        """Add a new player to the database.

        Prompts the user for player details and saves the new player.

        Returns:
            None
        """
        firstname, lastname, birthdate, national_id = self.view.get_player_info()
        player = Player(firstname, lastname, birthdate, national_id)
        self.players.append(player)
        self.db.save_players(self.players)
        self.view.display_message("Player added successfully!")

    def update_global_scores(self):
        """Update global player scores based on the current tournament's scores.

        Increments the global score of each player based on their tournament performance.

        Returns:
            None
        """
        if self.tournament:
            for tour_player in self.tournament.players:
                global_player = next(
                    (p for p in self.players if p.national_id == tour_player.national_id), None
                    )
                if global_player:
                    global_player.score += tour_player.score
            self.db.save_players(self.players)

    def manage_rounds(self):
        """Manage the rounds of the current tournament.

        Handles starting, finishing, and ending rounds interactively.

        Returns:
            None
        """
        if not self.tournament:
            self.view.display_message("Please create a tournament first!")
            return
        if not self.tournament.players:
            self.view.display_message(
                "No players registered for the tournament! "
                "Add players first."
                )
            return

        while True:
            choice = self.view.display_round_management_menu()

            if choice == "1":
                if self.tournament.start_round():
                    self.db.save_tournament(self.tournament)
                    self.view.display_message(
                        f"Round {self.tournament.current_round} "
                        "started!"
                        )
                else:
                    self.db.save_tournament(self.tournament)
                    self.view.display_message(
                        "No pairs could be generated for this round "
                        "or the tournament is complete!"
                        )
            elif choice == "2":
                if self.tournament.finish_round():
                    current_round = self.tournament.rounds[-1]
                    for match in current_round.matches:
                        if not match.is_finished:
                            self.view.display_message(
                                f"Match: {match.players[0][0].lastname}, "
                                f"{match.players[0][0].firstname} vs "
                                f"{match.players[1][0].lastname}, "
                                f"{match.players[1][0].firstname}"
                                )
                            winner_idx = self.view.get_match_result(
                                match.players[0][0],
                                match.players[1][0]
                                )
                            match.set_result(winner_idx)
                            for player, score in match.players:
                                player.score += score
                    self.db.save_tournament(self.tournament)
                    self.update_global_scores()
                    self.view.display_message(
                        f"Round {self.tournament.current_round} "
                        "finished!"
                        )
                else:
                    self.view.display_message("No round to finish!")
            elif choice == "3":
                if self.view.confirm_end_tournament():
                    if self.tournament.end_tournament():
                        self.db.save_tournament(self.tournament)
                        self.update_global_scores()
                        self.view.display_message(
                            f"Tournament '{self.tournament.name}' "
                            f"ended on {self.tournament.end_date}!"
                            )
                    else:
                        self.view.display_message(
                            "Cannot end tournament: it must have "
                            "completed all rounds or already ended."
                            )
            elif choice == "4":
                break
            else:
                self.view.display_message("Invalid option, try again.")

    def manage_existing_tournament(self):
        """Manage an existing unfinished tournament.

        Loads and allows management of an unfinished tournament.

        Returns:
            None
        """
        tournaments = []
        for filename in os.listdir(self.db.tournaments_dir):
            if filename.endswith('.json'):
                tournament_name = filename[:-5]
                tournament = self.db.load_tournament(tournament_name)
                if tournament:
                    tournaments.append(tournament)

        unfinished_tournaments = self.view.display_unfinished_tournaments(tournaments)
        if unfinished_tournaments is None:
            self.view.display_message("No unfinished tournaments available.")
            return

        try:
            choice = int(
                input("Select an unfinished tournament by number (or 0 to cancel): ")
                )
            if choice == 0:
                self.view.display_message("Returning to main menu.")
                return
            if 1 <= choice <= len(unfinished_tournaments):
                self.tournament = unfinished_tournaments[choice - 1]
                self.db.save_tournament(self.tournament)
                self.view.display_message(f"Loaded tournament: {self.tournament.name}")
                self.manage_rounds()
            else:
                self.view.display_message("Invalid choice, returning to main menu.")
        except ValueError:
            self.view.display_message("Please enter a number, returning to main menu.")

    def generate_reports(self):
        """Generate and display reports.

        Provides options to list players, tournaments, or detailed tournament info.

        Returns:
            None
        """
        if not self.players and not self.tournament:
            self.view.display_message("No data available for reports!")
            return

        while True:
            choice = self.view.display_reports_menu()

            if choice == "1":
                self.view.display_players(self.players)
            elif choice == "2":
                tournaments = []
                for filename in os.listdir(self.db.tournaments_dir):
                    if filename.endswith('.json'):
                        tournament_name = filename[:-5]
                        tournament = self.db.load_tournament(tournament_name)
                        if tournament:
                            tournaments.append(tournament)
                self.view.display_tournaments(tournaments)
            elif choice == "3":
                tournaments = []
                for filename in os.listdir(self.db.tournaments_dir):
                    if filename.endswith('.json'):
                        tournament_name = filename[:-5]
                        tournament = self.db.load_tournament(tournament_name)
                        if tournament:
                            tournaments.append(tournament)
                selected_tournament = self.view.select_tournament(tournaments)
                if selected_tournament:
                    self.view.display_tournament_details(selected_tournament)
            elif choice == "4":
                break
            else:
                self.view.display_message("Invalid option, try again.")

    def run(self):
        """Run the main application loop.

        Starts the interactive menu and processes user choices.

        Returns:
            None
        """
        self.view = View()
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.add_players()
            elif choice == "2":
                self.create_tournament()
            elif choice == "3":
                self.manage_existing_tournament()
            elif choice == "4":
                self.manage_rounds()
            elif choice == "5":
                self.generate_reports()
            elif choice == "6":
                self.view.display_message("Goodbye!")
                break
            else:
                self.view.display_message("Invalid option, try again.")
