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
* Customizable game assets
* Support for custom maps

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

Make sure the `assets/` folder and a map file (default: `example_map.txt`) are located in the project directory before running the application.

## Controls

| Key / Button | Action                                  |
| ------------ | --------------------------------------- |
| ↑ ↓ ← →      | Move the player                         |
| AI MODE      | Automatically solve the puzzle using A* |
| RESET        | Restart the current map                 |
| QUIT         | Exit the application                    |

## Customization

### Game Assets

Customize the game's appearance by replacing the image files inside the `assets/` folder while keeping their original filenames.

Replaceable assets include:

* `agent.png`
* `box.png`
* `box_on_goal.png`
* `floor.png`
* `goal.png`
* `wall.png`

### Custom Maps

You can create your own Sokoban maps by either:

* Editing the contents of `example_map.txt`, or
* Loading another map file by changing the file path in `main.py`:

```python
grid = load_map("your_map.txt")
```

## Screenshots

<img width="698" height="587" alt="image" src="https://github.com/user-attachments/assets/0b9cd0ed-068c-4d1f-be6a-76a7a48f207b" />


## Author

**Vo Huynh Duy Tan**
