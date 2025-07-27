import json

cmds = [ "pause", "unpause", "toggle-pause",
         "stop", "reset"
       ]

def handle_pause_state(json_obj, timer_id, args):
    pause_state = json_obj[timer_id]["paused"] 

    if args[2] == "pause":
        pause_state = True
    elif args[2] == "unpause":
        pause_state = False
    elif args[2] == "toggle-pause":
        pause_state = not pause_state

    json_obj[timer_id]["paused"] = pause_state

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

                if args[2] == "stop" or args[2] == "reset":
                    json_obj[timer_id]["reset"] = True

                with open(timers_filepath, "w") as file_handle:
                    json.dump(json_obj, file_handle, indent=2)

    except FileNotFoundError:
        return

