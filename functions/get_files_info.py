import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
        valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs
        target_is_dir = os.path.isdir(target_dir)

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not target_is_dir:
            return f'Error: "{directory}" is not a directory'

        items: list[str] = []
        for item in os.listdir(target_dir):
            item_details = (item, os.path.getsize(os.path.join(target_dir, item)), os.path.isdir(os.path.join(target_dir, item)))
            item_str = f"- {item_details[0]}: file_size={item_details[1]} bytes, is_dir={item_details[2]}"
            items.append(item_str)
        return "\n".join(items)

    except Exception as e:
        return f'Error: Exception generated: {e}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
