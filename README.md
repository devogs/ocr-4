# Chess Tournament Management System

A Python-based application for managing chess tournaments, including player registration, match scheduling, round management, and report generation. This system adheres to PEP 8 style guidelines with a maximum line length of 119 characters, validated using `flake8` and reported via `flake8-html`.

## Overview

This project provides a command-line interface to:
- Register players with personal details and lifetime scores.
- Create and manage chess tournaments with multiple rounds.
- Schedule matches based on player scores and pairing history.
- Generate reports on players, tournaments, and detailed match results.
- Persist data in a file-based database structure.

The system is designed for flexibility and ease of use, suitable for small to medium-sized chess tournaments.

## Features

- **Player Management**: Add and store player details (name, birthdate, national ID, score).
- **Tournament Creation**: Initialize tournaments with location, start date, and description.
- **Round Management**: Start, finish, and end rounds with automated pairing and scoring.
- **Global Score Tracking**: Update player lifetime scores based on tournament performance.
- **Reporting**: View lists of players, tournaments, and detailed tournament statistics.
- **Data Persistence**: Save and load data using JSON files in a structured directory.

## Directory Structure

```
ChessTournament/
├── data/
│   ├── players/          # Stores players.json with player data.
│   └── tournaments/      # Stores individual tournament files (e.g., EUChessTour.json).
├── model.py             # Defines data models (Player, Match, Round, Tournament, Database).
├── controller.py        # Manages application logic and user interactions.
├── view.py              # Handles user interface and input/output operations.
├── flake8_rapport/      # Contains the flake8-html report validating PEP 8 compliance.
├── .flake8              # Configuration file for flake8 (max-line-length = 119).
├── README.md            # This file.
└── requirements.txt     # List of dependencies (to be generated).
```

## Installation

### Prerequisites
- Python 3.6 or higher.
- `pip` for installing dependencies.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/devogs/ocr-4.git
   cd ocr-4
   ```

2. **Install Dependencies**:
   Install using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**:
   Check `flake8` and `flake8-html` versions:
   ```bash
   flake8 --version
   flake8-html --version
   ```

## Usage

### Running the Application
Launch the application from the command line:
```bash
python3 main.py
```

### Interactive Menu
Follow the on-screen menu:
- **1. Add players**: Enter player details to register them.
- **2. Create a new tournament**: Set up a new tournament with details.
- **3. Manage existing tournament**: Load and manage an unfinished tournament.
- **4. Manage tournament rounds**: Start, finish, or end rounds.
- **5. Generate reports**: View player lists, tournament lists, or details.
- **6. Exit**: Quit the application.

### Example Workflow
1. Add players (e.g., "John Doe", "Jane Smith").
2. Create a tournament (e.g., "EU Chess Open", "Paris", "06-03-2025").
3. Manage rounds to schedule matches and input results.
4. Generate reports to review tournament progress.
5. Saved data are automatically added to the `data/` directory.

## PEP 8 Compliance
- The codebase adheres to PEP 8 with a maximum line length of 119 characters.
- Run `flake8` to verify:
  ```bash
  flake8 . --max-line-length=119
  ```
- Generate an HTML compliance report:
  ```bash
  flake8 . --max-line-length=119 --format=html --htmldir=flake8_rapport
  ```
- The `flake8_rapport/index.html` file should show no errors, validating compliance.

## Author

- **Mathieu Patoz** - Initial development and PEP 8 compliance.
- **Updated**: March 06, 2025