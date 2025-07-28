from datetime import datetime, timedelta

def convert_duration_string_to_timestamp(duration):
    duration_timestamp = timedelta()

    duration_int = int(duration[:-1])

    if duration.endswith('s'):
        duration_timestamp += timedelta(seconds=duration_int)
    elif duration.endswith('m'):
        duration_timestamp += timedelta(minutes=duration_int)
    elif duration.endswith('h'):
        duration_timestamp += timedelta(hours=duration_int)

    return duration_timestamp

def format_timedelta(timedelta):
    total_seconds = int(timedelta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600) # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60) # 60 seconds in a minute
    milliseconds = timedelta.microseconds // 1000 # Get the microseconds and then floor

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

