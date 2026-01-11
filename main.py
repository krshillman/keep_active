#!/usr/bin/env python3
"""
Keep Active - Entry Point

This script provides the main entry point for the Keep Active utility.
It initializes and runs the keep-active controller with default settings.

Usage:
    python main.py

The script will:
    1. Move the mouse to the center of the screen at random intervals (30-60s)
    2. Perform a double-click to simulate activity
    3. Continue until interrupted with Ctrl+C

Safety:
    The pyautogui failsafe is enabled by default. Moving the mouse to the
    top-left corner of the screen will abort the script immediately.
"""

from keep_active import KeepActiveConfig, KeepActiveController


def main() -> None:
    """
    Main entry point for the Keep Active utility.

    Creates a controller with default configuration and starts the
    keep-active loop. The loop runs indefinitely until interrupted
    by the user with Ctrl+C.
    """
    # Create configuration with default settings
    # Customize by passing parameters: KeepActiveConfig(min_wait_seconds=20, ...)
    config = KeepActiveConfig()

    # Create and run the controller
    controller = KeepActiveController(config=config)
    controller.run()


if __name__ == "__main__":
    main()
