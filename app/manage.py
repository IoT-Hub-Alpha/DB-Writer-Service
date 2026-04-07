#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
import time

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_writer.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) > 1 and sys.argv[1] == "db_writer":
        manage_py = os.path.abspath(__file__)
        base_dir = os.path.dirname(manage_py)

        runserver_proc = subprocess.Popen(
            [
                sys.executable,
                manage_py,
                "runserver",
                "0.0.0.0:8033",
                "--noreload",
            ],
            cwd=base_dir,
        )

        time.sleep(1)

        if runserver_proc.poll() is not None:
            raise RuntimeError(
                f"runserver exited immediately with code {runserver_proc.returncode}"
            )

        try:
            execute_from_command_line(sys.argv)
        finally:
            runserver_proc.terminate()
            runserver_proc.wait(timeout=5)
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
