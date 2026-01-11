"""
Unit tests for the Keep Active controller module.
"""

from typing import List

import pytest

from keep_active.config import KeepActiveConfig
from keep_active.controller import KeepActiveController
from keep_active.mouse import MouseOperations, Position, ScreenSize


class MockMouse:
    """Mock implementation of MouseOperations for testing."""

    def __init__(
        self,
        initial_position: Position = Position(x=100, y=100),
        screen_size: ScreenSize = ScreenSize(width=1920, height=1080),
    ) -> None:
        self.failsafe_enabled = False
        self.current_position = initial_position
        self.screen_size_value = screen_size
        self.move_calls: List[tuple[Position, float]] = []
        self.double_click_count = 0

    def get_position(self) -> Position:
        return self.current_position

    def get_screen_size(self) -> ScreenSize:
        return self.screen_size_value

    def move_to(self, position: Position, duration: float = 0.5) -> None:
        self.move_calls.append((position, duration))
        self.current_position = position

    def double_click(self) -> None:
        self.double_click_count += 1

    def set_failsafe(self, enabled: bool) -> None:
        self.failsafe_enabled = enabled


class MockSleeper:
    """Mock sleep function that records calls without actually sleeping."""

    def __init__(self) -> None:
        self.sleep_calls: List[float] = []

    def __call__(self, seconds: float) -> None:
        self.sleep_calls.append(seconds)


class MockPrinter:
    """Mock print function that records output."""

    def __init__(self) -> None:
        self.output: List[str] = []

    def __call__(self, *args: object, **kwargs: object) -> None:
        self.output.append(" ".join(str(arg) for arg in args))


