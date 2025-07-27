import json

def handle_manage_cmd(timers_filepath, args):
    if len(args) <= 1:
        # TODO: Actually print to shell properly probs using stdout ("Invalid argument count")
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

                pause_state = None

                if args[2] == "pause":
                    pause_state = True
                elif args[2] == "unpause":
                    pause_state = False
                elif args[2] == "toggle-pause":
                    pause_state = not json_obj[timer_id]["paused"]
                else:
                    # TODO: Actually print to shell properly probs using stdout ("Invalid command provided for timer")
                    return

                json_obj[timer_id]["paused"] = pause_state

                with open(timers_filepath, "w") as file_handle:
                    json.dump(json_obj, file_handle, indent=2)

    except FileNotFoundError:
        return

