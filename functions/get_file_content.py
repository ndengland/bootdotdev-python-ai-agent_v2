import os.path
from config import READ_MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # validate the path to target file is INSIDE the working directory:
        working_dir_full_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_full_path, file_path))

        # make sure the target file path shares a common path (exists in) the working directory:
        is_valid_target_file = os.path.commonpath([working_dir_full_path, target_file]) == working_dir_full_path

        if not is_valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # read the file
        file_content_string = ""
        with open(target_file, "r") as f:
            file_content_string = f.read(READ_MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {READ_MAX_CHARS} characters]'

        return file_content_string

    except Exception as e:
        print(e)
        return f"Error: {e}"
