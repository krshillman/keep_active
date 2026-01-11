"""
Keep Active - A utility to prevent screen timeout and inactivity.

This package provides a modular, type-safe implementation of a keep-alive
utility that simulates mouse activity to prevent system sleep/screen timeout.

Modules:
    config: Configuration settings and dataclasses
    mouse: Mouse operation abstractions and implementations
    controller: Main application controller and execution logic
"""

from keep_active.config import KeepActiveConfig
from keep_active.controller import KeepActiveController
from keep_active.mouse import MouseOperations, PyAutoGUIMouseOperations

__version__ = "0.1.0"
__all__ = [
    "KeepActiveConfig",
    "KeepActiveController",
    "MouseOperations",
    "PyAutoGUIMouseOperations",
]
