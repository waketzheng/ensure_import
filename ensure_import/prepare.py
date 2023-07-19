import subprocess
import sys


def run():
    cmd = "pre-commit install && poetry install"
    print("--> Executing shell command:")
    print(cmd)
    rc = subprocess.call(cmd, shell=True)
    if rc:
        sys.exit(1)


if __name__ == "__main__":
    run()
