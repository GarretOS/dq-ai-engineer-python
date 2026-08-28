# 🤖 Dynamic AI Chatbot

Dynamic AI Chatbot is an interactive Python chatbot powered by Google's Gemini API. It demonstrates API integration, conversation context management, token counting with tiktoken, dynamic persona switching, and an object-oriented approach to building interactive AI applications. The chatbot maintains conversation history, enforces token budgets to manage API usage, and supports multiple predefined personas.

## Try it interactively

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GarretOS/dq-ai-engineer-python/blob/main/projects/03-dynamic-ai-chatbot/dynamic_ai_chatbot.ipynb)

Run the notebook in Google Colab. You'll be prompted to provide your own Gemini API key (get a free key at https://aistudio.google.com/apikey). Then chat interactively with the AI, switch between different personas, or customize the chatbot's behavior.

## Files

- `dynamic_ai_chatbot.py` — standalone command-line chatbot application and source code.
- `dynamic_ai_chatbot.ipynb` — interactive Google Colab demonstration.
- `requirements.txt` — dependency manifest; this project uses `openai` and `tiktoken` for API communication and token counting.

## Run locally

```bash
export GEMINI_API_KEY="your-api-key-here"
python dynamic_ai_chatbot.py
```

Ensure your `GEMINI_API_KEY` environment variable is set before running the chatbot.

## Important Notes

### Token Counting

This project uses `tiktoken` with the `cl100k_base` encoding to estimate token usage. This is an **approximation** and not Gemini's exact token counter. We intentionally use this approach to teach token counting concepts and management strategies. The approximate count helps manage conversation context within a budget to avoid excessive API costs, but actual Gemini API token usage may differ slightly.

### Personas

The chatbot comes with three predefined personas:
- **sassy_assistant** — Responds with attitude and sarcasm
- **angry_assistant** — Uses all-caps emphatic responses  
- **thoughtful_assistant** — Takes a step-by-step, analytical approach

You can also define custom personas by setting your own system message.

### Conversation History

Conversation history is automatically saved to a timestamped JSON file in the current directory (e.g., `conversation_20260828_121530.json`). These files are ignored by Git and won't be committed to the repository.
