#!/usr/bin/env python3
"""
Keep Active - Entry Point

This script provides the main entry point for the Keep Active utility.
It initializes and runs the keep-active controller with default settings.

Usage:
    python main.py                  # Default click mode
    python main.py --coding-mode    # Coding mode - types SQL/Python code

The script will:
    1. Move the mouse to the center of the screen at random intervals (30-60s)
    2. In default mode: perform a double-click to simulate activity
    3. In coding mode: type realistic SQL/Python code snippets
    4. Continue until interrupted with Ctrl+C

Safety:
    The pyautogui failsafe is enabled by default. Moving the mouse to the
    top-left corner of the screen will abort the script immediately.
"""

import argparse

from keep_active import KeepActiveConfig, KeepActiveController


def main() -> None:
    """
    Main entry point for the Keep Active utility.

    Parses command-line arguments, creates a controller with the
    appropriate configuration, and starts the keep-active loop.
    """
    parser = argparse.ArgumentParser(
        description="Keep Active - Prevent screen timeout by simulating activity"
    )
    parser.add_argument(
        "--coding-mode",
        action="store_true",
        default=False,
        help="Enable coding mode: types SQL/Python code instead of clicking",
    )
    parser.add_argument(
        "--typing-speed",
        type=float,
        default=0.05,
        help="Seconds between keystrokes in coding mode (default: 0.05)",
    )
    parser.add_argument(
        "--min-wait",
        type=int,
        default=30,
        help="Minimum wait seconds between actions (default: 30)",
    )
    parser.add_argument(
        "--max-wait",
        type=int,
        default=60,
        help="Maximum wait seconds between actions (default: 60)",
    )
    args = parser.parse_args()

    config = KeepActiveConfig(
        coding_mode=args.coding_mode,
        typing_speed=args.typing_speed,
        min_wait_seconds=args.min_wait,
        max_wait_seconds=args.max_wait,
    )

    controller = KeepActiveController(config=config)
    controller.run()


if __name__ == "__main__":
    main()
