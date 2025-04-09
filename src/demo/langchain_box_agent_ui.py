import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

from .langchain_box_agent_ui_utils import TypewriterText


class LangChainBoxAgentUI(tk.Tk):
    def __init__(self, agent, status_message: str = "Connected"):
        super().__init__()

        self.title("Box Agent")
        self.geometry("800x600")
        self.minsize(700, 500)
        # self.configure(bg=MacStyles.BG_COLOR)

        # Setup ttk styles
        # self.style = ttk.Style()
        self.style = ttk.Style().theme_use("clam")
        # MacStyles.configure_styles(self.style)

        # Store the Box agent and status message
        self.agent = agent
        self.status_message = status_message

        # Initialize typewriter effects
        self.user_typewriter = None
        self.agent_typewriter = None

        # Sample predefined prompts
        self.predefined_prompts = [
            "Who am I?",
            "Search for PDF files",
            "What's in my root folder?",
            "Create a folder called 'Demo'",
            "Read sample.txt",
            "Extract data from HAB-1-01.docx",
        ]

        # Setup UI
        self.create_widgets()

        # Display welcome message
        self.add_agent_message("Hello! I'm your Box Agent. How can I help you today?")

    def create_widgets(self):
        """Create the UI widgets with a simple, clean design."""

        # Main frame with padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Simple header
        header = ttk.Label(main_frame, text="Box Agent", style="Header.TLabel")
        header.pack(pady=(0, 10))

        # Chat history area (takes most of the space)
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            # bg=MacStyles.BG_COLOR,
            # font=(MacStyles.DEFAULT_FONT, MacStyles.FONT_SIZE),
            relief=tk.FLAT,
            # highlightthickness=1,
            # highlightbackground=MacStyles.BORDER_COLOR,
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        # Configure message styles
        self.chat_history.tag_configure(
            "user_message",
            # background=MacStyles.USER_BG,
            # foreground=MacStyles.USER_TEXT,
            justify="right",
            rmargin=20,
            lmargin1=100,
            lmargin2=100,
        )

        self.chat_history.tag_configure(
            "agent_message",
            # background=MacStyles.AGENT_BG,
            # foreground=MacStyles.AGENT_TEXT,
            justify="left",
            lmargin1=20,
            lmargin2=20,
            rmargin=100,
        )

        # User input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        self.user_input = tk.Text(
            input_frame,
            wrap=tk.WORD,
            height=3,
            # font=(MacStyles.DEFAULT_FONT, MacStyles.FONT_SIZE),
            relief=tk.FLAT,
            # highlightthickness=1,
            # highlightbackground=MacStyles.INPUT_BORDER,
            # bg=MacStyles.INPUT_BG,
            # foreground=MacStyles.USER_TEXT,
            padx=5,
            pady=5,
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.on_enter_key)
        self.user_input.focus_set()

        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style="Primary.TButton",
            width=8,
        )
        send_button.pack(side=tk.RIGHT, padx=(5, 0))

        # Quick prompts (simple row of buttons)
        prompts_frame = ttk.Frame(main_frame)
        prompts_frame.pack(fill=tk.X, pady=(0, 5))

        # Create flow layout for prompts
        for i, prompt in enumerate(self.predefined_prompts):
            prompt_button = ttk.Button(
                prompts_frame,
                text=prompt if len(prompt) < 20 else prompt[:17] + "...",
                command=lambda p=prompt: self.use_predefined_prompt(p),
                style="Prompt.TButton",
            )
            prompt_button.pack(side=tk.LEFT, padx=(0, 5), pady=2)

        # Simple status bar
        status_bar = ttk.Frame(self, height=24)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        separator = ttk.Separator(status_bar, orient="horizontal")
        separator.pack(fill=tk.X)

        self.status_var = tk.StringVar()
        self.status_var.set(self.status_message)
        status_label = ttk.Label(
            status_bar, textvariable=self.status_var, style="Status.TLabel"
        )
        status_label.pack(side=tk.LEFT, fill=tk.X)

        # Clear button in status bar
        clear_button = ttk.Button(
            status_bar,
            text="Clear Chat",
            command=self.clear_chat,
            style="Prompt.TButton",
            width=12,
        )
        clear_button.pack(side=tk.RIGHT, padx=5, pady=2)

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

        # Display user message
        self.add_user_message(user_text)

        # Process with agent in a separate thread
        threading.Thread(target=self.process_with_agent, args=(user_text,)).start()

    def on_enter_key(self, event):
        """Handle Enter key press in the input field."""
        # Don't send if shift is held (allow for newlines)
        if not event.state & 0x1:
            self.send_message()
            return "break"  # Prevent the default behavior
        return None  # Allow default behavior

    def process_with_agent(self, query: str):
        """Process the user query with the Box agent."""
        try:
            # Update status
            self.status_var.set("Processing query...")

            # Process query with the agent
            for message in self.agent.process_query_stream(query):
                # Add the agent's response to the chat
                self.add_agent_message(message)

            # Reset status
            self.status_var.set(self.status_message)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.add_agent_message(error_message)
            self.status_var.set("Error occurred")
            print(error_message)
        finally:
            # Re-enable the input field
            self.user_input.config(state=tk.NORMAL)
            self.user_input.delete(1.0, tk.END)
            self.user_input.focus_set()

    def add_user_message(self, message: str):
        """Add user message to chat with imessage-like bubble effect."""

        self.chat_history.config(state=tk.NORMAL)

        # Add some padding before message
        self.chat_history.insert(tk.END, "\n\n")

        # Create marker for the start of message
        start_position = self.chat_history.index(tk.END)

        # Add the message header
        self.chat_history.insert(tk.END, "You: \n", "user_message")

        self.chat_history.config(state=tk.DISABLED)

        # Start typewriter effect
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
        """Add agent message to chat with imessage-like bubble effect."""

        self.chat_history.config(state=tk.NORMAL)

        # Add some padding before message
        self.chat_history.insert(tk.END, "\n\n")

        # Create marker for the start of message
        start_position = self.chat_history.index(tk.END)

        # Add the message header
        self.chat_history.insert(tk.END, "Box: \n", "agent_message")

        self.chat_history.config(state=tk.DISABLED)

        # Start typewriter effect
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
        """Apply message formatting after typewriter effect is complete."""
        self.chat_history.config(state=tk.NORMAL)

        # Get end position
        end_position = self.chat_history.index(tk.END)

        # Apply tag to the entire message
        self.chat_history.tag_add(tag_name, start_position, end_position)

        # Ensure message is visible
        self.chat_history.see(tk.END)

        self.chat_history.config(state=tk.DISABLED)

    def clear_chat(self):
        """Clear the chat history."""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)

        # Add welcome message again
        self.add_agent_message("Hello! I'm your Box Agent. How can I help you today?")
