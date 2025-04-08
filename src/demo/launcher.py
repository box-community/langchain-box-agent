#!/usr/bin/env python3
"""
LangChain Box Agent Demo Launcher

This script launches the LangChain Box Agent demo application with either
a simulated agent or a real Box API connection.

Usage:
    python launcher.py [--demo]

Options:
    --demo    Launch with simulated agent (no real Box API connection)

Requirements:
    - Box API credentials (set in .env file or environment variables) for real mode
    - LangChain Box Agent package installed for real mode
    - OpenAI API key (for GPT-4) for real mode
"""

import argparse
import os
import sys
import threading
import tkinter as tk
import traceback
from tkinter import messagebox

import dotenv
from agent_implementations import RealBoxAgent, SimulatedAgent

# Import UI and agent implementations
# The UI component is split across multiple files, but we import from the main module
from langchain_box_agent_ui import LangChainBoxAgentUI

# Load environment variables from .env file
dotenv.load_dotenv()


def check_environment_vars():
    """Check if required environment variables are set."""
    required_vars = [
        "BOX_CLIENT_ID",
        "BOX_CLIENT_SECRET",
        "BOX_SUBJECT_TYPE",
        "BOX_SUBJECT_ID",
        "OPENAI_API_KEY",
    ]

    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    return missing_vars


def initialize_real_agent():
    """Initialize the real Box agent."""
    try:
        # Import LangChain Box Agent
        from langchain.chat_models import init_chat_model

        from langchain_box_agent.box.box_authentication import get_ccg_client
        from langchain_box_agent.box_agent import LangChainBoxAgent

        # Initialize Box client
        client = get_ccg_client()

        # Get user info for status message
        user_info = client.users.get_user_me()
        status_message = f"Connected as: {user_info.name}"

        # Initialize language model
        model = init_chat_model("gpt-4", model_provider="openai")

        # Create the Box agent
        langchain_agent = LangChainBoxAgent(client, model)

        # Wrap in our agent interface
        agent = RealBoxAgent(langchain_agent)

        return agent, status_message

    except Exception as e:
        error_message = f"Error initializing Box agent: {str(e)}"
        print(error_message)
        traceback.print_exc()
        raise


def initialize_demo_agent():
    """Initialize the simulated agent."""
    agent = SimulatedAgent()
    status_message = "Demo Mode (Simulated Agent)"
    return agent, status_message


