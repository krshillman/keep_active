"""
Configuration module for Keep Active.

This module defines the configuration settings for the keep-active utility
using dataclasses for type safety and immutability.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class KeepActiveConfig:
    """
    Configuration settings for the Keep Active utility.

    This immutable dataclass holds all configurable parameters for the
    keep-active behavior including timing intervals, mouse movement settings,
    and safety features.

    Attributes:
        min_wait_seconds: Minimum wait time between actions (default: 30).
        max_wait_seconds: Maximum wait time between actions (default: 60).
        mouse_move_duration: Duration in seconds for mouse movement animation (default: 0.5).
        post_click_pause: Pause duration in seconds after clicking (default: 0.5).
        enable_failsafe: Enable pyautogui failsafe - moving mouse to corner aborts (default: True).
        use_screen_center: If True, move to screen center; if False, move to offset position.
        verbose: Enable verbose logging output (default: True).

    Example:
        >>> config = KeepActiveConfig(min_wait_seconds=20, max_wait_seconds=40)
        >>> config.min_wait_seconds
        20

    Raises:
        ValueError: If min_wait_seconds > max_wait_seconds during validation.
    """

    min_wait_seconds: int = field(default=30)
    max_wait_seconds: int = field(default=60)
    mouse_move_duration: float = field(default=0.5)
    post_click_pause: float = field(default=0.5)
    enable_failsafe: bool = field(default=True)
    use_screen_center: bool = field(default=True)
    verbose: bool = field(default=True)

    def __post_init__(self) -> None:
        """
        Validate configuration after initialization.

        Raises:
            ValueError: If any timing values are negative.
            ValueError: If min_wait_seconds is greater than max_wait_seconds.
        """
        # Check for negative values first
        if self.min_wait_seconds < 0:
            raise ValueError("min_wait_seconds cannot be negative")
        if self.max_wait_seconds < 0:
            raise ValueError("max_wait_seconds cannot be negative")
        if self.mouse_move_duration < 0:
            raise ValueError("mouse_move_duration cannot be negative")
        if self.post_click_pause < 0:
            raise ValueError("post_click_pause cannot be negative")

        # Check logical constraints
        if self.min_wait_seconds > self.max_wait_seconds:
            raise ValueError(
                f"min_wait_seconds ({self.min_wait_seconds}) cannot be greater than "
                f"max_wait_seconds ({self.max_wait_seconds})"
            )

    def get_random_wait_time(self) -> int:
        """
        Generate a random wait time within the configured range.

        Returns:
            A random integer between min_wait_seconds and max_wait_seconds (inclusive).

        Example:
            >>> config = KeepActiveConfig(min_wait_seconds=10, max_wait_seconds=20)
            >>> wait_time = config.get_random_wait_time()
            >>> 10 <= wait_time <= 20
            True
        """
        import random

        return random.randint(self.min_wait_seconds, self.max_wait_seconds)
