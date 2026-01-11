"""
Unit tests for the Keep Active configuration module.
"""

import pytest

from keep_active.config import KeepActiveConfig


class TestKeepActiveConfig:
    """Tests for KeepActiveConfig dataclass."""

    def test_default_values(self) -> None:
        """Test that default configuration values are set correctly."""
        config = KeepActiveConfig()

        assert config.min_wait_seconds == 30
        assert config.max_wait_seconds == 60
        assert config.mouse_move_duration == 0.5
        assert config.post_click_pause == 0.5
        assert config.enable_failsafe is True
        assert config.use_screen_center is True
        assert config.verbose is True

    def test_custom_values(self) -> None:
        """Test that custom configuration values are accepted."""
        config = KeepActiveConfig(
            min_wait_seconds=10,
            max_wait_seconds=30,
            mouse_move_duration=0.3,
            post_click_pause=0.2,
            enable_failsafe=False,
            use_screen_center=False,
            verbose=False,
        )

        assert config.min_wait_seconds == 10
        assert config.max_wait_seconds == 30
        assert config.mouse_move_duration == 0.3
        assert config.post_click_pause == 0.2
        assert config.enable_failsafe is False
        assert config.use_screen_center is False
        assert config.verbose is False

    def test_immutability(self) -> None:
        """Test that config is immutable (frozen dataclass)."""
        config = KeepActiveConfig()

        with pytest.raises(AttributeError):
            config.min_wait_seconds = 100  # type: ignore[misc]

    def test_min_greater_than_max_raises_error(self) -> None:
        """Test that min_wait > max_wait raises ValueError."""
        with pytest.raises(ValueError, match="cannot be greater than"):
            KeepActiveConfig(min_wait_seconds=60, max_wait_seconds=30)

    def test_negative_min_wait_raises_error(self) -> None:
        """Test that negative min_wait_seconds raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            KeepActiveConfig(min_wait_seconds=-1)

    def test_negative_max_wait_raises_error(self) -> None:
        """Test that negative max_wait_seconds raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            KeepActiveConfig(max_wait_seconds=-1)

    def test_negative_mouse_duration_raises_error(self) -> None:
        """Test that negative mouse_move_duration raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            KeepActiveConfig(mouse_move_duration=-0.1)

    def test_negative_post_click_pause_raises_error(self) -> None:
        """Test that negative post_click_pause raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            KeepActiveConfig(post_click_pause=-0.1)

    def test_equal_min_max_is_valid(self) -> None:
        """Test that min_wait == max_wait is valid (fixed interval)."""
        config = KeepActiveConfig(min_wait_seconds=45, max_wait_seconds=45)

        assert config.min_wait_seconds == 45
        assert config.max_wait_seconds == 45


class TestGetRandomWaitTime:
    """Tests for the get_random_wait_time method."""

    def test_random_wait_in_range(self) -> None:
        """Test that random wait time is within configured range."""
        config = KeepActiveConfig(min_wait_seconds=10, max_wait_seconds=20)

        # Run multiple times to increase confidence
        for _ in range(100):
            wait_time = config.get_random_wait_time()
            assert 10 <= wait_time <= 20

    def test_fixed_interval_when_min_equals_max(self) -> None:
        """Test that wait time is fixed when min equals max."""
        config = KeepActiveConfig(min_wait_seconds=30, max_wait_seconds=30)

        for _ in range(10):
            assert config.get_random_wait_time() == 30

    def test_returns_integer(self) -> None:
        """Test that wait time is an integer."""
        config = KeepActiveConfig()
        wait_time = config.get_random_wait_time()

        assert isinstance(wait_time, int)