def show_launcher_gui():
    """Display a simple GUI to select the agent type."""
    root = tk.Tk()
    root.title("LangChain Box Agent Demo Launcher")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg="#f5f5f7")

    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry("{}x{}+{}+{}".format(width, height, x, y))

    # Check if environment variables are set
    missing_vars = check_environment_vars()
    env_status = (
        "✅ Environment variables set"
        if not missing_vars
        else f"❌ Missing: {', '.join(missing_vars)}"
    )

    # Set up a frame with padding
    main_frame = tk.Frame(root, bg="#f5f5f7", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Add title
    title_label = tk.Label(
        main_frame,
        text="LangChain Box Agent Demo",
        font=("Helvetica", 20, "bold"),
        bg="#f5f5f7",
        fg="#0070c9",
    )
    title_label.pack(pady=(0, 20))

    # Add explanation text
    explanation = tk.Label(
        main_frame,
        text="Choose a mode for the Box agent demo:\n\n"
        + "• Demo Mode uses a simulated agent with pre-programmed responses\n\n"
        + "• Real Agent connects to Box API and uses LangChain integration",
        justify=tk.LEFT,
        font=("Helvetica", 12),
        bg="#f5f5f7",
        fg="#333333",
        wraplength=460,
    )
    explanation.pack(pady=(0, 20), anchor="w")

    # Add environment status
    env_color = "#2ecc71" if not missing_vars else "#e74c3c"
    env_label = tk.Label(
        main_frame, text=env_status, font=("Helvetica", 10), bg="#f5f5f7", fg=env_color
    )
    env_label.pack(pady=(0, 20))

    # Add buttons
    button_frame = tk.Frame(main_frame, bg="#f5f5f7")
    button_frame.pack(pady=10)

    def start_demo_mode():
        root.destroy()
        launch_app(demo_mode=True)

    def start_real_mode():
        if missing_vars:
            messagebox.showerror(
                "Missing Environment Variables",
                f"Cannot start in real mode. Missing: {', '.join(missing_vars)}",
            )
            return

        root.destroy()
        launch_app(demo_mode=False)

    # Demo mode button
    demo_button = tk.Button(
        button_frame,
        text="Demo Mode",
        font=("Helvetica", 12),
        bg="#f0f0f0",
        fg="#333333",
        padx=20,
        pady=10,
        relief=tk.RAISED,
        command=start_demo_mode,
    )
    demo_button.pack(side=tk.LEFT, padx=10)

    # Real mode button
    real_button = tk.Button(
        button_frame,
        text="Real Agent",
        font=("Helvetica", 12),
        bg="#0070c9",
        fg="white",
        padx=20,
        pady=10,
        relief=tk.RAISED,
        command=start_real_mode,
    )
    real_button.pack(side=tk.LEFT, padx=10)

    # Status bar
    status_bar = tk.Label(
        root,
        text="© 2025 LangChain Box Agent Demo",
        font=("Helvetica", 8),
        bg="#333333",
        fg="white",
        padx=10,
        pady=5,
    )
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()


def launch_app(demo_mode=False):
    """Launch the app with either a simulated or real agent."""
    try:
        if demo_mode:
            # Use simulated agent
            agent, status_message = initialize_demo_agent()
            app = LangChainBoxAgentUI(agent, status_message)
            app.mainloop()
        else:
            # Show loading message
            loading_window = tk.Tk()
            loading_window.title("Connecting...")
            loading_window.geometry("300x100")
            loading_window.resizable(False, False)

            # Center the window
            loading_window.geometry(
                f"+{int((loading_window.winfo_screenwidth() - 300) / 2)}+{int((loading_window.winfo_screenheight() - 100) / 2)}"
            )

            loading_label = tk.Label(
                loading_window,
                text="Connecting to Box API...\nPlease wait",
                font=("Helvetica", 12),
                pady=20,
            )
            loading_label.pack(expand=True)
            loading_window.update()

            # Initialize agent in a separate thread
            def initialize_and_launch():
                try:
                    agent, status_message = initialize_real_agent()
                    # Pass the agent and status_message back to the main thread
                    loading_window.after(
                        0, lambda: on_agent_initialized(agent, status_message)
                    )
                except Exception as e:
                    loading_window.after(0, lambda: on_agent_initialization_failed(e))

            def on_agent_initialized(agent, status_message):
                """Callback for successful agent initialization."""
                loading_window.destroy()
                LangChainBoxAgentUI(agent, status_message).mainloop()

            def on_agent_initialization_failed(exception):
                """Callback for failed agent initialization."""
                loading_window.destroy()
                messagebox.showerror(
                    "Connection Error",
                    f"Failed to connect to Box API: {str(exception)}\n\nWould you like to try demo mode instead?",
                )

            # Start the thread
            threading.Thread(target=initialize_and_launch, daemon=True).start()

            # Run the loading window's main loop
            loading_window.mainloop()

    except Exception as e:
        error_message = f"Error launching application: {str(e)}"
        print(error_message)
        traceback.print_exc()
        messagebox.showerror("Error", error_message)


def main():
    """Main entry point for the launcher."""
    parser = argparse.ArgumentParser(description="Launch LangChain Box Agent Demo")
    parser.add_argument(
        "--demo", action="store_true", help="Launch with simulated agent"
    )

    args = parser.parse_args()

    if args.demo:
        # Launch directly with demo agent
        launch_app(demo_mode=True)
    else:
        # Show launcher GUI to let user choose
        show_launcher_gui()


if __name__ == "__main__":
    main()
