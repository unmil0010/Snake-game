# Snake Game

A classic grid-based Snake game written in Python with the standard-library `turtle` graphics module.

## Features

- Keyboard controls: **W/A/S/D** or the arrow keys
- Food collection and score tracking
- High-score tracking during the current run
- Snake growth after eating food
- Wall and self-collision detection
- Increasing game speed as the score grows
- Press **R** to restart after a game over

## Requirements

- Python 3.9 or newer
- A desktop environment with Tk support (the `turtle` module uses Tkinter)

There are no third-party runtime dependencies.

## Run the game

Clone the repository and enter its directory:

```bash
git clone https://github.com/unmil0010/Snake-game.git
cd Snake-game
python snake.py
```

On some systems, use `python3 snake.py` instead.

## Controls

| Key | Action |
| --- | --- |
| W / Up | Move up |
| S / Down | Move down |
| A / Left | Move left |
| D / Right | Move right |
| R | Restart after game over |

The game starts paused until a direction key is pressed.

## Run tests

Install the development test dependency and run pytest:

```bash
python -m pip install pytest
python -m pytest
```

The automated tests cover the direction rules, movement calculations, round reset behavior, and food placement.

## Project structure

```text
.
├── snake.py
├── tests/
│   └── test_game_logic.py
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```

## Contributing

Bug reports, suggestions, and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before making changes.

## Security

Please see [SECURITY.md](SECURITY.md) for responsible vulnerability reporting.

## License

No license has been added yet. Until a license is selected and included, normal copyright restrictions apply; please do not assume the code is available for unrestricted reuse.
