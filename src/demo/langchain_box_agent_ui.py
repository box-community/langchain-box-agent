import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import time
import sys
from typing import Protocol


class LangChainBoxAgentUI(tk.Tk):
    def __init__(self, agent, status_message: str = "Connected"):
        super().__init__()

        self.title("LangChain Box Agent Demo")
        self.geometry("1000x800")
        self.minsize(800, 600)

        # Import ModernStyles here to handle cross-imports
        from langchain_box_agent_ui_utils import ModernStyles

        self.configure(bg=ModernStyles.BG_COLOR)

        # Setup ttk styles
        self.style = ttk.Style()
        ModernStyles.configure_styles(self.style)

        # Sample predefined prompts
        self.predefined_prompts = [
            "Who am I?",
            "Search for all PDF files in my Box account",
            "What's in my root folder?",
            "Create a new folder called 'LangChain Demo'",
            "Read the content of sample.txt",
            "Extract tenant name and email from HAB-1-01.docx",
        ]

        # Initialize typing effects
        self.user_typewriter = None
        self.agent_typewriter = None

        # Store the Box agent
        self.agent = agent

        # Store status message
        self.status_message = status_message

        # Setup UI
        self.setup_ui()

        # Display welcome message
        self.add_agent_message(
            "Hello! I'm your LangChain Box Agent. I can help you manage your Box files and folders. What would you like to do today?"
        )

    def setup_ui(self):
        """Setup the user interface."""
        # Import ModernStyles here to handle cross-imports
        from langchain_box_agent_ui_utils import ModernStyles

        # Main frame
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(
            header_frame, text="LangChain Box Agent", style="Title.TLabel"
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(
            header_frame,
            text="Interact with your Box files using natural language",
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(side=tk.LEFT, padx=15)

        # Chat history area
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg="white",
            fg=ModernStyles.TEXT_COLOR,  # Ensure text is visible
            font=(ModernStyles.DEFAULT_FONT, ModernStyles.FONT_MEDIUM),
            height=15,
            padx=10,
            pady=10,
            relief=tk.FLAT,
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        # Apply custom tags for user and agent messages
        self.chat_history.tag_configure(
            "user_message",
            background=ModernStyles.USER_BG,
            foreground=ModernStyles.USER_TEXT,
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
        )

        self.chat_history.tag_configure(
            "agent_message",
            background=ModernStyles.AGENT_BG,
            foreground=ModernStyles.AGENT_TEXT,
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
        )

        # Input area
        input_frame = ttk.LabelFrame(main_frame, text="Your Message", padding=10)
        input_frame.pack(fill=tk.X, pady=10)

        self.user_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            bg="white",
            fg=ModernStyles.TEXT_COLOR,  # Ensure text is visible
            font=(ModernStyles.DEFAULT_FONT, ModernStyles.FONT_MEDIUM),
            height=4,
            padx=10,
            pady=10,
            relief=tk.FLAT,
        )
        self.user_input.pack(fill=tk.X)
        self.user_input.bind("<Return>", self.on_enter_key)
        self.user_input.focus_set()

        # Button area
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        send_button = ttk.Button(
            button_frame,
            text="Send",
            command=self.send_message,
            style="Primary.TButton",
            width=10,
        )
        send_button.pack(side=tk.RIGHT, padx=5)

        clear_button = ttk.Button(
            button_frame,
            text="Clear Chat",
            command=self.clear_chat,
            style="Secondary.TButton",
            width=10,
        )
        clear_button.pack(side=tk.RIGHT, padx=5)

        # Predefined prompts area
        prompts_frame = ttk.LabelFrame(main_frame, text="Quick Prompts", padding=10)
        prompts_frame.pack(fill=tk.X, pady=10)

        prompts_buttons_frame = ttk.Frame(prompts_frame)
        prompts_buttons_frame.pack(fill=tk.X)

        # Create buttons for predefined prompts in a grid layout
        for i, prompt in enumerate(self.predefined_prompts):
            col = i % 3
            row = i // 3

            # Create a shorter display version of the prompt if it's too long
            display_prompt = prompt if len(prompt) < 30 else prompt[:27] + "..."

            prompt_button = ttk.Button(
                prompts_buttons_frame,
                text=display_prompt,
                command=lambda p=prompt: self.use_predefined_prompt(p),
                style="PromptButton.TButton",
            )
            prompt_button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Configure grid columns to be equal width
        for i in range(3):
            prompts_buttons_frame.columnconfigure(i, weight=1)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(self.status_message)
        status_bar = ttk.Label(
            self, textvariable=self.status_var, style="Status.TLabel", anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def use_predefined_prompt(self, prompt: str):
        """Use a predefined prompt."""
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, prompt)
        self.send_message()

    def send_message(self):
        """Send the user message to the agent."""
        user_text = self.user_input.get(1.0, tk.END).strip()
        if not user_text:
            return

        # Disable input while processing
        self.user_input.config(state=tk.DISABLED)

        # Display user message with typewriter effect
        self.add_user_message(user_text)

        # Process with agent in a separate thread
        threading.Thread(target=self.process_with_agent, args=(user_text,)).start()

    def on_enter_key(self, event):
        """Handle Enter key press in the input field."""
        # Don't send if shift is held (allow for newlines)
        if not event.state & 0x1:  # 0x1 is the bitmask for Shift
            self.send_message()
            return "break"  # Prevent the default behavior (newline)
        return None  # Allow default behavior

    def process_with_agent(self, query: str):
        """Process the user query with the Box agent."""
        try:
            # Update status
            self.status_var.set("Processing query...")

            # Process query with the agent
            # response = self.agent.process_query(query)

            for message in self.agent.process_query_stream(query):
                # Add the agent's response to the chat
                self.add_agent_message(message)

            # Reset status
            self.status_var.set(self.status_message)
        except Exception as e:
            error_message = f"Error processing query: {str(e)}"
            self.add_agent_message(error_message)
            self.status_var.set("Error occurred")
            print(error_message)
        finally:
            # Re-enable the input field
            self.user_input.config(state=tk.NORMAL)
            self.user_input.delete(1.0, tk.END)
            self.user_input.focus_set()

    def add_user_message(self, message: str):
        """Add a user message to the chat history with typewriter effect."""
        # Import TypewriterText here to handle cross-imports
        from langchain_box_agent_ui_utils import TypewriterText

        # Create a message box for the user message
        self.chat_history.config(state=tk.NORMAL)

        # Add some padding before the message
        self.chat_history.insert(tk.END, "\n\n")

        # Create a marker for the start position of this message
        start_position = self.chat_history.index(tk.END)

        # Add the user prefix
        self.chat_history.insert(tk.END, "You: ", "user_message")

        self.chat_history.config(state=tk.DISABLED)

        # Start the typewriter effect
        if self.user_typewriter:
            self.user_typewriter.stop_typing()

        self.user_typewriter = TypewriterText(
            widget=self.chat_history,
            text=message,
            delay=0.01,
            callback=lambda: self.apply_message_formatting(
                "user_message", start_position
            ),
        )
        self.user_typewriter.start_typing()

    def add_agent_message(self, message: str):
        """Add an agent message to the chat history with typewriter effect."""
        # Import TypewriterText here to handle cross-imports
        from langchain_box_agent_ui_utils import TypewriterText

        # Create a message box for the agent message
        self.chat_history.config(state=tk.NORMAL)

        # Add some padding before the message
        self.chat_history.insert(tk.END, "\n\n")

        # Create a marker for the start position of this message
        start_position = self.chat_history.index(tk.END)

        # Add the agent prefix
        self.chat_history.insert(tk.END, "Agent: ", "agent_message")

        self.chat_history.config(state=tk.DISABLED)

        # Start the typewriter effect
        if self.agent_typewriter:
            self.agent_typewriter.stop_typing()

        self.agent_typewriter = TypewriterText(
            widget=self.chat_history,
            text=message,
            delay=0.01,
            callback=lambda: self.apply_message_formatting(
                "agent_message", start_position
            ),
        )
        self.agent_typewriter.start_typing()

    def apply_message_formatting(self, tag_name, start_position):
        """Apply message formatting after the typewriter effect is complete."""
        self.chat_history.config(state=tk.NORMAL)

        # Get end position
        end_position = self.chat_history.index(tk.END)

        # Apply tag to the entire message (including the prefix)
        self.chat_history.tag_add(tag_name, start_position, end_position)

        # Ensure the latest message is visible
        self.chat_history.see(tk.END)

        self.chat_history.config(state=tk.DISABLED)

    def clear_chat(self):
        """Clear the chat history."""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)

        # Add welcome message again
        self.add_agent_message(
            "Hello! I'm your LangChain Box Agent. I can help you manage your Box files and folders. What would you like to do today?"
        )
