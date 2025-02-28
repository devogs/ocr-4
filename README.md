# Chess Tournament Management System

## Introduction
This application is a chess tournament management system written in Python. It follows the Model-View-Controller (MVC) design pattern and allows users to organize chess tournaments, manage players, generate match pairings, record results, and display rankings.

## Features
- Offline functionality
- JSON-based data storage for players and tournaments
- Tournament rounds and match pairings generation
- Automatic ranking updates based on match results
- Simple CLI interface
- Compliance with PEP 8 coding standards

## Installation
### Prerequisites
Ensure you have Python installed (>=3.7). Install the required dependencies using:

```sh
pip install -r requirements.txt
```

## Usage
### Running the Application
To start the application, execute the following command:

```sh
python main.py
```

### Features
1. **Adding Players:**
   - Players can be manually added with their details (last name, first name, birth date, and identifier).

2. **Creating a Tournament:**
   - A new tournament can be initialized with a name, location, start & end dates, and number of rounds.

3. **Generating Tournament Rounds:**
   - The system generates match pairings using a Swiss-system format.

4. **Recording Match Results:**
   - After each round, results can be entered, updating players' points.

5. **Displaying Rankings:**
   - A leaderboard is displayed based on players' total points.

6. **Saving and Loading Tournaments:**
   - Tournament data is stored in `data/tournament.json` for persistence.

## Code Structure
The project follows the MVC architecture:
- `models.py` - Contains Player, Tournament, and Round classes.
- `controllers.py` - Handles tournament logic and player management.
- `views.py` - Provides a CLI for user interaction.
- `file_manager.py` - Manages JSON-based data storage.
- `main.py` - Entry point of the application.

## Linting and Code Quality
The project adheres to PEP 8 standards. To check for linting errors, run:

```sh
flake8 --max-line-length=119 --format=html --htmldir=flake8_report
```

This will generate an HTML report in the `flake8_report` directory.

## Future Improvements
- Implementing a GUI
- Exporting reports in CSV/HTML format
- Online database integration

