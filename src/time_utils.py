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

