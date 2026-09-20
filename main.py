import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI


def main():
    print("Hello from bootdotdev-python-ai-agent-v2!")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # If the environment variable wasn't found - i.e., if api_key is None - raise a RuntimeError with a helpful message.
    if api_key is None:
        raise RuntimeError("No value for OPENROUTER_API_KEY found in .env file.")

    # Handle command line arguments:
    parser = argparse.ArgumentParser(description="bootdotdev AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # Now we can access `args.user_prompt`
    user_prompt = args.user_prompt

    print(f"User Prompt: {user_prompt}")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    # The method returns a chat completion object. The model's text answer lives at response.choices[0].message.content. Print it to see the model's answer.
    response_message = response.choices[0].message.content

    """
    Prompt tokens: X
    Response tokens: Y
    """
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

    print("Response Message:")
    print(response_message)



if __name__ == "__main__":
    main()
