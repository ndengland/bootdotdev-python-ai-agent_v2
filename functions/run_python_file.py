import os.path
import subprocess

from config import RUN_PROCESS_TIMEOUT_SEC


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        # validate the path to target file is INSIDE the working directory:
        working_dir_full_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_full_path, file_path))

        # make sure the target file path shares a common path (exists in) the working directory:
        is_valid_target_file = os.path.commonpath([working_dir_full_path, target_file]) == working_dir_full_path

        if not is_valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # FIXME is this a better way or even necessary?
        # root, ext = os.path.splitext(file_path)
        # if ext != ".py":
        #     return f'Error: "{file_path}" is not a Python file'

        #
        # Set up the Command to run
        #
        command = ["python", target_file]

        # handle additional arguments:
        if args:
            command.extend(args)

        # run the process:
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=RUN_PROCESS_TIMEOUT_SEC)

        # Aggregate the output
        output_strings = list()
        if completed_process.returncode != 0:
            output_strings.append(f"Process exited with code {completed_process.returncode}.")
        if not completed_process.stdout and not completed_process.stderr:   # Check for empty strings returned
            output_strings.append("No output produced.")
        if completed_process.stdout:
            output_strings.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output_strings.append(f"STDERR:\n{completed_process.stderr}")

        return "\n".join(output_strings)


    except Exception as e:
        print(e)
        return f"Error: {e}"
