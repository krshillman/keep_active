# Keep Active

A Python utility to prevent screen timeout and system inactivity by simulating mouse activity.

## Features

- Moves mouse to screen center at random intervals (30-60 seconds by default)
- Performs double-click to simulate user activity
- Configurable timing and behavior
- Failsafe enabled by default (move mouse to top-left corner to abort)
- Fully typed with comprehensive documentation
- Modular architecture for easy testing and customization

## Installation

```bash
# Using uv
uv sync

# Or with pip
pip install -e .
```

## Usage

```bash
# Run directly
python main.py

# Or after installation
keep-active
```

Press `Ctrl+C` to stop the script.

## Configuration

You can customize the behavior by modifying the configuration in `main.py`:

```python
from keep_active import KeepActiveConfig, KeepActiveController

config = KeepActiveConfig(
    min_wait_seconds=20,      # Minimum wait between actions
    max_wait_seconds=40,      # Maximum wait between actions
    mouse_move_duration=0.3,  # Mouse movement animation time
    post_click_pause=0.2,     # Pause after clicking
    enable_failsafe=True,     # Enable corner abort
    verbose=True,             # Enable logging output
)

controller = KeepActiveController(config=config)
controller.run()
```

## Development

Install development dependencies:

```bash
uv sync --extra dev
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=keep_active
```

## Project Structure

```
keep_active/
├── keep_active/
│   ├── __init__.py     # Package exports
│   ├── config.py       # Configuration dataclass
│   ├── mouse.py        # Mouse operations (Protocol + implementation)
│   └── controller.py   # Main controller logic
├── tests/
│   ├── test_config.py     # Configuration tests
│   ├── test_mouse.py      # Mouse operations tests
│   └── test_controller.py # Controller tests
├── main.py             # Entry point
└── pyproject.toml      # Project configuration
```

## License

MIT
