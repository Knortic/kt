import json

from src.time_utils import convert_duration_string_to_timestamp

from datetime import datetime, timedelta

cmds = [ "pause", "toggle-pause", "toggle"
         "stop", "reset",
         "remove", "rm",
         "start",
         "unpause", "resume"
       ]

def on_unpause(json_obj, timer_id):
    current_time = datetime.now()

    # If there is no pause timestamp then it is assumed we
    # are trying to start an already active/ticking timer
    if not json_obj[timer_id].get("pause-timestamp"):
        return

    active_timestamp = datetime.fromisoformat(json_obj[timer_id]["timestamp"])
    pause_timestamp = datetime.fromisoformat(json_obj[timer_id]["pause-timestamp"])

    new_timestamp = None

    if active_timestamp < pause_timestamp:
        new_timestamp = current_time - (pause_timestamp - active_timestamp)
    else:
        new_timestamp = (active_timestamp - pause_timestamp) + current_time

        # If spammed fast enough new timestamp can actually be less than
        # current time which should be impossible for what we want,
        # so if that is the case then just set it to the current time instead
        # whilst this isn't a complete fix, it is a better alternative
        # than the impossible
        if new_timestamp < current_time:
            new_timestamp = current_time

    json_obj[timer_id]["timestamp"] = new_timestamp.isoformat()
    json_obj[timer_id].pop("pause-timestamp")

# Adds pause timestamp entry to json object
def on_pause(json_obj, timer_id):
    json_obj[timer_id]["pause-timestamp"] = datetime.now().isoformat()

def handle_pause_state(json_obj, timer_id, args):
    if args[2] == "pause":
        on_pause(json_obj, timer_id)
    elif args[2] == "unpause" or args[2] == "resume":
        on_unpause(json_obj, timer_id)
    elif args[2] == "toggle-pause" or args[2] == "toggle":
        if json_obj[timer_id].get("pause-timestamp"):
            on_unpause(json_obj, timer_id)
        else:
            on_pause(json_obj, timer_id)

def handle_reset_state(json_obj, timer_id, args):
    if args[2] == "stop" or args[2] == "reset":
        json_obj[timer_id]["reset"] = True

def handle_remove(json_obj, timer_id, args):
    if args[2] == "remove" or args[2] == "rm":
        json_obj.pop(timer_id)

        # Sort the items to rearrange their ids
        for idx, item in enumerate(json_obj):
            item["id"] = idx

def handle_start(json_obj, timer_id, args):
    if args[2] == "start":
        if not json_obj[timer_id].get("duration"):
            # TODO: Actually print to shell properly probs using stdout
            return

        duration_key = json_obj[timer_id]["duration"]
        duration_timestamp = datetime.now()
        duration_timestamp += convert_duration_string_to_timestamp(duration_key)

        json_obj[timer_id]["timestamp"] = duration_timestamp.isoformat()


def handle_manage_cmd(timers_filepath, args):
    if len(args) <= 1:
        # TODO: Actually print to shell properly probs using stdout ("Invalid argument count")
        return

    if not args[2] in cmds:
        # TODO: Actually print to shell properly probs using stdout ("Unrecognized command")
        return

    timer_id = int(args[1])

    try:
        with open(timers_filepath, "r") as file_handle:
            read_content = file_handle.read()

            if read_content != None:
                json_obj = json.loads(read_content)

                if timer_id > len(json_obj) - 1:
                    # TODO: Actually print to shell properly probs using stdout ("Invalid id provided")
                    return

                handle_pause_state(json_obj, timer_id, args)
                handle_reset_state(json_obj, timer_id, args)
                handle_remove(json_obj, timer_id, args)
                handle_start(json_obj, timer_id, args)

                with open(timers_filepath, "w") as file_handle:
                    json.dump(json_obj, file_handle, indent=2)

    except FileNotFoundError:
        return

