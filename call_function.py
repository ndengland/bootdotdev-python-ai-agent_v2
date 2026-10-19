# Our AI Agent needs a list of functions (more specifically, their schemas)
# This file contains our tools that the LLM can use.


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
