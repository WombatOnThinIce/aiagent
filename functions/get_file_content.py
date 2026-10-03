import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs
        target_is_file = os.path.isfile(target_file)

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not target_is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as file:
            file_content = file.read(MAX_CHARS)
            if file.read(MAX_CHARS):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content

    except Exception as e:
        return f"Error: Exception generated: {e}"

schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "Returns the content of a file as a string, up to a pre-defined number of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get file content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
