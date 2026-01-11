"""
Mouse operations module for Keep Active.

This module provides abstractions for mouse operations, allowing for
dependency injection and easy testing. It defines a Protocol for mouse
operations and provides a concrete implementation using pyautogui.
"""

from dataclasses import dataclass
from typing import Protocol, Tuple


@dataclass(frozen=True)
class Position:
    """
    Represents a 2D screen position.

    Attributes:
        x: Horizontal coordinate in pixels.
        y: Vertical coordinate in pixels.
    """

    x: int
    y: int

    def __str__(self) -> str:
        """Return string representation of position."""
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class ScreenSize:
    """
    Represents screen dimensions.

    Attributes:
        width: Screen width in pixels.
        height: Screen height in pixels.
    """

    width: int
    height: int

    @property
    def center(self) -> Position:
        """
        Calculate the center position of the screen.

        Returns:
            Position at the center of the screen.
        """
        return Position(x=self.width // 2, y=self.height // 2)


class MouseOperations(Protocol):
    """
    Protocol defining the interface for mouse operations.

    This protocol allows for dependency injection and testing by defining
    the required interface for mouse operations without coupling to a
    specific implementation.

    Implementations must provide methods for:
    - Getting current mouse position
    - Getting screen size
    - Moving the mouse to a position
    - Performing double-click
    - Setting failsafe mode
    """

    def get_position(self) -> Position:
        """
        Get the current mouse cursor position.

        Returns:
            Position object with current x, y coordinates.
        """
        ...

    def get_screen_size(self) -> ScreenSize:
        """
        Get the current screen dimensions.

        Returns:
            ScreenSize object with width and height.
        """
        ...

    def move_to(self, position: Position, duration: float = 0.5) -> None:
        """
        Move the mouse cursor to a specified position.

        Args:
            position: Target position to move the mouse to.
            duration: Time in seconds for the movement animation.
        """
        ...

    def double_click(self) -> None:
        """
        Perform a double-click at the current mouse position.
        """
        ...

    def set_failsafe(self, enabled: bool) -> None:
        """
        Enable or disable the failsafe feature.

        When enabled, moving the mouse to the top-left corner of the screen
        will raise an exception, allowing the user to abort the script.

        Args:
            enabled: True to enable failsafe, False to disable.
        """
        ...


class PyAutoGUIMouseOperations:
    """
    Concrete implementation of MouseOperations using pyautogui.

    This class wraps pyautogui functionality and implements the
    MouseOperations protocol for production use.

    Example:
        >>> mouse = PyAutoGUIMouseOperations()
        >>> mouse.set_failsafe(True)
        >>> current_pos = mouse.get_position()
        >>> screen = mouse.get_screen_size()
        >>> mouse.move_to(screen.center, duration=0.3)
    """

    def __init__(self) -> None:
        """Initialize the PyAutoGUI mouse operations handler."""
        # Import here to allow testing without pyautogui installed
        import pyautogui

        self._pyautogui = pyautogui

    def get_position(self) -> Position:
        """
        Get the current mouse cursor position using pyautogui.

        Returns:
            Position object with current x, y coordinates.
        """
        x, y = self._pyautogui.position()
        return Position(x=int(x), y=int(y))

    def get_screen_size(self) -> ScreenSize:
        """
        Get the current screen dimensions using pyautogui.

        Returns:
            ScreenSize object with width and height.
        """
        width, height = self._pyautogui.size()
        return ScreenSize(width=int(width), height=int(height))

    def move_to(self, position: Position, duration: float = 0.5) -> None:
        """
        Move the mouse cursor to a specified position using pyautogui.

        Args:
            position: Target position to move the mouse to.
            duration: Time in seconds for the movement animation.
        """
        self._pyautogui.moveTo(position.x, position.y, duration=duration)

    def double_click(self) -> None:
        """
        Perform a double-click at the current mouse position using pyautogui.
        """
        self._pyautogui.doubleClick()

    def set_failsafe(self, enabled: bool) -> None:
        """
        Enable or disable the pyautogui failsafe feature.

        Args:
            enabled: True to enable failsafe, False to disable.
        """
        self._pyautogui.FAILSAFE = enabled
