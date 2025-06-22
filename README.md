# A-Maze

A classic 3D maze game built with Pygame, featuring a first-person perspective, time tracking, and customizable maps. Navigate through challenging mazes and find the exit!

## 📋 Table of Contents

* [The Engine](#-the-engine)

* [Installation & Setup](#-installation--setup)

* [Game Instructions](#-game-instructions)

* [Creating New Maps](#-creating-new-maps)

* [Future Features](#-future-features)

* [License](#-license)

## 🌟 The Engine

The game is built around a robust engine that manages different states and components, ensuring a smooth and organized gameplay experience:

* **`engine.py`**: This is the heart of the application, responsible for the main game loop. It handles initialization of Pygame, manages the display window, processes events (like keyboard input), and orchestrates transitions between different game states (e.g., main menu, map selection, gameplay, game over, pause). It acts as the central hub that updates and draws the currently active game component.

* **`game.py`**: This module manages the higher-level game states, such as the `MAP_MENU`, `GAMEPLAY`, and `GAME_OVER` states. It loads maze data, initializes the `GameLogic` for active gameplay, and creates the appropriate menu screens.

* **`game_logic/game_logic.py`**: Contains the core mechanics of the maze traversal. This is where the 3D raycasting magic happens, rendering the maze walls, applying distance-based fading, and handling the pulsating effect of the end block. It also manages the in-game timer.

* **`game_logic/player.py`**: Defines the player's properties, movement logic (forward/backward, rotation), and collision detection within the maze environment.

* **`screens/`**: This package contains all the user interface elements and different screens of the game.

  * **`menu.py`**: A base class providing common functionality for all interactive menus (like button handling and rendering).

  * **`splash_screen.py`**: Displays an initial splash screen.

  * **`main_menu.py`**: The initial menu with options to start the game or quit.

  * **`map_menu.py`**: Allows players to select from available maze maps.

  * **`pause_menu.py`**: The menu displayed when the game is paused.

  * **`game_over_menu.py`**: Shows the player's score (total time) after completing a maze and options to return to the main menu.

* **`utils/`**: Contains utility classes and modules.

  * **`constants.py`**: Stores all global constants, including color schemes, display settings, player physics, and rendering parameters. This is where you can easily tweak game values.

  * **`config_manager.py`**: Handles loading and saving game settings to a `settings.json` file, ensuring preferences persist between sessions.

## ✨ Installation & Setup

To get started with A-Maze, follow these simple steps:

1. **Clone the repository:**

2. **Install Pygame:**

3. **Run the game:**

## 🗂 Game Instructions

The objective is simple: navigate through the 3D maze from your starting point to the glowing end block. Your time will be tracked in the bottom-left corner of the screen. Try to complete the maze as quickly as possible!

### Controls

* **Move Forward:** `W` or `Up Arrow`

* **Move Backward:** `S` or `Down Arrow`

* **Turn Left:** `A` or `Left Arrow`

* **Turn Right:** `D` or `Right Arrow`

* **Pause Game:** `ESC`

* **Menu Navigation:** `Up Arrow` / `Down Arrow` to select, `Enter` to confirm.

## 🚀 Creating New Maps

You can create your own custom mazes and share them with others!
Sample maze JSON files are located in the `assets/maps/` directory. Simply create a new `.json` file in this directory, following the existing structure, and it will appear in the game's map selection menu.

## 🛠 Future Features

We plan to add exciting new features in the future, including:

* **Dynamic Map Generation:** Implement various maze generation algorithms to create new, unique mazes on the fly.

* **Scoreboard Tracking:** Keep a persistent record of your best times for each maze, allowing for competitive play.

## 📜 License

This project is licensed under the MIT License. For detailed terms and conditions, please refer to the LICENSE file included in this repository.
