import sys
import os
import subprocess

import psutil

def start_service():
    print("starting service...")
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen(
        [sys.executable, "main.py", "--service"], # TEMP: Whilst testing, main.py is hard-coded but should be removed
        creationflags=DETACHED_PROCESS,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )

def handle_start_cmd(service_filepath):
    try:
        with open(service_filepath, "r") as file_handle:
            read_content = file_handle.read()

            print(f"read_content: {read_content}")

            if read_content != None:
                if (psutil.pid_exists(int(read_content))):
                    print("exists already")
                    # TODO: Print to console saying the service is already started (probs using stdout)
                    return
                else:
                    start_service()

    except FileNotFoundError:
        start_service()

