import json
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple


class Agent(Protocol):
    """Protocol for agent implementations."""

    def process_query(self, query: str) -> str:
        """Process a user query and return a response."""
        ...


class TypewriterText:
    """Simulates typewriter effect for text."""

    def __init__(self, widget, text, delay=0.02, callback=None):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.callback = callback
        self.i = 0
        self.typing = False
        self.cancel = False

    def start_typing(self):
        """Start the typewriter effect in a separate thread."""
        if not self.typing:
            self.typing = True
            self.cancel = False
            self.i = 0
            threading.Thread(target=self._type_text).start()

    def _type_text(self):
        """Implementation of typewriter effect."""
        while self.i < len(self.text) and not self.cancel:
            char = self.text[self.i]
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, char)
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)
            self.i += 1
            time.sleep(self.delay)

        self.typing = False
        if self.callback and not self.cancel:
            self.callback()

    def stop_typing(self):
        """Stop the typewriter effect and display the full text immediately."""
        self.cancel = True
        remaining_text = self.text[self.i :]
        if remaining_text:
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, remaining_text)
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)


class MacStyles:
    """Simple macOS-like styles for the application."""

    # Base colors
    BG_COLOR = "#ddd"  # White
    LIGHT_BG = "#f0f0f0"  # Very light gray
    DARK_TEXT = "#000000"  # Black
    HIGHLIGHT = "#0a84ff"  # Apple blue

    # Text Input colors
    INPUT_BG = "#fff"  # White background for text input
    INPUT_BORDER = "#000"  # Light gray border for text input

    # Button colors
    BUTTON_BG = "#ebebeb"  # Light gray
    BUTTON_HOVER = "#e5e5e5"  # Slightly darker gray for hover
    BUTTON_PRESS = "#d0d0d0"  # Even darker gray for pressed state

    # Primary button colors (blue)
    PRIMARY_BUTTON_BG = HIGHLIGHT  # Apple blue
    PRIMARY_BUTTON_HOVER = "#0077e5"  # Darker blue for hover
    PRIMARY_BUTTON_PRESS = "#0062c1"  # Even darker blue for pressed state
    PRIMARY_BUTTON_TEXT = "#ffffff"  # White text

    # Prompt button colors
    PROMPT_BUTTON_BG = "#f6f6f6"  # Very light gray
    PROMPT_BUTTON_HOVER = "#e5e5e5"  # Slightly darker for hover

    # Chat colors
    USER_BG = "#fff"  # Light gray (Messages app)
    USER_TEXT = "#333"  # Black
    AGENT_BG = "#fff"  # Apple blue
    AGENT_TEXT = "#333"  # White text

    # Other UI elements
    BORDER_COLOR = "#e0e0e0"  # Light gray for borders
    SEPARATOR_COLOR = "#e0e0e0"  # Light gray for separators

    # Font settings
    DEFAULT_FONT = "SF Pro"  # Will fall back to system default if not available
    FONT_SIZE = 12
    SMALL_FONT = 9

    @classmethod
    def configure_styles(cls, style):
        """Configure minimal ttk styles for a mac-like appearance."""
        # Reset all styles to defaults first
        style.theme_use("default")

        # Configure basic elements
        style.configure(
            ".",
            font=(cls.DEFAULT_FONT, cls.FONT_SIZE),
            background=cls.BG_COLOR,
            foreground=cls.DARK_TEXT,
        )

        # Frame styles
        style.configure("TFrame", background=cls.BG_COLOR)
        style.configure("TLabelframe", background=cls.BG_COLOR)
        style.configure("TLabelframe.Label", background=cls.BG_COLOR)

        # Label styles
        style.configure("TLabel", background=cls.BG_COLOR, padding=3)
        style.configure("Header.TLabel", font=(cls.DEFAULT_FONT, 15, "bold"))
        style.configure(
            "Status.TLabel",
            background=cls.LIGHT_BG,
            padding=3,
            font=(cls.DEFAULT_FONT, cls.SMALL_FONT),
        )

        # Button styles
        style.configure(
            "TButton",
            padding=6,
            relief="flat",
            background=cls.BUTTON_BG,
            borderwidth=0,
            font=(cls.DEFAULT_FONT, cls.FONT_SIZE),
        )

        style.map(
            "TButton",
            background=[("active", cls.BUTTON_HOVER), ("pressed", cls.BUTTON_PRESS)],
            relief=[("pressed", "sunken")],
        )

        # Primary button
        style.configure(
            "Primary.TButton",
            background=cls.PRIMARY_BUTTON_BG,
            foreground=cls.PRIMARY_BUTTON_TEXT,
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", cls.PRIMARY_BUTTON_HOVER),
                ("pressed", cls.PRIMARY_BUTTON_PRESS),
            ],
            foreground=[
                ("active", cls.PRIMARY_BUTTON_TEXT),
                ("pressed", cls.PRIMARY_BUTTON_TEXT),
            ],
        )

        # Prompt button
        style.configure(
            "Prompt.TButton",
            background=cls.PROMPT_BUTTON_BG,
            padding=4,
            font=(cls.DEFAULT_FONT, cls.SMALL_FONT),
        )

        style.map("Prompt.TButton", background=[("active", cls.PROMPT_BUTTON_HOVER)])

        # Separator style
        style.configure("TSeparator", background=cls.SEPARATOR_COLOR)
