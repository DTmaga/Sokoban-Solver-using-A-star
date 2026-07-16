# Sokoban Solver using A*

An interactive Sokoban puzzle solver that uses the A* search algorithm to automatically find solutions. The project also provides a Pygame-based graphical interface for manual gameplay and AI visualization.

## Features

* A* search algorithm for solving Sokoban puzzles
* Custom heuristic based on misplaced boxes
* Deadlock detection to prune invalid states
* Interactive GUI built with Pygame
* Manual and AI play modes
* Map loading from text files
* Execution statistics:

  * Execution time
  * Solution length
  * Expanded nodes
  * Maximum frontier size
* Move counter and best score tracking
* Customizable game appearance by replacing images in the `assets/` folder

## Technologies

* Python
* Pygame

## Project Structure

```text
.
├── assets/
│   ├── agent.png
│   ├── box.png
│   ├── box_on_goal.png
│   ├── floor.png
│   ├── goal.png
│   └── wall.png
├── example_map.txt
├── main.py
└── README.md
```

## How to Run

```bash
pip install pygame
python main.py
```

Make sure `example_map.txt` and the `assets/` folder are located in the project directory before running the application.

## Controls

| Key / Button | Action                                  |
| ------------ | --------------------------------------- |
| ↑ ↓ ← →      | Move the player                         |
| AI MODE      | Automatically solve the puzzle using A* |
| RESET        | Restart the current map                 |
| QUIT         | Exit the application                    |

## Customization

The game's appearance can be customized by replacing the image files inside the `assets/` folder while keeping their original filenames.

Replaceable assets include:

* `agent.png`
* `box.png`
* `box_on_goal.png`
* `floor.png`
* `goal.png`
* `wall.png`

## Screenshots

Add gameplay screenshots or GIFs here.

## Author

Vo Huynh Duy Tan
