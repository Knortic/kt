import pytest

from datetime import datetime, timedelta

from src.reader import FakeFileReader
from src.writer import FileWriter, FakeFileWriter
from src.config_manager import ConfigManager

timers_file_path = "timers.json"

def test_generate_timers_should_not_throw_exception():
    config_manager = ConfigManager(FakeFileReader(), FakeFileWriter())
    assert(config_manager.generate_timers_file(timers_file_path) == True)

def test_generate_timers_calls_file_write():
    writer = FakeFileWriter()
    config_manager = ConfigManager(FakeFileReader(), writer)
    config_manager.generate_timers_file(timers_file_path)

    assert(writer.write_amount == 1)



