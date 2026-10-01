import os,subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_file = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs
        target_is_file = os.path.isfile(target_file)

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not target_is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command,capture_output=True, cwd=work_dir_abs, text=True, timeout=30)

        parts = []
        if completed_process.returncode != 0:
            parts.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stderr and not completed_process.stdout:
            parts.append("No output produced")
        if completed_process.stderr:
            parts.append(f"STDERR: {completed_process.stderr}")
        if completed_process.stdout:
            parts.append(f"STDOUT: {completed_process.stdout}")
        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
