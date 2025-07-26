import pytest

from datetime import datetime, timedelta

from src.timer_data import TimerData
from src.timer_data_processor import JsonTimerDataProcessor
# from src.config_manager import ConfigManager

def test_given_valid_timer_info_call_to_generate_data_should_return_true():
    timer_info = TimerData(timestamp = datetime.now(),
                           message = "test msg",
                           duration = "20s")

    timer_data_gen = TimerDataGenerator(timer_info)
    assert(timer_data_gen.generate_data() == True)

def test_given_valid_timer_info_call_to_generate_data_should_contain_single():
    timer_info = TimerData(timestamp = datetime.now(), message = "test msg", duration = "20s")
    timer_data_gen = TimerDataGenerator(timer_info)
    assert(timer_data_gen.generate_data() == True)


