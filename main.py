import json
import os
import argparse
import sys

import call_function
from dotenv import load_dotenv
from openai import OpenAI
from call_function import available_functions, call_function
from config import AI_BASE_URL, AI_MODAL, AGENT_LOOP_LIMIT
from prompts import system_prompt


def main():

    # Handle command line arguments:
    parser = argparse.ArgumentParser(description="bootdotdev AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # If the environment variable wasn't found - i.e., if api_key is None - raise a RuntimeError with a helpful message.
    if not api_key:
        raise RuntimeError("No value for OPENROUTER_API_KEY found in .env file.")

    user_prompt = args.user_prompt
    verbose_mode = args.verbose

    client = OpenAI(
        base_url = AI_BASE_URL,
        api_key = api_key,
    )

    session_messages = [
        {
            "role": "system",
            "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    if verbose_mode:
        print(f"User prompt: {user_prompt}\n")

    for _ in range(AGENT_LOOP_LIMIT):
        try:
            final_response = generate_content(client, session_messages, verbose_mode)

            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate content: {e}")

    print(f"Maximum iterations ({AGENT_LOOP_LIMIT}) reached")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None



if __name__ == "__main__":
    main()
