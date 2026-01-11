"""
Controller module for Keep Active.

This module contains the main controller logic that orchestrates the
keep-active behavior, coordinating configuration, mouse operations,
and the main execution loop.
"""

import sys
import time
from typing import Callable, Optional

from keep_active.config import KeepActiveConfig
from keep_active.mouse import MouseOperations, Position, PyAutoGUIMouseOperations


class KeepActiveController:
    """
    Main controller for the Keep Active utility.

    This class orchestrates the keep-active behavior by managing the
    configuration, mouse operations, and main execution loop. It supports
    dependency injection for testing and customization.

    Attributes:
        config: Configuration settings for the controller.
        mouse: Mouse operations handler.

    Example:
        >>> config = KeepActiveConfig(min_wait_seconds=10, max_wait_seconds=20)
        >>> controller = KeepActiveController(config)
        >>> controller.run()  # Starts the keep-active loop
    """

    def __init__(
        self,
        config: Optional[KeepActiveConfig] = None,
        mouse: Optional[MouseOperations] = None,
        sleep_func: Optional[Callable[[float], None]] = None,
        print_func: Optional[Callable[..., None]] = None,
    ) -> None:
        """
        Initialize the Keep Active controller.

        Args:
            config: Configuration settings. Defaults to KeepActiveConfig().
            mouse: Mouse operations handler. Defaults to PyAutoGUIMouseOperations().
            sleep_func: Function to use for sleeping. Defaults to time.sleep.
                       Useful for testing to avoid actual delays.
            print_func: Function to use for output. Defaults to built-in print.
                       Useful for testing or custom logging.
        """
        self.config = config or KeepActiveConfig()
        self.mouse = mouse or PyAutoGUIMouseOperations()
        self._sleep = sleep_func or time.sleep
        self._print = print_func or print
        self._running = False
        self._iteration = 0

    def _log(self, message: str) -> None:
        """
        Log a message if verbose mode is enabled.

        Args:
            message: The message to log.
        """
        if self.config.verbose:
            self._print(message)

    def _setup(self) -> None:
        """
        Perform initial setup before starting the main loop.

        Configures failsafe settings and prints startup messages.
        """
        self.mouse.set_failsafe(self.config.enable_failsafe)
        self._log("Keep Active Script Started")
        self._log("Press Ctrl+C to stop")
        self._log("-" * 40)

    def _calculate_target_position(self) -> Position:
        """
        Calculate the target position for mouse movement.

        Returns:
            Position to move the mouse to (screen center by default).
        """
        screen = self.mouse.get_screen_size()
        return screen.center

    def _perform_activity(self) -> None:
        """
        Perform a single activity cycle: move mouse and double-click.

        This method executes one complete keep-active action, including:
        1. Getting current mouse position
        2. Calculating target position
        3. Moving mouse to target
        4. Performing double-click
        5. Brief pause after click
        """
        # Get current position for logging
        current_pos = self.mouse.get_position()
        target_pos = self._calculate_target_position()

        self._log(f"Moving mouse from {current_pos} to {target_pos}")
        self.mouse.move_to(target_pos, duration=self.config.mouse_move_duration)

        self._log("Double clicking...")
        self.mouse.double_click()

        # Small pause after click
        self._sleep(self.config.post_click_pause)

    def _run_iteration(self) -> None:
        """
        Run a single iteration of the keep-active loop.

        Each iteration:
        1. Increments the iteration counter
        2. Waits for a random interval
        3. Performs the activity (mouse movement and click)
        """
        self._iteration += 1
        wait_time = self.config.get_random_wait_time()

        self._log(f"\n[{self._iteration}] Waiting {wait_time} seconds...")
        self._sleep(wait_time)

        self._perform_activity()

    def run(self, max_iterations: Optional[int] = None) -> None:
        """
        Run the keep-active main loop.

        This method starts the keep-active loop, which continues until:
        - The user interrupts with Ctrl+C
        - An error occurs
        - max_iterations is reached (if specified)

        Args:
            max_iterations: Optional maximum number of iterations to run.
                          If None, runs indefinitely until interrupted.

        Raises:
            SystemExit: On keyboard interrupt (exit code 0) or error (exit code 1).
        """
        self._running = True
        self._iteration = 0
        self._setup()

        try:
            while self._running:
                self._run_iteration()

                # Check if we've reached max iterations
                if max_iterations is not None and self._iteration >= max_iterations:
                    self._log(f"\nCompleted {max_iterations} iterations")
                    break

        except KeyboardInterrupt:
            self._log("\n\nScript stopped by user")
            sys.exit(0)
        except Exception as e:
            self._log(f"\nError: {e}")
            sys.exit(1)

    def stop(self) -> None:
        """
        Stop the keep-active loop.

        This method can be called from another thread to gracefully
        stop the main loop.
        """
        self._running = False
