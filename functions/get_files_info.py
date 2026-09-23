import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
        valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs
        target_is_dir = os.path.isdir(target_dir)
    except Exception as e:
        return f'Error: Exception generated: {e}'
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not target_is_dir:
        return f'Error: "{directory}" is not a directory'
    else:
        return f'Success: "{directory}" is within the working directory'
