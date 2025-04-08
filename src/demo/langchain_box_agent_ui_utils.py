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


class ModernStyles:
    """Modern styles for the application."""

    # Colors
    BG_COLOR = "#f5f5f5"  # Light gray background
    PRIMARY_COLOR = "#007aff"  # macOS blue accent
    SECONDARY_COLOR = "#8e8e93"  # Subtle gray for secondary elements
    SUCCESS_COLOR = "#34c759"  # Green for success
    WARNING_COLOR = "#ffcc00"  # Yellow for warnings
    ERROR_COLOR = "#ff3b30"  # Red for errors

    # Text colors
    TEXT_COLOR = "#1c1c1e"  # Dark text
    TEXT_SECONDARY = "#8e8e93"  # Subtle gray for secondary text
    TEXT_LIGHT = "#ffffff"  # Light text for contrast

    # Chat colors
    USER_BG = "#e5e5ea"  # Light gray for user messages
    USER_TEXT = "#1c1c1e"  # Dark text for user messages
    AGENT_BG = "#007aff"  # Blue for agent messages
    AGENT_TEXT = "#ffffff"  # White text for agent messages

    # Font families
    DEFAULT_FONT = ".SF NS"  # macOS system font
    MONOSPACE_FONT = "Menlo"  # macOS monospace font

    # Font sizes
    FONT_LARGE = 16
    FONT_MEDIUM = 14
    FONT_SMALL = 12

    @classmethod
    def configure_styles(cls, style):
        """Configure ttk styles for the application."""
        style.configure("TFrame", background=cls.BG_COLOR)
        style.configure("TLabel", background=cls.BG_COLOR, foreground=cls.TEXT_COLOR)
        style.configure(
            "TButton",
            font=(cls.DEFAULT_FONT, cls.FONT_MEDIUM),
            background=cls.PRIMARY_COLOR,
            foreground=cls.TEXT_LIGHT,
            padding=10,
        )

        style.configure(
            "Primary.TButton",
            background=cls.PRIMARY_COLOR,
            foreground=cls.TEXT_LIGHT,
            relief="flat",
        )

        style.configure(
            "Secondary.TButton",
            background=cls.SECONDARY_COLOR,
            foreground=cls.TEXT_LIGHT,
            relief="flat",
        )

        style.configure(
            "TLabelframe",
            background=cls.BG_COLOR,
            foreground=cls.TEXT_COLOR,
            padding=10,
        )

        style.configure(
            "TLabelframe.Label",
            background=cls.BG_COLOR,
            foreground=cls.TEXT_COLOR,
            font=(cls.DEFAULT_FONT, cls.FONT_MEDIUM, "bold"),
        )

        style.configure(
            "Status.TLabel",
            background=cls.SECONDARY_COLOR,
            foreground=cls.TEXT_LIGHT,
            padding=5,
        )

        style.configure(
            "Title.TLabel",
            background=cls.BG_COLOR,
            foreground=cls.PRIMARY_COLOR,
            font=(cls.DEFAULT_FONT, cls.FONT_LARGE, "bold"),
        )

        style.configure(
            "Subtitle.TLabel",
            background=cls.BG_COLOR,
            foreground=cls.SECONDARY_COLOR,
            font=(cls.DEFAULT_FONT, cls.FONT_MEDIUM, "italic"),
        )

        style.configure(
            "PromptButton.TButton",
            background=cls.USER_BG,
            foreground=cls.TEXT_COLOR,
            font=(cls.DEFAULT_FONT, cls.FONT_SMALL),
            relief="flat",
        )

        style.map(
            "PromptButton.TButton",
            background=[("active", cls.PRIMARY_COLOR)],
            foreground=[("active", cls.TEXT_LIGHT)],
        )
