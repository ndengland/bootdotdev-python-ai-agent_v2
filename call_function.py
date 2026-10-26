# Our AI Agent needs a list of functions (more specifically, their schemas)
# This file contains our tools that the LLM can use.
import json
from collections.abc import Callable
from config import WORKING_DIR
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


# OpenAI SDK schema to define this as a function we can use in an LLM:
# Function signature (copied from source)
# def get_files_info(working_directory: str, directory: str = ".") -> str:
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List names and metadata for files in a directory. Use only when the user asks to list or inspect a directory; do not read or execute files.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The working directory path in which the program is scoped to run.",
                },
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required" : ["working_directory"],
        },
    },
}

# OpenAI SDK schema to define this as a function we can use in an LLM:
# Function signature (copied from source)
# def get_file_content(working_directory, file_path):
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read and return the text contents of one file. Use for requests to read, view, or inspect a file; never to execute it.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The working directory path in which the program is scoped to run. This is a required parameter.",
                },
                "file_path": {
                    "type": "string",
                    "description": "The path of the single file to read, relative to the working directory. This is a required parameter."
                },
            },
            "required" : ["working_directory", "file_path"],
        },
    },
}

# OpenAI SDK schema to define this as a function we can use in an LLM:
# Function signature (copied from source)
# def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python script and return its output. Use this whenever the user asks to run, execute, or launch a .py file. Do not use this to read or list files.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "The working directory path in which the program is scoped to run. This is a required parameter.",
                },
                "file_path": {
                    "type": "string",
                    "description": "File path and name in which to read the contents of, relative to the working directory. This is a required parameter.",
                },
                "args": {
                    "type": "array",
                    "description": "Optional runtime arguments that the python file may need to run.",
                    "items": {
                        "type" : "string",
                        "description" : "A single argument passed to the runtime environment."
                    }
                },

            },
            "required" : ["working_directory", "file_path"],
        },
    },
}

# OpenAI SDK schema to define this as a function we can use in an LLM:
# Function signature (copied from source)
# def write_file(working_directory: str, file_path: str, content: str) -> str:
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text to a specified file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Working directory that the target file exists in which we want to write to. This is a required parameter.",
                },
                "file_path": {
                    "type": "string",
                    "description": "File path and name in which to read the contents of, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content that will be written to the target file. This is a required parameter.",
                },
            },
            "required" : ["working_directory", "file_path", "content"],
        },
    },
}

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
    """

    :param tool_call: One of the tool-call objects from message.tool_calls
        contains tool_call.function.name (name of a function as a string)
        tool_call.function.arguments (arguments for the tool call as a JSON string)
        too_call.id (unique identifier for this specific call, and is needed to send the result back)
    :param verbose: if true, print more verbose output to console.
    :return:
    """

    function_name : str = tool_call.function.name
    function_args : dict = json.loads(tool_call.function.arguments or {})

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # we need to determine which of our internal functions we need to call (if any)
    # we need to map our function NAMES to a useful dictionary

    # noinspection bad-assignment
    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_name not in function_map:
        # if the provided function name is _not_ found in our mapping, return a tool message with appropriate details:
        unknown_function: dict = {
            "role": "tool",
            "tooL_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
        return unknown_function

    # We need to inject `working_directory` argument into the function_args dict. The LLM doesn't know about it:
    function_args["working_directory"] = WORKING_DIR

    # CALL THE FUNCTION:
    function_result = function_map[function_name](**function_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": function_result,
    }




