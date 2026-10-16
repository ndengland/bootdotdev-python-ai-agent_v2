import os.path

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        # validate the path to target file is INSIDE the working directory:
        working_dir_full_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_full_path, file_path))

        # make sure the target file path shares a common path (exists in) the working directory:
        is_valid_target_file = os.path.commonpath([working_dir_full_path, target_file]) == working_dir_full_path

        if not is_valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(working_dir_full_path, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Exception Occurred: {e}"
