import pytest
import time

from datetime import datetime, timedelta

from src.manage_cmd import on_pause, on_unpause

def test_pausing_on_same_minute_as_current_returns_expected_time():
    obj = []
    obj.append({})
    item_idx = 0

    current_timestamp = datetime.now()

    # Setup our test object to have a timestamp since it's required
    # for the function calls below
    obj[item_idx]["timestamp"] = current_timestamp.isoformat()

    on_pause(obj, item_idx)

    pause_timestamp_iso = obj[item_idx].get("pause-timestamp")
    pause_timestamp = datetime.fromisoformat(pause_timestamp_iso)

    assert(current_timestamp.hour == pause_timestamp.hour)
    assert(current_timestamp.minute == pause_timestamp.minute)
    assert(current_timestamp.second == pause_timestamp.second)

def test_waiting_two_seconds_returns_expected_time():
    obj = []
    obj.append({})
    item_idx = 0

    # Setup our test object to have a timestamp since it's required
    # for the function calls below
    obj[item_idx]["timestamp"] = datetime.now().isoformat()

    on_pause(obj, item_idx)

    pause_timestamp_iso = obj[item_idx].get("pause-timestamp")
    assert(pause_timestamp_iso)

    time.sleep(2)

    on_unpause(obj, item_idx)
    unpause_timestamp_iso = obj[item_idx].get("timestamp")
    assert(unpause_timestamp_iso)

    unpause_timestamp = datetime.fromisoformat(unpause_timestamp_iso)
    assert(unpause_timestamp)

    pause_timestamp = datetime.fromisoformat(pause_timestamp_iso)

    difference_min = unpause_timestamp.minute - pause_timestamp.minute

    # We check if the minute difference is either 0 or 1 because 
    # when storing the timestamps we grab the current time, this is
    # done individually which could lead to a potential discrepancy.
    # We can assume this is the case because our operations are not
    # expensive enough to surpass a second for the execution time
    assert(difference_min == 0 or difference_min == 1)

def test_pausing_and_unpausing_multiple_times_with_no_delay_returns_expected_time():
    obj = []
    obj.append({})
    item_idx = 0

    # Setup our test object to have a timestamp since it's required
    # for the function calls below
    obj[item_idx]["timestamp"] = datetime.now().isoformat()

    current_timestamp = datetime.now()

    for i in range(100):
        on_pause(obj, item_idx)
        on_unpause(obj, item_idx)

    active_timestamp_iso = obj[item_idx].get("timestamp")
    assert(active_timestamp_iso)

    active_timestamp = datetime.fromisoformat(active_timestamp_iso)

    assert(current_timestamp.hour == active_timestamp.hour)

    # We check if the current timestamp minute is the active timestamp minute or
    # the active timestamp minute - 1 because it could just so happen that
    # when the timestamp was generated it ticked over to the next minute
    # and so that discrepancy should be accounted for.
    assert(current_timestamp.minute == active_timestamp.minute
           or current_timestamp.minute == active_timestamp.minute - 1)

    # We check if the current timestamp second is the active timestamp second or
    # the active timestamp second - 1 because it could just so happen that
    # when the timestamp was generated it ticked over to the next second
    # and so that discrepancy should be accounted for.
    assert(current_timestamp.second == active_timestamp.second
           or current_timestamp.second == active_timestamp.second - 1)
