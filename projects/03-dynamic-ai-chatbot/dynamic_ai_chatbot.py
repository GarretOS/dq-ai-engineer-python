"""Interactive conversational chatbot powered by Gemini API."""

import os
import tiktoken
from openai import OpenAI
import datetime
import json


class ConversationManager:
    """
    Manages communication between the chatbot and the AI model.
    """

    def __init__(
        self,
        model="gemini-3.5-flash",
        temperature=0.7,
        max_tokens=2048,
        token_budget=4000,
        system_message="You are a sassy assistant who is fed up with answering questions.",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        history_file=None,
    ):
        # Get the API key securely from the environment variable.
        api_key = os.getenv("GEMINI_API_KEY")

        # Make sure the API key is available before creating the client.
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )
        
        # Store the default model and response settings
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.token_budget = token_budget

        # Store the file used to save and load conversation history.
        self.history_file = history_file
        
        # Generate a unique history filename if none was provided.
        if self.history_file is None:
            self.history_file = (
                f"conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        # Create the OpenAI client using Gemini's OpenAI-compatible API.
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # Define the chatbot's personality using a system message.
        self.system_message = system_message

        # Store the predefined personas that the chatbot can switch between.
        self.system_messages = {
    	    "sassy_assistant": "You are a sassy assistant who is fed up with answering questions.",
    	    "angry_assistant": "You are an angry assistant who likes yelling in ALL CAPS.",
    	    "thoughtful_assistant": (
        	"You are a thoughtful assistant who is always ready to dig deeper. "
        	"Ask clarifying questions to ensure understanding and approach problems "
        	"with a step-by-step methodology."
    	    ),
    	    "custom": system_message,
	}

        self.conversation_history = [
            {"role": "system", "content": self.system_message}
        ]

        
        # Load saved conversation history if a history file already exists.
        self.load_conversation_history()

    def load_conversation_history(self):
        """
        Load conversation history from the history file.
        """
        try:
            with open(self.history_file, "r") as file:
                self.conversation_history = json.load(file)

        except FileNotFoundError:
            # Start a new conversation if the history file does not exist.
            print("No previous conversation history found. Starting a new conversation.")
            self.conversation_history = [
                {"role": "system", "content": self.system_message}
            ]

        except json.JSONDecodeError:
            # Start a new conversation if the history file contains invalid JSON.
            print("The conversation history file is invalid. Starting a new conversation.")
            self.conversation_history = [
                {"role": "system", "content": self.system_message}
            ]

        except Exception as error:
            # Handle unexpected file errors without exposing sensitive information.
            print(f"Could not load conversation history: {error}")
            self.conversation_history = [
               {"role": "system", "content": self.system_message}
            ]

    def save_conversation_history(self):
        """
        Save the current conversation history to the history file.
        """
        try:
            with open(self.history_file, "w") as file:
                json.dump(self.conversation_history, file, indent=4)

        except Exception as error:
            # Handle unexpected file errors without exposing sensitive information.
            print(f"Could not save conversation history: {error}")

    def set_persona(self, persona):
        """
        Switch the chatbot to one of the predefined personas.
        """
        try:
            if persona not in self.system_messages:
                raise ValueError(f"Unknown persona: {persona}")

            self.system_message = self.system_messages[persona]

            # Update the system message in the conversation history.
            self.update_system_message_in_history()

        except Exception as error:
            # Handle errors while changing the chatbot's persona.
            print(f"Could not change persona: {error}")
   
    def set_custom_system_message(self, message):
        """
        Set a custom system message for the chatbot.
        """
        if not message.strip():
            raise ValueError("Custom system message cannot be empty.")

        self.system_messages["custom"] = message
        self.system_message = message

        # Update the system message in the conversation history.
        self.update_system_message_in_history()

    def update_system_message_in_history(self):
        """
        Update the system message stored in the conversation history.
        """
        self.conversation_history[0] = {
            "role": "system",
            "content": self.system_message,
        }

    def count_tokens(self, text):
        """
        Count the number of tokens in a piece of text.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def total_tokens_used(self):
        """
        Calculate the total number of tokens in the conversation history.
        """
        total = 0

        for message in self.conversation_history:
            total += self.count_tokens(message["content"])

        return total

    def enforce_token_budget(self):
        """
        Remove the oldest messages until the conversation fits within the token budget.
        Preserves the system message (at index 0) and only removes conversation messages.
        """
        try:
            while self.total_tokens_used() > self.token_budget:
                # Stop if only the system message remains (never remove it).
                if len(self.conversation_history) <= 1:
                    break
                # Remove the oldest conversation message (index 1).
                self.conversation_history.pop(1)

        except Exception as error:
            # Handle unexpected errors during token counting or history trimming.
            print(f"Could not enforce token budget: {error}")

    def chat_completion(
        self, 
        prompt, 
        temperature=None, 
        max_tokens=None, 
        model=None, 
    ):
        """
        Send a user's prompt to the AI model and return its response.
        """

        # Use the provided values, or fall back to the chatbot's default settings.
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        model = model if model is not None else self.model
        
        self.conversation_history.append(
            {"role": "user", "content": prompt}
        )

        # Calculate the total tokens used after adding the user's prompt.
        total_tokens = self.total_tokens_used()

        # Print the current token count for monitoring.
        print(f"Total tokens used: {total_tokens}")

        #  Remove older messages if the conversation exceeds the token budget.
        self.enforce_token_budget()

        try:
            # Send the system message and user's prompt to the AI model.
            response = self.client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=self.conversation_history,
            )

            # Extract the text generated by the AI model.
            assistant_message = response.choices[0].message.content

            # Add the AI's response to the conversation history.
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )
   
            # Save the updated conversation history to the JSON file.
            self.save_conversation_history() 
           
            return assistant_message

        except Exception as error:
            # Handle API errors without exposing the API key.
            print(f"Error communicating with the AI model: {error}")
            return None


def main():
    """
    Interactive command-line interface for the chatbot.
    """
    print("🤖 Dynamic AI Chatbot")
    print("=" * 50)
    print("Commands: 'help' for options, 'quit' to exit")
    print()
    
    # Initialize chatbot with default persona
    try:
        chatbot = ConversationManager(
            system_message="You are a thoughtful assistant who explains things clearly and step-by-step.",
            token_budget=1000,
        )
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GEMINI_API_KEY environment variable.")
        return
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        
        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("  persona <name>  - Switch persona (sassy_assistant, angry_assistant, thoughtful_assistant)")
            print("  custom <message> - Set a custom system message")
            print("  clear           - Start a new conversation")
            print("  quit            - Exit the chatbot")
            print()
            continue
        
        if user_input.lower().startswith("persona "):
            persona_name = user_input[8:].strip()
            chatbot.set_persona(persona_name)
            print(f"Persona changed to: {persona_name}\n")
            continue
        
        if user_input.lower().startswith("custom "):
            custom_message = user_input[7:].strip()
            chatbot.set_custom_system_message(custom_message)
            print(f"Custom system message set.\n")
            continue
        
        if user_input.lower() == "clear":
            chatbot.conversation_history = [
                {"role": "system", "content": chatbot.system_message}
            ]
            print("Conversation cleared.\n")
            continue
        
        # Send the user's message to the chatbot
        response = chatbot.chat_completion(user_input)
        if response:
            print(f"Assistant: {response}\n")


if __name__ == "__main__":
    main()
