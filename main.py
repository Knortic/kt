import sys
import json
import os
import time

import psutil

from winotify import Notification, audio

from datetime import datetime, timedelta

from src.start_cmd import handle_start_cmd
from src.stop_cmd import handle_stop_cmd
from src.add_cmd import handle_add_cmd
from src.ls_cmd import handle_ls_cmd

timers_filepath = "timers.json"
service_filepath = "kt.pid"

def handle_service_cmd(args):
    with open(service_filepath, "w") as file_handle:
        file_handle.write(str(os.getpid()))

    while True:
        time.sleep(1)

        if not os.path.exists(service_filepath):
            break

        read_content = None

        try:
            with open(timers_filepath, "r") as file_handle:
                read_content = file_handle.read()
        except Exception as e:
            # TODO: Actually print to shell properly probs using stdout
            print(f"Exception: {e}")

        json_obj = json.loads(read_content)

        current_time = datetime.now()

        # Remove the microseconds since we don't need our timestamp comparison
        # to be that precise
        converted_current_time = current_time.replace(microsecond=0)

        for idx, item in enumerate(json_obj):
            timestamp = datetime.fromisoformat(item["timestamp"])

            if (converted_current_time >= timestamp):
                try:
                    with open(timers_filepath, "w") as file_handle:
                        json_obj.pop(idx)
                        json.dump(json_obj, file_handle, indent=2)

                        toast = Notification(app_id="k timer (kt)",
                                             title=item["message"],
                                             #msg="test"
                                             duration="long" if converted_current_time == timestamp else "short") # Missed notifications will appear for a shorter amount of time

                        toast.set_audio(audio.LoopingAlarm9, loop=True)
                        toast.add_actions(label="Dismiss")
                        toast.show()

                except Exception as e:
                    # TODO: Actually print to shell properly probs using stdout
                    print(f"Exception: {e}")

        # JSON object no longer has items
        if not json_obj:
            break

def main():
    # Obtain the args but skip the main executable name
    args = sys.argv[1:]

    if args[0] == "start":
        handle_start_cmd(service_filepath)
    elif args[0] == "stop":
        handle_stop_cmd(service_filepath)
    elif args[0] == "--service":
        handle_service_cmd(args)
    elif args[0] == "add":
        handle_add_cmd(timers_filepath, args)
    elif args[0] == "ls":
        handle_ls_cmd(timers_filepath, args)
    else:
        # TODO: Actually print to shell properly probs using stdout
        print("Not a valid command")
        return

if __name__ == "__main__":
    main()
