from datetime import datetime, timedelta

def convert_duration_string_to_timestamp(duration):
    duration_timestamp = datetime.now() 

    duration_int = int(duration[:-1])

    if duration.endswith('s'):
        duration_timestamp += timedelta(seconds=duration_int)
    elif duration.endswith('m'):
        duration_timestamp += timedelta(minutes=duration_int)
    elif duration.endswith('h'):
        duration_timestamp += timedelta(hours=duration_int)

    # Subtract 1 second from the timestamp otherwise
    # the time won't be accurate
    duration_timestamp = duration_timestamp - timedelta(seconds=1)

    return duration_timestamp

def convert_duration_string_to_timestamp_without_microseconds(duration):
    timestamp = convert_duration_string_to_timestamp(duration)
    timestamp = timestamp.replace(microsecond=0)

    return timestamp

