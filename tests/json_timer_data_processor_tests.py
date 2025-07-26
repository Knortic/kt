import pytest

from src.timer_data import TimerData
from src.timer_data_processor import JsonTimerDataProcessor

def test_given_valid_data_can_remove_element():
    sample_data = []
    sample_data.append({})
    sample_data[0]["id"] = 0
    sample_data.append({})
    sample_data[1]["id"] = 1

    processor = JsonTimerDataProcessor()

    timer_id_to_remove = 1
    processor.remove_timer_entry_by_id(sample_data, timer_id_to_remove)

    assert(len(sample_data) == 1)

    sample_data.append({})
    sample_data[1]["id"] = 1

    sample_data.append({})
    sample_data[2]["id"] = 2

    sample_data.append({})
    sample_data[3]["id"] = 3

    sample_data.append({})
    sample_data[4]["id"] = 4

    timer_id_to_remove = 4
    processor.remove_timer_entry_by_id(sample_data, timer_id_to_remove)

    assert(len(sample_data) == 4)

    timer_id_to_remove = 3
    processor.remove_timer_entry_by_id(sample_data, timer_id_to_remove)

    assert(len(sample_data) == 3)

