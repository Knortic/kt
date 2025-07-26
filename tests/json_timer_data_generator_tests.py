import pytest

from datetime import datetime, timedelta

from src.timer_data_generator import JsonTimerDataGenerator, TimerData
from src.errors import InvalidArgumentError

def create_valid_timer_data():
    return TimerData(timestamp = datetime.now(),
                           message = "test",
                           duration = "20s")

def test_given_valid_timer_data_call_to_generate_data_should_return_true():
    timer_data = create_valid_timer_data()

    timer_data_gen = JsonTimerDataGenerator(timer_data)
    timer_data_gen.generate_data()

def test_given_valid_timer_data_call_to_generate_data_should_be_array():
    timer_data = create_valid_timer_data()
    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    timer_data_gen.generate_data()
    assert(isinstance(timer_data_gen.json_obj, list))

def test_given_valid_timer_data_call_to_generate_data_should_be_array_with_single_item():
    timer_data = create_valid_timer_data()
    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    timer_data_gen.generate_data()
    assert(isinstance(timer_data_gen.json_obj, list))
    assert(len(timer_data_gen.json_obj) == 1)

def test_given_invalid_timer_data_call_to_generate_data_should_throw_exception():
    orig_timestamp = datetime.now()
    orig_message = "test"
    orig_duration = "20s"

    timer_data = TimerData(timestamp = orig_timestamp,
                           message = orig_message,
                           duration = 20)
    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    with pytest.raises(InvalidArgumentError):
        timer_data_gen.generate_data()

    timer_data = TimerData(timestamp = orig_timestamp,
                           message = 1,
                           duration = orig_duration)
    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    with pytest.raises(InvalidArgumentError):
        timer_data_gen.generate_data()

    timer_data = TimerData(timestamp = None,
                           message = orig_message,
                           duration = orig_duration)
    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    with pytest.raises(InvalidArgumentError):
        timer_data_gen.generate_data()

def test_given_valid_timer_data_call_to_generate_data_should_return_expected_object():
    expected_obj = []
    expected_obj.append({})

    current_time = datetime.now()

    expected_obj[0]["id"] = 0;
    expected_obj[0]["message"] = "test";
    expected_obj[0]["duration"] = "1m";
    expected_obj[0]["paused"] = False;
    expected_obj[0]["reset"] = False;

    timer_data = TimerData(timestamp = current_time,
                           message = expected_obj[0]["message"],
                           duration = expected_obj[0]["duration"])

    timer_data_gen = JsonTimerDataGenerator(timer_data)

    expected_obj[0]["timestamp"] = timer_data_gen.timer_data.timestamp.isoformat();
    
    timer_data_gen.generate_data()

    assert(timer_data_gen.json_obj == expected_obj)

def test_given_existing_json_data_returns_correct_id_from_generated_object():
    sample_data = []
    sample_data.append({})

    current_time = datetime.now()

    sample_data[0]["id"] = 0;
    sample_data[0]["message"] = "test";
    sample_data[0]["duration"] = "1m";
    sample_data[0]["paused"] = False;
    sample_data[0]["reset"] = False;

    timer_data = TimerData(timestamp = current_time,
                           message = sample_data[0]["message"],
                           duration = sample_data[0]["duration"])

    timer_data_gen = JsonTimerDataGenerator(timer_data)

    timer_data_gen.generate_data_from_existing(sample_data)

    expected_id = 1
    assert(timer_data_gen.json_obj[-1]["id"] == expected_id)

    timer_data = TimerData(timestamp = current_time,
                           message = sample_data[0]["message"],
                           duration = sample_data[0]["duration"])

    timer_data_gen = JsonTimerDataGenerator(timer_data)

    timer_data_gen.generate_data_from_existing(sample_data)

    expected_id = 2
    assert(timer_data_gen.json_obj[-1]["id"] == expected_id)

    sample_data.append({})

    timer_data = TimerData(timestamp = current_time,
                           message = sample_data[0]["message"],
                           duration = sample_data[0]["duration"])

    timer_data_gen = JsonTimerDataGenerator(timer_data)

    timer_data_gen.generate_data_from_existing(sample_data)

    # In our sample data we should have 4 items by this point so our expected id should be
    # the amount of items
    expected_id = 4
    assert(timer_data_gen.json_obj[-1]["id"] == expected_id)

