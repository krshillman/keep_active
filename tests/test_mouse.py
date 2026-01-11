"""
Unit tests for the Keep Active mouse operations module.
"""

import pytest

from keep_active.mouse import Position, ScreenSize


class TestPosition:
    """Tests for the Position dataclass."""

    def test_creation(self) -> None:
        """Test Position creation with x and y coordinates."""
        pos = Position(x=100, y=200)

        assert pos.x == 100
        assert pos.y == 200

    def test_immutability(self) -> None:
        """Test that Position is immutable."""
        pos = Position(x=100, y=200)

        with pytest.raises(AttributeError):
            pos.x = 300  # type: ignore[misc]

    def test_string_representation(self) -> None:
        """Test Position string representation."""
        pos = Position(x=100, y=200)

        assert str(pos) == "(100, 200)"

    def test_equality(self) -> None:
        """Test Position equality comparison."""
        pos1 = Position(x=100, y=200)
        pos2 = Position(x=100, y=200)
        pos3 = Position(x=300, y=400)

        assert pos1 == pos2
        assert pos1 != pos3


class TestScreenSize:
    """Tests for the ScreenSize dataclass."""

    def test_creation(self) -> None:
        """Test ScreenSize creation with width and height."""
        screen = ScreenSize(width=1920, height=1080)

        assert screen.width == 1920
        assert screen.height == 1080

    def test_immutability(self) -> None:
        """Test that ScreenSize is immutable."""
        screen = ScreenSize(width=1920, height=1080)

        with pytest.raises(AttributeError):
            screen.width = 2560  # type: ignore[misc]

    def test_center_calculation(self) -> None:
        """Test center position calculation."""
        screen = ScreenSize(width=1920, height=1080)
        center = screen.center

        assert center.x == 960
        assert center.y == 540

    def test_center_with_odd_dimensions(self) -> None:
        """Test center calculation with odd dimensions (integer division)."""
        screen = ScreenSize(width=1921, height=1081)
        center = screen.center

        # Integer division rounds down
        assert center.x == 960
        assert center.y == 540

    def test_center_returns_position(self) -> None:
        """Test that center returns a Position object."""
        screen = ScreenSize(width=1920, height=1080)
        center = screen.center

        assert isinstance(center, Position)


class TestMockMouseOperations:
    """Tests using a mock implementation of MouseOperations protocol."""

    def test_protocol_compliance(self) -> None:
        """Test that a mock implementation satisfies the protocol."""
        from keep_active.mouse import MouseOperations

        class MockMouse:
            """Mock implementation of MouseOperations for testing."""

            def __init__(self) -> None:
                self.failsafe_enabled = False
                self.current_position = Position(x=0, y=0)
                self.screen_size = ScreenSize(width=1920, height=1080)
                self.move_calls: list[tuple[Position, float]] = []
                self.double_click_count = 0

            def get_position(self) -> Position:
                return self.current_position

            def get_screen_size(self) -> ScreenSize:
                return self.screen_size

            def move_to(self, position: Position, duration: float = 0.5) -> None:
                self.move_calls.append((position, duration))
                self.current_position = position

            def double_click(self) -> None:
                self.double_click_count += 1

            def set_failsafe(self, enabled: bool) -> None:
                self.failsafe_enabled = enabled

        mock = MockMouse()

        # Verify it can be used where MouseOperations is expected
        def use_mouse(mouse: MouseOperations) -> None:
            mouse.set_failsafe(True)
            pos = mouse.get_position()
            screen = mouse.get_screen_size()
            mouse.move_to(screen.center, duration=0.3)
            mouse.double_click()

        use_mouse(mock)

        assert mock.failsafe_enabled is True
        assert len(mock.move_calls) == 1
        assert mock.move_calls[0][0] == Position(x=960, y=540)
        assert mock.move_calls[0][1] == 0.3
        assert mock.double_click_count == 1
