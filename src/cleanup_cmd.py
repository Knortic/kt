import os

def handle_cleanup_cmd(timers_filepath):
    if not os.path.exists(timers_filepath):
        return

    os.remove(timers_filepath)

