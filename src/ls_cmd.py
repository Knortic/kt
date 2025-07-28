import os
import json
import time

from src.time_utils import convert_duration_string_to_timestamp

from datetime import datetime, timedelta

from rich.live import Live
from rich.table import Table
from rich.console import Console, Group
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn, SpinnerColumn
from rich.text import Text
from rich.columns import Columns
from rich.align import Align

current_time = None

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600) # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60) # 60 seconds in a minute
    milliseconds = td.microseconds // 1000 # Get the microseconds and then floor

    result = ""

    if hours > 0:
        result += f"{hours}h "
    if (hours > 0 and minutes >= 0) or minutes > 0:
        result += f"{minutes}m "
    if (minutes > 0 and seconds >= 0) or seconds > 0:# or result == "":
        result += f"{seconds}s"
    elif seconds == 0:
        ms_str = str(milliseconds)

        while len(ms_str) != 4:
            ms_str = "0" + ms_str

        result += f"{seconds}.{ms_str}s"

    return result

class ColorBarColumn(BarColumn):
    def render(self, task):
        # Choose color based on percentage
        percent = task.percentage or 0
        if percent < 30:
            self.complete_style = "red"
        elif percent < 100:
            self.complete_style = "yellow"
        else:
            self.complete_style = "green"

        return super().render(task=task)

class FieldTextColumn(TextColumn):
    def render(self, task):
        return self.text_format.format(**task.fields.get("item"))

class CustomTimeTextColumn(TextColumn):
    def render(self, task):
        item = task.fields.get("item")
        timestamp = datetime.fromisoformat(item["timestamp"])

        if item.get("pause-timestamp"):
            current_time = datetime.fromisoformat(item["pause-timestamp"])

        output = ""

        msg = item["message"]

        if msg:
            output += f'"{msg}" '

        if current_time > timestamp:
            output += f"{format_timedelta(current_time - timestamp)} ago\n"
        else:
            output += f"{format_timedelta(timestamp - current_time)}\n"

        return output

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

        def generate_output(json_obj):
            output = ""

            for idx, item in enumerate(json_obj):
                output += f"{item['id']} "
                output += f'"{item["message"]}" '

                timestamp = datetime.fromisoformat(item["timestamp"])

                if current_time > timestamp:
                    output += f"{format_timedelta(current_time - timestamp)} ago\n"
                else:
                    output += f"{format_timedelta(timestamp - current_time)}\n"

            return output

        # Add a bit of spacing between the command ran and where the print will occur
        Console().print('\r')

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

