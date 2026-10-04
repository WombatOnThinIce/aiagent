import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs
        target_is_dir = os.path.isdir(target_file)

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if target_is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Exception generated: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a string to a file, replacing the existing content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of file to write to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content of string to write to file",
                },
            },
        },
    },
}
