class View:
    def display_menu(self):
        print("\n=== Chess Tournament Management ===")
        print("1. Add players")
        print("2. Create a new tournament")
        print("3. Manage existing tournament")
        print("4. Manage tournament rounds")
        print("5. Generate reports")
        print("6. Exit")
        return input("Choose an option (1-6): ")

    def display_round_management_menu(self):
        print("\nRound Management:")
        print("1. Start next round")
        print("2. Finish current round")
        print("3. End tournament")
        print("4. Back to main menu")
        return input("Choose an option (1-4): ")

    def display_reports_menu(self):
        print("\nReports:")
        print("1. List all players (alphabetical)")
        print("2. List all tournaments")
        print("3. Show details of a specific tournament")
        print("4. Back to main menu")
        return input("Choose an option (1-4): ")

    def get_tournament_info(self):
        name = input("Enter tournament name: ")
        location = input("Enter tournament location: ")
        start_date = input("Enter tournament start date (DD-MM-YYYY): ")
        description = input("Enter tournament description (optional): ")
        return name, location, start_date, description

    def get_player_info(self):
        firstname = input("Enter player firstname: ")
        lastname = input("Enter player lastname: ")
        birthdate = input("Enter player birthdate (DD-MM-YYYY): ")
        national_id = input("Enter player national chess ID (e.g., AB12345): ")
        return firstname, lastname, birthdate, national_id

    def display_players(self, players):
        print("\nPlayers (alphabetical by lastname, firstname) with Lifetime Scores:")
        sorted_players = sorted(players, key=lambda p: (p.lastname, p.firstname))
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.lastname}, {player.firstname} (ID: {player.national_id}, Birthdate: {player.birthdate}, Lifetime Score: {player.score})")

    def display_tournaments(self, tournaments):
        if not tournaments or tournaments is None:
            print("\nNo tournaments available.")
            return
        print("\nTournaments:")
        for i, t in enumerate(tournaments, 1):  # 't' is now explicitly a tournament object
            print(f"{i}. {t.name} ({t.location}, {t.start_date} - {t.end_date or 'Ongoing'})")

    def display_unfinished_tournaments(self, tournaments):
        unfinished_tournaments = [t for t in tournaments if t.end_date is None]
        if not unfinished_tournaments:
            print("\nNo unfinished tournaments available.")
            return None
        print("\nUnfinished Tournaments:")
        for i, t in enumerate(unfinished_tournaments, 1):
            print(f"{i}. {t.name} ({t.location}, {t.start_date} - {t.end_date or 'Ongoing'})")
        return unfinished_tournaments

    def display_tournament_details(self, tournament):
        if not tournament:
            print("\nNo tournament available.")
            return
        print(f"\nTournament: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Dates: {tournament.start_date} - {tournament.end_date or 'Ongoing'}")
        print(f"Description: {tournament.description}")
        print(f"Number of Rounds: {tournament.number_of_rounds}")
        print(f"Current Round: {tournament.current_round}")
        self.display_players(tournament.players)  # List players (alphabetical by lastname, firstname) with tournament scores
        print("\nRounds and Matches:")
        for round in tournament.rounds:
            print(f"{round.name} ({round.start_time} - {round.end_time or 'Ongoing'})")
            for match in round.matches:
                p1, p2 = match.players
                white = "White" if match.white_player == 0 else "Black"
                black = "Black" if match.white_player == 0 else "White"
                print(f"  - {p1[0].lastname}, {p1[0].firstname} ({white}) vs {p2[0].lastname}, {p2[0].firstname} ({black})")
                print(f"    Scores: {p1[1]} - {p2[1]}")

    def display_message(self, message):
        print(message)

    def get_choice(self, prompt):
        return input(prompt)

    def get_match_result(self, player1, player2):
        print(f"\nMatch: {player1.lastname}, {player1.firstname} vs {player2.lastname}, {player2.firstname}")
        print("Default outcome is a win/loss (press 1 for Player 1 win, 2 for Player 2 win).")
        print("To specify a draw, type 'draw' and confirm twice (very rare in chess tournaments):")
        while True:
            choice = input("Choice (1/2) or 'draw': ").lower()
            if choice in ["1", "2"]:
                return 0 if choice == "1" else 1  # Player 1 or Player 2 wins (1-0 or 0-1)
            elif choice == "draw":
                confirm = input("Are you sure this is a draw? Type 'confirm' to proceed, or press Enter to default to win/loss: ").lower()
                if confirm == "confirm":
                    second_confirm = input("Confirm draw again (type 'confirm' or press Enter to default to win/loss): ").lower()
                    if second_confirm == "confirm":
                        return None  # Draw (0.5-0.5)
                # If not confirmed twice, default to a win/loss
                default_choice = random.choice(["1", "2"])  # Randomly default to Player 1 or Player 2 win
                print(f"Defaulting to {default_choice} (win/loss) due to lack of confirmation for draw.")
                return 0 if default_choice == "1" else 1
            else:
                print("Invalid choice, try again (use 1, 2, or 'draw').")

    def confirm_end_tournament(self):
        return input("End tournament? (yes/no): ").lower() == "yes"

    def select_tournament(self, tournaments):
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