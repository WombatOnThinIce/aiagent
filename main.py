import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from config import MAX_CHAT_ITERATIONS
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt to the AI model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API Key not found")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    for _ in range(MAX_CHAT_ITERATIONS):
        completed = generate_content(client, messages, args.verbose)
        if completed:
            break
    else:
        print("Maximum iterations reached")
        sys.exit(1)



def generate_content(client: OpenAI, messages: list, verbose: bool) -> bool:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("No Usage property available. Possible failed API request")
    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return True
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        if verbose:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args}")
        result_message = call_function(tool_call, verbose)
        if not result_message["content"]:
            raise Exception("Tool call did not return result message")
        messages.append(result_message)
        if verbose: print(f"-> {result_message['content']}")
    return False


if __name__ == "__main__":
    main()
