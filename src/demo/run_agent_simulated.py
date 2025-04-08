#!/usr/bin/env python3
"""
Quick launch script for the LangChain Box Agent Demo.
This automatically launches the demo in simulated mode (no real Box connection).
"""

if __name__ == "__main__":
    # Import required components
    from agent_implementations import SimulatedAgent
    from langchain_box_agent_ui import LangChainBoxAgentUI

    # Create a simulated agent
    agent = SimulatedAgent()

    # Start the UI with the simulated agent
    app = LangChainBoxAgentUI(agent, status_message="Demo Mode (Simulated Agent)")
    app.mainloop()
