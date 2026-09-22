import os
import argparse
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

_AI_MODAL = "openrouter/free"
_AI_BASE_URL = "https://openrouter.ai/api/v1"


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # If the environment variable wasn't found - i.e., if api_key is None - raise a RuntimeError with a helpful message.
    if api_key is None:
        raise RuntimeError("No value for OPENROUTER_API_KEY found in .env file.")

    # Handle command line arguments:
    parser = argparse.ArgumentParser(description="bootdotdev AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable verbose output")
    args = parser.parse_args()

    # Now we can access `args.user_prompt`
    user_prompt = args.user_prompt
    verbose_mode = args.verbose

    client = OpenAI(
        base_url = _AI_BASE_URL,
        api_key = api_key,
    )

    session_messages = [
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    response = client.chat.completions.create(
        model = _AI_MODAL,
        messages = session_messages
    )

    # The method returns a chat completion object. The model's text answer lives at response.choices[0].message.content. Print it to see the model's answer.
    response_message = response.choices[0].message.content

    """
    Prompt tokens: X
    Response tokens: Y
    """
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    if verbose_mode:
        # Print metadata:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")


    print(f"Response Message: {response_message}")



if __name__ == "__main__":
    main()
