import os
import json
import time

from src.time_utils import convert_duration_string_to_timestamp, format_timedelta
from src.custom_controls import CustomTimeTextColumn, ColorBarColumn, FieldTextColumn

from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn
from rich.console import Console, Group

from datetime import datetime, timedelta

current_time = None

# This is mainly used for slight spacing, not quite as much
# as a new line character but can result in prettier printing
def print_carriage_return(console):
    console.print('\r')

def handle_ls_cmd(timers_filepath, args):

    current_time = datetime.now()

    if len(args) == 2 and args[1] != "-p":
        return

    if not os.path.exists(timers_filepath):
        # TODO: Actually print to shell properly probs using stdout ("No active timers")
        return

    with open(timers_filepath, "r") as file_handle:
        read_content = file_handle.read()

        json_obj = json.loads(read_content)

        if not json_obj:
            # TODO: Actually print to shell properly probs using stdout ("No active timers")
            return

        console = Console()

        print_carriage_return(console)

        refresh_delay_sec = 1

        progress = Progress(FieldTextColumn('{id}'),
                            ColorBarColumn(bar_width=10),
                            CustomTimeTextColumn(""),
                            auto_refresh=False
                            )

        tasks = []

        for idx, item in enumerate(json_obj):
            tasks.append(progress.add_task("", total=100, item=item))

        arg_count = len(args)

        if arg_count <= 2:
            try:
                with progress:
                    time_threshold = 2.1
                    while not progress.finished or arg_count == 2:
                        refresh_display_fast = False
                        for task in tasks:
                            item = progress._tasks[task].fields.get("item")
                            current_timestamp = datetime.now().timestamp()
                            active_timestamp = datetime.fromisoformat(item["timestamp"]).timestamp()

                            has_pause_timestamp = False
                            if item.get("pause-timestamp"):
                                has_pause_timestamp = True
                                current_timestamp = datetime.fromisoformat(item["pause-timestamp"]).timestamp()

                            if current_timestamp < active_timestamp:
                                duration = convert_duration_string_to_timestamp(item['duration'])

                                start_timestamp = active_timestamp - duration.total_seconds()

                                if duration == 0:
                                    duration = -1

                                percentage = (current_timestamp - start_timestamp) / duration.total_seconds()

                                if not has_pause_timestamp:
                                    # Since sleep can be every second, we want to make sure
                                    # this will actually be hit by having a threshold
                                    if (active_timestamp - current_timestamp) < time_threshold:
                                        refresh_display_fast = True
                                        refresh_delay_sec = 0.05

                                # Clamp between 0 - 100 percent
                                percentage = max(0, min(percentage * 100, 100))
                            else:
                                if not has_pause_timestamp:
                                    if (current_timestamp - active_timestamp) < time_threshold:
                                        refresh_display_fast = True
                                        refresh_delay_sec = 0.05

                                percentage = 100

                            progress.update(task, completed=percentage)

                        if len(args) == 1:
                            break

                        progress.refresh()
                        time.sleep(refresh_delay_sec)

                        if not refresh_display_fast:
                            refresh_delay_sec = 1
            except KeyboardInterrupt:
                print_carriage_return(console)
                return

            print_carriage_return(console)


