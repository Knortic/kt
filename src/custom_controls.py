from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn, SpinnerColumn
from rich.text import Text
from rich.columns import Columns
from rich.align import Align

from datetime import datetime, timedelta

from src.time_utils import format_timedelta

class ColorBarColumn(BarColumn):
    def render(self, task):
        # Choose colour based on percentage
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

        pause_timestamp_iso = item.get("pause-timestamp")
        has_pause_timestamp = pause_timestamp_iso 

        if has_pause_timestamp:
            current_time = datetime.fromisoformat(item["pause-timestamp"])
        else:
            current_time = datetime.now()

        output = ""

        msg = item["message"]

        if msg:
            output += f'"{msg}" '

        if current_time > timestamp:
            output += f"{format_timedelta(current_time - timestamp)} ago"
        else:
            output += f"{format_timedelta(timestamp - current_time)}"

        if has_pause_timestamp:
            output += " (paused)"

        output += '\n'

        return output

