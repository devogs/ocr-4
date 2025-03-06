"""
view.py

A module handling the user interface and input/output operations for the chess tournament
management system. Provides menus, prompts, and display functions for user interaction.

Directory Structure:
    data/
        players/ - Directory for storing player data (players.json).
        tournaments/ - Directory for storing tournament data (e.g., EUChessTour.json).

Usage:
    Import and use with the Controller class:
        $ python3 -m controller

Classes:
    View: Handles all user interface and input/output operations.

Author:
    Mathieu Patoz
    Updated: March 06, 2025
"""

import random


class View:
    """A class handling user interface and input/output operations for the application.

    Attributes:
        None: All methods are stateless and operate on input parameters.

    Methods:
        display_menu(): Display the main menu and get user choice.
        display_round_management_menu(): Display the round management menu and get user choice.
        display_reports_menu(): Display the reports menu and get user choice.
        get_tournament_info(): Get tournament details from user input.
        get_player_info(): Get player details from user input.
        display_players(players): Display a sorted list of players with lifetime scores.
        display_tournaments(tournaments): Display a list of all tournaments.
        display_unfinished_tournaments(tournaments): Display a list of unfinished tournaments.
        display_tournament_details(tournament): Display detailed information about a tournament.
        display_message(message): Display a message to the user.
        get_choice(prompt): Get a choice from the user with a custom prompt.
        get_match_result(player1, player2): Get the result of a match from user input.
        confirm_end_tournament(): Confirm with the user to end the tournament.
        select_tournament(tournaments): Allow user to select a tournament from a list.
    """

    def display_menu(self):
        """Display the main menu and get user choice.

        Returns:
            str: The user's menu choice (1-6).
        """
        print("\n=== Chess Tournament Management ===")
        print("1. Add players")
        print("2. Create a new tournament")
        print("3. Manage existing tournament")
        print("4. Manage tournament rounds")
        print("5. Generate reports")
        print("6. Exit")
        return input("Choose an option (1-6): ")

    def display_round_management_menu(self):
        """Display the round management menu and get user choice.

        Returns:
            str: The user's menu choice (1-4).
        """
        print("\nRound Management:")
        print("1. Start next round")
        print("2. Finish current round")
        print("3. End tournament")
        print("4. Back to main menu")
        return input("Choose an option (1-4): ")

    def display_reports_menu(self):
        """Display the reports menu and get user choice.

        Returns:
            str: The user's menu choice (1-4).
        """
        print("\nReports:")
        print("1. List all players (alphabetical)")
        print("2. List all tournaments")
        print("3. Show details of a specific tournament")
        print("4. Back to main menu")
        return input("Choose an option (1-4): ")

    def get_tournament_info(self):
        """Get tournament details from user input.

        Returns:
            tuple: (name, location, start_date, description) as strings.
        """
        name = input("Enter tournament name: ")
        location = input("Enter tournament location: ")
        start_date = input("Enter tournament start date (DD-MM-YYYY): ")
        description = input("Enter tournament description (optional): ")
        return name, location, start_date, description

    def get_player_info(self):
        """Get player details from user input.

        Returns:
            tuple: (firstname, lastname, birthdate, national_id) as strings.
        """
        firstname = input("Enter player firstname: ")
        lastname = input("Enter player lastname: ")
        birthdate = input("Enter player birthdate (DD-MM-YYYY): ")
        national_id = input("Enter player national chess ID (e.g., AB12345): ")
        return firstname, lastname, birthdate, national_id

    def display_players(self, players):
        """Display a sorted list of players with lifetime scores.

        Args:
            players (list): List of Player objects to display.

        Returns:
            None
        """
        print("\nPlayers (alphabetical by lastname, firstname) with Lifetime Scores:")
        sorted_players = sorted(players, key=lambda p: (p.lastname, p.firstname))
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.lastname}, {player.firstname} (ID: {player.national_id}, "
                  f"Birthdate: {player.birthdate}, Lifetime Score: {player.score})")

    def display_tournaments(self, tournaments):
        """Display a list of all tournaments.

        Args:
            tournaments (list): List of Tournament objects to display.

        Returns:
            None
        """
        if not tournaments or tournaments is None:
            print("\nNo tournaments available.")
            return
        print("\nTournaments:")
        for i, t in enumerate(tournaments, 1):
            print(f"{i}. {t.name} ({t.location}, {t.start_date} - {t.end_date or 'Ongoing'})")

    def display_unfinished_tournaments(self, tournaments):
        """Display a list of unfinished tournaments.

        Args:
            tournaments (list): List of Tournament objects to filter.

        Returns:
            list: List of unfinished Tournament objects, or None if none available.
        """
        unfinished_tournaments = [t for t in tournaments if t.end_date is None]
        if not unfinished_tournaments:
            print("\nNo unfinished tournaments available.")
            return None
        print("\nUnfinished Tournaments:")
        for i, t in enumerate(unfinished_tournaments, 1):
            print(f"{i}. {t.name} ({t.location}, {t.start_date} - {t.end_date or 'Ongoing'})")
        return unfinished_tournaments

    def display_tournament_details(self, tournament):
        """Display detailed information about a specific tournament.

        Args:
            tournament (Tournament): The Tournament object to display.

        Returns:
            None
        """
        if not tournament:
            print("\nNo tournament available.")
            return
        print(f"\nTournament: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Dates: {tournament.start_date} - {tournament.end_date or 'Ongoing'}")
        print(f"Description: {tournament.description}")
        print(f"Number of Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round}")
        self.display_players(tournament.players)
        print("\nRounds and Matches:")
        for round_obj in tournament.rounds:
            print(f"{round_obj.name} ({round_obj.start_time} - {round_obj.end_time or 'Ongoing'})")
            for match in round_obj.matches:
                p1, p2 = match.players
                white = "White" if match.white_player == 0 else "Black"
                black = "Black" if match.white_player == 0 else "White"
                print(f"  - {p1[0].lastname}, {p1[0].firstname} ({white}) vs "
                      f"{p2[0].lastname}, {p2[0].firstname} ({black})")
                print(f"    Scores: {p1[1]} - {p2[1]}")

    def display_message(self, message):
        """Display a message to the user.

        Args:
            message (str): The message to display.

        Returns:
            None
        """
        print(message)

    def get_choice(self, prompt):
        """Get a choice from the user with a custom prompt.

        Args:
            prompt (str): The prompt message for user input.

        Returns:
            str: The user's input response.
        """
        return input(prompt)

    def get_match_result(self, player1, player2):
        """Get the result of a match from user input.

        Args:
            player1 (Player): The first player in the match.
            player2 (Player): The second player in the match.

        Returns:
            int or None: 0 for player1 win, 1 for player2 win, None for draw.
        """
        print(f"\nMatch: {player1.lastname}, {player1.firstname} vs {player2.lastname}, "
              f"{player2.firstname}")
        print("Default outcome is a win/loss (press 1 for Player 1 win, 2 for Player 2 "
              "win).")
        print("To specify a draw, type 'draw' and confirm twice (very rare in chess "
              "tournaments):")
        while True:
            choice = input(
                "Choice (1/2) or 'draw': ").lower()
            if choice in ["1", "2"]:
                return 0 if choice == "1" else 1
            elif choice == "draw":
                confirm = input(
                    "Are you sure this is a draw? Type 'confirm' to proceed, "
                    "or press Enter to default to win/loss: ").lower()
                if confirm == "confirm":
                    second_confirm = input(
                        "Confirm draw again (type 'confirm' or press "
                        "Enter to default to win/loss): ").lower()
                    if second_confirm == "confirm":
                        return None
                default_choice = random.choice(["1", "2"])
                print(f"Defaulting to {default_choice} (win/loss) due to lack of "
                      "confirmation for draw.")
                return 0 if default_choice == "1" else 1
            else:
                print("Invalid choice, try again (use 1, 2, or 'draw').")

    def confirm_end_tournament(self):
        """Confirm with the user to end the tournament.

        Returns:
            bool: True if confirmed, False otherwise.
        """
        return input("End tournament? (yes/no): ").lower() == "yes"

    def select_tournament(self, tournaments):
        """Allow user to select a tournament from a list.

        Args:
            tournaments (list): List of Tournament objects to choose from.

        Returns:
            Tournament: The selected Tournament object, or None if cancelled.
        """
        if not tournaments or tournaments is None:
            print("\nNo tournaments available.")
            return None
        self.display_tournaments(tournaments)
        while True:
            try:
                choice = int(input("Select a tournament by number (or 0 to cancel): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(tournaments):
                    return tournaments[choice - 1]
                print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a number.")
