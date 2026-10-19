"""
The key idea is that the `directory` parameter will be treated as a relative path within the `working_directory`.

We'll allow the LLM agent to specify which directory it wants to scan, but the working_directory will be set by us.

This means we can limit the scope of directories and files that the LLM is able to view.
"""
import os.path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """

    All of our "tool call" functions, including get_files_info, should always return a string.
    If errors can be raised inside them, we need to catch those errors and return a string describing the error instead.
    This will allow the LLM to handle errors gracefully.

    :param working_directory:
    :param directory:
    :return: str
    """

    # TODO this would be a useful tool function
    working_dir_abs_path = os.path.abspath(working_directory)
    target_dir_full_path = os.path.normpath(os.path.join(working_dir_abs_path, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir_full_path]) == working_dir_abs_path

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_dir_full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        contents_list = list()

        for item in os.listdir(target_dir_full_path):
            item_full_path = os.path.join(target_dir_full_path, item)
            if os.path.isdir(item_full_path):
                contents_list.append(f" - {item}: file_size={os.path.getsize(item_full_path)}, is_dir=True")
            elif os.path.isfile(item_full_path):
                contents_list.append(f" - {item}: file_size={os.path.getsize(item_full_path)}, is_dir=False")

        return "\n".join(contents_list)

    except Exception as e:
        return f"Error: {e}"
