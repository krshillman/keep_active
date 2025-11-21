#!/usr/bin/env python3
"""
Keep Window Active Script
Moves mouse and double-clicks at random intervals to prevent screen timeout/inactivity.
"""

import random
import sys
import time

import pyautogui


def main():
    print("Keep Active Script Started")
    print("Press Ctrl+C to stop")
    print("-" * 40)

    # Failsafe: moving mouse to top-left corner will abort
    pyautogui.FAILSAFE = True

    try:
        iteration = 0
        while True:
            iteration += 1

            # Random interval between 30-60 seconds
            wait_time = random.randint(30, 60)
            print(f"\n[{iteration}] Waiting {wait_time} seconds...")
            time.sleep(wait_time)

            # Get current mouse position
            current_x, current_y = pyautogui.position()

            # Move to a safe location (center of screen) or nearby
            screen_width, screen_height = pyautogui.size()
            target_x = screen_width // 2
            target_y = screen_height // 2

            print(
                f"Moving mouse from ({current_x}, {current_y}) to ({target_x}, {target_y})"
            )
            pyautogui.moveTo(target_x, target_y, duration=0.5)

            # Double click
            print("Double clicking...")
            pyautogui.doubleClick()

            # Small pause after click
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nScript stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
