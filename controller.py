from model import Player, Tournament, Database
from view import View
import os

class Controller:
    def __init__(self):
        self.db = Database()
        self.tournament = None
        self.players = self.db.load_players()
        self.view = View()  # Explicitly set view for use in model methods

    def create_tournament(self):
        name, location, start_date, description = self.view.get_tournament_info()
        self.tournament = Tournament(name, location, start_date, description)
        self.tournament.add_players_from_database(self.players)  # Add all players from database
        self.db.save_tournament(self.tournament)
        self.view.display_message(f"Tournament '{name}' created successfully with {len(self.tournament.players)} players!")

    def add_players(self):
        firstname, lastname, birthdate, national_id = self.view.get_player_info()
        player = Player(firstname, lastname, birthdate, national_id)
        self.players.append(player)
        self.db.save_players(self.players)
        self.view.display_message("Player added successfully!")

    def update_global_scores(self):
        """Update global player scores based on the current tournament's scores."""
        if self.tournament:
            for tour_player in self.tournament.players:
                # Find the corresponding player in self.players by national_id
                global_player = next((p for p in self.players if p.national_id == tour_player.national_id), None)
                if global_player:
                    global_player.score += tour_player.score  # Increment global score
            self.db.save_players(self.players)  # Save updated global scores to players.json

    def manage_rounds(self):
        if not self.tournament:
            self.view.display_message("Please create a tournament first!")
            return
        if not self.tournament.players:
            self.view.display_message("No players registered for the tournament! Add players first.")
            return

        while True:
            choice = self.view.display_round_management_menu()

            if choice == "1":
                # Start next round and save the updated tournament regardless of the result
                if self.tournament.start_round():
                    self.db.save_tournament(self.tournament)
                    self.view.display_message(f"Round {self.tournament.current_round} started!")
                else:
                    self.db.save_tournament(self.tournament)  # Save even if no pairs are generated
                    self.view.display_message("No pairs could be generated for this round or the tournament is complete!")
            elif choice == "2":
                if self.tournament.finish_round():
                    # Get match results interactively for all unfinished matches
                    current_round = self.tournament.rounds[-1]
                    for match in current_round.matches:
                        if not match.is_finished:
                            self.view.display_message(f"Match: {match.players[0][0].lastname}, {match.players[0][0].firstname} vs {match.players[1][0].lastname}, {match.players[1][0].firstname}")
                            winner_idx = self.view.get_match_result(match.players[0][0], match.players[1][0])
                            match.set_result(winner_idx)
                            # Update tournament scores after setting result
                            for player, score in match.players:
                                player.score += score
                    self.db.save_tournament(self.tournament)
                    self.update_global_scores()  # Update and save global scores after each round
                    self.view.display_message(f"Round {self.tournament.current_round} finished!")
                else:
                    self.view.display_message("No round to finish!")
            elif choice == "3":
                if self.view.confirm_end_tournament():
                    if self.tournament.end_tournament():
                        self.db.save_tournament(self.tournament)
                        self.update_global_scores()  # Update and save global scores when ending tournament
                        self.view.display_message(f"Tournament '{self.tournament.name}' ended on {self.tournament.end_date}!")
                    else:
                        self.view.display_message("Cannot end tournament: it must have completed all rounds or already ended.")
            elif choice == "4":
                break  # Return to main menu
            else:
                self.view.display_message("Invalid option, try again.")

    def manage_existing_tournament(self):
        # Load all tournaments from data/tournaments directory
        tournaments = []
        for filename in os.listdir(self.db.tournaments_dir):
            if filename.endswith('.json'):
                tournament_name = filename[:-5]  # Remove '.json' extension
                tournament = self.db.load_tournament(tournament_name)
                if tournament:
                    tournaments.append(tournament)
        
        # Display and select an unfinished tournament
        unfinished_tournaments = self.view.display_unfinished_tournaments(tournaments)
        if unfinished_tournaments is None:
            self.view.display_message("No unfinished tournaments available.")
            return

        try:
            # Prompt user to select an unfinished tournament
            choice = int(input("Select an unfinished tournament by number (or 0 to cancel): "))
            if choice == 0:
                self.view.display_message("Returning to main menu.")
                return
            if 1 <= choice <= len(unfinished_tournaments):
                self.tournament = unfinished_tournaments[choice - 1]
                self.db.save_tournament(self.tournament)  # Save the loaded tournament to ensure persistence
                self.view.display_message(f"Loaded tournament: {self.tournament.name}")
                self.manage_rounds()  # Manage the selected tournament's rounds
            else:
                self.view.display_message("Invalid choice, returning to main menu.")
        except ValueError:
            self.view.display_message("Please enter a number, returning to main menu.")

    def generate_reports(self):
        if not self.players and not self.tournament:
            self.view.display_message("No data available for reports!")
            return

        while True:
            choice = self.view.display_reports_menu()

            if choice == "1":
                self.view.display_players(self.players)  # List all players (alphabetical by lastname, firstname) with global scores
            elif choice == "2":
                # Load all tournaments from data/tournaments directory
                tournaments = []
                for filename in os.listdir(self.db.tournaments_dir):
                    if filename.endswith('.json'):
                        tournament_name = filename[:-5]  # Remove '.json' extension
                        tournament = self.db.load_tournament(tournament_name)
                        if tournament:
                            tournaments.append(tournament)
                self.view.display_tournaments(tournaments)  # List all tournaments
            elif choice == "3":
                # Show details of a specific tournament
                tournaments = []
                for filename in os.listdir(self.db.tournaments_dir):
                    if filename.endswith('.json'):
                        tournament_name = filename[:-5]  # Remove '.json' extension
                        tournament = self.db.load_tournament(tournament_name)
                        if tournament:
                            tournaments.append(tournament)
                selected_tournament = self.view.select_tournament(tournaments)
                if selected_tournament:
                    self.view.display_tournament_details(selected_tournament)  # Show name, dates, players, rounds, and matches
            elif choice == "4":
                break
            else:
                self.view.display_message("Invalid option, try again.")

    def run(self):
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