class TestKeepActiveController:
    """Tests for KeepActiveController class."""

    def test_initialization_with_defaults(self) -> None:
        """Test controller initializes with default config."""
        mock_mouse = MockMouse()
        controller = KeepActiveController(mouse=mock_mouse)

        assert controller.config.min_wait_seconds == 30
        assert controller.config.max_wait_seconds == 60

    def test_initialization_with_custom_config(self) -> None:
        """Test controller initializes with custom config."""
        config = KeepActiveConfig(min_wait_seconds=10, max_wait_seconds=20)
        mock_mouse = MockMouse()
        controller = KeepActiveController(config=config, mouse=mock_mouse)

        assert controller.config.min_wait_seconds == 10
        assert controller.config.max_wait_seconds == 20

    def test_setup_enables_failsafe(self) -> None:
        """Test that setup enables failsafe when configured."""
        config = KeepActiveConfig(enable_failsafe=True)
        mock_mouse = MockMouse()
        controller = KeepActiveController(config=config, mouse=mock_mouse)

        controller._setup()

        assert mock_mouse.failsafe_enabled is True

    def test_setup_disables_failsafe(self) -> None:
        """Test that setup disables failsafe when configured."""
        config = KeepActiveConfig(enable_failsafe=False)
        mock_mouse = MockMouse()
        controller = KeepActiveController(config=config, mouse=mock_mouse)

        controller._setup()

        assert mock_mouse.failsafe_enabled is False

    def test_calculate_target_position_returns_center(self) -> None:
        """Test that target position is screen center."""
        mock_mouse = MockMouse(screen_size=ScreenSize(width=1920, height=1080))
        controller = KeepActiveController(mouse=mock_mouse)

        target = controller._calculate_target_position()

        assert target.x == 960
        assert target.y == 540

    def test_perform_activity_moves_mouse(self) -> None:
        """Test that perform_activity moves mouse to center."""
        config = KeepActiveConfig(mouse_move_duration=0.3, post_click_pause=0.1)
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        controller = KeepActiveController(
            config=config, mouse=mock_mouse, sleep_func=mock_sleeper
        )

        controller._perform_activity()

        assert len(mock_mouse.move_calls) == 1
        assert mock_mouse.move_calls[0][0] == Position(x=960, y=540)
        assert mock_mouse.move_calls[0][1] == 0.3

    def test_perform_activity_double_clicks(self) -> None:
        """Test that perform_activity performs double click."""
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        controller = KeepActiveController(mouse=mock_mouse, sleep_func=mock_sleeper)

        controller._perform_activity()

        assert mock_mouse.double_click_count == 1

    def test_perform_activity_pauses_after_click(self) -> None:
        """Test that perform_activity pauses after click."""
        config = KeepActiveConfig(post_click_pause=0.2)
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        controller = KeepActiveController(
            config=config, mouse=mock_mouse, sleep_func=mock_sleeper
        )

        controller._perform_activity()

        assert mock_sleeper.sleep_calls[-1] == 0.2

    def test_run_with_max_iterations(self) -> None:
        """Test running controller with maximum iterations limit."""
        config = KeepActiveConfig(min_wait_seconds=1, max_wait_seconds=1)
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        mock_printer = MockPrinter()
        controller = KeepActiveController(
            config=config,
            mouse=mock_mouse,
            sleep_func=mock_sleeper,
            print_func=mock_printer,
        )

        controller.run(max_iterations=3)

        # Should have moved mouse 3 times
        assert len(mock_mouse.move_calls) == 3
        # Should have double-clicked 3 times
        assert mock_mouse.double_click_count == 3

    def test_run_logs_iteration_number(self) -> None:
        """Test that run logs iteration numbers."""
        config = KeepActiveConfig(min_wait_seconds=1, max_wait_seconds=1)
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        mock_printer = MockPrinter()
        controller = KeepActiveController(
            config=config,
            mouse=mock_mouse,
            sleep_func=mock_sleeper,
            print_func=mock_printer,
        )

        controller.run(max_iterations=2)

        # Check that iteration numbers are logged
        output_text = "\n".join(mock_printer.output)
        assert "[1]" in output_text
        assert "[2]" in output_text

    def test_verbose_false_suppresses_output(self) -> None:
        """Test that verbose=False suppresses log output."""
        config = KeepActiveConfig(
            min_wait_seconds=1, max_wait_seconds=1, verbose=False
        )
        mock_mouse = MockMouse()
        mock_sleeper = MockSleeper()
        mock_printer = MockPrinter()
        controller = KeepActiveController(
            config=config,
            mouse=mock_mouse,
            sleep_func=mock_sleeper,
            print_func=mock_printer,
        )

        controller.run(max_iterations=1)

        # Should have no output when verbose is False
        assert len(mock_printer.output) == 0

    def test_stop_method_stops_loop(self) -> None:
        """Test that stop() method can stop the controller."""
        mock_mouse = MockMouse()
        controller = KeepActiveController(mouse=mock_mouse)

        controller._running = True
        controller.stop()

        assert controller._running is False


class TestControllerIntegration:
    """Integration tests for controller with all components."""

    def test_full_iteration_cycle(self) -> None:
        """Test a complete iteration cycle with all components."""
        config = KeepActiveConfig(
            min_wait_seconds=5,
            max_wait_seconds=5,
            mouse_move_duration=0.2,
            post_click_pause=0.1,
        )
        mock_mouse = MockMouse(
            initial_position=Position(x=50, y=50),
            screen_size=ScreenSize(width=800, height=600),
        )
        mock_sleeper = MockSleeper()
        mock_printer = MockPrinter()
        controller = KeepActiveController(
            config=config,
            mouse=mock_mouse,
            sleep_func=mock_sleeper,
            print_func=mock_printer,
        )

        controller.run(max_iterations=1)

        # Verify mouse moved to center (400, 300)
        assert mock_mouse.current_position == Position(x=400, y=300)

        # Verify sleep was called with correct duration
        assert 5 in mock_sleeper.sleep_calls  # Wait time
        assert 0.1 in mock_sleeper.sleep_calls  # Post-click pause

        # Verify double click happened
        assert mock_mouse.double_click_count == 1

        # Verify failsafe was enabled
        assert mock_mouse.failsafe_enabled is True
