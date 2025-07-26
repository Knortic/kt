import sys
import json
import os
import time
import subprocess

import psutil

from winotify import Notification, audio

from datetime import datetime, timedelta

timers_filepath = "timers.json"
service_filepath = "kt.pid"

def start_service():
    print("starting service...")
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen(
        [sys.executable, __file__, "--service"],
        creationflags=DETACHED_PROCESS,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )

def handle_add_cmd(args):
    # Drop the command from the args e.g. "add"
    args = args[1:]

    arg_count = len(args)

    # Required argument count is either 2 or 4 because the format is as follows:
    # 2: "-t" "20s"
    # 4: "-m" "Message here" "-t" "20s"
    has_invalid_arg_count = arg_count != 2 and arg_count != 4
    if has_invalid_arg_count:
        # TODO: Actually print to shell properly probs using stdout
        print("Invalid argument count provided!")
        return

    if arg_count == 2:
        if args[0] != "-t":
            # TODO: Actually print to shell properly probs using stdout
            print("Provided invalid first argument, expected '-t'")
            return
    else:
        if args[0] != "-m":
            # TODO: Actually print to shell properly probs using stdout
            print("Provided invalid first argument, expected '-m'")
            return

    cmd_duration = args[-1]
    cmd_message = args[1]

    if args[0] == "-t":
        cmd_message = ""

    read_content = None
    json_obj = None
    cmd_timestamp = datetime.now() 

    cmd_duration_int = cmd_duration[:-1]

    if cmd_duration.endswith('s'):
        cmd_timestamp += timedelta(seconds=int(cmd_duration_int))
    elif cmd_duration.endswith('m'):
        cmd_timestamp += timedelta(minutes=int(cmd_duration_int))
    elif cmd_duration.endswith('h'):
        cmd_timestamp += timedelta(hours=int(cmd_duration_int))

    cmd_timestamp = cmd_timestamp.replace(microsecond=0)

    # Subtract 1 second from the converted time otherwise
    # the time won't be accurate
    cmd_timestamp = cmd_timestamp - timedelta(seconds=1)

    try:
        with open(timers_filepath, "r") as file_handle:
            read_content = file_handle.read()

        if read_content != None:
            json_obj = json.loads(read_content)

            # We compute the latest_id by first getting the length of the items
            # in the json data and then substracting one to convert it to index-based
            latest_id = len(json_obj) - 1

            json_obj.append({})

            # Since this is the next item we are generating we need to add one
            # otherwise the latest id will point to the previous item and not the new
            # item we are generating
            json_obj[-1]["id"] = latest_id + 1;

            json_obj[-1]["message"] = cmd_message;
            json_obj[-1]["duration"] = cmd_duration;
            json_obj[-1]["timestamp"] = cmd_timestamp.isoformat();

            json_obj[-1]["paused"] = False;
            json_obj[-1]["reset"] = False;

            with open(timers_filepath, "w") as file_handle:
                json.dump(json_obj, file_handle, indent=2)

            # self.json_obj[-1]["timestamp"] = self.timer_data.timestamp.isoformat();

    except FileNotFoundError:
        with open(timers_filepath, "w") as file_handle:
            json_obj = []
            json_obj.append({})

            json_obj[0]["id"] = 0
            json_obj[0]["message"] = cmd_message
            json_obj[0]["duration"] = cmd_duration
            json_obj[0]["timestamp"] = cmd_timestamp.isoformat();
            json_obj[0]["pause"] = False
            json_obj[0]["reset"] = False

            json.dump(json_obj, file_handle, indent=2)

    print(json_obj)
    return


    toast = Notification(app_id="k timer (kt)",
                         title=timer_title,
                         #msg="test"
                         duration="long")

    toast.set_audio(audio.LoopingAlarm9, loop=True)
    toast.add_actions(label="Dismiss")

    toast.show()

def handle_start_cmd(args):
    try:
        with open(service_filepath, "r") as file_handle:
            read_content = file_handle.read()

        if read_content != None:
            if (psutil.pid_exists(int(read_content))):
                print("exists already")
                # TODO: Print to console saying the service is already started (probs using stdout)
                return
            else:
                start_service()

    except FileNotFoundError:
        start_service()

def handle_stop_cmd(args):
    if not os.path.exists(service_filepath):
        # TODO: Print to console saying the service is already started
        return

    os.remove(service_filepath)

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
        handle_start_cmd(args)
    elif args[0] == "stop":
        handle_stop_cmd(args)
    elif args[0] == "--service":
        handle_service_cmd(args)
    elif args[0] == "add":
        handle_add_cmd(args)
    else:
        # TODO: Actually print to shell properly probs using stdout
        print("Not a valid command")
        return

if __name__ == "__main__":
    main()
