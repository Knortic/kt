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

    expected_obj[0]["id"] = 0;
    expected_obj[0]["message"] = "test";
    expected_obj[0]["duration"] = "1m";
    expected_obj[0]["paused"] = False;
    expected_obj[0]["reset"] = False;

    timer_data = TimerData(timestamp = datetime.now(),
                           message = expected_obj[0]["message"],
                           duration = expected_obj[0]["duration"])

    timer_data_gen = JsonTimerDataGenerator(timer_data)
    
    timer_data_gen.generate_data()

    assert(timer_data_gen.json_obj == expected_obj)

