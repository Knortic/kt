import os
import json

from datetime import datetime, timedelta

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600) # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60) # 60 seconds in a minute

    result = ""

    if hours > 0:
        result += f"{hours}h "
    if minutes > 0:
        result += f"{minutes}m "
    if seconds > 0 or not parts:
        result += f"{seconds}s"

    return result

def handle_ls_cmd(timers_filepath, args):
    if not os.path.exists(timers_filepath):
        # TODO: Actually print to shell properly probs using stdout ("No active timers")
        return

    with open(timers_filepath, "r") as file_handle:
        read_content = file_handle.read()

        json_obj = json.loads(read_content)

        if not json_obj:
            # TODO: Actually print to shell properly probs using stdout ("No active timers")
            return

        output = ""

        for idx, item in enumerate(json_obj):
            output += f"{item['id']} "
            output += f'"{item["message"]}" '

            timestamp = datetime.fromisoformat(item["timestamp"])
            current_time = datetime.now()

            if current_time > timestamp:
                output += f"{format_timedelta(current_time - timestamp)} ago\n"
            else:
                output += f"{format_timedelta(timestamp - current_time)}\n"

        # TODO: Actually print to shell properly probs using stdout ("No active timers")
        print(output)


