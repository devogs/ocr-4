"""
main.py

The entry point script for the chess tournament management system.
Imports and runs the controller module.

Usage:
    Run the application:
        $ python3 main.py
"""

from controller import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.run()
